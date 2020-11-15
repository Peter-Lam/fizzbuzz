import os
from redis import Redis
from rq import Worker, Queue, Connection


def main():
    '''
    Create and starts workers on redis queue
    '''
    listen = ['default']
    con = Redis(host='redis', port=6379)
    with Connection(con):
        worker = Worker(list(map(Queue, listen)))
        worker.work()


if __name__ == '__main__':
    main()
