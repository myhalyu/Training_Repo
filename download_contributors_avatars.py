import requests
import json
import os
import argparse

BASE_URL = 'https://api.github.com/repos/{}/{}/contributors'


#get list of contributors with avatars
def get_contributors(user_name, project_name):
    contributors_avatars = {}
    response = requests.get(BASE_URL.format(user_name, project_name))
    json_data = json.loads(response.text)

    for record in json_data:
        contributors_avatars[record['login']] = record['avatar_url']

    return contributors_avatars


#save single picture to disk
def download_picture(user_name, project_name, contributor_name, picture_url):
    folder_name = '{}/{}'.format(user_name,project_name)
    os.makedirs(folder_name, exist_ok=True)

    response = requests.get(picture_url, stream=True)
    file_type = response.headers['Content-Type'].split('/')[1]
    file_name = '{}/{}.{}'.format(folder_name, contributor_name, file_type)

    with open(file_name, 'wb') as image:
        for chunk in response.iter_content(chunk_size=128):
            image.write(chunk)


#parse input arguments
parser = argparse.ArgumentParser(description='Download avatars from GitHub project')
parser.add_argument('-u', '--user', required=True, help='input GitHub user', action='store')
parser.add_argument('-p', '--project', required=True, help='input user project', action='store')

args = parser.parse_args()

cont_avatars = get_contributors(args.user, args.project)

for contributor in cont_avatars:
    download_picture(args.user, args.project, contributor, cont_avatars[contributor])
