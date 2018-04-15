import sys
from os.path import dirname,abspath
sys.path.append(dirname(dirname(abspath(__file__))))

from unittest import TestCase
from unittest import main

current_dir = abspath(dirname(__file__))

import restbot

class TestCase1(TestCase):

    def test_yml_to_tests(self):
        result = restbot.yml_to_tests(current_dir + "/assets/tests1.yml")
        expected = [{
            "name": "Testing restbot #1",
              "path": "/",
              "url": "http://localhost:3000/api/boards/",
              "request": "GET",
             "expected": [{"status":200}]
        },{
            "name": "Testing restbot #2",
              "path": "/hello",
              "url": "http://localhost:3000/api/boards/hello",
              "request": "POST",
              "data":{"name":"As a user, I want to test GET/POST requests"},
             "expected": [{"not_content":""}]
        }]
        self.assertEqual(expected,result)

if __name__ == '__main__':
    main()
