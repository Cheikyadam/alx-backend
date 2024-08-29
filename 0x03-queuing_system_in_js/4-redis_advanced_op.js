import { createClient, print } from 'redis';

const client = createClient();

client.on('error', err => console.log(`Redis client not connected to the server: ${err.message}`));

const key = "HolbertonSchools";

function setValue(field, value) {
  client.HSET(key, field, value, print);
}

function getKeyValue() {
  client.HGETALL(key, (err, reply) =>{
  
  if (err) {
    console.log(`Error: ${err.message}`);
  }
  else{
   console.log(reply);
  }

  });
}

client.on('connect', () => {
  console.log('Redis client connected to the server');
  setValue('Portland', 50);
  setValue('Seattle', 80);
  setValue('New York', 20);
  setValue('Bogota', 20);
  setValue('Cali', 40);
  setValue('Paris', 2);
 
  getKeyValue();
});
