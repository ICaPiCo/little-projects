import pyxel,math

class Window():

    def __init__(self):
        pyxel.init(100,100,"Light tests",display_scale=4,fps=120)
        self.space = 2
        self.points = []
        for x in range(0,pyxel.width,self.space):
            for y in range(0,pyxel.width,self.space):
                self.points.append([x,y,0])
        pyxel.mouse(True)
        pyxel.run(self.update,self.draw)

    def get_distance(self,x1,y1,x2,y2):
        return math.sqrt(((x2-x1)**2)+((y2-y1)**2))

    def controls(self):
        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            for point in self.points:
                x = point[0]
                y = point[1]
                if self.get_distance(x,y,pyxel.mouse_x,pyxel.mouse_y) < self.space + 1:
                    point[2] = 100
        elif pyxel.btn(pyxel.MOUSE_BUTTON_RIGHT):
            for point in self.points:
                x = point[0]
                y = point[1]
                if self.get_distance(x,y,pyxel.mouse_x,pyxel.mouse_y) < self.space + 1:
                    point[2] = -100

    def average_out(self):
        grid_width = pyxel.width // self.space
        for i in range(len(self.points)):
            neighbors = [
            i - grid_width - 1,  # up-left
            i - grid_width,      # up
            i - grid_width + 1,  # up-right
            i - 1,               # left
            i + 1,               # right
            i + grid_width - 1,  # down-left
            i + grid_width,      # down
            i + grid_width + 1   # down-right
            ]
            nb_points = 1
            total_i = self.points[i][2]
            for rank in neighbors:
                try:
                    total_i += self.points[rank][2]
                    nb_points += 1
                except: pass
            total_i /= nb_points
            self.points[i][2] = total_i


    def update(self):
        self.controls()
        self.average_out()

    def draw_points(self):
        for point in self.points:
            x = point[0]
            y = point[1]
            intensity = point[2]
            pyxel.pset(x,y-intensity,5)

    def draw(self):
        pyxel.cls(0)
        self.draw_points()

Window()