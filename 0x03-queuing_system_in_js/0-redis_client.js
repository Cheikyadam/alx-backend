import { createClient } from 'redis';

async function initialize(){
const client = createClient();
  client.on('error', err => console.log(`Redis client not connected to the server: ${err.message}`))
  client.on('connect', () => console.log('Redis client connected to the server'));
}

initialize();
