from django.test import TestCase

# Create your tests here.

import json
msg='中文,'

u=json.dumps(msg)
print(u)

print(type(u))

n=json.loads(u)
print(n)