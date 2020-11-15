# fizzbuzz

Hello, human.

Your goal is to demonstrate your ninja coding skills by writing a producer-consumer demo dashboard using Docker, python3, and a bit of magic.

Please fork this repo (you may opt to share a private repo with us to preserve your privacy) and then do the following:

- Create a branch in your forked repo
- Create containers to model a producer-consumer pattern: (1) a producer in python that generates 10 POST requests within 100 ms, once per second at the start of the second, and (2) a consumer in python that receives the requests and stores the requests and their arrival time. The POST payload will be the message number, counting up from 0, and the transmission time recorded on the side of the producer container. (3) Put a queue between the producer and the consumer (e.g. https://python-rq.org/).
- Show in an ipynb notebook that:
 - The API of the consumer is receiving POST requests.
 - The consumer container is storing the received POST requests in a database (e.g. SQL, Elasticsearch, MongoDB, etc).
- Create a page that can be reached on localhost, which shows the highest number in the consumer database so far, and the average transmission time of messages received in the past 10 seconds (time arrived minus time sent is the time to transmit). Design the page so that it updates as the numbers are added to the database. Updates every second will probably look nicer than super super fast page updates. Use your own judgement to decide how to make the page.
- Wrap the producer, consumer, and queue into a docker container that uses the containers above. If your database is containerized, or you used nginx or something, there may be more containers in the mix, and that's totally fine. docker-compose would be nice to see.
- Write a script to launch the example
- Create a pull request and you can approve it yourself and merge the branch into trunk
- Document the process for using your updated repo in README.md so that we can try out your demo ourselves

Please spend minimal effort on graphics and UI, as this is not a test of your UI coding skills. If you use a web framework like Laravel that's totally cool. Just don't stress on frontend stuff.


## How to Run Demo

### System Requirements
- Docker
- Python 3.6+

## Getting Started
1. Use one of the following scripts to start up Docker containers with docker-compose and install python library dependencies for the Python notebook:
    - `setup.bat`
    - `setup.sh`
    
2. The following containers should be running (check with `docker ps -a`)
    - producer: Contains the producer which sends POST requests to the Consumer
    - consumer: Contains a RESTful consumer API which receives POST requests, and stores into database
    - queue: Contains the workers for the Redis queue
    - redis: Redis Server
    - es: ElasticSearch server
3. Open and run the notebook `producer_consumer.ipynb`
4. For the website, go to
    - http://localhost:5000/fizzbuzz/