import couchdb
import argparse
import json


def load_args():
    parser = argparse.ArgumentParser(description="Load recipes to couchdb instance",
                                     eplilog="python load_recipe_to_server.py -s \"http://10.1.10.106:5984\" -r light_blue_red_72hours.json")
    parser.add_argument('-s', '--server', help='Couchdb Server: http://localhost:5984  (dont forget the http or port)')
    parser.add_argument('-r', '--recipe', help='Recipe json file path. It should be a proper json file.')
    args = parser.parse_args()
    return args.server, args.recipe


def load_recipe(file_name):
    with open(file_name, 'r') as f:
        data = json.load(f)
    return data


def save_to_server(server_uri, db_name, document):
    server = couchdb.Server(server_uri)
    db = server[db_name]
    db[document['_id']] = document


def main():
    server_uri, recipe_file_name = load_args()
    recipe_dict = load_recipe(recipe_file_name)
    db_name = "recipes"
    print(recipe_dict)
    save_to_server(server_uri, db_name, recipe_dict)


if __name__ == '__main__':
    main()
