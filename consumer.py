import common
from datetime import datetime, timedelta
from elasticsearch import Elasticsearch
from flask import Flask, request, jsonify, render_template
from pytz import timezone
from time import sleep

app = Flask(__name__)

# RESTful API


@ app.route('/consumer/api/post_data/', methods=['POST'])
def post_data():
    try:
        if request.method == "POST":
            content = request.json
            # Confirm that the correct values are sent
            if ['msg_no', 'time_sent'] == list(content.keys()):
                print(
                    f"POST request received ({content['msg_no']}, {content['time_sent']})")
                # Establish connection to ES
                es = Elasticsearch(
                    ["http://host.docker.internal:9500"], verify_certs=True)
                while not es.ping():
                    print("Waiting for ES to startup...")
                    sleep(60)
                common.create_index()
                # Push data to ES
                doc = {'msg_no': content['msg_no'], 'time_sent': content['time_sent'], 'time_received': str(
                    datetime.now(timezone('UTC')).isoformat())}
                response = es.index(index='fizzbuzz', body=doc)
                print(response)
                return f'Successfully uploaded: {doc}', 200
            else:
                return 'One of the folling parameters are missing [msg_no, time_sent]. Could not process request.', 400
        else:
            return 'Expecting POST request. Could not process request.'
    except Exception as ex:
        return 'Expecting JSON format. Could not process request.', 400

# Webpage


@ app.route('/fizzbuzz/', methods=['GET'])
def show_data():
    # Estable ES connection
    es = Elasticsearch(["http://host.docker.internal:9500"], verify_certs=True)
    while not es.ping():
        print("Unable to connect to Elasticsearch, trying again in 60 secs")
        sleep(60)
    # Search for the highest msg_no stored in Elasticsearch
    if not es.indices.exists(index="fizzbuzz"):
        common.create_index()
    result = es.search(index='fizzbuzz', body={"fields": ["msg_no"], "query": {
                       "match_all": {}}, "sort": {"msg_no": "desc"}, "size": 1})
    if len(result['hits']['hits']) == 0:
        return "Unable to locate data, please use the Producer/notebook to upload to Elasticsearch"
    max_no = {result['hits']['hits'][0]['_source']['msg_no']}
    # Search for entries in the past 10 seconds
    result = es.search(index='fizzbuzz', body={"query": {"range": {"time_received": {
        "gte": str((datetime.now() - timedelta(seconds=10)).isoformat()), "lte": "now"}}}})
    # Calculate average transmission time
    total_time = timedelta(0)
    counter = 0
    for doc in result['hits']['hits']:
        received = datetime.strptime(doc['_source']
                                     ['time_received'], "%Y-%m-%dT%H:%M:%S.%f%z")
        sent = datetime.strptime(doc['_source']
                                 ['time_sent'], "%Y-%m-%dT%H:%M:%S.%f%z")

        total_time += (received - sent)
        counter += 1

    trans_time = total_time / \
        counter if counter > 0 else 'No requests made in the past 10 seconds, Unable to calculate the transmission time.'
    return render_template("index.html", message_number=max_no, trans_time=trans_time)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
