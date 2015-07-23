import sys
import argparse
import zmq

def main():
    parser = argparse.ArgumentParser(description='gmusic server/client crap')
    parser.add_argument('-a', action='store')
    parser.add_argument('-s', action='store')
    parser.add_argument('-q', action='store_true')
    parser.add_argument('-w', action='store_true')
    parser.add_argument('--pause', action='store_true')
    parser.add_argument('--play', action='store_true')
    parser.add_argument('--stop', action='store_true')
    parser.add_argument('--skip', action='store_true')
    parser.add_argument('--prev', action='store_true')
    parser.add_argument('--halt', action='store_true')

    args = parser.parse_args()

    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect('tcp://127.0.0.1:6666')

    if args.w:
        msg = {'command': 'what'}
        socket.send_json(msg)
    if args.a:
        if args.q:
            msg = {'command': 'albumquery', 'query': args.a, 'queue': True}
            socket.send_json(msg)
        else:
            msg = {'command': 'albumquery', 'query': args.a}
            socket.send_json(msg)
    elif args.s:
        if args.q:
            msg = {'command': 'trackquery', 'query': args.s, 'queue': True}
            socket.send_json(msg)
        else:
            msg = {'command': 'trackquery', 'query': args.s}
            socket.send_json(msg)
    elif args.pause:
        print('pause')
        msg = {'command': 'pause'}
        socket.send_json(msg)
    elif args.play:
        print('play')
        msg = {'command': 'play'}
        socket.send_json(msg)
    elif args.stop:
        print('stop')
        msg = {'command': 'stop'}
        socket.send_json(msg)
    elif args.skip:
        print('skip')
        msg = {'command': 'skip'}
        socket.send_json(msg)
    elif args.prev:
        print('prev')
        msg = {'command': 'prev'}
        socket.send_json(msg)
    elif args.halt:
        print('halt')
        msg = {'command': 'halt'}
        socket.send_json(msg)

if __name__ == "__main__":
    main()
