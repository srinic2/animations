#Visual animation that draws a set of projectiles

from tkinter import *
import random
import math

def init(data):
    data.time = 0
    data.projectiles = []
    data.radius = 4
    data.counter = 0
    data.color = "orange"
    data.fill = ["#87ceeb", "#ffd700", "#3cb371", "#ffd700", "#ffa500", "#ff1493"]
    data.t = 0

#returns bounds given radius and center (x,y) of a circle
def getCircle(radius, x, y, data):
    x0 = x - radius
    y0 = y + radius
    x1 = x + radius
    y1 = y - radius
    return (x0, y0, x1, y1)

#makes projectiles defined by initial position (x,y) and initial angle 
def makeProjectiles(data):
    if data.time % 500 == 0: 
        #n = random.uniform(0.15, 0.3 )
        n = 1/3
        theta = -n*math.pi
        xinit = data.width*0.25
        yinit = data.height/2
        #vinit = random.uniform(6,7) #meters per second
        vinit = 6
        tt = 0
        data.projectiles.append([xinit, yinit, theta, vinit, tt])
        data.counter += 1

#moves pendulums as defined by kinematic equations of motion
def moveProjectiles(data):
    for i in range(len(data.projectiles)):
        dt = 0.01 #choose small interval for calculation purposes
        gg = 9.8 #acceleration due to gravity in m/s^2
        
        #retrieve current set of variables for calculations
        tt = data.projectiles[i][4]
        xinit = data.projectiles[i][0]
        yinit = data.projectiles[i][1]
        theta = data.projectiles[i][2]
        vinit = data.projectiles[i][3]

        #calculations based on kinematic equations of motion
        dy = vinit*math.sin(theta)*(tt) + (0.5*gg*(tt**2))
        dx = vinit*math.cos(theta)*(tt)
        
        xinit = xinit + dx
        yinit = yinit + dy
        tt = tt + dt
        
        #Update all values in the list
        data.projectiles[i][0] = xinit
        data.projectiles[i][1] = yinit
        data.projectiles[i][4] = tt

#draws all projectiles using latest calculated positions        
def drawProjectiles(canvas,data):
    for i in range(len(data.projectiles)):
        #n = random.randint(0, len(data.fill)-1)
        data.color = "yellow"
        posX = data.projectiles[i][0]
        posY = data.projectiles[i][1]
        
        #projectiles "disappear" (become color of background) once they strike the "ground"
        if data.projectiles[i][1] >= data.height/2: fill = "black" 
        else: fill = data.color
        
        (x0,y0,x1,y1) = getCircle(data.radius, posX, posY, data)
        canvas.create_oval(x0,y0,x1,y1, fill = fill)

#draws a line at "ground level"
def drawLines(canvas,data):
    canvas.create_line(0.1*data.width, data.height/2, 0.9*data.width, data.height/2, fill = "white", width = 2)
    
def mousePressed(event, data):
    pass

def keyPressed(event, canvas, data):
    pass
        
def timerFired(data):
    data.time += data.timerDelay
    makeProjectiles(data)
    moveProjectiles(data)
        
def redrawAll(canvas, data):
    drawProjectiles(canvas, data)
    drawLines(canvas, data)

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
    data.timerDelay = 100 # milliseconds
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


