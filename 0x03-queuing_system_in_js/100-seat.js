import express from 'express';
import { createClient, print } from 'redis';
const { promisify } = require('util');
import kue from 'kue';
const queue = kue.createQueue();

const client = createClient();

function reserveSeat(number){
  client.set("available_seats", number);
}

let reservationEnabled = true;

client.on('error', err => console.log(`Redis client not connected to the server: ${err.message}`));
client.on('connect', () => {
  console.log('Redis client connected to the server');
  reserveSeat(50);
});


const getAsync = promisify(client.get).bind(client);

async function getCurrentAvailableSeats(){
  try{
    const reply = await getAsync("available_seats");
    return reply;
  }
  catch (err) {
    console.log(`Error: ${err.message}`);
  } 
}

const app = express();

app.use(express.json());

app.get('/available_seats', async (req, res) => {
    try {
      const av = await getCurrentAvailableSeats();
      res.json({"numberOfAvailableSeats": av});
    }
    catch (err) {}
});


app.get('/reserve_seat', async (req, res) => {
  if (reservationEnabled === false){
    res.statusCode = 404;
    res.json({"status": "Reservation are blocked"});
  }
  else {
     const job =  queue.create('reservation_job')
    .save((err) => {
      if (err) {
        res.statusCode = 404;
        res.json({"status": "Reservation failed"});
      } else{
         res.json({"status": "Reservation in process"});
      }
   });

   job.on('complete', () => {
     console.log(`Seat reservation job ${job.id} completed`);
   }).on('failed', (error) =>{
    console.log(`Seat reservation job ${job.id} failed: ${error}`);
  });
 }
});

app.get('/process', (req, res) => {
  res.json({"status": "Queue processing"});
  queue.process('reservation_job', async (job, done) => {
    const av = await getCurrentAvailableSeats();
    if (av == 0){
      reservationEnabled = false;
    }
    if (av >= 0){
      if (av != 0){
        reserveSeat(av - 1);
      }
      done();
    }
    else{
      done(new Error("Not enough seats available"));
    }
  });

});


app.listen(1245, () => {
  console.log('app running in port 1245');
});



