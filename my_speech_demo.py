#!/usr/bin/env python3
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A demo of the Google CloudSpeech recognizer."""
import argparse
import locale
import logging
import requests

from aiy.voice import tts
from aiy.board import Board, Led
from aiy.cloudspeech import CloudSpeechClient



def get_hints(language_code):
    if language_code.startswith('en_'):
        return ('CPE', 'cpe', 'csc',
                'CSC')
    return None

def locale_language():
    language, _ = locale.getdefaultlocale()
    return language

def create_query_endpoint(query, host_ip):
    base_endpoint = "http://" + host_ip + "/"
    query_endpoint = "query?query=" + query.replace(" ", "+")
    return base_endpoint + query_endpoint


def main():
    host_ip = "192.168.1.87:5000"
    logging.basicConfig(level=logging.DEBUG)

    #parser = argparse.ArgumentParser(description='Assistant service example.')
    #parser.add_argument('--language', default=locale_language())
    #args = parser.parse_args()

    #logging.info('Initializing for language %s...', args.language)
    hints = get_hints(locale_language())
    client = CloudSpeechClient()
    with Board() as board:
        while True:
            if hints:
                logging.info('Say something, e.g. %s.' % ', '.join(hints))
            else:
                logging.info('Say something.')
            text = client.recognize(language_code=locale_language(),
                                    hint_phrases=hints)
            if text is None:
                logging.info('You said nothing.')
                continue

            logging.info('You said: "%s"' % text)
            text = text.lower()
            query_endpoint = create_query_endpoint(text, host_ip)
            response = requests.get(query_endpoint).text
            print(response+ "\n\n")
            tts.say(response)

if __name__ == '__main__':
    main()
