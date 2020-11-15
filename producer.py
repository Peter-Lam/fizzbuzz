import os
from datetime import datetime
from redis import Redis
from pytz import timezone
from rq import Queue
from rq.job import Job
from time import sleep
from common import create_request

# Initializing queue
CONN = Redis(host='redis' if 'DOCKER' in os.environ else 'localhost', port=6379)
Q = Queue(connection=CONN)

MSG_NO = 0


def increment():
    '''
    Incrementing global counter
    '''
    global MSG_NO
    MSG_NO += 1


def show_results(job_key):
    '''
    Get the results for a job within the queue
    '''
    job = Job.fetch(job_key, connection=CONN)
    while not job.is_finished:
        print("Waiting for job to finish...")
        sleep(60)
    print(job.result.decode('utf-8'))


def main():
    job_ids = []
    # Sends 10 post requests in queue
    for i in range(10):
        time_sent = str(datetime.now(timezone('UTC')).isoformat())
        print(
            f"Sending POST request to consumer: (msg_no: {MSG_NO}, time_sent: {time_sent})")
        response = Q.enqueue(create_request, MSG_NO, time_sent)
        job_ids.append(response.get_id())
        increment()
        # Waits 1 second to send the next request
        sleep(1)
    # Get the results when the jobs are completed
    for job in job_ids:
        show_results(job)


if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        raise ex
