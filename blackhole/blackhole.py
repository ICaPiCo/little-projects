import pyxel,math

class Window():

    def __init__(self):
        pyxel.init(700,700,"")
        pyxel.run(self.update,self.draw)

    def update(self):
        pass

    def draw(self):
        pass

Window()