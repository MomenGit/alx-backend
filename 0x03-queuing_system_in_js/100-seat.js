import kue from "kue";
import { promisify } from "util";
import { createClient } from "redis";
import express from "express";

const app = express();
const port = 1245;
const hostname = "localhost";

const redisClient = createClient();
const redisGetAsync = promisify(redisClient.get).bind(redisClient);
const redisSetAsync = promisify(redisClient.set).bind(redisClient);

const available_seats = 50;
let reservationEnabled = true;

async function reserveSeat(number) {
  await redisSetAsync("available_seats", number);
}

async function getCurrentAvailableSeats() {
  return await redisGetAsync("available_seats");
}

reserveSeat(available_seats);

app.get("/available_seats", async (req, res) => {
  res.json({ numberOfAvailableSeats: await getCurrentAvailableSeats() });
});
app.get("/reserve_seat", async (req, res) => {
  const currentSeats = await getCurrentAvailableSeats();

  if (!reservationEnabled) {
    res.json({ status: "Reservations are blocked" });
  } else {
    const queue = kue.createQueue();
    const job = queue.create("reserve_seat");

    job
      .on("complete", function (result) {
        console.log(`Seat reservation job ${job.id} completed`);
      })
      .on("failed", function (errorMessage) {
        console.log(`Seat reservation job ${job.id} failed:`, errorMessage);
      });

    job.save((err) => {
      if (!err) res.json({ status: "Reservation in process" });
      else res.json({ status: "Reservation failed" });
    });
  }
});
app.get("/process", async (req, res) => {
  const queue = kue.createQueue();

  queue.process("reserve_seat", async (job, done) => {
    try {
      let currentSeats = await getCurrentAvailableSeats();
      currentSeats--;
      await reserveSeat(currentSeats);

      if (currentSeats === 0) {
        reservationEnabled = false;
      }

      if (currentSeats >= 0) {
        done();
      } else {
        throw new Error("Not enough seats available");
      }
    } catch (error) {
      done(error);
    }
  });

  res.json({ status: "Queue processing" });
});

app.listen(port, hostname, () => {
  console.log(`Server listening on ${hostname}:${port}`);
});
