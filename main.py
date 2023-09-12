import os
import requests
import random
import threading


def start_workers():
    workers = os.environ.get('thread_count', 10)
    # 1 - only send GET
    # 2 - only POST, will post a random work from preset lis
    http_method = os.environ.get('method', 1)
    target_url = os.environ.get('target_url', "127.0.0.1")  # url or IP



def hit_url(http_method, target_url):
    post_list = ['Dog', 'Cat', 'Cow', 'Hen', 'Sheep', 'Rabbit', 'Duck',
                 'Horse', 'Pig', 'Turkey', 'Chicken', 'Donkey', 'Goat',
                 'Guinea Pig', 'Deer', 'Fish', 'Bee', 'Goat', 'Goose', 'Rat']

    while True:
        if http_method == 1:
            r = requests.get(target_url)
            print(r.status_code)
        else:
            animal = random.randrange(21)
            r = requests.post(target_url, json={post_list[animal]: 1})
            print(r.status_code)


if __name__ == '__main__':
    start_workers()
    print("hi")




