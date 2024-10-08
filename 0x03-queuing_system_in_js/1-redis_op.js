import { createClient, print } from 'redis';

const client = createClient();

function initialize(){
  client.on('error', err => console.log(`Redis client not connected to the server: ${err.message}`))
  client.on('connect', () => console.log('Redis client connected to the server'));
}

function setNewSchool(schoolName, value){
  client.set(schoolName, value, print);
}

function displaySchoolValue(schoolName){
  client.get(schoolName, (err, reply) => {
    if (err) {
    console.log(`Error: ${err.message}`);
  } else {
    console.log(`${reply}`);
  }
  });
}

initialize();
displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
