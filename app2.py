from flask import Flask, Response, render_template, request, jsonify
import threading
from multiprocessing import Process, Queue
import json
import os
import signal
from trilobot import *


app = Flask(__name__)
SPEED = 0.7
robot_initialized = False
robot_lock = threading.Lock()
robot_process = None
command_que = None

def initialize_robot(speed):
    # Lock to only allow a single thread to run this code at one time
    with robot_lock:
        global robot_initialized
        # Only initialize the processs to control Trilobot once in a thread
        if not robot_initialized:
            global robot_process
            global command_que
            # queue to push commands to the control process
            command_que = Queue()
            # Initialize and start the process
            robot_process = Process(target=dispatch_command, args=(command_que, 
                                                                   SPEED))
            robot_process.start()
            robot_initialized = True

def dispatch_command(que, speed):
    tbot = Trilobot()
    while True:
        # If there is a command in the queue, dequeue and execute it
        if not que.empty():
            command = que.get()
            if command == "exit":
                tbot.stop()
                break
            elif command == "forward":
                tbot.forward(speed)
            elif command == "reverse":
                tbot.backward(speed)
            elif command == "left":
                tbot.turn_left(speed)
            elif command == "right":
                tbot.turn_right(speed)
            else:
                tbot.stop()

# Route to load the webpage
@app.route('/')
def home():
    return render_template('index.html')

# Route for remote controls (you can adapt this as needed)
@app.route('/controls')
def remote_controls():
    initialize_robot(SPEED)
    command = request.args.get("command")
    if command == "exit":
        # push "exit" command
        command_que.put("exit")
        # wait for control process to exit
        robot_process.join()
        status = {'status': 'exit'}
        os.kill(os.getpid(), signal.SIGINT)
    else:
        command_que.put(command)
        status = {'status': command}
    return jsonify(json.dumps(status))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

