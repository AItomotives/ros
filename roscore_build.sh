source $rossetup
catkin_make
./mavlink_setup
roscore &
roslaunch launch/launch.apm
