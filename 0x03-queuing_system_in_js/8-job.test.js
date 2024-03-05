import { after, afterEach, before, describe } from "mocha";
import createPushNotificationsJobs from "./8-job";
import kue from "kue";
import { expect } from "chai";

describe("createPushNotificationsJobs", () => {
  const queue = kue.createQueue();

  before(() => {
    queue.testMode.enter();
  });
  afterEach(() => {
    queue.testMode.clear();
  });
  after(() => {
    queue.testMode.exit();
  });

  it("display an error message if jobs is not an array", () => {
    expect(() => createPushNotificationsJobs("", queue)).to.throw();
  });

  it("create two new jobs to the queue", () => {
    const jobs = [
      {
        phoneNumber: "4154318781",
        message: "This is the code 4562 to verify your account",
      },
      {
        phoneNumber: "4151218782",
        message: "This is the code 4321 to verify your account",
      },
    ];
    createPushNotificationsJobs(jobs, queue);
    expect(queue.testMode.jobs.length).to.equal(2);
  });
  it("each job has the correct data", () => {
    const jobs = [
      {
        phoneNumber: "4154318781",
        message: "This is the code 4562 to verify your account",
      },
      {
        phoneNumber: "4151218782",
        message: "This is the code 4321 to verify your account",
      },
    ];
    createPushNotificationsJobs(jobs, queue);

    // Assert that each job has the correct data
    jobs.forEach((jobData, index) => {
      expect(queue.testMode.jobs[index].type).to.equal(
        "push_notification_code_3",
      );
      expect(queue.testMode.jobs[index].data).to.equal(jobData);
    });
  });
});
