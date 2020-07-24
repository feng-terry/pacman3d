import math, copy, random
import character, rayCast, helper, ai

#Citation: From tertis unit https://www.cs.cmu.edu/~112/notes/hw6.html
from cmu_112_graphics import *
###############################################
#Model
###############################################
def gameDimensions():
    rows = 31
    cols = 28
    cellSize = 25
    return(rows,cols,cellSize)

def playPacman():
    rows,cols,cellSize = gameDimensions()
    w = cols*cellSize
    h = rows*cellSize
    runApp(width = 700, height = 775)

def generateBoard(app):
    app.board = [[app.pillColor]*app.cols for i in range(app.rows)]
    wallList = {0:[i for i in range(28)],
                1:[0,13,14,27],
                2:[0,2,3,4,5,7,8,9,10,11,13,14,16,17,18,19,20,22,23,24,25,27],
                3:[0,2,3,4,5,7,8,9,10,11,13,14,16,17,18,19,20,22,23,24,25,27],
                4:[0,2,3,4,5,7,8,9,10,11,13,14,16,17,18,19,20,22,23,24,25,27],
                5:[0,27],
                6:[0,2,3,4,5,7,8,10,11,12,13,14,15,16,17,19,20,22,23,24,25,27],
                7:[0,2,3,4,5,7,8,10,11,12,13,14,15,16,17,19,20,22,23,24,25,27],
                8:[0,7,8,13,14,19,20,27],
            9:[0,1,2,3,4,5,7,8,9,10,11,13,14,16,17,18,19,20,22,23,24,25,26,27],
               10:[5,7,8,9,10,11,13,14,16,17,18,19,20,22],
               11:[5,7,8,19,20,22],
               12:[5,7,8,10,11,12,13,14,15,16,17,19,20,22],
           13:[0,1,2,3,4,5,7,8,10,11,12,13,14,15,16,17,19,20,22,23,24,25,26,27],
               14:[10,11,12,13,14,15,16,17],
           15:[0,1,2,3,4,5,7,8,10,11,12,13,14,15,16,17,19,20,22,23,24,25,26,27],
               16:[5,7,8,10,11,12,13,14,15,16,17,19,20,22],
               17:[5,7,8,19,20,22],
               18:[5,7,8,10,11,12,13,14,15,16,17,19,20,22],
           19:[0,1,2,3,4,5,7,8,10,11,12,13,14,15,16,17,19,20,22,23,24,25,26,27],
               20:[0,13,14,27],
               21:[0,2,3,4,5,7,8,9,10,11,13,14,16,17,18,19,20,22,23,24,25,27],
               22:[0,2,3,4,5,7,8,9,10,11,13,14,16,17,18,19,20,22,23,24,25,27],
               23:[0,4,5,22,23,27],
               24:[0,1,2,4,5,7,8,10,11,12,13,14,15,16,17,19,20,22,23,25,26,27],
               25:[0,1,2,4,5,7,8,10,11,12,13,14,15,16,17,19,20,22,23,25,26,27],
               26:[0,7,8,13,14,19,20,27],
           27:[0,2,3,4,5,6,7,8,9,10,11,13,14,16,17,18,19,20,21,22,23,24,25,27],
           28:[0,2,3,4,5,6,7,8,9,10,11,13,14,16,17,18,19,20,21,22,23,24,25,27],
               29:[0,27],
               30:[i for i in range(28)]}

    emptyList = {9:[12,15],
                10:[12,15],
                11:[9,10,11,12,13,14,15,16,17,18],
                12:[9,18],
                13:[9,18],
                14:[0,1,2,3,4,5,7,8,9,18,19,20,22,23,24,25,26,27],
                15:[9,18],
                16:[9,18],
                17:[9,10,11,12,13,14,15,16,17,18],
                18:[9,18],
                19:[9,18],
                23:[13,14]}

    superList = {3:[1,26],
                23:[1,26]}

    for i in range(31):
        walls = wallList[i]
        for col in walls:
            app.board[i][col] = app.wallColor

    for i in emptyList:
        empty = emptyList[i]
        for col in empty:
            app.board[i][col] = app.emptyColor

    for i in superList:
        sup = superList[i]
        for col in sup:
            app.board[i][col] = app.superColor

def appStarted(app):
    app.rows,app.cols,app.cellSize = gameDimensions()
    app.pac = character.pac(23,13,"orange",3,app)

    #Ghosts
    app.g1 = character.ghost(11,13,"red",app)
    app.g2 = character.ghost(12,13,"pink",app)
    app.g3 = character.ghost(12,13,"aquamarine",app)
    app.g4 = character.ghost(12,13,"orange",app)
    app.ghostList = [app.g1]
    #####

    app.pillColor = "yellow" 
    app.emptyColor = "grey"
    app.pacColor = "orange"
    app.wallColor = "blue"
    app.superColor = "blueviolet"
    generateBoard(app)
    app.pacDrow = 1
    app.pacDcol = 0
    app.score = 0
    app.timerDelay = 10
    #Ciation: smoothKeyMotion.py by Mike Taylor
    app.keysPressed = set()                 ###
    ###^^^above^^^#############################
    app.fov = 66
    app.timer = 0
    app.superHold = 0
    app.pellets = 0
    app.display = ""
    app.win = False
    app.start = False
    app.debug = False
    character.ghost.scatter = True
    character.ghost.scared = False

def movePac(app,direction):
    shiftX = (app.pac.speed*math.cos(math.radians(app.pac.angle)))*direction
    shiftY = (app.pac.speed*math.sin(math.radians(app.pac.angle)))*direction

    app.pac.x += shiftX
    app.pac.y -= shiftY

    #Boundry Move
    row,col = helper.getCell(app,app.pac.x,app.pac.y)
    if row == 14:
        if app.pac.x <= app.pac.radius + 1:
            app.pac.x = app.width - app.pac.radius -1
        elif app.pac.x >= app.width - app.pac.radius -1:
            app.pac.x = app.pac.radius +1

    #Legal Check
    if not legalPacMove(app):
        app.pac.x -= shiftX
        app.pac.y += shiftY
        return False
    elif app.board[row][col] == app.emptyColor:
        return False
    return True

def legalPacMove(app):
    if (app.pac.x < 0 or app.pac.y < 0 or 
    app.pac.x > app.width or app.pac.y >=app.height):
        return False

    for node in app.pac.collision:
        nodeX,nodeY = node
        row,col = helper.getCell(app,app.pac.x+nodeX,app.pac.y+nodeY)

        if (app.board[row][col] != app.pillColor 
            and app.board[row][col] != app.emptyColor
            and app.board[row][col] != app.superColor):
            return False
    return True

def pacDead(app):
    if character.ghost.scared == False:
        row,col = helper.getCell(app,app.pac.x,app.pac.y)
        return helper.ghostCell(app,row,col)
    else:
        return False

def eat(app):
    row,col = helper.getCell(app,app.pac.x,app.pac.y)

    if app.board[row][col] == app.pillColor:
        app.score+=10
        app.pellets += 1
    elif app.board[row][col] == app.superColor:
        app.score+=50
        character.ghost.scared = True
        character.ghost.speed = 20
        app.pac.speed = app.cellSize/14
        app.superHold = app.timer

    app.board[row][col] = app.emptyColor

def updateGhostList(app):
    #25 app.timer increases is roughtly 1 second on my computer
    if app.timer < 160:
        #Game Start Ghost Appearances
        if app.timer == 50:
            app.ghostList.append(app.g2)
        if app.timer == 100:
            app.ghostList.append(app.g3)
        if app.timer == 150:
            app.ghostList.append(app.g4)
    if app.timer<2200:
        ##Scatter Intervals####
        if app.timer == 175:
            character.ghost.scatter = False
        if app.timer == 675:
            character.ghost.scatter = True
        if app.timer == 850:
            character.ghost.scatter = False
        if app.timer == 1350:
            character.ghost.scatter = True
        if app.timer == 1475:
            character.ghost.scatter = False
        if app.timer == 1975:
            character.ghost.scatter = True
        if app.timer == 2100:
            character.ghost.scatter = False

    #If Pac Man eats a ghost
    row,col = helper.getCell(app,app.pac.x,app.pac.y)
    if character.ghost.scared:
        for ghost in app.ghostList:
            if ghost.row == row and ghost.col == col:
                app.score+=200
                ghost.tod = app.timer
                app.ghostList.remove(ghost)
    
    #Length of super time
    if app.timer - app.superHold == 150:
        character.ghost.scared = False
        character.ghost.speed = 14
        app.pac.speed = app.cellSize/16

    #Length of death time
    if app.timer > 160:
        for ghost in [app.g1,app.g2,app.g3,app.g4]:
            if ghost not in app.ghostList and app.timer-ghost.tod == 100:
                ghost.row = 12
                ghost.col = 13
                ghost.rowDir = -1
                ghost.colDir = 0
                app.ghostList.append(ghost)
    
def updateDisplay(app):
    if character.ghost.scared == True:
        app.display = "!!!SUPER!!!"
    else:
        app.display = ""
        
###############################################
#Controller
###############################################
def keyPressed(app,event):
    if (app.pac.dead == False) and app.start == True:
        app.keysPressed.add(event.key)
    elif event.key == "r" and app.pac.dead == True:
        appStarted(app)
    elif app.start == False and event.key == "s":
        appStarted(app)
        app.start = True
    elif app.start == False and event.key == "d":
        appStarted(app)
        app.start = True
        app.debug = True

def keyReleased(app,event):
    if app.pac.dead == False and app.start == True:
        if event.key in app.keysPressed:
            app.keysPressed.remove(event.key)

def timerFired(app):
    if app.start == True:
        app.timer += 1
        if app.pac.dead == False:
            if "Left" in app.keysPressed:
                app.pac.angle += 5
            if "Right" in app.keysPressed:
                app.pac.angle -= 5
            if "Up" in app.keysPressed:
                if movePac(app,1):
                    eat(app)
            if "Down" in app.keysPressed:
                if movePac(app,-1):
                    eat(app)
            updateGhostList(app)
            updateDisplay(app)
            ai.ghostMove(app)
            #Death Check
            if pacDead(app):
                app.pac.dead = True
            if app.pellets >= 240:
                app.pac.dead == True


###############################################
#View
###############################################
def redrawAll(app,canvas):
    #Play mode
    if app.start == True and app.debug == False:
        canvas.create_rectangle(0,0,app.width,app.height,fill = "darkkhaki")
        rayCast.run(app,canvas) 
            
        if (app.pac.dead == True):
            drawEndScreen(app,canvas,app.pellets,app.debug)

        #Draw Score/Display
        canvas.create_text(app.width/8,app.height/16,text = f"Score:{app.score}"
        ,font = "Times 25 bold", fill = app.superColor) 
        canvas.create_text(5*app.width/8,app.height/16,text = f"{app.display}"
        ,font = "Times 25 bold", fill = app.superColor)
    
    #Debug Mode
    elif app.start == True and app.debug == True:
        drawBoard(app,canvas)
        drawPac(app,canvas)

        if (app.pac.dead == True):
            drawEndScreen(app,canvas,app.pellets,app.debug)

        #Draw Score/Display/Ghost Mode
        canvas.create_text(app.width/2,app.height/2,text = f"Score:{app.score}"
        ,font = "Times 25 bold", fill = app.pillColor) 
        canvas.create_text(app.width/2,7*app.height/16,text = f"{app.display}"
        ,font = "Times 25 bold", fill = app.pillColor)
        if character.ghost.scared:
            canvas.create_text(app.width/2,10*app.height/16,
            text = "Ghost Mode: Frightened"
            ,font = "Times 16 bold", fill = app.pillColor)
        elif character.ghost.scatter:
            canvas.create_text(app.width/2,10*app.height/16,
            text = "Ghost Mode: Scatter"
            ,font = "Times 16 bold", fill = app.pillColor)
        else:
            canvas.create_text(app.width/2,10*app.height/16,
            text = "Ghost Mode: Chase"
            ,font = "Times 16 bold", fill = app.pillColor)

        
    #Start Screen
    else:
        drawStart(app,canvas)

def drawEndScreen(app,canvas,pellets,debug):
    if pellets >= 240:
        message = "WIN"
    else:
        message = "LOSE"
    if app.debug == False:
        canvas.create_text(app.width/2,app.height/2-25,text = f"YOU {message}",
                            fill = app.superColor,
                            font = "Times 45 bold")
        canvas.create_text(app.width/2,app.height/2 + 25,
                            text = f"Score: {app.score}",
                            fill = app.superColor,
                            font = "Times 45 bold")
        canvas.create_text(app.width/2,app.height/2 + 75,
                            text = "[r] Restart Game",
                            fill = app.superColor,
                            font = "Times 45 bold")
    else:
        canvas.create_text(app.width/2,app.height/2-50,text = f"[r] Restart Game"
        ,font = "Times 16 bold", fill = app.pillColor) 

def drawStart(app,canvas):
    canvas.create_rectangle(0,0,app.width,app.height,fill = "black")
    canvas.create_text(app.width/2,app.height/6,text = "PAC MAN 3D",
                        fill = "yellow",
                        font = "Times 70 bold")
    rayCast.drawGhost(app,canvas,app.width/4,28,"red")
    x = 3*app.width/4
    y = app.height/2 +20
    r = 125
    canvas.create_oval(x-r,y-r,x+r,y+r,fill = "yellow",width = 0)
    canvas.create_polygon(x,y,x+r+5,y+r-20,x+r+5,y-r+20,fill = "black")

    canvas.create_text(app.width/2,4*app.height/5 - 20,text = "[s] Start Game",
                        fill ="blue", font = "Times 30 bold")
    canvas.create_text(app.width/2,4*app.height/5 + 50,text = "[d] Debug Mode",
                        fill ="blue", font = "Times 30 bold")                    

def drawBoard(app,canvas):
    canvas.create_rectangle(0,0,app.width,app.height,fill = app.wallColor)
    for row in range(app.rows):
        for col in range(app.cols):
            if app.board[row][col] != app.wallColor:
                drawCell(app,canvas,row,col,app.board[row][col])
    drawGhost(app,canvas)

def drawCell(app,canvas,row,col,color):
    x1 = col*app.cellSize
    y1 = row*app.cellSize
    x2 = (col+1)*app.cellSize
    y2 = (row+1)*app.cellSize

    canvas.create_rectangle(x1,y1,x2,y2,fill = color, width = 2)

def drawGhost(app,canvas):
    for ghost in app.ghostList:
        #The ghost
        gX,gY = helper.getCxCy(app,ghost.row,ghost.col)

        drawCell(app,canvas,ghost.row,ghost.col,ghost.color)
        canvas.create_text(gX,gY,text="G",font="Times 12 bold")


        #Their target Cell
        targetRow,targetCol = ghost.target
        targetX,targetY = helper.getCxCy(app,targetRow,targetCol)

        drawCell(app,canvas,targetRow,targetCol,ghost.color)
        canvas.create_text(targetX,targetY,text="T",font="Times 12 bold")

        #Their testTiles
        for tile in ghost.testTiles:
            testRow,testCol = tile
            testX,testY = helper.getCxCy(app,testRow,testCol)

            canvas.create_rectangle(testX-app.cellSize/2,testY-app.cellSize/2,
                                    testX+app.cellSize/2,testY+app.cellSize/2,
                                    outline="green",width="5")
            canvas.create_text(testX,testY,text="?",font="Times 12 bold",
                                fill="green")

    if (app.g3 in app.ghostList and not character.ghost.scared 
        and not character.ghost.scatter):
        #Inkys intermediate cell
        intRow,intCol = app.g3.intermediate
        inkyRow,inkyCol = app.g3.target
        intX,intY = helper.getCxCy(app,intRow,intCol)
        blinkyX,blinkyY = helper.getCxCy(app,app.g1.row,app.g1.col)
        inkyX,inkyY = helper.getCxCy(app,inkyRow,inkyCol)

        drawCell(app,canvas,intRow,intCol,app.g3.color)
        canvas.create_text(intX,intY,text="I",font="Times 12 bold")
        canvas.create_line(blinkyX,blinkyY,inkyX,inkyY,fill="red",width=1)

    if (app.g4 in app.ghostList and not character.ghost.scared 
        and not character.ghost.scatter):
        #Clyde's proximity circle
        x = app.pac.x
        y = app.pac.y
        multiplier = 8*app.cellSize*math.cos(math.pi/4)

        canvas.create_oval(x-multiplier,y-multiplier,x+multiplier,y+multiplier,
                            outline = "orange")


def drawPac(app,canvas):
    app.pac.draw(app,canvas)

###############################################
#Main
###############################################
playPacman()
