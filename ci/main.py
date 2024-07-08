#!/usr/bin/env python
import json

from websockets.sync.client import connect
import datetime


def workflow_printer(message):
    result = json.loads(message)
    if is_complete(result):
        print(f"::notice::Tests complete")
        return
    test = result.get('report')
    if test is not None and test.get('reporter') == 'spec':
        print(f"::group::{test.get('spec').get('relative')}")  # group title
        stats = test.get('reporterStats', '')
        state = 'error' if stats.get('failures') > 0 else 'notice'
        print(f"::{state}::Tests: {stats.get('tests')} ; Passes: {stats.get('passes')} ; Fails: {stats.get('failures')}")
        for t in test.get('tests'):
            state = 'error' if t.get('state') != 'passed' else 'notice'
            title = ' > '.join(t.get('title', ''))
            print(f"::{state}::{title}")
        print("::endgroup::")
    else:
        print(f"::notice::{json.dumps(result)}")


def is_complete(result):
    report = result.get('report')
    if report is not None and type(report) is not str:
        return report.get('complete')
    else:
        return False


def main():
    with connect("wss://c81f-2601-547-cc01-6200-8df3-bd33-eb87-696f.ngrok-free.app") as websocket:
        websocket.send(f"Requesting Cypress reports ... Date: {datetime.datetime.now()}. ")
        receiving = True
        results = {}
        while receiving is True:
            message = websocket.recv()
            #print('received', message)
            result = json.loads(message)
            if is_complete(result):
                receiving = False
            else:
                workflow_printer(message)
            results.update(result)

        return json.dumps(results)


main()