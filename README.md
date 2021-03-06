# Restbot: Automate testing on JSON API's using the YAML language.

(In development currently, started on 15 april 2018.)

## Features
- Test GET,POST,PUT,DELETE requests
- Multiple assertions checks

## Example
```
$ cat restbot/tests/assets/tests-github.yml
url: "https://github.com/restbot/restbot"
tests:
    - name: "Testing if Restbot repo is up"
      path: "/"
      request: "GET"
      expected:
        - status: 200
        - content: "Automate testing on JSON API's"

$ restbot/restbot.py restbot/tests/assets/tests-github.yml 
Time: 1287 ms

OK (1 tests, 1 assertions)
```

## Prerequisites
To run Restbot, you will need the following:
- git
- python3
- pip3

## Installation
Install dependencies from requirements.txt
```
git clone [this repository]
cd restbot/restbot
sudo pip3 install -r requirements.txt
```

## Assertion criteria
Use the <b>expected</b> parameter to assert expected behaviour from a test.

| option | description |
|-|-|
| content | Matches if value is in content, case-insensitive |
| value | Matches if value is equal to content, case-sensitive |
| status | Matches if value is equal to HTTP response code |
| not_content | Matches if value is <b>not</b> in content, case-insensitive |
| not_value | Matches if value is <b>not</b> equal to content, case-sensitive |
| not_status | Matches if value is <b>not</b> equal to HTTP response code |

## Test parameters
The following parameters need to be used in a test:

| | |
|-|-|
| **name** | name of the test |
| **request** | type of request (GET,POST,PUT,DELETE) |
| **path** | path to endpoint |
| **expected** | assertion criteria |
| **sleep** (optional) | sleep specified seconds after test |
| **headers** (optional) | list of specified headers |

## License
Licensed under AGPL3.
