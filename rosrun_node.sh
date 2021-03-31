source $rossetup
catkin_make
source devel/setup.bash
rosrun linearity linearbreak.py &
rosrun linearity readwaypoints.py
