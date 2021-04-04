source $rossetup
catkin_make
./mavlink_setup
source devel/setup.bash
rosrun linearity linearbreak.py &
rosrun linearity readwaypoints.py
