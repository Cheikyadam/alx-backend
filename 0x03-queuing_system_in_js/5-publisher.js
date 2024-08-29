import { createClient } from 'redis';

const publisher = createClient();

const channelName = "holberton school channel";

publisher.on('error', err => console.log(`Redis client not connected to the server: ${err.message}`));

publisher.on('connect', () => console.log('Redis client connected to the server'));

function publishMessage(message, time) {
  setTimeout(() => {
    console.log(`About to send ${message}`);
    publisher.publish(channelName, message, (err) => {
      if (err) {
        console.log(`Error publishing message: ${err.message}`);
     }});
  }, time);
}


publishMessage("Holberton Student #1 starts course", 100);
publishMessage("Holberton Student #2 starts course", 200);
publishMessage("KILL_SERVER", 300);
publishMessage("Holberton Student #3 starts course", 400);
