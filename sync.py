from sys import path as file_dir
from os import chdir
from shutil import unpack_archive
from subprocess import run

import requests
from bs4 import BeautifulSoup

settings = {
    # Overleaf instance url
    "OVERLEAF_INSTANCE_URL": "http://hostname.com",
    # Project id (can be seen in the url when project is opened)
    "OVERLEAF_PROJECT_ID": "",
    # Overleaf login email
    "OVERLEAF_USER_EMAIL": "",
    # Overleaf login password
    "OVERLEAF_USER_PASSWORD": "",
    # A subdirectory where the project code is stored to in repository
    "GIT_SUBDIR": "latex",
    # Git branch name
    "GIT_BRANCH_NAME": "main",
    # Git commit user name
    "GIT_USER_NAME": "User Name",
    # Git commit user email
    "GIT_USER_EMAIL": "user@domain.com",
    # Git repository url. Repo must already be created
    "GIT_REMOTE_URL": "git@github.com:user/repo.git"
}

def main():
    # Prepare repository directory
    run(["/bin/bash", "-c", "./pre_sync.sh"], env=settings)

    # Get data from overleaf
    s = requests.Session()
    # First get the login site to get a valid csrf token
    r = s.get(f"{settings['OVERLEAF_INSTANCE_URL']}/login")
    soup = BeautifulSoup(r.text, "html.parser")
    csrf_token = soup.select_one('input[name="_csrf"]')['value']

    # Now login
    r = s.post(f"{settings['OVERLEAF_INSTANCE_URL']}/login", json={"email": settings["OVERLEAF_USER_EMAIL"], "password": settings["OVERLEAF_USER_PASSWORD"], "_csrf": csrf_token}, headers={"Content-Type": "application/json", "X-Csrf-Token": csrf_token})
    # Then just download the project zip file
    r = s.get(f"{settings['OVERLEAF_INSTANCE_URL']}/project/{settings['OVERLEAF_PROJECT_ID']}/download/zip")
    with open("content.zip", "wb") as file:
        file.write(r.content)
    
    # Unzip it
    unzip_path = "content"
    if(settings["GIT_SUBDIR"] and settings["GIT_SUBDIR"] != ""):
        unzip_path += "/" + settings["GIT_SUBDIR"]
    unpack_archive("content.zip", unzip_path)

    # Git commit and push
    run(["/bin/bash", "-c", "./commit_script.sh"], env=settings)

    # Cleanup
    run(["rm", "content.zip"])
    run(["rm", "-rf", "content"])

if __name__ == "__main__":
    chdir(file_dir[0])
    main()