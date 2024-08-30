export default function createPushNotificationsJobs(jobs, queue){
  if (Array.isArray(jobs) === false){
    throw (new Error("Jobs is not an array"));
  } else {
  for (const curJob of jobs) {
    const job =  queue.create('push_notification_code_3', curJob)
    .save((err) => {
      if (err) {
        console.error('Error creating job:', err);
      } else {
        console.log(`Notification job created: ${job.id}`);
      }
    });

    job.on('complete', () => {
      console.log(`Notification job ${job.id} completed`);
    }).on('failed', (error) =>{
    console.log(`Notification job ${job.id} failed: ${error}`);
    }).on('progress', (progress) =>{
      console.log(`Notification job ${job.id} ${progress}% complete`);
    });
  }
 }
}
