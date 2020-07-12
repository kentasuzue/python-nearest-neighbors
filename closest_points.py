# python3
from collections import namedtuple
from itertools import combinations
import sys
from random import randint

import sys
import threading
# import math
# from typing import List, Union
sys.setrecursionlimit(10 ** 9)  # max depth of recursion
threading.stack_size(2 ** 27)  # new thread will get stack of such size

from math import sqrt

Point = namedtuple('Point', 'x y')

def distance_squared(first_point, second_point):
    return (first_point.x - second_point.x) ** 2 + (first_point.y - second_point.y) ** 2

def minimum_distance_squared_naive(points):
    min_distance_squared = float("inf")

    for p, q in combinations(points, 2):
        min_distance_squared = min(min_distance_squared,
                                   distance_squared(p, q))

    return sqrt(min_distance_squared)


def merge_lists(list_one, list_two):
    list_merged = []
    list_one_index = 0
    list_two_index = 0
    #print("list one premerge", list_one)
    #print("list two premerge", list_two)

    while list_one_index < len(list_one) and list_two_index < len(list_two):
        if list_one[list_one_index].y <= list_two[list_two_index].y:
            list_merged.append(list_one[list_one_index])
            list_one_index += 1
        else:
            list_merged.append(list_two[list_two_index])
            list_two_index += 1
    #print("list one index", list_one_index)
    #print("list two index", list_two_index)
    #print("merged list until one list is done but not both", list_merged)
    #print("list one remaining", list_one[list_one_index:])
    #print("list two remaining", list_two[list_two_index:])

    list_merged.extend(list_one[list_one_index:])
    list_merged.extend(list_two[list_two_index:])

    return list_merged

def minimum_distance_squared(points):

    #print(f"points: {points}")

    def min_dist_recurs(x_sort, y_sort):
        #print(points)
        if len(points) <= 1:
            #print("len <= 1")
            return float("inf")

        if len(points) == 2:
            #print("len == 2")
            return distance_squared(*points)

        if len(points) == 3:
            #print("len == 3")
            return min(distance_squared(points[0], points[1]), distance_squared(points[0], points[2]),\
                distance_squared(points[1], points[2]))

        mid_x_index = len(x_sort) // 2
        x_sort_left = x_sort[:mid_x_index]
        x_sort_right = x_sort[mid_x_index:]

        points_left_set = set(x_sort_left)
        #points_left = x_sort[:mid_x_index]
        #points_right = x_sort[mid_x_index:]

        y_sort_left = []
        y_sort_right = []
        for y in y_sort:
            if y in points_left_set:
                y_sort_left.append(y)
            else:
                y_sort_right.append(y)
        #print(f"y_sort_left {y_sort_left}")
        #print(f"y_sort_right {y_sort_right}")

        min_dist = min(min_dist_recurs(x_sort_left, y_sort_left),\
            min_dist_recurs(x_sort_right, y_sort_right))
        #print(f"min_dist_recurs_left min_dist_recurs(points_left, x_sort_left, y_sort_left)")
        #print(f"min_dist_recurs_right min_dist_recurs(points_right, x_sort_right, y_sort_right)")
        #print(f"min_dist {min_dist}")
        #print(f"min_dist {min_dist}")
        #if min_dist == 0:
        #return 0

        y_sort_left_in_min_x_width = [point for point in y_sort_left if point.x >= x_sort_right[0].x - min_dist]

        #y_sort_left_in_min_x_width = []

        """
        prior_point = None
        for point in y_sort_left:
            if point.x >= x_sort_right[0].x - min_dist:
                if point.y == prior_y and :
                    
            prior_y = point.y
        """
        #[point for point in y_sort_left if point.x >= x_sort_right[0].x - min_dist]


        #assert all(y_sort_left_in_min_x_width[index].y <= y_sort_left_in_min_x_width[index + 1].y\
                   #for index in range(len(y_sort_left_in_min_x_width) - 1))
        #print(f"y_sort_left_in_min_x_width {y_sort_left_in_min_x_width}")

        y_sort_right_in_min_x_width = [point for point in y_sort_right if point.x <= x_sort_left[-1].x + min_dist]
        #assert all(y_sort_right_in_min_x_width[index].y <= y_sort_right_in_min_x_width[index + 1].y\
                   #for index in range(len(y_sort_right_in_min_x_width) - 1))
        #print(f"y_sort_right_in_min_x_width {y_sort_right_in_min_x_width}")

        y_sort_merged_in_min_x_width = merge_lists(y_sort_left_in_min_x_width, y_sort_right_in_min_x_width)
        #print(f"y_sort_merged_in_min_x_width {y_sort_merged_in_min_x_width}")

        for index, point in enumerate(y_sort_merged_in_min_x_width):
            #print(f"index {index} point {point}")
            index_limit = index + 8
            while index + 1 < len(y_sort_merged_in_min_x_width) and \
                index + 1 < index_limit:
                #y_sort_merged_in_min_x_width[index + 1].y <= point.y + min_dist:

                min_dist = min(min_dist, distance_squared(point, y_sort_merged_in_min_x_width[index + 1]))
                #print(f"min_dist {min_dist}")
                index += 1

        return min_dist
    """
    duplicate_check = {}

    for point in points:
        if point.x not in duplicate_check:
            duplicate_check[point.x] = [point.y]
        else:
            duplicate_check[point.x].append(point.y)

    for x_value, y_list in duplicate_check.items():
        y_set = set()
        for y_value in y_list:
            if y not in y_set:
                y_set.add(y_value)
            else:
                return 0 #duplicate point found
    #print(sorted(points, key=lambda point: point.x))
    #return min_dist_recurs(sorted(points, key=lambda point: point.x))
    """

    x_sort = sorted(points, key=lambda point: point.x)
    y_sort = sorted(points, key=lambda point: point.y)
    return sqrt(min_dist_recurs(x_sort, y_sort))
    # return min_dist_recurs(points, x_sort, y_sort)


if __name__ == '__main__':
    """
    print("Hey")
    for n in [2, 5, 10, 20, 100, 1000]:

        for max_value in [5, 6, 1000]:
        #for max_value in [1, 2, 3, 1000]:
            points = []
            for _ in range(n):
                x = randint(-max_value, max_value)
                y = randint(-max_value, max_value)
                points.append(Point(x, y))
            print(f"minimum_distance_squared_naive(points) {minimum_distance_squared_naive(points)}")
            print(f"minimum_distance_squared(points) {minimum_distance_squared(points)}")
    
    points = [Point(0, 0), Point(5, 6), Point(3, 4), Point(7, 2)]
    print(f"minimum_distance_squared_naive(points) {minimum_distance_squared_naive(points)}")
    print(f"minimum_distance_squared(points) {minimum_distance_squared(points)}")

    """ 
    input_n = int(input())
    input_points = []
    for _ in range(input_n):
        x, y = map(int, input().split())
        input_point = Point(x, y)
        input_points.append(input_point)

    print("{0:.9f}".format(minimum_distance_squared(input_points)))
    
    
    """
    #print("{0:.9f}".format(sqrt(minimum_distance_squared_naive(input_points))))
    for n in [10 ** 5]:
        for max_value in [1, 2, 3, 1000]:
            points = []
            for _ in range(n):
                x = randint(-2 * max_value, -max_value)
                y = randint(max_value, 2 * max_value)
                points.append(Point(x, y))
            pointA = Point(0, 0)
            pointB = Point(1e-04, -1e-04)
            points.append(pointA)
            points.append(pointB)

            smallPoints = [pointA, pointB]
            print(minimum_distance_squared(points))
            print(minimum_distance_squared_naive(smallPoints))
    """
    #for n in [2, 5, 10, 100]:
