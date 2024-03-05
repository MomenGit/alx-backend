import { createClient, print } from 'redis';

const client = createClient();

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

client.on('error', (err) => {
  console.log('Redis client not connected to the server:', err.toString());
});

const HolbertonSchools = {
  Portland: 50,
  Seattle: 80,
  'New York': 20,
  Bogota: 20,
  Cali: 40,
  Paris: 2,
};

for (const [key, value] of Object.entries(HolbertonSchools)) {
  client.HSET('HolbertonSchools', key, value, print);
}

client.HGETALL('HolbertonSchools', (err, reply) => {
  print(JSON.stringify(reply, null, 2));
});
