#Visual animation that draws a central circle that radiates smaller circles 
#added code to make some circles move faster than others

from tkinter import *
import random
import math
import wave


####################################
# customize these functions
####################################

def init(data):
    data.centerRadius = random.randint(10,15)
    data.fill = ["#87ceeb", "#ffd700", "#3cb371", "#ffd700", "#ffa500", "#ff1493"]  #for all other circles
    data.radii = [5,7,9]  #possible values for radius of target
    data.gap = 10
    data.centerX = data.width/2 + data.gap
    data.centerY = data.height/2 + data.gap
    data.ListOfCircles = [] #tuple with a list of all circles available at any given time
    data.time = 0 #millseconds
    data.circleDelay = [200, 400, 800, 1600, 3200] #A new circle is generated every n milliseconds
    
def getCircle(radius, x, y, data):
    x0 = x - radius
    y0 = y + radius
    x1 = x + radius
    y1 = y - radius
    return (x0, y0, x1, y1)

#makes circles of random radii at random times
def makeCircle(data):
    n = random.randint(1,3)
    delay = data.circleDelay[n] #randomly chooses time delay between creation of circles
    m = random.randint(1,len(data.radii)-1)
    radius = data.radii[m] #random selection of sizes of circles
    
    if data.time % delay == 0:
        for angle in range(0,360,15):
            temp = data.ListOfCircles
            theta = math.pi*(angle/180)
            centerX = data.width/2 + (data.gap + data.centerRadius)*math.cos(theta)
            centerY = data.height/2 + (data.gap + data.centerRadius)*math.sin(theta)
            temp.append([centerX, centerY, radius, theta])
            data.ListOfCircles = temp

#moves circles along a lineear path outwards from center
def moveCircles(data):
    for i in range(len(data.ListOfCircles)):
        theta = data.ListOfCircles[i][3]
        radius = data.ListOfCircles[i][2]
        dx = math.cos(theta)*(radius)
        dy = math.sin(theta)*(radius)
        data.ListOfCircles[i][0] += dx
        data.ListOfCircles[i][1] += dy
        data.ListOfCircles[i][2] -= 0.02*radius
        
        #code that makes some circles go faster than other
        if (data.ListOfCircles[i][0] >= data.width/3 and data.ListOfCircles[i][1] >= data.height/3) or (data.ListOfCircles[i][0] <= data.width*2/3 and data.ListOfCircles[i][1] <= data.height*2/3) :
            data.ListOfCircles[i][0] += 1.25*dx
            data.ListOfCircles[i][1] += 1.25*dy
            data.ListOfCircles[i][2] -= 0.01*radius

def drawCircle(canvas, data):
    n = random.randint(0,len(data.fill)-1)
    fill = data.fill[n] #choose circle fill colors randomly
    for i in range(len(data.ListOfCircles)):
        radius = data.ListOfCircles[i][2]
        centerX = data.ListOfCircles[i][0]
        centerY = data.ListOfCircles[i][1]
        (x0, y0, x1, y1) = getCircle(radius, centerX, centerY, data)
        canvas.create_oval(x0,y0,x1,y1, fill = fill, width = 0)

def drawCenterCircle(canvas, data):
    n = len(data.fill)
    (x0, y0, x1, y1) = getCircle(data.centerRadius, data.width/2, data.height/2, data)
    randomIndex = random.randint(0,n-1)
    fill = data.fill[randomIndex]
    canvas.create_oval(x0,y0,x1,y1, fill = fill, width = 0)
    #draws circles with increasing radii such radii are in the Golden ratio
    for j in range (1,20):
        i = 1.618*j #golden ratio
        (a0, b0, a1, b1) = getCircle(i*data.centerRadius, data.width/2, data.height/2, data)
        canvas.create_oval(a0, b0, a1, b1, width = 1, outline = "#d3d3d3", dash=(6,5,2,4))
        
def drawLines(canvas, data):
    canvas.create_line(0,0, data.width, data.height, fill = "#d3d3d3", width = 1, dash=(6,5,2,4))
    canvas.create_line(data.width,0, 0, data.height, fill = "#d3d3d3", width = 1, dash=(6,5,2,4))
    canvas.create_line(data.width/2,0, data.width/2, data.height, fill = "#d3d3d3", width = 1, dash=(6,5,2,4))
    canvas.create_line(0,data.height/2, data.width, data.height/2, fill = "#d3d3d3", width = 1, dash=(6,5,2,4))
    
def mousePressed(event, data):
    pass

def keyPressed(event, canvas, data):
    pass
        
def timerFired(data):
    data.time += data.timerDelay
    makeCircle(data)
    moveCircles(data)
        
def redrawAll(canvas, data):
    drawLines(canvas, data)
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
    data.timerDelay = 150 # milliseconds
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

run(600, 600)


