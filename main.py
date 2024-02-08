#!/bin/python3
import pygame
import time
import copy
import random
from math import sqrt

WIDTH = 1000
HIGHT = 1000
FPS = 30

pygame.init()
surface = pygame.display.set_mode((WIDTH, HIGHT), pygame.RESIZABLE)
clock = pygame.time.Clock()

PI = 3.1415926
G = 6.67385#e-11
focus = 0
show_vectors = 0
show_orbits = 0
SCALE = 4
MOVEX = WIDTH / 2
MOVEY = HIGHT / 2
SPEED = 10
MIN_SPEED = 0
MAX_SPEED = 100
VECTOR_SIZE = 100






objects = [
#{'mass': 0, 'r': 0, 'color': 0, 'x': 0, 'y': 0, 'vx': 0, 'vy': 0, 'del': 0}
{'mass': 1000, 'r': 100, 'color': [255, 200, 200], 'x': 0, 'y': 0, 'vx': 0, 'vy': 0, 'del': 0},
{'mass': 10, 'r': 10, 'color': [200, 200, 200], 'x': 700, 'y': 0, 'vx': 0, 'vy': -3, 'del': 0}
]

for i in range(50):
    objects.append(copy.deepcopy(objects[i]))


def radius(radius_mass):
    return int(sqrt(radius_mass/PI))


def fill_random():
    for object in objects:
        rndcolor = [0, 200, 200]
        rndcolor[0] = random.randint(200, 255)
        object['color'] = rndcolor
        object['mass'] = random.randint(100, 500)
        object['r'] = radius(object['mass'])
        object['x'] = random.randint(-1000, 1000)
        object['y'] = random.randint(-1000, 1000)
        object['vx'] = (random.random() - random.randint(0, 1))#*10 #objects[i]['y'] / 100 * -1#
        object['vy'] = (random.random() - random.randint(0, 1))#*10 #objects[i]['x'] / 100 * -1#


    #objects[0]['mass'] = 7.36e22
    #objects[0]['r'] = 1737100
    #objects[0]['color'] = (255, 255, 255)
    #objects[0]['x'] = 0
    #objects[0]['y'] = 0
    #objects[0]['vx'] = 0
    #objects[0]['vy'] = 0

    #objects[1]['mass'] = 65
    #objects[1]['r'] = 2
    #objects[1]['color'] = (255, 200, 200)
    #objects[1]['x'] = 0
    #objects[1]['y'] = -1737200
    #objects[1]['vx'] = 0
    #objects[1]['vy'] = 0

    #objects[1]['mass'] = 65
    #objects[1]['r'] = 2
    #objects[1]['color'] = (255, 200, 200)
    #objects[1]['x'] = 0
    #objects[1]['y'] = -9737100
    #objects[1]['vx'] = 1250/2
    #objects[1]['vy'] = 0

    #objects[2]['mass'] = 100
    #objects[2]['r'] = 4
    #objects[2]['color'] = (255, 200, 200)
    #objects[2]['x'] = 0
    #objects[2]['y'] = 1737100 + 2422000
    #objects[2]['vx'] = -138 * 7
    #objects[2]['vy'] = 0


fill_random()




tmpobjects = copy.deepcopy(objects)

def disp():
    if not show_orbits:
        surface.fill((0, 0, 0))
    for object in objects:
        if focus:
            pygame.draw.circle(surface, (object['color']), (int((object['x']-objects[focus-1]['x'])/SCALE+WIDTH/2), int((object['y']-objects[focus-1]['y'])/SCALE+HIGHT/2)), int(object['r']/SCALE))
            if show_vectors:
                pygame.draw.line(surface, (255, 0, 0), (int((object['x']-objects[focus-1]['x'])/SCALE+WIDTH/2), int((object['y']-objects[focus-1]['y'])/SCALE+HIGHT/2)), (int(((object['vx']*VECTOR_SIZE + object['x'])-objects[focus-1]['x'])/SCALE+WIDTH/2), int(((object['vy']*VECTOR_SIZE + object['y'])-objects[focus-1]['y'])/SCALE+HIGHT/2)))
        else:
            pygame.draw.circle(surface, (object['color']), (int(object['x']/SCALE+MOVEX), int(object['y']/SCALE+MOVEY)), int(object['r']/SCALE))
            if show_vectors:
                pygame.draw.line(surface, (255, 0, 0), (int(object['x']/SCALE+MOVEX), int(object['y']/SCALE+MOVEY)), (int((object['vx']*VECTOR_SIZE/SCALE + object['x'])/SCALE+MOVEX), int((object['vy']*VECTOR_SIZE/SCALE + object['y'])/SCALE+MOVEY)))
    pygame.display.update()



def velocity(I, E, T):
    TMPI = copy.deepcopy(I)
    TMPI['vx'] = T['vx']
    TMPI['vy'] = T['vy']

    distx = E['x']-I['x']
    disty = E['y']-I['y']
    squarex = distx ** 2
    squarey = disty ** 2
    squaredist = squarex + squarey
    if squaredist != 0:
        gamma = ((G*I['mass']*E['mass'])/squaredist)/I['mass']
    else:
        gamma = 0
    if squaredist > E['r']**2 + I['r']**2:
        if squarex != 0 and distx != 0:
            TMPI['vx'] += gamma * percent(squaredist, squarex) * (distx / abs(distx))
        if squarey != 0 and disty != 0:
            TMPI['vy'] += gamma * percent(squaredist, squarey) * (disty / abs(disty))
    else:
        #абсолютно неупругий удар
        TMPI['vx'] = (I['mass']*TMPI['vx'] + E['mass']*E['vx'])/(I['mass']+E['mass'])
        TMPI['vy'] = (I['mass']*TMPI['vy'] + E['mass']*E['vy'])/(I['mass']+E['mass'])
        #абсолютно упругий удар
        #TMPI['vx'] = (2 * E['mass'] * E['vx'] + I['vx'] * (I['mass'] - E['mass'])) / (I['mass'] + E['mass'])
        #TMPI['vy'] = (2 * E['mass'] * E['vy'] + I['vy'] * (I['mass'] - E['mass'])) / (I['mass'] + E['mass'])
        #абсолютно упругий удар - 10% энергии
        #TMPI['vx'] = (2 * E['mass'] * E['vx'] + I['vx'] * (I['mass'] - E['mass'])) / (I['mass'] + E['mass']) / 1.1
        #TMPI['vy'] = (2 * E['mass'] * E['vy'] + I['vy'] * (I['mass'] - E['mass'])) / (I['mass'] + E['mass']) / 1.1
    return(TMPI)

def position(I):
    I['x'] += I['vx']
    I['y'] += I['vy']


def percent(percent_full, percent_part):
    return 1 / percent_full * percent_part


#check = [
#{'mass': 7.36e22, 'r': 100, 'color': 0, 'x': 0, 'y': 1, 'vx': 0, 'vy': 0, 'del': 0},
#{'mass': 65, 'r': 10, 'color': 0, 'x': 1737100, 'y': 1, 'vx': 0, 'vy': 0, 'del': 0},
#{'mass': 0, 'r': 0, 'color': 0, 'x': 0, 'y': 1, 'vx': 0, 'vy': 0, 'del': 0}
#]
#print(velocity(check[1], check[0], check[0]))





while(True):
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit()
        if e.type == pygame.VIDEORESIZE:
            WIDTH = e.w
            HIGHT = e.h
            MOVEX = WIDTH / 2
            MOVEY = HIGHT / 2
            surface = pygame.display.set_mode((WIDTH, HIGHT), pygame.RESIZABLE)
        if e.type == pygame.KEYDOWN:
            if (e.key == pygame.K_EQUALS) and SCALE >= 2:
                SCALE = SCALE / 2
                MOVEX = WIDTH / 2
                MOVEY = HIGHT / 2
            if (e.key == pygame.K_MINUS):
                SCALE = SCALE * 2
                MOVEX = WIDTH / 2
                MOVEY = HIGHT / 2
            if (e.key == pygame.K_KP_PLUS) and SPEED > MIN_SPEED:
                if SPEED >= 20:
                    SPEED -= 10
                else:
                    SPEED -= 1
                print(SPEED)
            if (e.key == pygame.K_KP_MINUS) and SPEED < MAX_SPEED:
                if SPEED >= 10:
                    SPEED += 10
                else:
                    SPEED += 1
                print(SPEED)
            if e.key == pygame.K_UP:
                MOVEY += 100
            if e.key == pygame.K_DOWN:
                MOVEY -= 100
            if e.key == pygame.K_LEFT:
                MOVEX += 100
            if e.key == pygame.K_RIGHT:
                MOVEX -= 100
            if e.key == pygame.K_0:
                focus = 0
            if e.key == pygame.K_1:
                focus = 1
            if e.key == pygame.K_2:
                focus = 2
            if e.key == pygame.K_3:
                focus = 3
            if e.key == pygame.K_4:
                focus = 4
            if e.key == pygame.K_5:
                focus = 5
            if e.key == pygame.K_6:
                focus = 6
            if e.key == pygame.K_9:
                focus = -1
            if e.key == pygame.K_s:
                print(objects[focus-1])
            if e.key == pygame.K_r:
                fill_random()
            if e.key == pygame.K_v:
                show_vectors = not show_vectors
            if e.key == pygame.K_o:
                show_orbits = not show_orbits




    for object in objects:
        if object['del'] == 1:
            objects.remove(object)

    tmpobjects = copy.deepcopy(objects)

    tmp = 0
    for object in objects:
        for another in objects:
            if object != another:
                tmpobjects[tmp] = velocity(object, another, tmpobjects[tmp])
        tmp += 1

    objects = copy.deepcopy(tmpobjects)

    for object in objects:
        for another in objects:
            if object != another:
                if (object['x'] - another['x'])**2 + (object['y'] - another['y'])**2 <= (object['r'] + another['r'])**2 and object['del'] == 0 and another['del'] == 0:
                    if object['mass'] > another['mass']:
                        object['mass'] += another['mass']
                        object['r'] = radius(object['mass'])
                        object['vx'] = (object['mass']*object['vx'] + another['mass']*another['vx'])/(object['mass']+another['mass'])
                        object['vy'] = (object['mass']*object['vy'] + another['mass']*another['vy'])/(object['mass']+another['mass'])
                        #another['mass'] = 0
                        another['vx'] = 0
                        another['vy'] = 0
                        another['del'] = 1
                    else:
                        another['mass'] += object['mass']
                        another['r'] = radius(another['mass'])
                        another['vx'] = (another['mass']*another['vx'] + object['mass']*object['vx'])/(another['mass']+object['mass'])
                        another['vy'] = (another['mass']*another['vy'] + object['mass']*object['vy'])/(another['mass']+object['mass'])
                        #object['mass'] = 0
                        object['vx'] = 0
                        object['vy'] = 0
                        object['del'] = 1

    for object in objects:
        position(object)




    disp()
    time.sleep(SPEED/100)
