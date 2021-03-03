import numpy as np
import math


def get_input():

    print('Program to transform frame A to frame B, then input position of a point in a frame and output position of the same point in another frame')
    print('\nFollowing transformations can be performed:')
    print('1. Enter rotation about x-axis')
    print('2. Enter rotation about y-axis')
    print('3. Enter rotation about z-axis')
    print('4. enter translation about x-axis')
    print('5. enter translation about y-axis')
    print('6. enter translation about z-axis')

    r_x = math.pi/180*int(input('\nangle to rotate x-axis: '))
    r_y =  math.pi/180*int(input('angle to rotate y-axis: '))
    r_z =  math.pi/180*int(input('angle to rotate z-axis: '))

    t_x = int(input('translation x-axis: '))
    t_y = int(input('translation y-axis: '))
    t_z = int(input('translation z-axis: '))

    frame_known = "" ;
    while frame_known != 'a' and frame_known != 'b':
        frame_known = input('Point is known in frame? (A/B): ').lower()
        if frame_known != 'a' and frame_known != 'b':
            print('Enter either A or B')

    init_coord = np.array(list(
        map(int, input('\nEnter the coordianate of the point of the frame: ').split())))

    return init_coord, transf_matrix(r_x, r_y, r_z, t_x, t_y, t_z, frame_known)


def transf_matrix(rotation_x, rotation_y, rotation_z, translation_x, translation_y, translation_z, frame_known):

    Rx = np.array([
            [1, 0, 0],
            [0, math.cos(rotation_x), -math.sin(rotation_x)],
            [0, math.sin(rotation_x), math.cos(rotation_x)]]
        )

    Ry = np.array([
            [math.cos(rotation_y), 0, math.sin(rotation_y)],
            [0, 1, 0],
            [-math.sin(rotation_y), 0, math.cos(rotation_y)]
        ]
        )

    Rz = np.array([
            [math.cos(rotation_z), -math.sin(rotation_z), 0],
            [math.sin(rotation_z), math.cos(rotation_z), 0],
            [0, 0, 1]
        ])

    R_multiplication = Rz @ Ry @ Rx

    if frame_known == 'a':
        temp = np.vstack((-R_multiplication.T@np.array([[translation_x], [translation_y], [translation_z]]), [1]))
        return np.hstack((np.vstack((R_multiplication.T, np.array([0, 0, 0]))), temp))

    elif frame_known == 'b':
        d = np.array([[translation_x], [translation_y], [translation_z], [1]])

        transformation_matrix = np.hstack(
            (np.vstack((R_multiplication, np.array([0, 0, 0]))), d))

        return transformation_matrix


def transform(initial_coordinates, transformation_matrix):
    initial_coordinates = np.hstack((initial_coordinates, 1))
    final_coordinates = transformation_matrix@initial_coordinates

    return final_coordinates[:3]


def print_final_answer(final_coordinates):
    print('\nPosition of the point in other frame is: ({}, {}, {})'.format(
          final_coordinates[0], final_coordinates[1], final_coordinates[2]))


if _name_ == '_main_':
    initial_coordinates, transformation_matrix = get_input()
    final_coordinates = transform(initial_coordinates, transformation_matrix)
    print_final_answer(final_coordinates)