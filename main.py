from flask import Flask, render_template
import os
import random
import glob
import requests

app = Flask(__name__)




NAVIDROME_URL = os.environ.get("NAVIDROME_URL")
USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")




API_VERSION = "1.16.1"
CLIENT_NAME = "flask-now-playing"

def get_now_playing():
    endpoint = f"{NAVIDROME_URL}/rest/getNowPlaying.view"

    params = {
        "u": USERNAME,
        "p": PASSWORD,
        "v": API_VERSION,
        "c": CLIENT_NAME,
        "f": "json"
    }

    r = requests.get(endpoint, params=params, timeout=5)
    r.raise_for_status()

    data = r.json()
    return data["subsonic-response"]["nowPlaying"].get("entry", [])



@app.route("/")
def home():
    img_dir = os.path.join(app.static_folder, "img")
    images = os.listdir(img_dir)
    random_image = random.choice(images)
    try:
        now_playing_raw = get_now_playing()
    except:
        now_playing_raw = []

    if now_playing_raw == []:
        title = artist = suffix = None
        return render_template("index.html", image=random_image, title=title, artist=artist, suffix=suffix)

        

    else: 
        title = now_playing_raw[0]["title"]
        artist = now_playing_raw[0]["artist"]
        suffix = now_playing_raw[0]["suffix"]
        return render_template("index.html", image=random_image, title=title, artist=artist, suffix=suffix)



#if __name__ == '__main__':
#    app.run()