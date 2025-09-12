import pyxel,math

class Window():

    def __init__(self):
        self.original_points = [] #x,y,point initial rotation 
        self.points = self.original_points.copy()
        self.global_rotation = 0
        self.amplitude_x = 50
        self.amplitude_y = 30

        pyxel.init(300,300,"3d Drawing test",fps=120)
        pyxel.mouse(True)
        pyxel.run(self.update,self.draw)

    def refresh(self):
        self.points = self.original_points.copy()


    def controls(self):
        if pyxel.btn(pyxel.KEY_RIGHT): self.global_rotation+=1
        if pyxel.btn(pyxel.KEY_LEFT): self.global_rotation-=1
        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT): 
            self.original_points.append([pyxel.mouse_x,pyxel.mouse_y,self.global_rotation])
            self.refresh()
        if self.global_rotation>360:self.global_rotation=0
        if self.global_rotation<0:self.global_rotation=360


    def update_points_trig(self,x,y,rot,rank):
        distance_from_center = self.original_points[rank][0] - 150  # How far from center when clicked
        x=150+distance_from_center*math.cos(math.radians(self.global_rotation-rot))
        y=self.original_points[rank][1]+distance_from_center*0.5*math.sin(math.radians(self.global_rotation-rot))
        self.points[rank]=[x,y,rot]

    def update(self):
        self.controls()
        for i in range(len(self.points)):
            x,y,rot=self.original_points[i]
            self.update_points_trig(x,y,rot,i)

    def draw_point(self,x,y,rank):
        """
        if rank == len(self.points)-1:
            pyxel.circ(x,y,3,8)

        elif rank == len(self.points)-2:
            pyxel.circ(x,y,3,10)

        elif rank == 0:
            pyxel.circ(x,y,3,11)
        """

        pyxel.pset(x,y,7)

    def draw_debug(self):
        pyxel.text(0,0,f"global_rotation: {self.global_rotation}",7)

    def draw(self):
        pyxel.cls(0)
        for i in range(len(self.points)):
            x1,y1,rot1=self.points[i]
            if i+1 < len(self.points):
                x2,y2,rot2=self.points[i+1]
                pyxel.line(x1,y1,x2,y2,7)
            """
            else:
                x0,y0,rot0=self.points[0]
                pyxel.line(x1,y1,x0,y0,7)
            """
            self.draw_point(x1,y1,i)
        self.draw_debug()

Window()