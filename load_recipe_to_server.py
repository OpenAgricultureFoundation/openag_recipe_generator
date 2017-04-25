#!/usr/bin/python
import couchdb
import argparse
import json
import requests
import subprocess
import sys

SERVICE_BASE_URI = "/_openag/api/0.0.1/service"

def load_args():
    parser = argparse.ArgumentParser(description="Load recipes to couchdb instance",
                                     epilog="Example usage: ./load_recipe_to_server.py -a \"http://10.1.10.106:5984\" -r light_blue_red_72hours.json -u --start_recipe")
    parser.add_argument('-a', '--server_url', help='Couchdb Server: http://localhost:5984  (dont forget the http or port)')
    parser.add_argument('-f', '--server_list', help='Server URLs file name')
    parser.add_argument('-r', '--recipe', help='Recipe json file path. It should be a proper json file.')
    parser.add_argument('-u', '--upload_recipe', help='Upload the recipe to the server (True/False) Default:False', action='store_true', default=False)
    parser.add_argument('-s', '--start_recipe', help='Start recipe after uploading it? (True/False) Default:False', action='store_true', default=False)
    parser.add_argument('-q', '--stop_recipe', help='Stop recipe running on pfc (True/False) Default:False', action='store_true', default=False)

    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()
    return args, parser


def validate_server_uri(server_uri):
    # Need to account for ending slash
    if not server_uri.startswith("http"):
        server_uri = "http://" + server_uri
    if not server_uri[-5] == ":":
        server_uri += ":5984"
    return server_uri


def load_recipe(file_name):
    with open(file_name, 'r') as f:
        data = json.load(f)
    return data


def save_to_server(server_uri, db_name, document):
    server = couchdb.Server(server_uri)
    db = server[db_name]
    db[document['_id']] = document


def start_recipe_on_server(server_uri=None, recipe_id=None, environment="environment_1"):
    service_url = server_uri + SERVICE_BASE_URI
    api_url = service_url + "/environments/{}/start_recipe".format(environment)
    print(api_url)
    # r = requests.post(api_url, params = recipe_id)
    # Not sure what format the post needs to be in...
    cmd_string = "curl -H 'Content-Type: application/json' \
                       -X POST {} \
                       -d \'[\"{}\"]\'".format(api_url, recipe_id)
    print(cmd_string)
    subprocess.call(cmd_string, shell=True)
    # assert r.status_code == "200"


def stop_recipe_on_server(server_uri=None, environment="environment_1"):
    service_url = server_uri + SERVICE_BASE_URI
    api_url = service_url + "/environments/{}/stop_recipe".format(environment)
    cmd_string = "curl -X POST {} ".format(api_url)
    print(cmd_string)
    subprocess.call(cmd_string, shell=True)


def upload_and_start_recipe(server_uri=None,
                            upload_recipe=None,
                            recipe_dict=None):
    print(upload_recipe)
    if server_uri and upload_recipe:
        db_name = "recipes"
        print("Uploading " + recipe_dict["_id"] + " ...")
        save_to_server(server_uri, db_name, recipe_dict)
    if start_recipe:
        print("Sending command to start recipe " + recipe_dict["_id"])
        start_recipe_on_server(server_uri, recipe_dict["_id"])


def start_recipe_on_mutiple_pfcs(server_list_file_name=None, **kwargs):
    """
    Start a recipe running on a group of PFCS
    """
    server_list = load_list_of_servers(server_list_file_name)
    for server_uri in server_list:
            upload_and_start_recipe(server_uri, **kwargs)


def main():
    args, parser = load_args()
    recipe_dict = load_recipe(args.recipe)
    if 'server_list_file_name' in args and os.path.exists(args.server_list_file_name):
        print(args)
        start_recipe_on_mutiple_pfcs(server_list_file_name=args.server_list_file_name,
                                     recipe_dict=recipe_dict, **args)
    elif 'server_uri' in args:
        upload_and_start_recipe(**args)
    elif 'stop_recipe' in args:
        stop_recipe_on_server(**args)
    else:
        print("Command not found.")
        print(args)
        parser.print_help()

def test_start_recipe_on_server():
    results = start_recipe_on_server("http://10.1.10.240:5984", "light_blue_red_72hours")
    assert results["message"] == "Success" and results["success"] == True


def test_stop_recipe_on_server():
    print(stop_recipe_on_server("http://10.1.10.2:5984"))
    assert False


if __name__ == '__main__':
    main()
