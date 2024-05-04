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
                ('green', 10000),
                ('yellow', 10000),
                ('red', 10000),
                ('blue', 10000),
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
        self.my_device_id = self.get_parameter('device_id').value
        self.my_command_id = self.get_parameter('command_id').value
        self.my_green = str(self.get_parameter('green').value)
        self.my_yellow= str(self.get_parameter('yellow').value)
        self.my_blue = str(self.get_parameter('blue').value)
        self.my_red = str(self.get_parameter('red').value)


    def publish_can_frame(self, data_to_msg, frame: Frame = None):
        msg = Frame()
        msg.id = (self.my_device_id <<5) | self.my_command_id
        msg.is_extended = False
        msg.is_error = False
        msg.dlc = len(data_to_msg)
        msg.data = [int(data_to_msg[i]) if i < len(data_to_msg) else 0 for i in range(8)]

        self.publisher.publish(msg)
        self.get_logger().info(f"Published CAN frame {data_to_msg}")

    def topic_callback(self, msg):
        if msg.data == "Locked":
            self.my_blue= 11111
            self.my_data = 10001
            self.publish_can_frame(str(self.my_data))
        elif msg.data == "__none":
            self.my_red= 11111
            self.my_data = 11000
            self.publish_can_frame(str(self.my_data))
        elif msg.data == "joy_diff_drive":
            self.my_green = 11111
            self.my_data = 10100
            self.publish_can_frame(str(self.my_data))
        elif msg.data == "autonomic":
            self.my_yellow = 11111
            self.my_data = 10010
            self.publish_can_frame(str(self.my_data))
        


        

def main(args=None):
    rclpy.init(args=args)
    sent_canbus_messages = SentCanbusMessages()
    rclpy.spin(sent_canbus_messages)
    sent_canbus_messages.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()