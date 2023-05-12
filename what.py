from misc import ascii as art
from misc import animation
from misc import lolcat

from tts import tts

import traceback
import requests
import json
import os

DEFAULT_PLUGIN = "naruto"

def main():
    lolcat.rainbow(art.logo)
    plugin = DEFAULT_PLUGIN
    @animation.process("Checking...", animation.braille)
    def run_checks():
        plugin_path = os.path.join(
                os.path.dirname(__file__),
                        "plugins", plugin, "plugin.json")
        if not os.path.exists(plugin_path):
            print()
            print(f"[ FATAL ] Plugin '{plugin}' has no information file. Please re-install it or use another one")
            print(f"HINT: {plugin_path}")
            return False
        try:
            with open(plugin_path, "r") as f:
                info = json.load(f)
        except json.JSONDecodeError as e:
            print()
            print(f"[ FATAL ] Plugin '{plugin}' - information file invalid. Please re-install the plugin or use another one")
            print(f"HINT: {e}")
            print(f"HINT: {plugin_path}")
            return False
        reqfiles = []
        for x in info["format"]:
            reqfiles.append(x["file"])
            if x["audio"]:
                reqfiles.append(x["audio"])
        for file in reqfiles:
            if not os.path.exists(
                    os.path.join(
                        os.path.dirname(__file__),
                        "plugins",
                        plugin,
                        file
                    )):
                print()
                print(f"[ FATAL ] Plugin '{plugin}' - dependency not found - {file}")
                return False
        return info
    try:
        info = run_checks()
        if info == False:
            exit(1)
    except KeyError:
        print(traceback.format_exc())
        print("[ FATAL ] Invalid plugin information file")
        exit(1)
    @animation.process("Fetching resources...")
    def load_source():
        source = info["api"]
        collected = []
        for i in range(1):
            response = requests.get(source)
            data = json.loads(response.text)
            collected.append(data)
        return collected
    
    data = load_source()
    credit = [x["source"] for x in data]
    n = []
    for i in credit:
        if not i in n:
            n.append(i) # Remove duplicate sources
    credit = n
    
    text = data[0]["text"]
    temp_dir = os.path.join(os.path.dirname(__file__), "temp/")
    if not os.path.exists(temp_dir):
        os.mkdir(temp_dir)

    @animation.process("Processing text-to-speech...")
    def generate_tts():
        path = os.path.join(temp_dir, "audio.mp3")
        tts.save(text, path)

    generate_tts()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Terminating...")
        exit()
