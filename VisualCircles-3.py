#Visual animation that draws a central circle that radiates smaller circles in
#all directions of various colors

from tkinter import *
import random
import math


####################################
# customize these functions
####################################

def init(data):
    data.counter = 0  # number of circles 
    data.centerFill = "teal" #For central circle
    data.centerRadius = 60
    data.fill = ["#87ceeb", "#ffd700", "#3cb371", "#ffd700", "#ffa500", "#ff1493"]  #for all other circles
    data.radii = [10,14,16]  #possible values for radius of target
    data.radius = 10
    data.gap = 10
    data.centerX = data.width/2 + data.gap
    data.centerY = data.height/2 + data.gap
    data.angle = 0
    data.ListOfCircles = [] #tuple with a list of all targets available at any given time
    data.time = 0 #millseconds
    data.circleDelay = 250 #A new circle is generated every 50 milliseconds
    data.GameOver = False
    data.gameMode = "s" # s for start, p for play, o for game over

def drawCenterCircle(canvas, data):
    n = len(data.fill)
    data.centerRadius = random.randint(50,60)
    #if data.centerRadius == 40: data.centerRadius=48
    #elif data.centerRadius > 40: data.centerRadius = 40
    (x0, y0, x1, y1) = getCircle(data.centerRadius, data.width/2, data.height/2, data)
    randomIndex = random.randint(0,n-1)
    fill = data.fill[randomIndex]
    #fill = "#ffd700"
    canvas.create_oval(x0,y0,x1,y1, fill = fill, width = 0)
    for j in range (1,10):
        i = 1.618*j
        (a0, b0, a1, b1) = getCircle(i*data.centerRadius, data.width/2, data.height/2, data)
        canvas.create_oval(a0, b0, a1, b1, width = 1, outline = "#d3d3d3", dash=(6,5,2,4))
    
def getCircle(radius, x, y, data):
    x0 = x - radius
    y0 = y + radius
    x1 = x + radius
    y1 = y - radius
    return (x0, y0, x1, y1)

def makeCircle(data):
    n = random.randint(1,3)
    delay = n*data.circleDelay
    if data.time % delay == 0:
        for angle in range(0,360, 45):
            #angle = 22.5*i
            temp = data.ListOfCircles
            theta = math.pi*(angle/180)
            m = random.randint(1,len(data.radii)-1)
            radius = data.radii[m]
            #radius = data.radius
            centerX = data.width/2 + (data.gap + data.centerRadius)*math.cos(theta)
            centerY = data.height/2 + (data.gap + data.centerRadius)*math.sin(theta)
            temp.append([centerX, centerY, radius, theta])
            data.ListOfCircles = temp
            #print (data.ListOfCircles)

def moveCircles(data):
    for i in range(len(data.ListOfCircles)):
        theta = data.ListOfCircles[i][3]
        radius = data.ListOfCircles[i][2]
        dx = math.cos(theta)*radius*1.1
        dy = math.sin(theta)*radius*1.1
        data.ListOfCircles[i][0] += dx
        data.ListOfCircles[i][1] += dy
        data.ListOfCircles[i][2] -= 0.025*radius
        #data.ListOfCircles[i][3] = theta

def drawCircle(canvas, data):
    for i in range(len(data.ListOfCircles)):
        radius = data.ListOfCircles[i][2]
        centerX = data.ListOfCircles[i][0]
        centerY = data.ListOfCircles[i][1]
        n = random.randint(0,len(data.fill)-1)
        fill = data.fill[n]
        (x0, y0, x1, y1) = getCircle(radius, centerX, centerY, data)
        canvas.create_oval(x0,y0,x1,y1, fill = fill, width = 0)
    
def mousePressed(event, data):
    pass

def keyPressed(event, canvas, data):
    #if event.keysym == "Left": makeCircle(data)
    pass
        
def timerFired(data):
    data.time += data.timerDelay
    makeCircle(data)
    moveCircles(data)
    #print (data.time)
        
def redrawAll(canvas, data):
    drawCircle(canvas, data)
    drawCenterCircle(canvas, data)

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,fill='white', width=0)
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

run(800, 600)


