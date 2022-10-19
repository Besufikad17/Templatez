import requests
import os
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

def print_menu():
    print("\t Welcome to Automata 🤖")
    print("1. Create react-vite template")
    print("2. Create express-ts-mongo")
    print("3. Exit")
    choice = int(input('-> '))
    return choice


def main():
    while True:
        ch = print_menu()



# response = requests.get(URL)
# open("template.zip", "wb").write(response.content)

