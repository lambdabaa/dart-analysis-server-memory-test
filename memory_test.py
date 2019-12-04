#!/usr/bin/env python3

import json
import os
import subprocess

flutter = '/usr/local/google/home/ariaye/flutter'

def wait_for_message(server, test):
    while True:
        stdout_line = server.stdout.readline()
        try:
            message = json.loads(stdout_line)
            if test(message):
                return message
        except:
            continue

def make_request_with_test(server, id, method, options, test):
    payload = json.dumps({'id': str(id), 'method': method, 'params': options}) + '\n'
    server.stdin.write(payload)
    return wait_for_message(server, test)

def make_request(server, id, method, options):
    return make_request_with_test(server, id, method, options, lambda msg: msg.get('id') == str(id))

def main():
    # Start an analysis server with ML completion and observatory enabled.
    server = subprocess.Popen(
        [
            '%s/bin/cache/dart-sdk/bin/dart' % flutter,
            '--disable-service-auth-codes',
            '--max_profile_depth=256',
            '--observe=8888',
            '--pause_isolates_on_unhandled_exceptions=false',
            '%s/bin/cache/dart-sdk/bin/snapshots/analysis_server.dart.snapshot' % flutter,
            '--enable-completion-model',
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        bufsize=1,
        universal_newlines=True,
        encoding='utf-8')
    cwd = os.getcwd()
    test = '%s/%s' % (cwd, 'test.dart')
    # Set analysis roots.
    make_request(server, 0, 'analysis.setAnalysisRoots', {'included': [cwd], 'excluded': []})
    # Set priority files.
    make_request(server, 1, 'analysis.setPriorityFiles', {'files': [test]})
    # Set completion subscriptions.
    make_request(server, 2, 'completion.setSubscriptions', {'subscriptions': ['AVAILABLE_SUGGESTION_SETS']})
    # Make 100k completion requests.
    for i in range(3, 100000):
        print(i)
        make_request_with_test(
            server, i, 'completion.getSuggestions',
            {'file': test, 'offset': i % 260},
            lambda msg: msg.get('event') == 'completion.results')


if __name__ == '__main__':
    main()
