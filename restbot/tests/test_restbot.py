import sys
from os.path import dirname,abspath
sys.path.append(dirname(dirname(abspath(__file__))))

from unittest import TestCase
from unittest import main

current_dir = abspath(dirname(__file__))

import restbot

class TestCase1(TestCase):

    def test_assert_test4(self):
        """
        Test false status code, good content
        """
        test = {
              "name": "Testing HTTPBIN.org, 200 status",
              "path": "/",
              "url": "http://httpbin.org/get",
              "request": "GET",
              "expected": [{"status":404},{"content":"Accept-Encoding"}]
        }
        result,errors = restbot.assert_test(test)
        expected = False
        self.assertEqual(expected,result)
        self.assertEqual(1,len(errors))
        self.assertEqual(("status",404,200),errors[0])

    def test_assert_test3(self):
        """
        Test good status code, good content
        """
        test = {
              "name": "Testing HTTPBIN.org, 200 status",
              "path": "/",
              "url": "http://httpbin.org/get",
              "request": "GET",
              "expected": [{"status":200},{"content":"Accept-Encoding"}]
        }
        result,errors = restbot.assert_test(test)
        expected = True
        self.assertEqual(expected,result)
        self.assertEqual(0,len(errors))


    def test_assert_test2(self):
        """
        Test false status code
        """
        test = {
              "name": "Testing HTTPBIN.org, 200 status",
              "path": "/",
              "url": "http://httpbin.org/get",
              "request": "GET",
              "expected": [{"status":300}]
        }
        result,errors = restbot.assert_test(test)
        expected = False
        self.assertEqual(expected,result)
        self.assertEqual(1,len(errors))
        self.assertEqual(("status",300,200),errors[0])

    def test_assert_test(self):
        """
        Test good status code
        """
        test = {
              "name": "Testing HTTPBIN.org, 200 status",
              "path": "/",
              "url": "http://httpbin.org/get",
              "request": "GET",
              "expected": [{"status":200}]
        }
        result,errors = restbot.assert_test(test)
        expected = True
        self.assertEqual(expected,result)
        self.assertEqual(0,len(errors))

    def test_request_to_response(self):
        request = {
            "url": "http://httpbin.org/get",
            "verb" : "GET",
            "headers": {},
            "data": {},
            "verify": True
        }
        result,time_took = restbot.request_to_response(request)
        self.assertEqual(200,result.status_code)
        self.assertTrue(time_took < 4)

    def test_test_to_request(self):
        test = {
              "name": "Testing restbot #1",
              "path": "/",
              "url": "http://httpbin.org/get",
              "request": "GET",
              "expected": [{"status":200}]
        }
        result = restbot.test_to_request(test)
        expected = {
            "url": "http://httpbin.org/get",
            "verb" : "GET",
            "headers": {},
            "data": {},
            "verify": True
        }
        self.assertEqual(expected,result)

    def test_yml_to_tests(self):
        result = restbot.yml_to_tests(current_dir + "/assets/tests1.yml")
        expected = [{
            "name": "Testing restbot #1",
              "path": "/",
              "url": "http://httpbin.org/get",
              "request": "GET",
             "expected": [{"status":200}]
        },{
            "name": "Testing restbot #2",
              "path": "/hello",
              "url": "http://httpbin.org/get/hello",
              "request": "POST",
              "data":{"name":"As a user, I want to test GET/POST requests"},
             "expected": [{"not_content":""}]
        }]
        self.assertEqual(expected,result)

if __name__ == '__main__':
    main()
