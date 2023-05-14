# TurtleSim Lawn Mover

##  About
The goal of this application is to create a lawnmower pattern in the Turtlesim Simulator using the length and width entered by the user.

## Output 
![image](https://user-images.githubusercontent.com/94766962/152721301-66108074-871d-41b5-b393-055b128b6c8f.png)

## To Clone 
```shell
cd ~/catkin_ws/src
git clone https://github.com/vkella/SES598.git
catkin build turtlesim_lawn

```
## To Run 
Launch Three Terminals 

Terminal 1
```shell
roscore

```
Terminal 2
```shell
rosrun turtlesim turtlesim_node

```
Terminal 3
```shell
rosrun turtlesim_lawn move.py

```
