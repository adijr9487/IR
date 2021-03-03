import numpy as np
import math


def get_input():

    print('Program to transform frame A to frame B, then input position of a point in a frame and output position of the same point in another frame')
    print('\nFollowing transformations can be performed:')
    print('1. Rotation about x-axis')
    print('2. Rotation about y-axis')
    print('3. Rotation about z-axis')
    print('4. Translation about x-axis')
    print('5. Translation about y-axis')
    print('6. Translation about z-axis')

    # Angle in degree
    rotation_x = int(input('\nEnter angle to rotate x-axis (in degrees): '))
    rotation_x = math.pi/180*rotation_x
    rotation_y = int(input('Enter angle to rotate y-axis (in degrees): '))
    rotation_y = math.pi/180*rotation_y
    rotation_z = int(input('Enter angle to rotate z-axis (in degrees): '))
    rotation_z = math.pi/180*rotation_z

    translation_x = int(input('Enter translation from x-axis: '))
    translation_y = int(input('Enter translation from y-axis: '))
    translation_z = int(input('Enter translation from z-axis: '))

    frame_known = ''
    while frame_known != 'a' and frame_known != 'b':
        frame_known = input('Point is known in frame? (A/B): ').lower()
        if frame_known != 'a' and frame_known != 'b':
            print('Two frames are \'A\' or \'B\'')

    initial_coordinates = np.array(list(
        map(int, input('\nEnter position of the point in the frame: ').split())))

    # returns: coordinates given by user and transformation matrix for given transformations
    return initial_coordinates, calculate_transformation_matrix(rotation_x, rotation_y, rotation_z, translation_x, translation_y, translation_z, frame_known)


def calculate_transformation_matrix(rotation_x, rotation_y, rotation_z, translation_x, translation_y, translation_z, frame_known):

    # rotation matrix for rotation about x-axis
    rx = np.array([[1, 0, 0],
                   [0, math.cos(rotation_x), -math.sin(rotation_x)],
                   [0, math.sin(rotation_x), math.cos(rotation_x)]])

    # rotation matrix for rotation about y-axis
    ry = np.array([[math.cos(rotation_y), 0, math.sin(rotation_y)],
                   [0, 1, 0],
                   [-math.sin(rotation_y), 0, math.cos(rotation_y)]])

    # rotation matrix for rotation about z-axis
    rz = np.array([[math.cos(rotation_z), -math.sin(rotation_z), 0],
                   [math.sin(rotation_z), math.cos(rotation_z), 0],
                   [0, 0, 1]])

    # final rotation matrix is the matrix multiplication of all three rotation matrices
    r = rz @ ry @ rx

    # if point is known is frame 'A' we need inverse transformation matrix
    if frame_known == 'a':
        # displacement matrix representing displacement about 3 axes
        d = np.array([[translation_x], [translation_y], [translation_z]])
        temp = -r.T@d
        temp = np.vstack((temp, [1]))

        transformation_matrix = np.hstack(
            (np.vstack((r.T, np.array([0, 0, 0]))), temp))

        return transformation_matrix

    elif frame_known == 'b':
        # displacement matrix representing displacement about 3 axes
        d = np.array([[translation_x], [translation_y], [translation_z], [1]])

        transformation_matrix = np.hstack(
            (np.vstack((r, np.array([0, 0, 0]))), d))

        return transformation_matrix


def transform(initial_coordinates, transformation_matrix):
    # 1 is appending to the coordinates for matrix multiplication
    initial_coordinates = np.hstack((initial_coordinates, 1))
    final_coordinates = transformation_matrix@initial_coordinates

    # removing '1' in the last dimension
    return final_coordinates[:3]


def print_final_answer(final_coordinates):
    print('\nPosition of the point in other frame is: ({}, {}, {})'.format(
          final_coordinates[0], final_coordinates[1], final_coordinates[2]))


if __name__ == '__main__':
    initial_coordinates, transformation_matrix = get_input()
    final_coordinates = transform(initial_coordinates, transformation_matrix)
    print_final_answer(final_coordinates)
