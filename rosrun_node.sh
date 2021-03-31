source $rossetup
catkin_make
source devel/setup.bash
rosrun linearity $1
