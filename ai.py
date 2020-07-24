import helper, math, character, random
# 0.5.Find target tile
# 1.Look ahead at next tile in direction
# 2.Make a list of test tiles (2 from current tile)
# 3.Find test tile with shortest distance to target tile and set
# 4.Move 1 tile in direction | Found test tile becomes new lookAhead tile

##############################################################################
# CITATION
# https://www.gamasutra.com/view/feature/3938/the_pacman_dossier.php?print=1
# 
# FOR ALL THE PACMAN GHOST ALGLORTHIMS, BASICALLY THE WEBSITE EXPLAINED
# EVERYTHING I CODED UP IN THIS FILE
#############################################################################

def ghostMove(app):
    if app.timer%character.ghost.speed == 0:
        dicDir = {1:(-1,0),2:(0,-1),3:(1,0),4:(0,1)}
        ############Do for each ghost##############
        for ghost in app.ghostList:
            target = findTarget(app,ghost)
            ghost.target = target
            
            ###Boundry Move####
            newRow = ghost.row+ghost.rowDir
            newCol = ghost.col+ghost.colDir
            if newRow == 14:
                if newCol == 28:
                    newCol = 0
                elif newCol == -1:
                    newCol = 27
            ####################

            lookAhead = (newRow,newCol)

            testTiles = generateTestTiles(app,lookAhead,ghost)
            ghost.testTiles = testTiles

            bestDirection = findOptimalDirection(app,testTiles,target)

            ghost.row,ghost.col = lookAhead #Moving the ghost

            ghost.rowDir,ghost.colDir = dicDir[bestDirection] #Turning the ghost

        ##################Repeat#####################################

def findTarget(app,ghost):
    if ghost.scared == True:
        return scaredTarget(app,ghost)
    #Blinky (Need to add Elroy later)
    if ghost.color == "red": 
        #Normal Blinky
        if app.pellets < 220:
            if ghost.scatter == True:
                return (-3,25)
            else: 
                return blinkyTarget(app)
        #Elroy
        else:
            return blinkyTarget(app)
    
    #Pinky
    if ghost.color == "pink":
        if ghost.scatter == True:
            return (-3,2)
        else: 
            return pinkyTarget(app)

    #Inky
    if ghost.color == "aquamarine":
        if ghost.scatter == True:
            return (32,27)
        else:
            return inkyTarget(app)

    #Clyde
    if ghost.color == "orange":
        if ghost.scatter == True:
            return (32,0)
        else:
            return clydeTarget(app)
    

def generateTestTiles(app,cell,ghost):
    dirDic = {(-1,0):1,(0,-1):2,(1,0):3,(0,1):4}
    result = {}
    row,col = cell
    for rowDir in [-1,0,1]:
        for colDir in [-1,0,1]:
            if abs(rowDir + colDir) == 1:
                newRow = row+rowDir
                newCol = col+colDir
                        #print(f"Checking Row:{newRow} Col:{newCol}")
                ###Boundry Move####
                if newRow == 14:
                    if newCol == 28:
                        newCol = 0
                    elif newCol == -1:
                        newCol = 27
                ####################
                if (app.board[newRow][newCol] != app.wallColor and
                    (newRow,newCol) != (ghost.row,ghost.col)):
                    
                    result[(newRow,newCol)] = dirDic[(rowDir,colDir)]
    
    return result

def findOptimalDirection(app,tileDic,target):
    closestCell = None
    closestDistance = 8000000  # > the largest dimension of the window
    for tile in tileDic:
        dis = distance(app,tile,target)
        if dis < closestDistance:
            closestDistance = dis
            closestCell = tile
        elif dis == closestDistance:
            closestCell = [closestCell] + [tile]

    if type(closestCell)==list and len(closestCell) > 1:
        if tileDic[closestCell[0]] < tileDic[closestCell[1]]:
            return tileDic[closestCell[0]]
        else:
            return tileDic[closestCell[1]]
    else:
        return tileDic[closestCell]

def distance(app,cell1,cell2):
    row1,col1 = cell1
    row2,col2 = cell2
    x1,y1 = helper.getCxCy(app,row1,col1)
    x2,y2 = helper.getCxCy(app,row2,col2)
    return helper.length(x1,y1,x2,y2)

def blinkyTarget(app):
    return helper.getCell(app,app.pac.x,app.pac.y)

def pinkyTarget(app):
    dicDir = {1:(-1,0),2:(0,-1),3:(1,0),4:(0,1)}
    pacUp = False

    #Pac Dir = Up
    if math.sin(math.radians(app.pac.angle)) >= 1/(2**0.5):
        direction = dicDir[1]
        pacUp = True
    #Pac Dir = Left
    elif math.cos(math.radians(app.pac.angle)) <= -1/(2**0.5):
        direction = dicDir[2]
    #Pac Dir = Down
    elif math.sin(math.radians(app.pac.angle)) <= -1/(2**0.5):
        direction = dicDir[3]
    #Pac Dir = Right
    elif math.cos(math.radians(app.pac.angle)) >= 1/(2**0.5):
        direction = dicDir[4]

    rowShift,colShift = direction
    pacRow,pacCol = helper.getCell(app,app.pac.x,app.pac.y)

    if pacUp == True:
        #Special case, can read about it in the citation
        return (pacRow-4,pacCol-4)
    else:
        return (pacRow + 4*rowShift,pacCol + 4*colShift)

def inkyTarget(app):
    intermediate = None
    ######BASCIALLY PINKY'S CODE WITH 2 TILES################
    dicDir = {1:(-1,0),2:(0,-1),3:(1,0),4:(0,1)}
    pacUp = False

    #Pac Dir = Up
    if math.sin(math.radians(app.pac.angle)) >= 1/(2**0.5):
        direction = dicDir[1]
        pacUp = True
    #Pac Dir = Left
    elif math.cos(math.radians(app.pac.angle)) <= -1/(2**0.5):
        direction = dicDir[2]
    #Pac Dir = Down
    elif math.sin(math.radians(app.pac.angle)) <= -1/(2**0.5):
        direction = dicDir[3]
    #Pac Dir = Right
    elif math.cos(math.radians(app.pac.angle)) >= 1/(2**0.5):
        direction = dicDir[4]

    rowShift,colShift = direction
    pacRow,pacCol = helper.getCell(app,app.pac.x,app.pac.y)

    if pacUp == True:
        #Special case, can read about it in the citation
        intermediate = (pacRow-2,pacCol-2)
    else:
        intermediate = (pacRow + 2*rowShift,pacCol + 2*colShift)
    ########PINKY'S CONTRIBUTION ENDS HERE#############
    app.g3.intermediate = intermediate
    ########NOW WE FACTOR IN BLINKY'S DITANCE TO THE TILE######
    x1,y1 = helper.getCxCy(app,app.g1.row,app.g1.col) #Blinkys coord
    x2,y2 = helper.getCxCy(app,intermediate[0],intermediate[1]) #Inter coord
    

    dX = x2-x1
    dY = y2-y1

    finalX = x1 + 2*dX
    finalY = y1 + 2*dY

    return helper.getCell(app,finalX,finalY)

def clydeTarget(app):
    clydeCell = (app.g4.row,app.g4.col)
    pacCell = helper.getCell(app,app.pac.x,app.pac.y)
    prox = distance(app,clydeCell,pacCell)

    if prox > app.cellSize*8: #8 tiles away
        return pacCell
    else:
        return (32,0) #His scatter target

def scaredTarget(app,ghost):
    dicDir = {1:(-1,0),2:(0,-1),3:(1,0),4:(0,1)}

    nextTile = (ghost.row+ghost.rowDir,ghost.col+ghost.colDir)
    possible = generateTestTiles(app,nextTile,ghost)
    if len(possible) > 1:
        #Citation: https://stackoverflow.com/questions/4859292/how-to-get-a-random-value-from-dictionary-in-python
        return random.choice(list(possible.keys()))
        #####################################################################
    else:
        return nextTile
