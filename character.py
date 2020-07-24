import math

class character(object):
    def __init__(self,row,col,color,app):
        self.row = row
        self.col = col
        self.x = col*app.cellSize + app.cellSize/2
        self.y = row*app.cellSize + app.cellSize/2
        self.color = color
        self.dead = False

class pac(character):
    def __init__(self,row,col,color,radius,app):
        super().__init__(row,col,color,app)
        self.angle = 90
        self.speed = app.cellSize/16
        self.radius = radius
        self.collision = [(0,radius*-1),(radius,radius*-1),
                         (radius,0),(radius,radius),
                         (0,radius),(radius*-1,radius),
                         (radius*-1,0),(radius*-1,radius*-1)]

    def draw(self,app,canvas):
        radius = app.cellSize/2
        x2 = self.x + radius*math.cos(math.radians(self.angle-30))
        y2 = self.y - radius*math.sin(math.radians(self.angle-30))

        x3 = self.x + radius*math.cos(math.radians(self.angle+30))
        y3 = self.y - radius*math.sin(math.radians(self.angle+30))

        canvas.create_oval(self.x-self.radius,self.y-self.radius,
                         self.x+self.radius,self.y+self.radius,fill=self.color)
        for node in self.collision:
            nodeX,nodeY = node
            canvas.create_oval(self.x+nodeX,self.y+nodeY,
                         self.x+nodeX,self.y+nodeY,fill="red")


        canvas.create_line(self.x,self.y,x2,y2)
        canvas.create_line(self.x,self.y,x3,y3)

class ghost(character):
    speed = 14 #Higher the number the slower
    scatter = True
    scared = False

    def __init__(self,row,col,color,app):
        super().__init__(row,col,color,app)
        self.speed = 0.9*(app.cellSize/16)
        self.rowDir = 0
        self.colDir = 0
        self.target = (0,0)
        self.testTiles = []
        self.intermediate = (-1,-1)
        self.tod = 0
        


