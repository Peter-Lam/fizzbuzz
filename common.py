import os
import requests
from elasticsearch import Elasticsearch


def create_index():
    '''
    Create an Elasticsearch index (table) using a mapping to define field types
    '''
    try:
        # Connecting to Elasticsearch
        es = Elasticsearch(
            ["http://host.docker.internal:9500"], verify_certs=True)
        # If index exists, just ignore
        if es.indices.exists('fizzbuzz'):
            return
        try:
            print(f"Creating fizzbuzz index...")
            es.indices.create('fizzbuzz', body={"mappings": {"properties": {"msg_no": {
                              "type": "long"}, "time_received": {"type": "date"}, "time_sent": {"type": "date"}}}})
            print(f"Successfully created fizzbuzz index!")
        except Exception as ex:
            raise Exception(
                f"Unable to create index")
    except Exception as ex:
        raise ex


def create_request(msg_no, time_sent):
    '''
    Create a POST requests to consumer, with payload containing msg_no and time_sent
    :param msg_no: Message number
    :param time_sent: The time, in ISO format, when the request was made
    :type msg_no: int
    :type time_sent: str
    :return: response status code of the POST request
    :rtype: int
    '''
    url = 'http://consumer:5000/consumer/api/post_data/' if 'DOCKER' in os.environ else 'http://localhost:5000/consumer/api/post_data/'

    response = requests.post(
        url, json={'msg_no': msg_no, 'time_sent': time_sent})

    return response.content
