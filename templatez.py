from halo import Halo
from termcolor import colored
import requests


def add_template():
    return None

def to_string(x: list):
    s = ""
    for element in x:
        if x.index(element) == len(x) - 1:
            s = s + str(element)
        else:
            s = s + str(element) +","
    return s
   
def fetch_templates(filters={}):
    if len(filters.items()) == 0:
        return requests.get("https://jade-clean-hedgehog.cyclic.cloud/templates").json()
    else:
        query = "?"
        for key in filters.keys():
            if list(filters.keys()).index(key) == len(filters.keys()):
                query = query + key + "=" + filters[key]
            else:
                query = query + key + "=" + filters[key] + "&"
        return requests.get(f"https://jade-clean-hedgehog.cyclic.cloud/templates{query}").json() 

def print_ascii():
    with open('ascii.txt', 'r') as f:
        for line in f:
            print(line.rstrip())

def print_menu(): 
    return input(" -> ")

def parse_filters(cmd: str):
    cmd_list = cmd.split(" ")
    filters = {}
    for command in cmd_list:
        if "=" in command:
            filters[command.split("=")[0] + "_like"] = command.split("=")[1]
    return filters

print_ascii()

while True:
    choice = print_menu()
    if choice.startswith("t") or choice.startswith("templates"):
        templates = []
        if choice == "t" or choice == "templates":
            with Halo("Fetching templates..", spinner='dots'):
                templates = fetch_templates() 
        else:
            with Halo("Fetching templates..", spinner='dots'):
                templates = fetch_templates(parse_filters(choice))
        print(colored("\t{:<25} {:<15} {:<10} {:<20} {:<15} {:<15}".format("Name", "Language", "Type", "Technologies", "Author", "Stars"), "blue"))
        for template in  templates:
            print("\t{:<25} {:<15} {:<10} {:<20} {:<15} {:<15}".format(template["name"], template["language"], template["type"], 
                                                                        to_string(template["technologies"]), 
                  template["author"], "⭐" * template["stars"]))
    elif choice == "a" or choice == "add":
        pass
    elif choice == "q" or choice == "quit":
        break
    elif choice == "h" or choice == "help":
        pass
    else:
        print("Invalid choice, use 'h' to get info")

