import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { MongoClient } from 'mongodb';
import dotenv from 'dotenv';

dotenv.config({ path: '../.env' });

const client = new MongoClient(process.env.MONGODB_URI);
const db = client.db(process.env.MONGODB_DATABASE || 'dealpulse');

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

// Connect to MongoDB first
await client.connect();
console.log('Connected to MongoDB Atlas');

// List tools
server.setRequestHandler('tools/list', async () => {
  return {
    tools: [
      {
        name: 'query_clients',
        description: 'Query financial services clients',
        inputSchema: {
          type: 'object',
          properties: {
            min_aum: { type: 'number' },
            min_deal_value: { type: 'number' }
          }
        }
      },
      {
        name: 'get_at_risk_deals',
        description: 'Get at-risk deals',
        inputSchema: { type: 'object', properties: {} }
      }
    ]
  };
});

// Handle tool calls
server.setRequestHandler('tools/call', async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {
      case 'query_clients':
        const filter = {};
        if (args?.min_aum) filter.aum = { $gte: args.min_aum };
        if (args?.min_deal_value) filter['current_deal.value'] = { $gte: args.min_deal_value };
        
        const clients = await db.collection('clients').find(filter).toArray();
        return { 
          content: [{ 
            type: 'text', 
            text: `Found ${clients.length} clients:\n${JSON.stringify(clients, null, 2)}` 
          }] 
        };

      case 'get_at_risk_deals':
        const atRisk = await db.collection('clients').find({
          $or: [
            { 'current_deal.stage': 'stalled' },
            { portfolio_performance: { $lt: 0 } }
          ]
        }).toArray();
        
        return { 
          content: [{ 
            type: 'text', 
            text: `Found ${atRisk.length} at-risk deals:\n${JSON.stringify(atRisk, null, 2)}` 
          }] 
        };

      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error) {
    return { 
      content: [{ 
        type: 'text', 
        text: `Error: ${error.message}` 
      }] 
    };
  }
});

const transport = new StdioServerTransport();
await server.connect(transport);
console.log('MCP Server started successfully');