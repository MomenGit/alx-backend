import { createClient, print } from 'redis';
import { promisify } from 'node:util';

const client = createClient();

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

client.on('error', (err) => {
  console.log('Redis client not connected to the server:', err.toString());
});

function setNewSchool(schoolName, value) {
  client.set(schoolName, value, (err, reply) => {
    if (!err) print(`Reply: ${reply}`);
  });
}
const get = promisify(client.get).bind(client);

async function displaySchoolValue(schoolName) {
  const value = await get(schoolName);
  print(value);
}

displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
