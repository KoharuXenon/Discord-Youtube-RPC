import signal
import subprocess
import threading
import time
import requests
from pypresence import Presence
import discord
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from asyncio import tasks
import os
os.system("cls")

global rpc_connected
rpc_connected = False

bot_token = 'BOT_TOKEN'
client_id = 'RPC_APPLICATION_ID'

TARGET_USER = 0 #Replace with your discord ID
TARGET_GUILD = 0 #Replace with a server you share with the bot

global s_song_name
global s_song_artist
s_song_name = "No song name."
s_song_artist = "No artist."

RPC = Presence(client_id)
intents = discord.Intents.all()
client = discord.Client(intents=intents)
app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes


def nonewlineprint(stringtoprint:str):
    print(stringtoprint, "\u001b[F" * stringtoprint.count('\n'), end='\r')


@app.route('/update_presence', methods = ["GET", "POST"])
def update_presence():
    global s_song_name
    global s_song_artist
    songName = request.args.get("name", "No name.")
    songArtist = request.args.get("artist", "No artist.")
    clearit = request.args.get("clearit", "no")

    s_song_name = songName
    s_song_artist = songArtist
    if clearit == "yes":
        s_song_name = None
        s_song_artist = None
        finalStatus = f"Song cleared."
    else:
        finalStatus = f"Status changed to:\n\n{s_song_name}\n{s_song_artist}"

    return Response(finalStatus, mimetype='text/plain')

    
@app.route('/shutdown')
def shutdown_server():
    os.kill(os.getpid(), signal.SIGINT)
    RPC.clear()
    return "Shutting down"


def start_flask():
    global rpc_connected
    RPC.connect()
    rpc_connected = True

    app.run(debug=False)

    print("Closing rpc loop")


@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    presence_thread.start()
    activities_thread.start()


def update_client_activities():
    global s_song_name
    global s_song_artist
    global rpc_connected

    times = 0

    while True:
        if rpc_connected:
            nonYoutubeActivites = []
            theUser:discord.Member = client.get_guild(TARGET_GUILD).get_member(TARGET_USER)
            for activity in theUser.activities:
                #print(activity)
                if activity.name != "YouTube":
                    nonYoutubeActivites.append(activity.name)

            
            nonewlineprint(" "*100)

            if times % 10 == 0:
                firefoxoutput = subprocess.check_output("tasklist /FI \"IMAGENAME eq firefox.exe\"", shell=True, text=True).strip()
                if "No tasks are running which match the specified criteria." in firefoxoutput:
                    s_song_name = None
                    s_song_artist = None

            if len(nonYoutubeActivites) != 0 or (s_song_name == None and s_song_artist == None):
                if s_song_name == None and s_song_artist == None:
                    nonewlineprint("Song cleared")
                else:
                    nonewlineprint(f"There are non youtube activites: {', '.join(nonYoutubeActivites)}.")
                RPC.clear()
            else:
                nonewlineprint("No other activites")
                RPC.update(details=s_song_name, state=s_song_artist, large_image="big_icon")

            times += 1

        time.sleep(1)


presence_thread = threading.Thread(target=start_flask)
activities_thread = threading.Thread(target=update_client_activities)

client.run(bot_token)
nonewlineprint(" "*100)
print("Closing bot")
rpc_connected = False
requests.get("http://127.0.0.1:5000/shutdown")


presence_thread.join()