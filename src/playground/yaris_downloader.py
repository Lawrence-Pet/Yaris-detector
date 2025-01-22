import json
import os
import requests

# Set the current working directory to the file location
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# List of files with links to Yaris: 
json_lists = ['./100_response.json', './101_response.json']
yaris_list = []
for file in json_lists: 
    with open(file, 'r') as f:
        data = json.load(f)
        for item in data['items']:
            yaris_list.append(item)

Success = 0
Fails = 0

for i, yaris in enumerate(yaris_list):
    response = requests.get(yaris['link'])
    if response.status_code == 200:
        filename = os.path.join('./yaris_downloads', os.path.basename(yaris['link']))
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {filename}")
        Success+=1
    else:
        print(f"Failed to download {yaris['link']}")
        Fails+=1

print(f'\n Totally downloaded {Success} images!\nFailed to download {Fails} images :(')

