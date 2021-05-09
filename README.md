# Setup instructions
Note: These setup instructions assume you’re running on a Windows machine, and require you to have Ubuntu 18.04 Windows Subsystem for Linux 2, which adds additional capabilities (such as Docker) over base WSL.

- Clone [AItomotives/Ardupilot](https://github.com/AItomotives/Ardupilot) repository
- Clone [AItomotive/ros](https://github.com/AItomotives/ros) repository
- Clone the [EXACT](https://github.com/travisdesell/exact) repository
- Install [MissionPlanner](https://ardupilot.org/planner/docs/mission-planner-installation.html)
- Enable [WSL2](https://docs.microsoft.com/en-us/windows/wsl/install-win10) on your computer. Make sure you follow the steps to enable WSL2.
- Install [Docker](https://docs.docker.com/docker-for-windows/install/) for Windows.

### Run the docker container
1. `cd` to the ardupilot directory 
2. Build the docker container with 

  ```
  docker build . -t ardupilot
  ``` 

If this is the first time, this may take a while, as the docker container will be cloning and downloading Ros, which is a few gigabytes, so you can estimate based on your internet speed.

4. Run this command. Replace `{path_to_exact}` with the location of your EXACT clone and `{path_to_ros}` with the location of your ROS clone.

  ```
  docker run --rm -it -v {path_to_exact}/exact/build/rnn_examples:/exact -v {path_to_ros}/ros:/catkin_ws -v `pwd`:/ardupilot ardupilot:latest bash
  ```

7. Your docker container should now be running. You will have to have more terminals connected to this container, so if you’re comfortable using things like `tmux`, you can do that. Alternatively, you can open a new terminal and connect to the container. To do this, get the name of the container from the Docker gui or the command `docker container ls`. Then use the command `docker exec -it {container name} /bin/bash` to enter the container. 

### Start Ardupilot
1. In a non-docker terminal run `ip config` to find the ip address of the currently running WSL instance.
2. Start MissionPlanner
3. In your docker instance `cd ArduCopter`
4. `./run.sh {IP_Address}` with your WSL ip address. Mission Planner should automatically connect but if it doesn’t then connect to your MissionPlanner instance with the connect button in the top right. Feel free to go into the script and just put in your IP address as long as you don't commit it, especially if you're running this multiple times. Otherwise, I recommend you keep it on hand. Ardupilot should continue

### Start ROS
1. Open a new terminal and connect to the Docker instance
2. `cd /catkin_ws` and `./roscore_build.sh` For some reason this fails the first time it's run, run it again. This was happening for a little bit, but shouldn't. If it keeps failing, there may be additional issues.
3. Open a new terminal and connect to the Docker instance
4. `cd /catkin_ws` and `./rosrun_node.sh`
