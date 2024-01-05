import os
import json
import pyemvue

# Get the absolute path to the keys.json file
local = os.path.dirname(os.path.abspath(__file__))
parent = os.path.dirname(local)
keys_path = os.path.join(parent, 'docs', 'keys.json')
with open(keys_path) as f:
    key = json.load(f)  # Load the keys from the JSON file

def login_pyemvue():
    vue = pyemvue.PyEmVue()
    try:
        vue.login(
            username=key['username'],
            password=key['password'],            
        )
    except OSError as e:
        print(f"Error: {e}")
        return None

    print("Logged in to the EMPORIA API", vue)
    return vue
