source $rossetup
catkin_make
./mavlink_setup
roscore &
sleep 5
roslaunch launch/launch.apm
