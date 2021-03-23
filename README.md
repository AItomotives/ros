# ros
In the AItomotives Ardupilot Docker image, once Ardupilot is running and connected to MissionPlanner.
- In a new terminal: `rosrun roscore` : Roscore is what allows nodes and topics within ros to exist
- In a new terminal: `roslaunch apm.launch` : This will startup MAVRos. Ardupilot will recognize a new connection at this point
- In a new terminal: `catkin_make_isolated` : This will be how you build the source code. If it's the first time you've done this, this will make new directories in your catkin workspace. Everytime you build you'll need to `source devel_isolated/setup.bash`. This won't take up a terminal all by itself, but you need a workspace to run these commands in a terminal that isn't already being occupied by a node.
- Any node you startup like this will need it's own separate terminal. `rosrun ros_package ros_node.py` : This will run any node that you pass it within the corresponding ros package