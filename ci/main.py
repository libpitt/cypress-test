#!/usr/bin/env python
import json

from websockets.sync.client import connect
import datetime

def main():
    with connect("ws://localhost:8765") as websocket:
        websocket.send(f"Requesting Cypress reports ... Date: {datetime.datetime.now()}. ")
        receiving = True
        results = {}
        while receiving is True:
            message = websocket.recv()
            result = json.loads(message)
            results.update(result)
            print(f"Received: {message}")
            path = result.get('path')
            if path is not None and 'complete.json' in result.get('path'):
                receiving = False

        return json.dumps(results)


main()
