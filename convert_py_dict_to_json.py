import json
import sys
import os
from light_blue_red_72hours import recipe as data

file_name = "light_blue_red_72hours"
#file_name = sys.argv[1]

#print(file_name)
#with open(file_name, 'r') as f:
#    data = json.loads(f)
print(data)
new_file_name = os.path.splitext(file_name)[0] + ".json"
print(new_file_name)
with open(new_file_name, 'w') as outfile:
    json.dump(data, outfile)

