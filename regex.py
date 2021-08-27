import re
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import math

file = open('text.txt', 'r')

p = re.compile('^https:\/\/github\.com\/(?P<owner>[a-zA-Z]*)\/(?P<repo>[a-zA-Z.]*)$')

ghinfos = []

for line in file:
    m = p.match(line)
    if m:
        ghinfo = {'owner': m.group('owner'), 'repo': m.group('repo')}
        ghinfos.append(ghinfo)

print(ghinfos)

#for info in ghinfos:
#    r = requests.get(f'https://api.github.com/repos/{info["owner"]}/{info["repo"]}')
#    print(f'Information about {info["repo"]} retrieved')
#    with open(f'./repos/{info["repo"]}_{info["owner"]}.json', "w") as out_file:
#        json.dump(r.json(), out_file, sort_keys = False)
#    print(f'Project {info["repo"]} exported with success!')

#for info in ghinfos:
#    r = requests.get(f'https://api.github.com/repos/{info["owner"]}/{info["repo"]}/stats/code_frequency')
#    print(f'Information about {info["repo"]} retrieved')
#    with open(f'./weekly/{info["repo"]}_{info["owner"]}.json', "w") as out_file:
#        json.dump(r.json(), out_file, sort_keys = False)
#    print(f'Project\'s commits {info["repo"]} exported with success!')

weekly_info = []
infos = []

for info in ghinfos:
    infos.append(info["repo"])
    with open(f'./weekly/{info["repo"]}_{info["owner"]}.json') as json_file:
        data = json.load(json_file)
        # Adds columns to the weekly activity
    df = pd.DataFrame(data, columns=['ts', 'add', 'del'])
    # Filters activity before 2016
    df = df[df.ts > 1451606400]
    # Transforms from UNIX to Date
    df['ts'] = df['ts'].apply(lambda x: datetime.datetime.fromtimestamp(x))
    df['dif'] = (df['add'] - df['del'])
    weekly_info.append(df)
    plt.plot(df['ts'], df['dif'])
    plt.savefig(f'./graphs/{info["repo"]}_{info["owner"]}_weekly.png')
    plt.clf()

print(infos)
df_keys = pd.concat(weekly_info, keys=infos)
df_keys.to_csv('repos_weekly_concat.csv')
