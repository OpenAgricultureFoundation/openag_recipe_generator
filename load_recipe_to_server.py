#!/usr/bin/python
import couchdb
import argparse
import json
import requests
import subprocess
import sys
import pdb
import os

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


def validate_server_url(server_url):
    # Need to account for ending slash
    if not server_url.startswith("http"):
        server_url = "http://" + server_url
    if not server_url[-5] == ":":
        server_url += ":5984"
    return server_url


def load_recipe(file_name):
    with open(file_name, 'r') as f:
        data = json.load(f)
    return data


def save_to_server(server_url, db_name, document):
    server = couchdb.Server(server_url)
    db = server[db_name]
    db[document['_id']] = document


def start_recipe_on_server(server_url=None, recipe_id=None, environment="environment_1"):
    service_url = server_url + SERVICE_BASE_URI
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


def stop_recipe_on_server(server_url=None, environment="environment_1", **kwargs):
    service_url = server_url + SERVICE_BASE_URI
    api_url = service_url + "/environments/{}/stop_recipe".format(environment)
    cmd_string = "curl -X POST {} ".format(api_url)
    print(cmd_string)
    subprocess.call(cmd_string, shell=True)


def upload_and_start_recipe(server_url=None,
                            upload_recipe=None,
                            recipe_dict=None,
                            start_recipe=None,
                            stop_recipe=None, **kwargs):
    print(upload_recipe)

    if server_url and upload_recipe:
        db_name = "recipes"
        print("Uploading " + recipe_dict["_id"] + " ...")
        try:
            save_to_server(server_url, db_name, recipe_dict)
        except couchdb.http.ResourceConflict:
            print("Warning: Recipe failed to upload. Already on the server. \
            Recipe Name: {} PFC: {}".format(recipe_dict['_id'], server_url))

    if start_recipe:
        if stop_recipe is not None and stop_recipe: # Stop currently running recipe
            stop_recipe_on_server(server_url=server_url, **kwargs)
        print("Sending command to start recipe " + recipe_dict["_id"])
        start_recipe_on_server(server_url, recipe_dict["_id"])


def load_list_of_servers(file_name):
    if not os.path.exists(file_name):
        raise Exception("File is missing. " + file_name)
    server_list = []
    with open(file_name, 'r') as f:
        for line in f:
            server_list.append(line)
    return server_list


def start_recipe_on_mutiple_pfcs(server_list=None, server_url=None, **kwargs):
    """
    Start a recipe running on a group of PFCS
    """
    server_list = load_list_of_servers(server_list)
    for server_url in server_list:
            server_url = server_url.replace("\n", "")
            server_url = server_url.replace("\r", "")
            print("Running recipe on {}".format(server_url))
            upload_and_start_recipe(server_url=server_url, **kwargs)
            print("----------------\n\n")

def main():
    args, parser = load_args()
    recipe_dict = load_recipe(args.recipe)
    if args.server_list is not None and os.path.exists(args.server_list):
        start_recipe_on_mutiple_pfcs(recipe_dict=recipe_dict, **vars(args))
    elif args.server_url is not None:
        upload_and_start_recipe(recipe_dict=recipe_dict, **vars(args))
    elif args.stop_recipe is not None:
        stop_recipe_on_server(**vars(args))
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
