from boto3 import client
import botocore
import os
import random
import requests
import logging
import time
from multiprocessing import Process


def start_workers():
    # 1 - only send GET
    # 2 - only POST, will post a random work from preset lis
    http_method = os.environ.get('METHOD', 1)
    target_url = os.environ.get('TARGET_URL', "https://1.1.1.1")  # url or IP
    for _ in range(os.cpu_count()):
        Process(target=hit_url, args=(http_method, target_url,)).start()


def hit_url(http_method, target_url):
    post_list = ['Dog', 'Cat', 'Cow', 'Hen', 'Sheep', 'Rabbit', 'Duck',
                 'Horse', 'Pig', 'Turkey', 'Chicken', 'Donkey', 'Goat',
                 'Guinea Pig', 'Deer', 'Fish', 'Bee', 'Goat', 'Goose', 'Rat']

    while True:
        try:
            if http_method == 1:
                r = requests.get(target_url, timeout=5)
                result = str(r.status_code)

            else:
                animal = random.randrange(20)
                r = requests.post(target_url, json={post_list[animal]: 1},
                                  timeout=5)
                result = str(r.status_code)

        except (requests.exceptions.ConnectionError,  # DNS or connection reset
                requests.exceptions.Timeout,  # timeout defined above
                requests.exceptions.RequestException,) as e:  # anything else

            result = str(e)

        print(result)
        response = log_client.put_log_events(
            logGroupName=os.environ.get('LOG_GROUP', "stress-tester"),
            logStreamName=os.environ.get('LOG_STREAM', "stress-tester-default"),
            logEvents=[{
                'timestamp': int(round(time.time() * 1000)),
                'message': result
            }]
        )

        # TODO: check log client response for errors here


if __name__ == '__main__':

    region = os.environ.get('AWS_REGION', "us-east-2")
    log_group = os.environ.get('LOG_GROUP', "stress-tester")
    log_stream = os.environ.get('LOG_STREAM', "stress-tester-default")

    try:
        log_client = client('logs', region_name=region)
        log_client.create_log_group(logGroupName=log_group)
        log_client.create_log_stream(
            logGroupName=log_group,
            logStreamName=log_stream
        )

    # we do not care if the log group/stream already exists
    except log_client.exceptions.ResourceAlreadyExistsException as e:
        pass

    start_workers()
