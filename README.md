# ros
In the AItomotives Ardupilot Docker image, once Ardupilot is running and connected to MissionPlanner.

In order to get access to the ros commands, everytime you open a new container, run `source $rossetup`.

- In a new terminal: `catkin_make` : This will be how you build the source code. If it's the first time you've done this, this will make new directories in your catkin workspace. 
- In a new terminal: `roscore` : Roscore is what allows nodes and topics within ros to exist
- In a new terminal: `roslaunch apm.launch` : This will startup MAVRos. Ardupilot will recognize a new connection at this point
- Any node you startup like this will need it's own separate terminal. `rosrun ros_package ros_node.py` : This will run any node that you pass it within the corresponding ros package
