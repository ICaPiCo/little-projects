import pyxel,math

class Window():

    def __init__(self):
        black_hole = [350,350,30,4,10] #X,Y,radius,strength,distance depletion
        light_points = [[0,100],[0,200],[0,300],[0,400],[0,500],[0,600]]
        initial_light_speed = 10
        initial_light_direction = 0
        pyxel.init(700,700,"Light tests")
        pyxel.run(self.update,self.draw)

    def update(self):
        pass

    def draw(self):
        pass

Window()