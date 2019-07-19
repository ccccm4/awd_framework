import sys
import requests
import re
from forexp.forexp import *
import random
import string

argv_array = sys.argv
url = argv_array[-1]    # 
salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))
webshell = generate_nodieshell(salt)
# print url
flag_pattern = re.compile('flag\{.*\}')

# exp
webshell_url = 'aaaaaaaaaaaaaaaaaaaaaa'
flag = 'flag{aaaaaaaaaaaaaaaaaaaaaaaaaaaa}'
# url = url+'/flag.txt'
# r = requests.get(url)
# flag = flag_pattern.findall(r.content)[0]

print [flag,salt]


