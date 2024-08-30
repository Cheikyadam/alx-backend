import kue from 'kue';
const queue = kue.createQueue();

const black = ["4153518780", "4153518781"];

function sendNotification(phoneNumber, message, job, done){
  let completedSteps = 0;
  const totalSteps = 100;
  job.progress(completedSteps, totalSteps);
  if (black.includes(phoneNumber)){
      done(new Error(`Phone number ${phoneNumber} is blacklisted`));
  } 

  function performStep() {
    if (completedSteps === 50) {
      console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);
      job.progress(completedSteps, totalSteps);
    }
    completedSteps += 50;
    if (completedSteps < totalSteps) {
      setTimeout(performStep, 100);
    } else {
      done();
    }
  }
  performStep();
}

queue.process('push_notification_code_2', 2, (job, done) =>{
  sendNotification(job.data['phoneNumber'], job.data['message'], job, done);
});
