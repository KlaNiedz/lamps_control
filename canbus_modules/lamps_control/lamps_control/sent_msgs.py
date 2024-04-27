import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from can_msgs.msg import Frame

class SentCanbusMessages(Node):
    def __init__(self):
        super().__init__('sent_msgs')
        self.declare_parameters(
            namespace='',
            parameters=[
                ('device_id', 0),
                ('command_id', 0),
        ])
        self.my_data = 0

        self.send_topic = self.declare_parameter('send_topic', '/sent_canbus_messages').value
        self.default_receive_topics = [
            '/joy_multiplexer/selected_output',
            '/relaxing_middleware/state'
        ]
        self.receive_topics = self.declare_parameter('receive_topics', self.default_receive_topics).value
        for topic in self.receive_topics:
            self.subscription_ = self.create_subscription(
            String, topic, self.topic_callback, 10)

        self.publisher = self.create_publisher(Frame, self.send_topic, 10)
        # (self.my_device_id, self.my_command_id, self.my_data) = self.get_parameters(['device_id', 'command_id', 'data'])
        self.my_device_id = self.get_parameter('device_id').value
        self.my_command_id = self.get_parameter('command_id').value
        # self.my_data = str(self.get_parameter('data').value)
        # self.publisher_locked = self.create_publisher(Frame, 'can_frames_locked', 10)
        # self.publisher_idle = self.create_publisher(Frame, 'can_frames_idle', 10)
        # self.publisher_joy_diff_drive = self.create_publisher(Frame, 'can_frames_joy_diff_drive', 10)
        # self.publisher_none= self.create_publisher(Frame, 'can_frames_none', 10)


    def publish_can_frame(self, data_to_msg, frame: Frame = None):
        msg = Frame()
        msg.id = (self.my_device_id <<5) | self.my_command_id
        msg.is_extended = False
        msg.is_error = False
        msg.dlc = len(data_to_msg)
        msg.data = [int(data_to_msg[i]) if i < len(data_to_msg) else 0 for i in range(8)]

        self.publisher.publish(msg)
        # self.get_logger().info("Published CAN frame %s.", str(self.my_data))
        self.get_logger().info(f"Published CAN frame {data_to_msg}")

    def topic_callback(self, msg):
        if msg.data == "Locked":
            self.my_data = 10100
        elif msg.data == "__none":
            self.my_data = 10010
        elif msg.data == "joy_diff_drive":
            self.my_data = 10000
        elif msg.data == "autonomic":
            self.my_data = 11000
        else:
            self.my_data = 11011
        self.publish_can_frame(str(self.my_data))


        

def main(args=None):
    rclpy.init(args=args)
    # try:
    sent_canbus_messages = SentCanbusMessages()
    # sent_canbus_messages = SentCanbusMessages()
    rclpy.spin(sent_canbus_messages)
    sent_canbus_messages.destroy_node()
    rclpy.shutdown()
    # except rclpy.ROSInterruptException:
    #     pass
if __name__ == '__main__':
    main()