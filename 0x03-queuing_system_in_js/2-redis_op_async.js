import { createClient, print } from 'redis';
import { promisify } from 'util';

const client = createClient();

function initialize(){
  client.on('error', err => console.log(`Redis client not connected to the server: ${err.message}`))
  client.on('connect', () => console.log('Redis client connected to the server'));
}

function setNewSchool(schoolName, value){
  client.set(schoolName, value, print);
}


const getAsync = promisify(client.get).bind(client);

async function displaySchoolValue(schoolName){
  try{
    const reply = await getAsync(schoolName);
    console.log(`${reply}`);
  }
  catch (err) {
    console.log(`Error: ${err.message}`);
  } 
}

async function main(){
  initialize();
  await displaySchoolValue('Holberton');
  setNewSchool('HolbertonSanFrancisco', '100');
  await displaySchoolValue('HolbertonSanFrancisco');
}

main();
