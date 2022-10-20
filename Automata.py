#!/usr/bin/env python3
import requests
import os
from zipfile import ZipFile
from halo import Halo


TEMPLATES = [
    {
        "name": "react-vite-template",
        "language": "JavaScript",
        "technologies": ["Reactjs", "ViteJs"],
        "type": "Frontend",
        "url": "https://github.com/Besufikad17/react-vite-template/releases/download/%23template/react-vite-template.zip",
        "github": "https://github.com/Besufikad17/react-vite-template",
        "autour": "Besufikad"
    },
    {
        "name": "express-ts-mongo",
        "language": "TypeScript",
        "technologies": ["Expressjs", "MongoDB"],
        "type": "Backend",
        "url": "https://github.com/Besufikad17/express-ts-mongo-template/releases/download/%23template/express-ts-mongo.zip",
        "github": "https://github.com/Besufikad17/express-ts-mongo-template",
        "autour": "Besufikad"
    },
    {
        "name": "express-js-mongo",
        "language": "JavaScript",
        "technologies": ["Expressjs", "MongoDB"],
        "type": "Backend",
        "url": "https://github.com/Besufikad17/express-js-mongo-template/releases/download/%23template/express-js-mongo.zip",
        "github": "https://github.com/Besufikad17/express-js-mongo-template",
        "autour": "Besufikad"
    }
]

def install(url, fpath, github):
    halo = Halo("Downloading template..", spinner='dots')
    halo.start()
    response = requests.get(url)
    open("template.zip", "wb").write(response.content)
    halo.stop()

    halo.clear()
    halo.start("Extracting files..")
    with ZipFile("template.zip", 'r') as zip_ref:
        zip_ref.extractall(fpath)
    halo.stop()

    halo.clear()
    halo.start("Cleaning files..")
    
    os.remove("template.zip")
    halo.stop()
    print(f"Done, make sure you follow instructions listed here '{github}' and star the project 😜")

def print_menu():
    print("\t Welcome to Automata 🤖")
    print("1. Create react-vite template")
    print("2. Create express-ts-mongo")
    print("3. Create express-js-mongo")
    print("4. Exit")
    choice = int(input('-> '))
    return choice


def main():
    cwd = os.getcwd()
    while True:
        ch = print_menu()
        if ch != 4 and ch > 0:
            url = TEMPLATES[ch - 1]["url"]
            github_url = TEMPLATES[ch - 1]["github"]
            install(url, cwd, github_url)
            break
        elif ch == 4:
            print("Oyasumi")
            break
        else:
            print("Invalid option!! please try again.")

main()