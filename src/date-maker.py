# program to extrat timestamps from ostree summary file
# only required if you also administer an ostree repository for MaPS
# requires 
# www-data ostree summary --repo=/srv/ostree/repo -v | grep "* " -A3 > summary.txt
# as input
import json

timestamps = {}
with open("summary.txt") as summaryfile:
    key = ""
    val = ""
    for i in summaryfile:
        if i[0] == '*':
            key = i.split()[-1]
        if 'Timestamp' in i:
            val = i.split()[-1].split('T')[0]
            timestamps[key] = val

with open("summary.json", 'w') as jsonfile:
    json.dump(timestamps, jsonfile)
