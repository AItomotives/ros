source $rossetup
catkin_make
./mavlink_setup.sh
source devel/setup.bash
rosrun linearity linearbreak.py &
sleep 2
rosrun linearity DroneState.py &
sleep 2
rosrun linearity readwaypoints.py
