import pyxel,math,time,random

class Window():

    def __init__(self):
        size=500
        pyxel.init(size,size,"Mountain",display_scale=2,fps=100000)
        self.points_x = []
        self.points_y = []
        self.temp_point_x = None
        self.temp_point_y = None
        self.touching = True
        self.points_x.append(pyxel.width/2)
        self.points_y.append(pyxel.height/2)
        self.bounding_x_start = int((pyxel.width/2) - 25)
        self.bounding_x_end = int((pyxel.width/2) + 25)
        self.bounding_y_start = int((pyxel.height/2) - 25)
        self.bounding_y_end = int((pyxel.height/2) + 25)

        pyxel.run(self.update,self.draw)

    def new_point(self):
        self.temp_point_x = random.randint(int(self.bounding_x_start),int(self.bounding_x_end-1))
        self.temp_point_y = random.randint(int(self.bounding_y_start),int(self.bounding_y_end-1))
        self.touching = False

    def reset(self):
        self.points_x.append(self.temp_point_x)
        self.points_y.append(self.temp_point_y)
        self.touching = True

        min_x = min(self.points_x)
        max_x = max(self.points_x)
        min_y = min(self.points_y)
        max_y = max(self.points_y)
        if min_x - self.bounding_x_start <= 25: self.bounding_x_start-=1
        if self.bounding_x_end - max_x <= 25: self.bounding_x_end+=1
        if min_y - self.bounding_y_start <= 25: self.bounding_y_start-=1
        if self.bounding_y_end - max_y <= 25: self.bounding_y_end+=1

    def update(self):
        
        if self.touching:
            self.new_point()
        else:
            xORy_choice = random.randint(1,2)
            if xORy_choice == 1:
                pORm_choice = random.randint(1,2)

                if pORm_choice == 1 and self.temp_point_x<int(self.bounding_x_end-1):
                    self.temp_point_x+=1

                elif pORm_choice == 2 and self.temp_point_x>int(self.bounding_x_start):
                    self.temp_point_x-=1

            else:
                pORm_choice = random.randint(1,2)

                if pORm_choice == 1 and self.temp_point_y<int(self.bounding_y_end-1):
                    self.temp_point_y+=1

                elif pORm_choice == 2 and self.temp_point_y>int(self.bounding_y_start):
                    self.temp_point_y-=1

            for i in range(len(self.points_x)):
                if abs(self.points_x[i] - self.temp_point_x) == 1 and abs(self.points_y[i] - self.temp_point_y) == 0:
                    self.reset()
                    break

                if abs(self.points_x[i] - self.temp_point_x) == 0 and abs(self.points_y[i] - self.temp_point_y) == 1:
                    self.reset()
                    break

    def draw(self):
        pyxel.cls(0)
        for i in range(len(self.points_x)):
            pyxel.pset(self.points_x[i],self.points_y[i],7)
        pyxel.pset(self.temp_point_x,self.temp_point_y,7)
        pyxel.rectb(int(self.bounding_x_start),int(self.bounding_y_start),int(self.bounding_x_end-self.bounding_x_start),int(self.bounding_y_end-self.bounding_y_start),9)

Window()