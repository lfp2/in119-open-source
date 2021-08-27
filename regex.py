import re
import requests
import json
import pandas

file = open('text.txt', 'r')

p = re.compile('^https:\/\/github\.com\/(?P<owner>[a-zA-Z]*)\/(?P<repo>[a-zA-Z.]*)$')

ghinfos = []

for line in file:
    m = p.match(line)
    if m:
        ghinfo = {'owner': m.group('owner'), 'repo': m.group('repo')}
        ghinfos.append(ghinfo)

print(ghinfos)

for info in ghinfos:
    r = requests.get(f'https://api.github.com/repos/{info["owner"]}/{info["repo"]}')
    print(f'Information about {info["repo"]} retrieved')
    with open(f'./repos/{info["repo"]}_{info["owner"]}.json', "w") as out_file:
        json.dump(r.json(), out_file, sort_keys = False)
    print(f'Project {info["repo"]} exported with success!')