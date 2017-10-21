#Visual animation that draws a set of projectiles

from tkinter import *
import random
import math

def init(data):
    data.time = 0
    data.projectiles = []
    data.radius = 2
    data.counter = 0
    data.color = "orange"
    data.fill = ["#87ceeb", "#ffd700", "#3cb371", "#ffd700", "#ffa500", "#ff1493"]
    data.t = 0

#returns bounds for a circle given radius and center (x,y) of circle
def getCircle(radius, x, y, data):
    x0 = x - radius
    y0 = y + radius
    x1 = x + radius
    y1 = y - radius
    return (x0, y0, x1, y1)

#makes projectiles as defined by position (x,y) and angle of projection
def makeProjectiles(data):
    #picks random angle of projection per defined window
    n = random.uniform(0.47, 0.53) #change to make wider
    theta = -n*math.pi
    xinit = data.width*0.5
    yinit = 2*data.height/3
    vinit = random.uniform(6,7) #meters per second. Picks random value between 6 and 7
    tt = 0
    data.projectiles.append([xinit, yinit, theta, vinit, tt])
    data.counter += 1

#calculates new position of projectile after a small time interval dt
def moveProjectiles(data):
    for i in range(len(data.projectiles)):
        dt = 0.008 #choose a small time interval
        gg = 9.8 #acceleration due to gravity on earth
        dx = 0
        #retrieve values from list for calculations
        tt = data.projectiles[i][4] #time elapsed
        xinit = data.projectiles[i][0]
        yinit = data.projectiles[i][1]
        theta = data.projectiles[i][2]
        vinit = data.projectiles[i][3]
        
        #calculations per kinematics
        dy = vinit*math.sin(theta)*(tt) + (0.5*gg*(tt**2)) # s = ut + 0.5gt^2
        if theta < 0:
            dx = vinit*math.cos(theta)*(tt)
        else: dx = -vinit*math.cos(theta)*(tt)
        #calculate new position of projectile 
        xinit = xinit + dx
        yinit = yinit + dy
        tt = tt + dt
        #Update all values in list
        data.projectiles[i][0] = xinit
        data.projectiles[i][1] = yinit
        data.projectiles[i][4] = tt

#draws projectiles to reflect their updated positions
def drawProjectiles(canvas,data):
    for i in range(len(data.projectiles)):
        n = random.randint(0, len(data.fill)-1)
        data.color = data.fill[n]
        posX = data.projectiles[i][0]
        posY = data.projectiles[i][1]
        if data.projectiles[i][1] >= 2*data.height/3: fill = "black"
        else: fill = data.color
        (x0,y0,x1,y1) = getCircle(data.radius, posX, posY, data)
        canvas.create_oval(x0,y0,x1,y1, fill = fill)

def drawLines(canvas,data):
    canvas.create_line(0.1*data.width, 2*data.height/3, 0.9*data.width, 2*data.height/3, fill = "white", width = 2)
    
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
    data.timerDelay = 10 # milliseconds
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


