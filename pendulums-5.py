#Visual animation that draws a set of oscillating pendulums

from tkinter import *
import random
import math

def init(data):
    data.radius = 6
    data.margin = data.height/2
    data.centerX = data.width/2
    data.centerY = data.margin
    data.fill = ["#87ceeb", "#ffd700", "#3cb371", "#ffd700", "#ffa500", "#ff1493"] 
    data.pendulums1 = []
    data.pendulums2 = []
    data.time = 0
    data.counter1 = 0
    data.counter2 = 0
    data.length = 100
    data.color = "orange"
    
def getCircle(radius, x, y, data):
    x0 = x - radius
    y0 = y + radius
    x1 = x + radius
    y1 = y - radius
    return (x0, y0, x1, y1)
    
def makePendulums1(data):
    theta = -(math.pi/3)
    length = data.length
    omega = 0
    posX = data.width/2 + length*math.sin(theta)
    posY = data.margin + length*math.cos(theta)
    omega = 0
    data.pendulums1.append([ posX, posY, length, omega, theta ])
    data.length += 8
    data.counter1 += 1
    
def movePendulum1(data):
    for i in range(len(data.pendulums1)):
        dt = 0.1
        
        posX = data.pendulums1[i][0]
        posY = data.pendulums1[i][1]
        length = data.pendulums1[i][2]
        omega = data.pendulums1[i][3]
        theta = (data.pendulums1[i][4])
        
        #Calculations
        alpha = -9.8*math.sin(theta)/length
        domega = alpha*dt
        omega = omega + domega
        dtheta = omega*dt
        theta = theta + dtheta
        
        posX = data.width/2 + length*math.sin(theta)
        posY = data.margin + length*math.cos(theta)
        
        #Update all the values in data.pendulum
        data.pendulums1[i][0] = posX
        data.pendulums1[i][1] = posY
        data.pendulums1[i][3] = omega
        data.pendulums1[i][4] = theta
        
        
def drawPendulum1(canvas,data):
    if data.time % 100 == 0:
        n = random.randint(0, len(data.fill)-1)
        data.color = data.fill[n]
    for i in range(len(data.pendulums1)):
        posX = data.pendulums1[i][0]
        posY = data.pendulums1[i][1]
        (x0,y0,x1,y1) = getCircle(data.radius, posX, posY, data)
        canvas.create_oval(x0,y0,x1,y1, fill = data.color)

def drawLines1(canvas,data):
    for i in range(len(data.pendulums1)):
        posX = data.pendulums1[i][0]
        posY = data.pendulums1[i][1]
        (x0,y0,x1,y1) = getCircle(data.radius, posX, posY, data)
        canvas.create_line(data.centerX, data.centerY, posX, posY, fill = "gray25", width = 0)
    
    
def mousePressed(event, data):
    pass

def keyPressed(event, canvas, data):
    pass
        
def timerFired(data):
    data.time += data.timerDelay
    if data.counter1 < 20: makePendulums1(data)
    movePendulum1(data)
        
def redrawAll(canvas, data):
    drawLines1(canvas,data)
    drawPendulum1(canvas, data)

####################################
# Run function - don't change
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,fill='black', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, canvas, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 50 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height, scrollregion=(0, 0, 620,820))
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(600,600)


