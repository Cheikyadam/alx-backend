import { createClient } from 'redis';

const client = createClient();

client.on('error', err => console.log(`Redis client not connected to the server: ${err.message}`));

client.on('connect', () => console.log('Redis client connected to the server'));

const channelName = 'holberton school channel';

client.subscribe(channelName, (err) => {
  if (err) {
    console.log(`Error subscribing to channel: ${err.message}`);
  }
});

client.on('message', (channel, message) => {
  console.log(message);
  if(message === "KILL_SERVER"){
    client.unsubscribe(channelName);
    client.quit();
  }
});
