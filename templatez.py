from halo import Halo
from termcolor import colored
from zipfile import ZipFile
import requests
import sys, os

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

def download_and_install(template: dict):
    cwd = os.getcwd()
    url = template["url"]
    github = template["github"]
    with Halo("Downloading template archive..", spinner='dots') as halo:
        try:
            response = requests.get(url)
            open("template.zip", "wb").write(response.content)
            halo.succeed("Download completed")
        except requests.exceptions.Timeout:
            halo.fail(colored("Took longer than expected, please check your connection and try again!!", "red"))
        except requests.exceptions.HTTPError as err:
            halo.fail(colored(err, "red"))
    with Halo("Extracting files..", spinner='dots') as halo:
        try:
            with ZipFile("template.zip", 'r') as zip_ref:
                zip_ref.extractall(cwd)
            halo.succeed("Extracting files completed")
        except BadZipfile:
            halo.fail(colored("Corrupted template archive!!", "red"))
    with Halo("Cleaning files..") as halo:
        try:
            os.remove("template.zip")
            halo.succeed("Done")
        except OSError:
            halo.fail(colored("Template archive not found!!"))
    print(f"Done, make sure you follow instructions listed here {github} and star the project 😜")

def print_ascii():
    with open('ascii.txt', 'r') as f:
        for line in f:
            print(line.rstrip())

def print_menu(): 
    return input(" -> ")

def print_template_info(template: dict, no=0):
    if no == 0:
        print("\t{:<25} {:<15} {:<10} {:<20} {:<15} {:<15}".format(template["name"], template["language"], template["type"], 
                                                                        to_string(template["technologies"]), 
                  template["author"], "⭐" * template["stars"]))
    else:
        print("\t{:<3} {:<25} {:<15} {:<10} {:<20} {:<15} {:<15}".format(str(no), template["name"], template["language"], template["type"], 
                                                                        to_string(template["technologies"]), 
                  template["author"], "⭐" * template["stars"]))

def parse_filters(cmd: str):
    cmd_list = cmd.split(" ")
    filters = {}
    for command in cmd_list:
        if "=" in command:
            filters[command.split("=")[0] + "_like"] = command.split("=")[1]
    return filters


if len(sys.argv) == 1:
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
            for template in  templates:
                print_template_info(template)
        elif choice.startswith("u") or choice.startswith("use"): 
            filters = parse_filters(choice)
            template = []
            if len(filters) == 0: 
                print(colored("Please enter the name of the template you want to use!!", "red"))
            else: 
                with Halo("Fetching template..", spinner='dots'):
                    template = fetch_templates(filters)
            if len(template) == 0:
                print(colored("The specified template could not found!!", "red"))
            else:
                print(colored("\t{:<3} {:<25} {:<15} {:<10} {:<20} {:<15} {:<15}".format("No.","Name", "Language", "Type", "Technologies", "Author", "Stars"), "blue"))
                for i in range(len(template)):
                    print_template_info(template[i], i + 1)
                no = int(input("select template : "))
                try:
                   t = template[no - 1]
                   project_title = input("project title: ") 
                   os.mkdir(project_title)
                   os.chdir(project_title)
                   download_and_install(t)
                except OSError:
                    print(colored(f"Directory exists with the name {project_title}!!", "red"))
                except (IndexError, ValueError):
                   print(colored("Please select valid template number", "red"))  
        elif choice == "a" or choice == "add":
            pass
        elif choice == "q" or choice == "quit":
            break
        elif choice == "h" or choice == "help":
            pass
        else:
            print("Invalid choice, use 'h' to get help")
else:
    print(sys.argv)
