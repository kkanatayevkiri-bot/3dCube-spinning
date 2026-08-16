import pygame as pg
import math

#SETTINGS
X, Y = 800,800
RES = X,Y
HALFX, HALFY = X//2, Y//2
FPS = 60

#CUBE:
cube_vertices = [
    [-1, -1, -1],
    [1, -1, -1],
    [1, 1, -1],
    [-1, 1, -1],
    [-1, -1, 1],
    [1, -1, 1],
    [1, 1, 1],
    [-1, 1, 1],
]

# The 12 lines (edges) connecting the corners
edges = [
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0),
    (4, 5),
    (5, 6),
    (6, 7),
    (7, 4),
    (0, 4),
    (1, 5),
    (2, 6),
    (3, 7),
]
SCALE = 100

class Game:
    def __init__(self):
        pg.init()
        self.display = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.play = True
        self.Xa = self.Ya = self.Za = 0

    def xRotation(self,x,y,z):
        # Rotate in 3D
        dx = x
        dy = y * math.cos(self.Xa) - z * math.sin(self.Xa)
        dz = y * math.sin(self.Xa) + z * math.cos(self.Xa)

        return dx, dy, dz

    def yRotation(self,x,y,z):
        dy = y
        dx = x*math.cos(self.Ya) - z*math.sin(self.Ya)
        dz = x*math.sin(self.Ya) + z*math.cos(self.Ya)

        return dx, dy, dz

    def zRotation(self,x,y,z):
        dz = z
        dx = x*math.cos(self.Za) - y*math.sin(self.Za)
        dy = x*math.sin(self.Za) + y*math.cos(self.Za)
        return dx,dy,dz
    
    def keyboard(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.play = False

    def update(self):
        self.clock.tick(FPS)
        self.Xa = (self.Xa+0.01)%math.tau
        self.Ya = (self.Ya+0.01)%math.tau
        self.Za = (self.Za+0.01)%math.tau

    def draw(self):
        self.display.fill((0,76,153))
        dots=[]
        for x,y,z in cube_vertices:
            newX,newY,newZ = self.xRotation(x,y,z)
            newX,newY,newZ = self.yRotation(newX,newY,newZ)
            newX,newY,newZ = self.zRotation(newX,newY,newZ)
            dots.append((newX,newY))

        for a,b in edges:
            dot = dots[a]
            dot2 = dots[b]
            x, y = dot
            x2, y2 = dot2
            point1 = HALFX+x*100, HALFX+y*100
            point2 = HALFX+x2*100, HALFX+y2*100
            pg.draw.line(self.display,(255,0,0),point1,point2)

        # for i in range(len(dots)-2):
        #     dot1 = (HALFX+dots[i][0]*100,HALFY+dots[i][1]*100)
        #     dot2 = (HALFX+dots[i+1][0]*100,HALFY+dots[i+1][1]*100)
        #     pg.draw.line(self.display,(255,0,0),dot1,dot2)

        for sx,sy in dots:
            pg.draw.circle(self.display,(255,255,0),(HALFX+(sx*100),HALFY+(sy*100)),5)
        pg.display.flip()

    def run(self):
        while self.play:
            self.keyboard()
            self.update()
            self.draw()

if __name__ == "__main__":
    g = Game()
    g.run()
    pg.quit()