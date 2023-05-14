#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import time
PI = 3.1415926535897

x = 0
y = 0
theta = 0
x0,y0=5.4,5.4
def go_to_goalpose(x_goal, y_goal):
    global x, y, theta
    velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    vel_msg = Twist()

    while True:
        K_linear = 1
        distance = abs(math.sqrt((((x_goal - x) ** 2) + ((y_goal - y) ** 2))))

        linear_speed = distance * K_linear

        K_angular = 20.0
        desired_angle_goal = math.atan2(y_goal - y, x_goal-x)
        angular_speed = (desired_angle_goal - theta) * K_angular

        vel_msg.linear.x = linear_speed
        vel_msg.angular.z = angular_speed

        velocity_publisher.publish(vel_msg)

        if (distance <= 0.01):
            break
        
def takepose(pose_message):
    global x, y, theta
    x = pose_message.x
    y = pose_message.y
    theta = pose_message.theta
    #print("x: ",x,"y: ",y,"theta: ",theta)


def move():
    # Starts a new node
    rospy.init_node('robot_lawn', anonymous=True)
    velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    vel_msg = Twist()
    global x, y, theta
    n=5
    #Receiveing the user's input
    print("Let's move your robot")
    speed = input("Input your speed:")
    l = float(input("Type your Length:"))
    w = float(input("Type your width:"))
    angle =90
    #Since we will be moving just in x-axis
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    vel_msg.angular.z = 0
    angular_speed = 30*2*PI/360
    relative_angle = angle*2*PI/360
    i=1
    while i<=n:
        vel_msg.linear.x = abs(speed)
        #Setting the current time for distance calculus
        mt0 = rospy.Time.now().to_sec()
        current_distance = 0
        
        #Code for Wall avoidance
        if(i%2!=0 and (i+1)%4==0):
            if(x-l>0):
                d=l
                
            else:
                d=x
                
           
        elif(i%2!=0 and (i+1)%4!=0):
            if(x+l<10.5):
                d=l
                
            else:
                d=10.5-x
                
        else:   
            if(y+w<10.5):
                d=w
                
            else:
                d=10.5-y       

        if(d<0.5):
               break
########################### Moving the  Turtle ##########################                     
        while(current_distance < d):
            #Publish the velocity
            velocity_publisher.publish(vel_msg)
            #Takes actual time to velocity calculus
            mt1=rospy.Time.now().to_sec()
            #Calculates distancePoseStamped
            current_distance= speed*(mt1-mt0)
        #After the loop, stops the robot
        vel_msg.linear.x = 0
        velocity_publisher.publish(vel_msg)
################## Rotating the Turtle #################################
        if i%4==0 or (i+1)%4==0:
            vel_msg.angular.z = -abs(angular_speed)
        else:
            vel_msg.angular.z = abs(angular_speed)
        if(i==n):
            vel_msg.angular.z =0
            
        t0 = rospy.Time.now().to_sec()
        current_angle = 0
        while(current_angle < relative_angle):
           velocity_publisher.publish(vel_msg)
           t1 = rospy.Time.now().to_sec()
           current_angle = angular_speed*(t1-t0)
        vel_msg.angular.z = 0
        vel_msg.linear.x =  0
        velocity_publisher.publish(vel_msg)
        i+=1  
    
if __name__ == '__main__':
    try:
        #Getting the Turtles Postion
        position_topic = "/turtle1/pose"
        pose_subscriber = rospy.Subscriber(position_topic, Pose, takepose)
        time.sleep(2)
        move()
        #Moving the Turtle Back to initial  Postion        
        go_to_goalpose(x0,y0)
    except rospy.ROSInterruptException: pass


