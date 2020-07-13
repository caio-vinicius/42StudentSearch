#!/usr/bin/env python3

import json
import requests
import sys

print(sys.argv[1])

authorization = 'Bearer ################################################################'
headers = {'Authorization': authorization}

try:
    s = requests.get('https://api.intra.42.fr/v2/campus', headers=headers)
except:
    print("Something went wrong")

r = json.loads(s.text)

print(json.dumps(r, indent=4, sort_keys=True))
