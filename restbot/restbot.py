import yaml

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
            test["url"] = "%s%s" % (doc.get("url"),test["path"])
            tests.append(test)

    return tests
