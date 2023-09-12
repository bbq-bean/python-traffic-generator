import os
import requests
import random
from multiprocessing import Process


def start_workers():
    # 1 - only send GET
    # 2 - only POST, will post a random work from preset lis
    http_method = os.environ.get('method', 1)
    target_url = os.environ.get('target_url', "http://google.com")  # url or IP
    for _ in range(os.cpu_count()):
        Process(target=hit_url, args=(http_method,target_url,)).start()


def hit_url(http_method, target_url):
    post_list = ['Dog', 'Cat', 'Cow', 'Hen', 'Sheep', 'Rabbit', 'Duck',
                 'Horse', 'Pig', 'Turkey', 'Chicken', 'Donkey', 'Goat',
                 'Guinea Pig', 'Deer', 'Fish', 'Bee', 'Goat', 'Goose', 'Rat']

    while True:
        if http_method == 1:
            r = requests.get(target_url)
            print(r.status_code)
        else:
            animal = random.randrange(20)
            r = requests.post(target_url, json={post_list[animal]: 1})
            print(r.status_code)


if __name__ == '__main__':
    start_workers()
