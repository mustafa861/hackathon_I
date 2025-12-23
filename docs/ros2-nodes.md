# ROS 2 Fundamentals

:::note Learning Objectives
- Create and configure ROS 2 nodes
- Publish and subscribe to topics
- Understand Quality of Service (QoS) policies
- Launch multi-node systems with Python launch files
:::

## Nodes: The Building Blocks

A **node** is a process that performs computation. In ROS 2, nodes communicate via:

- **Topics**: Asynchronous publish/subscribe (1-to-many)
- **Services**: Synchronous request/response (1-to-1)
- **Actions**: Long-running goals with feedback (1-to-1)

For this chapter, we focus on topics—the most common pattern.

## Creating Your First Node

```python
# File: minimal_publisher.py
# ROS 2 Humble - Ubuntu 22.04 LTS

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher = self.create_publisher(String, 'chatter', 10)
        self.timer = self.create_timer(0.5, self.timer_callback)
        self.count = 0

    def timer_callback(self):
        msg = String()
        msg.data = f'Hello ROS 2: {self.count}'
        self.publisher.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.count += 1

def main(args=None):
    rclpy.init(args=args)
    node = MinimalPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**Explanation**:
- `create_publisher(msg_type, topic_name, queue_size)`: Sets up a publisher
- `create_timer(period_sec, callback)`: Periodic callback (500ms here)
- `rclpy.spin(node)`: Keeps node alive, processing callbacks

## Quality of Service (QoS)

QoS policies control message delivery:

| Policy | Options | Use Case |
|--------|---------|----------|
| Reliability | `RELIABLE`, `BEST_EFFORT` | Sensor data (best effort) vs commands (reliable) |
| Durability | `TRANSIENT_LOCAL`, `VOLATILE` | Late-joining subscribers get history vs real-time only |
| History | `KEEP_LAST(n)`, `KEEP_ALL` | Buffer size for unprocessed messages |

**Example**:
```python
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

qos = QoSProfile(
    reliability=ReliabilityPolicy.RELIABLE,
    history=HistoryPolicy.KEEP_LAST,
    depth=10
)
self.publisher = self.create_publisher(String, 'critical_commands', qos)
```

## Subscriber Example

```python
# File: minimal_subscriber.py
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'chatter',
            self.listener_callback,
            10
        )

    def listener_callback(self, msg):
        self.get_logger().info(f'I heard: "{msg.data}"')

def main(args=None):
    rclpy.init(args=args)
    node = MinimalSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Python Launch Files

Launch files orchestrate multi-node systems:

```python
# File: talker_listener_launch.py
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='my_package',
            executable='minimal_publisher',
            name='talker',
            output='screen'
        ),
        Node(
            package='my_package',
            executable='minimal_subscriber',
            name='listener',
            output='screen'
        )
    ])
```

**Run with**: `ros2 launch my_package talker_listener_launch.py`

## Package Structure

```text
my_ros2_package/
├── package.xml          # Package metadata
├── setup.py             # Python package setup
├── my_ros2_package/
│   ├── __init__.py
│   ├── minimal_publisher.py
│   └── minimal_subscriber.py
├── launch/
│   └── talker_listener_launch.py
└── test/
```

**package.xml** (excerpt):
```xml
<?xml version="1.0"?>
<package format="3">
  <name>my_ros2_package</name>
  <version>0.0.1</version>
  <description>ROS 2 basics example</description>
  <maintainer email="you@example.com">Your Name</maintainer>
  <license>Apache-2.0</license>

  <depend>rclpy</depend>
  <depend>std_msgs</depend>
</package>
```

## Further Reading

- ROS 2 Humble Tutorials: https://docs.ros.org/en/humble/Tutorials.html
- DDS Specification: https://www.dds-foundation.org/
- Quigley, M., et al. (2009). "ROS: an open-source Robot Operating System". *ICRA Workshop*.

## Check Your Understanding

:::note Question 1
What is the primary purpose of a ROS 2 node?
A) To store data only
B) A process that performs computation
C) To provide power to the robot
D) To act as a communication hub only
**Answer**: B
:::

:::note Question 2
Which of the following is NOT a communication method between ROS 2 nodes?
A) Topics
B) Services
C) Actions
D) Direct function calls
**Answer**: D
:::

:::note Question 3
What does QoS stand for in ROS 2?
A) Quality of Service
B) Quick Operating System
C) Quantum Operating System
D) Quality of Software
**Answer**: A
:::

:::note Question 4
In the publisher example, what does create_timer(0.5, callback) do?
A) Creates a timer that triggers every 0.5 seconds
B) Creates a timer that runs for 0.5 seconds
C) Creates a timer that delays execution by 0.5 seconds
D) Creates a timer that limits processing to 0.5 seconds
**Answer**: A
:::

:::note Question 5
What is the purpose of rclpy.spin(node)?
A) To stop the node immediately
B) To keep the node alive, processing callbacks
C) To reset the node to initial state
D) To compile the node code
**Answer**: B
:::