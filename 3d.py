import pygame
import numpy as np
from math import *
import sys

size = (width, height) = 800, 600
pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption("A 3D cube in python.")

scale = 100 # the size of the 2D printed cube
theme = "dark"
circles_positions = [screen.get_width()/2, screen.get_height()/2] #x, y

# making the 3D cube:
points = []
points.append(np.matrix([-1, -1, 1]))
points.append(np.matrix([1, -1, 1]))
points.append(np.matrix([1, 1, 1]))
points.append(np.matrix([-1, 1, 1]))
points.append(np.matrix([-1, -1, -1]))
points.append(np.matrix([1, -1, -1]))
points.append(np.matrix([1, 1, -1]))
points.append(np.matrix([-1, 1, -1]))

# how will project?
projection_matrix = np.matrix([
    [1, 0, 0],
    [0, 1, 0],
])
projected_points = [
    [n,n] for n in range(len(points))
]

def connect_points(i, j, points):
    color = "white"
    if theme == "white": color = "black"
    pygame.draw.line(screen, color, (points[i][0], points[i][1]), (points[j][0], points[j][1]))

angle = 0
while True:
    pygame.time.Clock().tick(120)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
            if theme == "white":
                theme = "dark"
            else:
                theme = "white"

    # update stuff
    

    rotation_z = np.matrix([
        [cos(angle), -sin(angle), 0],
        [sin(angle), cos(angle), 0],
        [0, 0, 1],
    ])
    rotation_x = np.matrix([
        [1, 0, 0],
        [0, cos(angle), -sin(angle)],
        [0, sin(angle), cos(angle)],
    ])
    rotation_y = np.matrix([
        [cos(angle), 0, sin(angle)],
        [0, 1, 0],
        [-sin(angle), 0, cos(angle)],
    ])

    angle += .01


    # draw stuff
    if theme == "white":
        screen.fill("white")
    else:
        screen.fill("black")

    toRenderPoints = []
    render_line_index = 0
    for point in points:
        rotated2D_x = np.dot(rotation_x, point.reshape((3, 1)))
        rotated2D_y = np.dot(rotation_y, rotated2D_x)
        rotated2D_z = np.dot(rotation_z, rotated2D_y)

        projected2D = np.dot(projection_matrix, rotated2D_z)

        x = int(projected2D[0][0] * scale) + circles_positions[0]
        y = int(projected2D[1][0] * scale)+ circles_positions[1]

        projected_points[render_line_index] = [x,y]
        toRenderPoints.append((x,y))
        #pygame.draw.circle(screen, "black", (x,y), 5)
        render_line_index += 1

    for liga in range(4):
        connect_points(liga, (liga+1)%4, projected_points)
        connect_points(liga+4, ((liga+1)%4)+4, projected_points)
        connect_points(liga, (liga+4), projected_points)

    for axys in toRenderPoints:
        pygame.draw.circle(screen, "red", axys, 5)


    print(projected_points)

    # render stuff
    pygame.display.update()