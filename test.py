import requests

URL = 'http://localhost:8181'

assert requests.get(URL + '/store/asd:qwe').content == b'qwe'
assert requests.get(URL + '/store/aska:qweka').content == b'qweka'
assert requests.get(URL + '/store/foo:bar').content == b'bar'
assert requests.get(URL + '/store/').status_code == 418

assert requests.get(URL + '/get/asd').content == b'qwe'
assert requests.get(URL + '/get/').status_code == 418

assert requests.get(URL + '/find/qw').content == b'asd, qwe'
assert requests.get(URL + '/find/').status_code == 418

print("Test ran successfully")


