export default function createPushNotificationsJobs(jobs, queue) {
  if (!Array.isArray(jobs)) throw new Error("Jobs is not an array");

  jobs.forEach((jobData) => {
    const job = queue.create("push_notification_code_3", jobData);

    job
      .on("enqueue", function () {
        console.log(`Notificaiton job created: ${job.id}`);
      })
      .on("complete", function (result) {
        console.log(`Notification job ${job.id} completed`);
      })
      .on("failed", function (errorMessage) {
        console.log(`Notification job ${job.id} failed:`, errorMessage);
      })
      .on("progress", (progress, data) => {
        console.log(`Notificaiton job ${job.id} ${progress}% complete`);
      });
    job.save();
  });
}
