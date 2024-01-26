# trilobot-web-remote

A basic web page remote control for a Pimoroni Trilobot. It runs a Flask
server on the robot, and can be accessed on one's LAN. Controls for robot to
go forward, reverse, left, right, or stop. Exit button closes the web server.

To install clone or download this repository to the Trilobot Raspberry Pi,
and install required pacakges (trilobot, flask). On the RPi CLI, to
start the server you can run:

```
python3 app2.py
```

You can get the IP address on your device by running in the CLI:

```
ifconfig
```

And that should do it. Remember not to drive your bot off the table!

!['ui'](screenshot.jpg)

