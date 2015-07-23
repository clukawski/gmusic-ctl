# conrad's terrible google play music client

Something I'm just making for fun on my own that I can integrate
it into my window manager with something no fuss like dmenu.

Don't expect this to work. It's a WIP I threw together one night;
some things (like the queue) are broken because initially I was
just writing this for kicks before I realized I'd actually prefer
this over Google's clunky JS/HTML5 interface.

I claim no responsibility for any harm physical or emotional
attempting to use this tool.

See LICENSE for copyright/liability stuff (MIT).

### vague instructions

The tool is designed to use google to figure out what you wanted to listen to,
type what you wanted and it'll select the first/most popular result (so far it's
worked 100% of the time for things I've tried)

* control.py is the controller
* server.py is the server

You will have to chmod +x these.

### less vague instructions

replace queue with a song:

```sh
python2 control.py -s "gordon lightfoot edmund fitzgerald"
```

replace queue with an album:

```sh
python2 control.py -a "wu tang 36 chambers"
```

add song to the queue:

```sh
python2 control.py -q -s "gordon lightfoot edmund fitzgerald"
```

add album to the queue:

```sh
python2 control.py -q -a "wu tang 36 chambers"
```

The rest of the commands should be fairly obvious (control.py --help), but are probably broken.

### requires:

* python 2.7
  * toml
  * gst/pygst
  * zmq
  * latest development build of gmusicapi:
	* pip install --upgrade git+https://github.com/simon-weber/gmusicapi.git@develop
	* this may be pip2 if you're on archlinux
