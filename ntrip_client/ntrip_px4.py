import rclpy
from rclpy.node import Node
from ntrip_client.submodules import ntrip
from px4_msgs.msg import GpsInjectData

class NtripRosNode(Node):
    def __init__(self):
        super().__init__('ntrip_ros_node')
        self.pub_ = self.create_publisher(GpsInjectData, "drone1/fmu/gps_inject_data/in", 10)
        self.timer_ = self.create_timer(0.1, self.timer_callback)
        self.ntrip_client_ = ntrip.NtripClient(caster="141.211.25.177", user="mair:Xjr6JbciWpnF", port=2102, mountpoint="MTF", lat=42.2944313, lon=-83.71044393888889, height=270.0)

    def timer_callback(self):
        data = self.ntrip_client_.read()
        if data is not None:
            print("got: ", len(data))
            msg = GpsInjectData()
            msg.timestamp = int(self.get_clock().now().nanoseconds / 1e6)
            msg.device_id = 0
            msg.len = min(300, len(data))
            msg.flags = 0
            msg.data[0:len(data)] = data
            self.pub_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    ntrip_node = NtripRosNode()
    rclpy.spin(ntrip_node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
