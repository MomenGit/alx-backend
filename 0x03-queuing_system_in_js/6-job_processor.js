import kue from "kue";

const queue = kue.createQueue();

const jobData = { phoneNumber: "1234567890", message: "Hello, world!" };

const job = queue.process("push_notification_code", (job, done) => {
  sendNotification(job.data.phoneNumber, job.data.message);
});

function sendNotification(phoneNumber, message) {
  console.log(
    `Sending notification to ${phoneNumber}, with message: ${message}`,
  );
}
