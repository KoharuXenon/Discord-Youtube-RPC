# Discord-Youtube-RPC
YouTube to Discord RPC (like spotify)

Very simple script to show what song youre currently listening to on youtube.

(only works when listening to the "my mix" playlist, unless youre smart enough to change the playist code in the js)


## Requirements

1. Uh your computer silly
2. python installed on said computer
3. discord
4. these python packages:
   requests, pypresence, discord.py, flask, flask-cors

   command to quick install them: `pip install requests pypresence discord.py flask flask-cors`
5. An internet browser that you can install [Tampermonkey](https://www.tampermonkey.net/) on.
6. the tampermonkey script installed.
7. at least 1 braincell

### Notes
If you want to run the python script automatically, you could make a task in the windows task scheduler, and make `pythonw.exe` open the script instead of `python.exe`, or rename the script's extension to .pyw and then put it in the startup folder or do what you want with it.

(pythonw won't create a window for the script so you wont have a cmd window open constantly that way :3)
(same for .pyw files (i think))
