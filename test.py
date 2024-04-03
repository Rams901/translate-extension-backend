import requests
url = "http://127.0.0.1:8000/upload/"

with open("../input.mp3", "rb") as file:
    r = requests.post(url, files={'file': file})