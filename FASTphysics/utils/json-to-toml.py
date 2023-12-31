# helper file not actually used in FASTphysics
# useful for making the firestore json key to streamlit-readable toml key

import toml, os

current_file_path = os.path.dirname(os.path.realpath(__file__))

key_file = os.path.join(current_file_path, "../.streamlit/firestore.json")
output_file = os.path.join(current_file_path, "../.streamlit/secrets.toml")

# check if FIRESTORE_KEY is already in secrets.toml, if yes then exit
with open(output_file) as target:
    if "FIRESTORE_KEY" in target.read():
        print("FIRESTORE_KEY already in secrets.toml")
        exit()

with open(key_file) as json_file:
    json_text = json_file.read()

config = {"FIRESTORE_KEY": json_text}
toml_config = toml.dumps(config)

with open(output_file, "a") as target:
    target.write(toml_config)
