# ros
More in depth ROS commands. You won't need to do these things all of the time, as the setup scrips handle most of it. You'll see these steps in the scripts that you run, so here is a way to do it manually.

In order to get access to the ros commands, everytime you open a new container, run `source $rossetup`.

- In a new terminal: `catkin_make` : This will be how you build the source code. If it's the first time you've done this, this will make new directories in your catkin workspace. 
- In a new terminal: `roscore` : Roscore is what allows nodes and topics within ros to exist
- In a new terminal: `roslaunch launch/launch.apm` : This will startup MAVRos. Ardupilot will recognize a new connection at this point
- Any node you startup like this will need it's own separate terminal. `catkin_make` again, then `source devel/setup.bash` from your catkin_ws. Thwn you can `rosrun <ros_package> <ros_node.py>` : This will run any node that you pass it within the corresponding ros package
