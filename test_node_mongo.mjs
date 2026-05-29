import { MongoClient } from 'mongodb';
import dotenv from 'dotenv';

dotenv.config({ path: '.env' });

const uri = process.env.MONGODB_URI.replace('&tls=true&tlsAllowInvalidCertificates=true', '');

console.log('Testing MongoDB connection via Node.js...');

try {
  const client = new MongoClient(uri);
  await client.connect();
  await client.db('admin').command({ ping: 1 });
  console.log('SUCCESS! MongoDB connected!');
  
  const db = client.db('dealpulse');
  const collections = await db.listCollections().toArray();
  console.log('Collections:', collections.map(c => c.name));
  
  const count = await db.collection('clients').countDocuments();
  console.log('Clients:', count);
  
  await client.close();
} catch (e) {
  console.log('Failed:', e.message);
}