import pygame
import random
import math
import time

pygame.init()

clock = pygame.time.Clock()
window = pygame.display.set_mode([1920,1080])
running = True

#I should change things such that running into a wall while turnning will stop the rotation untill the key is released and pressed again. 
#change a boolien on bounce if the key is down
#change the boolean back when the key is depressed. 

#Colors!
#not sure how much I've actually used them, but they're here
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)

moveSpeed = pygame.Vector2(0,1)
rotateSpeed = 1.5
airResitance = .98
bounceEfficiency = .9
offset = .01 # I don't think this should acually be needed, but It's here
frameCount = 0
lastCollsion = (0,0)

walls = []

#Color, point 1, point 2, Width
wallData = [
[(255,0,0), (700,0), (0,700), 5],
[(255,0,0), (1220,0), (1920,700), 5],
[(255,0,0), (0,700), (700,1080), 5]]

class playerObject:
    angle = 0.0
    size = 30
    color = (23,147,209)
    position = pygame.Vector2(window.get_width() / 2, window.get_height() / 2)
    points = [pygame.Vector2(0,0),pygame.Vector2(0,0),pygame.Vector2(0,0),pygame.Vector2(0,0)]
    speed = pygame.Vector2(0,0)

class wallsClass:
    pointOne = pygame.Vector2(0,0)
    pointTwo = pygame.Vector2(0,0)
    width = 5
    slope = 0
    color = (255,0,0)
    b = 0

def drawPlayer():

    player.points[0] = pygame.Vector2(player.position + pygame.Vector2(0,-50).rotate(player.angle))
    player.points[1] = pygame.Vector2(player.position + pygame.Vector2(30,20).rotate(player.angle))
    player.points[2] = pygame.Vector2(player.position + pygame.Vector2(0,10).rotate(player.angle))
    player.points[3] = pygame.Vector2(player.position + pygame.Vector2(-30,20).rotate(player.angle))
    
    playerSurface = pygame.Surface((60,90), pygame.SRCALPHA)
    playerSurface.fill((0,0,0,0))
    pygame.draw.polygon(playerSurface, player.color, [(30,0), (60,70), (30,50), (0,70)])
    
    playerSurface = pygame.transform.rotate(playerSurface, -player.angle)
    
    window.blit(playerSurface, (player.position.x - (playerSurface.get_width() / 2), player.position.y - (playerSurface.get_height() / 2)))
    
    pygame.draw.circle(window, black, player.points[0], 2)
    pygame.draw.circle(window, black, player.points[1], 2)
    pygame.draw.circle(window, black, player.points[3], 2)
    
def screenEdgeCollision (collisionObject):
    global lastCollsion
    collisionTotal = 0
    for i in range(len(collisionObject.points)):
        if collisionObject.points[i].y < 0:
            #top edge
            collisionTotal += 1
        if collisionObject.points[i].x > window.get_width():
            #right side
            collisionTotal += 10
        if collisionObject.points[i].y > window.get_height():
            #bottom edge
            collisionTotal += 100
        if collisionObject.points[i].x < 0:
            #left side
            collisionTotal += 1000
    if collisionTotal % 10 >= 1:
        #top edge
        if lastCollsion[0] == 1 and frameCount - lastCollsion[1] <= 5:
            return
        if not collisionObject.speed.x == 0:
            angle = math.degrees(math.atan((collisionObject.speed.y / collisionObject.speed.x)))
        else:
            angle = 90
        collisionObject.speed.y = collisionObject.speed.y * -bounceEfficiency
        collisionObject.angle -= 2 * angle
        print(1, collisionObject.angle)
        lastCollsion = (1, frameCount)
        
    if collisionTotal % 100 >= 10:
        #right Side
        if lastCollsion[0] == 2 and frameCount - lastCollsion[1] <= 5:
            return
        if not collisionObject.speed.x == 0:
            angle = math.degrees(math.atan((collisionObject.speed.y / collisionObject.speed.x)))
        else:
            angle = 0
        collisionObject.speed.x = collisionObject.speed.x * -bounceEfficiency
        collisionObject.angle -= (2 * angle) + 180
        print(2, collisionObject.angle)
        lastCollsion = (2, frameCount)
        
    if collisionTotal % 1000 >= 100:
        #bottom Edge
        if lastCollsion[0] == 3 and frameCount - lastCollsion[1] <= 5:
            return
        if not collisionObject.speed.x == 0:
            angle = math.degrees(math.atan((collisionObject.speed.y / collisionObject.speed.x)))
        else:
            angle = 90
        collisionObject.speed.y = collisionObject.speed.y * -bounceEfficiency
        collisionObject.angle -= 2 * angle
        print(3, collisionObject.angle)
        lastCollsion = (3, frameCount)
        
    if collisionTotal >= 1000:
        #left side
        if lastCollsion[0] == 4 and frameCount - lastCollsion[1] <= 5:
            return
        if not collisionObject.speed.x == 0:
            angle = math.degrees(math.atan((collisionObject.speed.y / collisionObject.speed.x)))
        else:
            angle = 0
        collisionObject.speed.x = collisionObject.speed.x * -bounceEfficiency
        collisionObject.angle -= (2 * angle) + 180
        print(4, collisionObject.angle)
        lastCollsion = (4, frameCount)

def wallCollision (collisionObject):
    global lastCollsion
    for i in range(len(walls)):
        sideOfLine = []
        crossed = False
        for j in range(len(collisionObject.points)):
            #y - mx + b  -- find out which side of the line this point is on. 
            sideOfLine.append(collisionObject.points[j].y - ((walls[i].slope * collisionObject.points[j].x) + (walls[i].b)))
        if sideOfLine[0] > 0:
            for k in range(len(sideOfLine) - 1):
                if sideOfLine[k + 1] < 0:
                    crossed = True
                    lastCollsion = (5 + i, frameCount, lastCollsion[0])
                    break
        else:
            for k in range(len(sideOfLine) -1):
                if sideOfLine[k + 1] > 0:
                    crossed = True
                    lastCollsion = (5 + i, frameCount, lastCollsion[0])
                    break
        if crossed == True and not (lastCollsion[2] == lastCollsion[0] and frameCount - lastCollsion[1] <= 5):
            collisionObject.angle += 2 * (collisionObject.speed.angle_to(pygame.Vector2(1,walls[i].slope)))
            collisionObject.speed = collisionObject.speed.rotate((2 * collisionObject.speed.angle_to(pygame.Vector2(1,walls[i].slope))))
            collisionObject.speed.x = collisionObject.speed.x * bounceEfficiency
            collisionObject.speed.y = collisionObject.speed.y * bounceEfficiency
            print(lastCollsion[0], collisionObject.angle)
            

def getInput ():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player.speed -= moveSpeed.rotate(player.angle)
    if keys[pygame.K_s]:
        player.speed -= moveSpeed.rotate(player.angle + 180)
    if keys[pygame.K_d]:
        player.angle += rotateSpeed
    if keys[pygame.K_a]:
        player.angle -= rotateSpeed
    
    if keys[pygame.K_UP]:
        player.position.y -= moveSpeed.y
    if keys[pygame.K_DOWN]:
        player.position.y += moveSpeed.y
    if keys[pygame.K_LEFT]:
        player.position.x -= moveSpeed.y
    if keys[pygame.K_RIGHT]:
        player.position.x += moveSpeed.y

def drawWalls ():
    for wall in walls:
        pygame.draw.line(window, wall.color, wall.pointOne, wall.pointTwo, 5)

#game setup
player = playerObject()
for i in range(len(wallData)):
    walls.append(wallsClass())
    walls[i].color = pygame.Color(wallData[i][0][0], wallData[i][0][1], wallData[i][0][2])
    walls[i].pointOne = pygame.Vector2(wallData[i][1])
    walls[i].pointTwo = pygame.Vector2(wallData[i][2])
    walls[i].width = wallData[i][3]
    walls[i].slope = (walls[i].pointOne.y - walls[i].pointTwo.y) / (walls[i].pointOne.x - walls[i].pointTwo.x)
    walls[i].b = walls[i].pointOne.y - (walls[i].slope * walls[i].pointOne.x)


#main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False 
    
    #background
    window.fill(white)
    
    #manage input
    getInput()
    
    #air resistance on the player
    player.speed.y = player.speed.y * airResitance
    player.speed.x = player.speed.x * airResitance

    #bouncie arround the edges
    screenEdgeCollision(player)
    wallCollision(player)

    #Normalize the player's rotation
    player.angle = player.angle % 360

    #update player position
    player.position += player.speed
    
    #gamedraw
    drawPlayer()
    drawWalls()
    
    #flip to display
    pygame.display.flip()

    #frame rate limiter
    frameCount += 1
    clock.tick(60)
pygame.quit()