# -*- coding: utf-8 -*-
"""Untitled61.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1CPCJBHaWX9Q4tmdZKMaqDgLa76hJMgTk
"""


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.path as mplPath
import cv2
from queue import PriorityQueue

frame_length, frame_breadth = 500, 1200
frame_color = (255, 255, 255)
output_file_path = 'output.mp4'
fps = 30



# Initializing frame
frame = np.ones((frame_length, frame_breadth, 3), dtype=np.uint8)

# Video writer setup
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

video_writer = cv2.VideoWriter(output_file_path, fourcc, fps, (frame_breadth, frame_length))

# Shape definitions
hexagon_points = np.array([[771, 320], [650, 390], [528, 320], [528, 180], [650, 110], [771, 179]])
u_shape_points = np.array([
    [900, 50], [1100, 50], [1100, 450], [900, 450],
    [900, 125], [1020, 125], [1020, 375], [900, 375]
])


# Drawing shapes on the canvas
# Hexagon
cv2.polylines(frame, [hexagon_points], True, frame_color, 5)
cv2.fillPoly(frame, [hexagon_points], frame_color)

# First rectangle
cv2.rectangle(frame, (100, 0), (175, 400), frame_color, -1)


# Second rectangle
cv2.rectangle(frame, (275, 100), (350, 500), frame_color, -1)

# U shape
cv2.polylines(frame, [u_shape_points], True, frame_color, 5)
cv2.fillPoly(frame, [u_shape_points], frame_color)

class Node:


    def __init__(self, x, y, cost=None, parent=None):

        self.x = x
        self.y = y
        self.cost = cost
        self.parent = parent

    def __lt__(self, other):

        return self.cost < other.cost

    def getPoints(self):

        return (self.x, self.y)

    def getCost(self):

        return self.cost

    def addCost(self, cost):

        self.cost = cost

    def updateCost(self, cost):

        if self.cost is None or cost < self.cost:
            self.cost = cost

    def getParent(self):

        return self.parent

    def addParent(self, parent):

        self.parent = parent




def canMove(point):
    if point[0] < 6 or point[0] > 1195 or point[1] < 6 or point[1] > 495:
        return False
    point_color = frame[point[1], point[0]]
    if point_color[0] == 1 and point_color[1] == 1 and point_color[2] == 1:
        return True
    if point_color[0] == 255 and point_color[1] == 0 and point_color[2] == 0:
        return True
    return False


def get_start_end_points():
    initial_point = int(input("Enter for initial x coordinate : ")), int(input("Enter for initial y coordinate : "))
    goal_point = int(input("Enter for final x coordinate: ")), int(input("Enter for final y coordinate : "))
    if canMove(initial_point) and canMove(goal_point):
        return initial_point, goal_point
    else:
        print("These Invalid points. Please enter the valid points.")
        return get_start_end_points()

#Action Space

def to_move_up(node):
    given_points = node.getPoints()
    new_points = (given_points[0],given_points[1]+1)
    if not canMove(new_points):
        return False , None ,0
    return True, new_points, 1


def to_move_up_left(node):
    given_points = node.getPoints()
    new_points = (given_points[0]-1,given_points[1]+1)
    if not canMove(new_points):
        return False , None ,0
    return True, new_points , 1.4

def to_move_up_right(node):
    given_points = node.getPoints()
    new_points = (given_points[0]+1,given_points[1]+1)
    if not canMove(new_points):
        return False , None,0
    return True, new_points , 1.4

def to_move_down(node):
    given_points = node.getPoints()
    new_points = (given_points[0],given_points[1]-1)
    if not canMove(new_points):
        return False , None ,0
    return True, new_points , 1

def to_move_down_left(node):
    given_points = node.getPoints()
    new_points = (given_points[0]-1,given_points[1]-1)
    if not canMove(new_points):
        return False , None, 0
    return True, new_points, 1.4

def to_move_down_right(node):
    given_points = node.getPoints()
    new_points = (given_points[0]+1,given_points[1]-1)
    if not canMove(new_points):
        return False , None ,0
    return True, new_points, 1.4

def to_move_left(node):
    given_points = node.getPoints()
    new_points = (given_points[0]-1,given_points[1])
    if not canMove(new_points):
        return False , None ,0
    return True, new_points, 1

def to_move_right(node):
    given_points = node.getPoints()
    new_points = (given_points[0]+1,given_points[1])
    if not canMove(new_points):
        return False , None ,0
    return True, new_points, 1


def to_find_and_plt_backTracking(node):
    path = []

    while node is not None:
        path.append(node.getPoints())
        node = node.getParent()

    path =path[::-1]
    for i in range(1, len(path)):
        cv2.line(frame, path[i-1], path[i], (255, 255, 0), 2)
        video_writer.write(frame)

    video_writer.release()
    plt.imshow(frame)
    plt.show()


def shortest_path_with_dijkstra(start, goal):
    open_list = PriorityQueue()
    my_dict = dict()
    close_list = set()


    start_node = Node(start[0], start[1],cost=0)
    open_list.put((0, start_node))
    my_dict[start] = start_node

    while not open_list.empty():
        current_node = open_list.get()[1]


        if current_node.getPoints() == goal:
            print("Goal reached")
            return current_node

        temp = my_dict.get(current_node.getPoints())
        if temp is not None:
            if temp.getCost() < current_node.getCost():
                continue


        actions = [to_move_up, to_move_down, to_move_left, to_move_right, to_move_up_left, to_move_up_right, to_move_down_left, to_move_down_right]

        for action in actions:
            canMove, newPoints, newCost = action(current_node)
            if canMove:
                possible_next_node = Node(newPoints[0], newPoints[1], cost=newCost+ current_node.getCost() , parent=current_node)

                if my_dict.get(newPoints) is None:
                    my_dict[newPoints] = possible_next_node
                    open_list.put((possible_next_node.getCost(), possible_next_node))
                else:
                    if my_dict[newPoints].getCost() > possible_next_node.getCost():
                        my_dict[newPoints] = possible_next_node
                        open_list.put((possible_next_node.getCost(), possible_next_node))


if __name__ == "__main__":
    intial, final = get_start_end_points()
    goalreached = shortest_path_with_dijkstra(intial, final)
    to_find_and_plt_backTracking(goalreached)