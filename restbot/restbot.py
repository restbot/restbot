import yaml
import time
import requests

verify = True
global_headers = {}

class Asserter():

    def __init__(self,expected,response,time_took):
        self.expected = expected
        self.response = response
        self.time_took = time_took

    def content(self):
        return str(self.expected).lower() in str(self.response.text).lower()

    def not_content(self):
        return str(self.expected).lower() not in str(self.response.text).lower()

    def value(self):
        return self.expected == self.response.text

    def not_value(self):
        return self.expected != self.response.text

    def status(self):
        return self.expected == self.response.status_code

    def not_status(self):
        return self.expected != self.response.status_code

def assert_test(test):
    result = True
    request = test_to_request(test)
    response,time_took = request_to_response(request)
    errors = []
    asserters = ["content","value","status","not_content","not_value","not_status"]
    for expected in test["expected"]: # [ {status:200},{content:hello}]
        for key,expected_value in expected.items(): # status:200
            for asserter in asserters: # asserters
                if key == asserter:
                    a = Asserter(expected_value,response,time_took)
                    if not getattr(a,asserter)():
                        result = False
                        result_response = response.text
                        if "status" in asserter:
                            result_response = response.status_code

                        errors.append((asserter,expected_value,result_response))

    return result,errors

def request_to_response(request):
    response = None
    time_start = time.time()
    verb = request["verb"].upper()
    if verb == 'GET':
        response = requests.get(request["url"],headers=request["headers"],verify=request["verify"])
    elif verb == 'POST':
        response = requests.post(request["url"],json=request["data"],headers=request["headers"],verify=request["verify"])
    elif verb == 'PUT':
        response = requests.put(request["url"],json=request["data"],headers=request["headers"],verify=request["verify"])
    elif verb == 'DELETE':
        response = requests.delete(request["url"],json=request["data"],headers=request["headers"],verify=request["verify"])
    else:
        raise Exception("Unsupported HTTP method: %s" % request)

    time_took = time.time()-time_start
    return response,time_took

def test_to_request(test):
    global verify,global_headers
    request = {}
    request["url"] = test["url"]
    request["headers"] = {}
    request["data"] = test.get("data",{})

    # Load global headers
    for g_header,g_value in global_headers.items():
        request["headers"][g_header] = g_value

    # Override global headers with test headers
    if test.get("headers") is not None:
        for header,value in test["headers"].items():
            request["headers"][header] = value


    request["verify"] = verify
    request["verb"] = test["request"]
    return request

def yml_to_tests(yml_file):
    tests = []
    test_counter = 0
    with open(yml_file,'r') as f:
        doc = yaml.load(f)
        if doc.get("url",None) is None:
            raise Exception("[url] not found in file %d" % test_counter)

        if doc.get("tests",None) is None:
            raise Exception("[tests] not found in file %d" % test_counter)

        for test in doc.get("tests"):

            # Check required parameters
            req_params = ["path","name","request","expected"]
            for req_param in req_params:
                if test.get(req_param,None) is None:
                    raise Exception("[%s] not found in test %d" % (req_param,test_counter))

            # Create url from endpoint+path
            test["url"] = "%s%s" % (doc.get("url"),test["path"].rstrip("/"))
            tests.append(test)

    return tests
