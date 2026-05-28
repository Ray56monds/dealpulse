import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { MongoClient } from 'mongodb';
import dotenv from 'dotenv';

dotenv.config({ path: '../.env' });

const client = new MongoClient(process.env.MONGODB_URI);
const db = client.db(process.env.MONGODB_DATABASE);

const server = new Server(
  {
    name: 'dealpulse-mcp-server',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Tool: Query clients with filters
server.setRequestHandler('tools/call', async (request) => {
  const { name, arguments: args } = request.params;

  switch (name) {
    case 'query_clients':
      const filter = {};
      if (args.min_aum) filter.aum = { $gte: args.min_aum };
      if (args.min_deal_value) filter['current_deal.value'] = { $gte: args.min_deal_value };
      if (args.client_type) filter.client_type = args.client_type;
      if (args.days_since_contact) {
        const cutoff = new Date();
        cutoff.setDate(cutoff.getDate() - args.days_since_contact);
        filter.last_contact = { $lt: cutoff };
      }
      if (args.renewal_within_days) {
        const renewalCutoff = new Date();
        renewalCutoff.setDate(renewalCutoff.getDate() + args.renewal_within_days);
        filter.renewal_date = { $lt: renewalCutoff };
      }
      
      const clients = await db.collection('clients').find(filter).toArray();
      return { content: [{ type: 'text', text: JSON.stringify(clients, null, 2) }] };

    case 'get_at_risk_deals':
      const atRisk = await db.collection('clients').find({
        $or: [
          { 'current_deal.stage': 'stalled' },
          { last_contact: { $lt: new Date(Date.now() - 21 * 24 * 60 * 60 * 1000) } },
          { 'current_deal.close_date': { $lt: new Date() } },
          { 'current_deal.probability': { $lt: 0.4 } },
          { portfolio_performance: { $lt: 0 } },
          { renewal_date: { $lt: new Date(Date.now() + 60 * 24 * 60 * 60 * 1000) } }
        ]
      }).toArray();
      return { content: [{ type: 'text', text: JSON.stringify(atRisk, null, 2) }] };

    case 'create_follow_up':
      const task = {
        client_id: args.client_id,
        type: args.task_type || 'follow_up',
        message: args.message,
        priority: args.priority || 'medium',
        deal_value: args.deal_value,
        created_at: new Date()
      };
      await db.collection('tasks').insertOne(task);
      return { content: [{ type: 'text', text: `Follow-up created for client ${args.client_id}` }] };

    case 'get_daily_priorities':
      const priorities = await db.collection('clients').aggregate([
        {
          $addFields: {
            priority_score: {
              $add: [
                { $multiply: ['$current_deal.value', 0.3] },
                { $multiply: ['$aum', 0.0001] },
                { $cond: [{ $lt: ['$last_contact', new Date(Date.now() - 14 * 24 * 60 * 60 * 1000)] }, 100000, 0] },
                { $cond: [{ $eq: ['$current_deal.stage', 'final_approval'] }, 50000, 0] },
                { $cond: [{ $lt: ['$renewal_date', new Date(Date.now() + 90 * 24 * 60 * 60 * 1000)] }, 75000, 0] },
                { $cond: [{ $lt: ['$portfolio_performance', 0] }, 25000, 0] }
              ]
            }
          }
        },
        { $sort: { priority_score: -1 } },
        { $limit: 10 }
      ]).toArray();
      return { content: [{ type: 'text', text: JSON.stringify(priorities, null, 2) }] };

    case 'analyze_portfolio_performance':
      const performanceAnalysis = await db.collection('clients').aggregate([
        {
          $group: {
            _id: '$client_type',
            avg_performance: { $avg: '$portfolio_performance' },
            total_aum: { $sum: '$aum' },
            client_count: { $sum: 1 },
            avg_deal_value: { $avg: '$current_deal.value' }
          }
        },
        { $sort: { total_aum: -1 } }
      ]).toArray();
      return { content: [{ type: 'text', text: JSON.stringify(performanceAnalysis, null, 2) }] };

    default:
      throw new Error(`Unknown tool: ${name}`);
  }
});

server.setRequestHandler('tools/list', async () => {
  return {
    tools: [
      {
        name: 'query_clients',
        description: 'Query financial services clients with filters for AUM, deal value, client type, and contact history',
        inputSchema: {
          type: 'object',
          properties: {
            min_aum: { type: 'number', description: 'Minimum Assets Under Management' },
            min_deal_value: { type: 'number', description: 'Minimum deal value' },
            client_type: { type: 'string', enum: ['institutional', 'family_office', 'pension_fund', 'insurance', 'venture_capital'] },
            days_since_contact: { type: 'number', description: 'Days since last contact' },
            renewal_within_days: { type: 'number', description: 'Renewal date within X days' }
          }
        }
      },
      {
        name: 'get_at_risk_deals',
        description: 'Identify deals at risk based on stage, contact frequency, performance, and renewal dates',
        inputSchema: { type: 'object', properties: {} }
      },
      {
        name: 'create_follow_up',
        description: 'Create follow-up task for relationship management',
        inputSchema: {
          type: 'object',
          properties: {
            client_id: { type: 'string' },
            message: { type: 'string' },
            priority: { type: 'string', enum: ['low', 'medium', 'high', 'critical'] },
            task_type: { type: 'string', enum: ['follow_up', 'contract_review', 'urgent_call', 'needs_assessment', 'final_approval'] },
            deal_value: { type: 'number' }
          },
          required: ['client_id', 'message']
        }
      },
      {
        name: 'get_daily_priorities',
        description: 'Calculate priority scores based on AUM, deal value, contact recency, stage urgency, renewal proximity, and portfolio performance',
        inputSchema: { type: 'object', properties: {} }
      },
      {
        name: 'analyze_portfolio_performance',
        description: 'Analyze portfolio performance metrics by client type',
        inputSchema: { type: 'object', properties: {} }
      }
    ]
  };
});

const transport = new StdioServerTransport();
await server.connect(transport);
await client.connect();