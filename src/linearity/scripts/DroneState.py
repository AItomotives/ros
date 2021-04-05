import rospy
from mavros_msgs import ParamGet

class DroneState:

    def __init__(self):
        self.time_interval = 5
        self.curr_time = 0
        self.state_list = []

    def droneSnapshot(self):
        wind_speed = 0
        wind_angle = 0
        battery_voltage = 0
        battery_current = 0
        position_x = 0
        position_y = 0
        position_z = 0
        orientation_x = 0
        orientation_y = 0
        orientation_z = 0
        orientation_w = 0
        velocity_x = 0
        velocity_y = 0
        velocity_z = 0
        angular_x = 0
        angular_y = 0
        angular_z = 0
        linear_acceleration_x = 0
        linear_acceleration_y = 0
        linear_acceleration_z = 0

        return {
            "time": self.curr_time,
            "wind_speed": wind_speed,
            "wind_angel": wind_angle,
            "battery_voltage": battery_voltage,
            "battery_current": battery_current,
            "position_x": position_x,
            "position_y": position_y,
            "position_z": position_z,
            "orientation_x": orientation_x,
            "orientation_y": orientation_y,
            "orientation_z": orientation_z,
            "orientation_w": orientation_w,
            "velocity_x": velocity_x,
            "velocity_y": velocity_y,
            "velocity_z": velocity_z,
            "angular_x": angular_x,
            "angular_y": angular_y,
            "angular_z": angular_z,
            "linear_acceleration_x": linear_acceleration_x,
            "linear_acceleration_y": linear_acceleration_y,
            "linear_acceleration_z": linear_acceleration_z
        }

if __name__ == '__main__':
    ds = DroneState()
    ds.state_list.append(ds.droneSnapshot())
    print(ds.state_list)