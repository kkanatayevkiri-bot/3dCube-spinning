import pygame as pg
import math

#SETTINGS
X, Y = 800,800
RES = X,Y
HALFX, HALFY = X//2, Y//2
FPS = 60

#CUBE:
cube_vertices = [
    [-0.302, -0.26, -0.069],
    [0.302, -0.26, -0.069],
    [0.302, 0.26, -0.069],
    [-0.302, 0.26, -0.069],
    [-0.302, -0.26, 0.069],
    [0.302, -0.26, 0.069],
    [0.302, 0.26, 0.069],
    [-0.302, 0.26, 0.069],
]

faces = [
    (0, 1, 2, 3),  # Front
    (5, 4, 7, 6),  # Back
    (4, 0, 3, 7),  # Left
    (1, 5, 6, 2),  # Right
    (4, 5, 1, 0),  # Top
    (3, 2, 6, 7)   # Bottom
]

face_colors = [
    (255, 50, 50),   # Red
    (50, 255, 50),   # Green
    (50, 50, 255),   # Blue
    (255, 255, 50),  # Yellow
    (255, 50, 255),  # Purple
    (50, 255, 255)   # Cyan
]

SCALE = 100

class Game:
    def __init__(self):
        pg.init()
        self.display = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.play = True
        self.Xa = self.Ya = self.Za = 0

        self.freeze=False
        self.offsetX, self.offsetY = 400,400
        self.scale = 100

    def rotation(self,x,y,z):
        #rotation around 'x' axis
        dx = x
        dy = y * math.cos(self.Xa) - z * math.sin(self.Xa)
        dz = y * math.sin(self.Xa) + z * math.cos(self.Xa)

        #rotation around 'y' axis
        newY = dy
        newX = dx*math.cos(self.Ya) - dz*math.sin(self.Ya)
        newZ = dx*math.sin(self.Ya) + dz*math.cos(self.Ya)

        #rotation around 'z' axis
        final_z = newZ
        final_x = newX*math.cos(self.Za) - newY*math.sin(self.Za)
        final_y = newX*math.sin(self.Za) + newY*math.cos(self.Za)

        return final_x,final_y,final_z
    
    def controls(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.play = False
            elif event.type == pg.MOUSEMOTION:
                if not self.freeze:
                    dirX, dirY = event.rel
                    dirX, dirY = dirX*0.25, dirY*0.25
                    self.Ya += dirX/math.tau % math.tau
                    self.Xa += dirY/math.tau % math.tau
            elif event.type == pg.MOUSEWHEEL:
                if event.y < 1:
                    self.scale-=5
                else:
                    self.scale+=5

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_f:
                    if self.freeze:
                        self.freeze = False
                    else:
                        self.freeze = True

    def update(self):
        self.clock.tick(FPS)

    def draw(self):
        self.display.fill((0,76,153))
        dots=[]
        for x,y,z in cube_vertices:
            newX,newY,newZ = self.rotation(x,y,z)
            dots.append((newX, newY, newZ))

        qeue = []
        for i, f in enumerate(faces):
            ave_z = sum(dots[index][2] for index in f)/4
            qeue.append((ave_z, f, face_colors[i]))

        qeue.sort(key=lambda item:item[0], reverse=True)

        for z, f, c in qeue:
            points = [(self.scale*dots[i][0]+offsetX, self.scale*self.offsetY[i][1]+400) for i in f]
            pg.draw.polygon(self.display, c, points)
            # pg.draw.polygon(self.display, (0, 0, 0), points, 2)

        pg.display.flip()
    def run(self):
        while self.play:
            self.controls()
            self.update()
            self.draw()

if __name__ == "__main__":
    g = Game()
    g.run()
    pg.quit()