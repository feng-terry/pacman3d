#Citation(getCell):https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
def getCell(app,x,y):    
    gridWidth  = app.width
    gridHeight = app.height
    cellWidth  = gridWidth / app.cols
    cellHeight = gridHeight / app.rows

    row = int((y) / cellHeight)
    col = int((x) / cellWidth)
    return (row,col)
##########^above^#####################################

def pointInGrid(app,x,y):
    return (x >= 0 and x <= app.width and y >= 0
            and y<= app.height)

def getCxCy(app,row,col):
    x = col * app.cellSize + app.cellSize/2
    y = row * app.cellSize + app.cellSize/2
    return (x,y)

def near(app,coord1,coord2):
    pillX,pillY = coord1
    x,y = coord2
    error = app.cellSize/15

    if (x > pillX - error and x < pillX + error 
    and y > pillY - error and y < pillY + error):
        return True

    return False

def ghostCell(app,row,col):
    for ghost in app.ghostList:
        if (row == ghost.row and col == ghost.col) and ghost.scared == False:
            return True
    return False

def length(x1,y1,x2,y2):
    return ((x2-x1)**2 + (y2-y1)**2)**0.5
 