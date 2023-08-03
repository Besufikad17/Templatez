from halo import Halo
from termcolor import colored
from zipfile import ZipFile
import requests
import sys, os
import readline
import json, shutil

history_file = '.myhistory'
readline.read_history_file(history_file)

def add_template(template: dict):
    url = "https://jade-clean-hedgehog.cyclic.cloud/templates"
    l = len(fetch_templates())
    payload = json.dumps({
      "id": l + 1,
      "name": template["name"],
      "type": template["type"],
      "author": template["author"],
      "technologies": template["technologies"],
      "github": template["github"],
      "url": template["url"],
      "stars": template["stars"],
      "language": template["language"]
    })
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.status_code
    except requests.exceptions.Timeout:
        halo.fail(colored("Took longer than expected, please check your connection and try again!!", "red"))
    except requests.exceptions.HTTPError as err:
        halo.fail(colored(err, "red"))
   
def to_string(x: list):
    s = ""
    for element in x:
        if x.index(element) == len(x) - 1:
            s = s + str(element)
        else:
            s = s + str(element) +","
    return s
   
def fetch_templates(filters={}):
    try:
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
    except requests.exceptions.Timeout:
        halo.fail(colored("Took longer than expected, please check your connection and try again!!", "red"))
    except requests.exceptions.HTTPError as err:
        halo.fail(colored(err, "red"))
         

def fetch_repo_data(author: str, repo_name: str):
    url = f"https://api.github.com/repos/{author}/{repo_name}" 
    try:
        response = requests.get(url).json()
        url = f"https://api.github.com/repos/{author}/{repo_name}/zipball/main"
        if response["fork"]:
            return response["parent"]["language"], response["stargazers_count"], url
        else:
            return response["language"], response["stargazers_count"], url
    except requests.exceptions.Timeout:
        halo.fail(colored("Took longer than expected, please check your connection and try again!!", "red"))
    except requests.exceptions.HTTPError as err:
        halo.fail(colored(err, "red"))

def move_and_remove(dir_name: str):
    source_folder = os.getcwd() + "/" + dir_name + "/"
    destination_folder = os.getcwd() + "/"

    for file_name in os.listdir(source_folder):        
        source = source_folder + file_name
        destination = destination_folder + file_name
        shutil.move(source, destination)
    os.rmdir(source_folder)

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
            if os.listdir()[0].startswith(template["author"]):
                move_and_remove(os.listdir()[0])
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
        try:
           choice = print_menu()
           if choice.startswith("templates"):
               templates = []
               if choice == "t" or choice == "templates":
                   with Halo("Fetching templates..", spinner='dots'):
                       templates = fetch_templates() 
               else:
                   with Halo("Fetching templates..", spinner='dots'):
                       templates = fetch_templates(parse_filters(choice)) 
               print(colored("\t{:<25} {:<15} {:<10} {:<20} {:<15} {:<15}".format("Name", "Language", "Type", "Tech Stack", "Author", "Stars"), "blue"))
               for template in  templates:
                   print_template_info(template)
           elif choice.startswith("use"): 
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
                   print(colored("\t{:<3} {:<25} {:<15} {:<10} {:<20} {:<15} {:<15}".format("No.","Name", "Language", "Type", "Tech Stack", "Author", "Stars"), "blue"))
                   for i in range(len(template)):
                       print_template_info(template[i], i + 1)
                   no = int(input("select template : "))
                   try:
                       t = template[no - 1]
                       project_title = input("project title: ") 
                       os.mkdir(project_title)
                       os.chdir(project_title)
                       download_and_install(t)
                       break
                   except OSError:
                       print(colored(f"Directory exists with the name {project_title}!!", "red"))
                   except (IndexError, ValueError):
                       print(colored("Please select valid template number", "red"))  
           elif choice == "a" or choice == "add":
                name = input("name of the template : ")
                ttype = input("type of the template : ")
                technologies = input("tech stack used : ")
                github_url = input("github url : ")
                gdata = github_url.split("/")
                if name == "" or ttype == "" or technologies == "":
                    print(colored("Please enter valid inputs!!", "red"))
                    break
                if gdata[0] == "https:" and gdata[2] == "github.com" and len(gdata) == 5:
                    with Halo("Checking the github repo...", spinner='dots'):
                        template = fetch_templates({"github": github_url})
                    if len(template) == 0:
                        stars = 0
                        lang = ""
                        url = ""
                        with Halo("Fetching repo info..", spinner='dots'):
                            lang, stars, url = fetch_repo_data(gdata[3], gdata[4])
                        template = {
                            "name": name,
                            "type": ttype,
                            "author": gdata[3],
                            "technologies": [technologies],
                            "github": github_url,
                            "url": url,
                            "stars": stars,
                            "language": lang
                        }
                        print(colored("\t{:<25} {:<15} {:<10} {:<20} {:<15} {:<15}".format("Name", "Language", "Type", "Tech Stack", "Author", "Stars"), "blue"))
                        print_template_info(template)
                        c = input("Submit (Y/N) ? ")
                        if c.startswith("y"):
                            with Halo("Uploading template...", spinner='dots') as halo:
                                code = add_template(template)
                                if code != 500:
                                    halo.succeed("Done...")
                                else:
                                    halo.fail("Error occurred")
                    else:
                        print(colored("There is a template with this github repo!!", "red"))
                else:
                    print(colored("Please enter valid github url!!", "red"))
           elif choice == "q" or choice == "quit":
                break
           elif choice == "h" or choice == "help":
                pass
           else:
                print(colored("Invalid choice, use 'h' to get help", "red")) 
        except (KeyboardInterrupt, EOFError):
            break 
        readline.add_history(choice)
        readline.write_history_file(history_file) 
else:
    print(sys.argv)
