import helper, math

def run(app,canvas):
    seenPill = set()
    seenGhost = set()
    entityList = {}
    distanceList = []
    ########################################
    #Big Loop
    for i in range(app.fov):
        angle = app.pac.angle + app.fov/2 - i
        x = app.pac.x
        y = app.pac.y
        hitWall = False

        #Extend x,y out in an angle until it hits a wall
        while hitWall == False:
            row,col = helper.getCell(app,x,y)
            entDis = distance(app,x,y,i)

            #Ghost Check
            for ghost in app.ghostList:
                if ((row == ghost.row and col == ghost.col)
                    and (row,col) not in seenGhost
                    and helper.near(app,helper.getCxCy(app,row,col),(x,y))):

                    seenGhost.add((row,col))
                    entityList[entDis] = entityList.get(entDis,[])
                    entityList[entDis] += [(i,ghost.color)]
                    distanceList.append(entDis)

            #Pill Check
            if (col < 28
                and col > -1
                and (app.board[row][col] == app.pillColor 
                or app.board[row][col] == app.superColor)
                and (row,col) not in seenPill 
                and helper.near(app,helper.getCxCy(app,row,col),(x,y))
                and helper.ghostCell(app,row,col) == False):
                if entDis > 0:
                    seenPill.add((row,col))
                    entityList[entDis] = entityList.get(entDis,[])
                    if app.board[row][col] == app.pillColor:
                        entityList[entDis] += [(i,app.pillColor)]
                    elif app.board[row][col] == app.superColor:
                        entityList[entDis] += [(i,app.superColor)]
                    distanceList.append(entDis)

    
            #Wall Check
            if (col > 27 
                or col < 0
                or (app.board[row][col] != app.pillColor
                and app.board[row][col] != app.emptyColor
                and app.board[row][col] != app.superColor)):
                hitWall = True

            x += math.cos(math.radians(angle))
            y -= math.sin(math.radians(angle))

        #Find the projection distance of that
        wallDis = distance(app,x,y,i)

        #Draw a line/rectangle with correct height
        width = app.width/(app.fov)
        cx = width * i
        drawWall(app,canvas,cx,wallDis)

        #Repeat for all angles in FOV
        #######################################
    #Drawing all the pills
    entity(app,canvas,entityList,distanceList)

def entity(app,canvas,entityList,distanceList):
    width = app.width/(app.fov)

    distanceList = sorted(distanceList)  
    distanceList = distanceList[::-1]
    #Drawing from the fartherst in so the farther ones are covererd if they 
    #should be

    for dis in distanceList:
        for item in entityList[dis]:
            i,color = item
            cx = width*i

            if color == app.pillColor:
                drawPill(app,canvas,cx,dis,app.pillColor)
            elif color == app.superColor:
                drawPill(app,canvas,cx,dis,app.superColor)
            else:
                drawGhost(app,canvas,cx,dis,color)
                

def distance(app,x,y,i):
    result = helper.length(app.pac.x,app.pac.y,x,y)
    #Citation: https://lodev.org/cgtutor/raycasting.html 
    result *= math.cos(math.radians(abs(i - app.fov/2)))
    #For the idea to use perpendicular distance above ^^^^
    return result

def drawWall(app,canvas,cx,distance):
    width = app.width/(app.fov)
    color = app.wallColor
    #Citation: https://lodev.org/cgtutor/raycasting.html
    height = 10*app.height*(1/distance)
    #For pixel height calculation above ^^^
    cy = app.height/2
    if height > 0 :
        canvas.create_rectangle(cx-width/2,cy-height/2,cx+width/2,cy+height/2,
                                fill=color,width = 1)

def drawPill(app,canvas,cx,distance,color):
    width = 2*app.height*(1/distance) #Same citation as above for the height
    cy = app.height/2

    canvas.create_rectangle(cx-width/2,cy-width/2+2*width,cx+width/2,
                                cy+width/2+2*width,
                                fill=color,width = 0)

def drawGhost(app,canvas,cx,distance,color):
    if distance <= 0:
        distance = 0.001
    width =10*app.height*(1/distance) #Same citation as above for the height
    cy = app.height/2
    
    if app.g1.scared == True:
        color = "darkblue"

    #Body#####################
    canvas.create_polygon(cx-width/2,cy+width/2,cx-3*width/8,cy+width/4,
    cx-width/3,cy,cx-width/4,cy-width/4,cx,cy-3*width/8,cx+width/4,cy-width/4,
    cx+width/3,cy,cx+3*width/8,cy+width/4,cx+width/2,cy+width/2,
    cx+3*width/8,cy+width*3/8,cx+width/4,cy+width/2,cx+width/8,cy+width*3/8,
    cx,cy+width/2,cx-width/8,cy+width*3/8,cx-width/4,cy+width/2,
    cx-3*width/8,cy+width*3/8,cx-width/2,cy+width/2,fill=color,width=2)
    ######################
    #Eyes################
    x1 = cx-width/8
    x2 = cx+width/8
    y = cy-width/6
    r = width/24
    
    canvas.create_oval(x1-r,y-r,x1+r,y+r,fill="white",width=0)
    canvas.create_oval(x2-r,y-r,x2+r,y+r,fill="white",width=0)
    canvas.create_oval(x1-r/2,y-r,x1+r/2,y+r,fill="black")
    canvas.create_oval(x2-r/2,y-r,x2+r/2,y+r,fill="black")
    canvas.create_oval(x1-r/4,y-r/4,x1+r/4,y+r/4,fill="red")
    canvas.create_oval(x2-r/4,y-r/4,x2+r/4,y+r/4,fill="red")
    ###########################
    #Mouth########################
    r = width/6
    canvas.create_oval(cx-3*r/2,cy+r+width/16,cx+3*r/2,cy-r+width/16,
                        fill="white",width=0)
    if app.g1.scared == False:
        canvas.create_oval(cx-3*r/2,cy+r+width/24,cx+3*r/2,cy-r+width/24,
                        fill=color,width=0)
    else:
        canvas.create_oval(cx-3*r/2,cy+r+width/12,cx+3*r/2,cy-r+width/12,
                        fill=color,width=0)
    #############################
