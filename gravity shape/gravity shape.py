import pyxel,math,random

class Window():

    def __init__(self):
        self.particles = []
        self.color = 7
        self.force = 10
        self.distance_threshold = 30
        pyxel.init(1920,1135,"Rig Simulation",fps=240)
        pyxel.mouse(True)
        pyxel.run(self.update,self.draw)

    def controls(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.particles.append([pyxel.mouse_x,pyxel.mouse_y])


    def get_distance(self,x1,y1,x2,y2):
        return math.sqrt(((x2-x1)**2)+((y2-y1)**2))

    def attraction_and_repulsion(self):
        for i in range(len(self.particles)):
            for j in range(len(self.particles)):
                if i != j:
                    first_particle = self.particles[j]
                    second_particle = self.particles[i]

                    x1 = first_particle[0]
                    y1 = first_particle[1]
                    x2 = second_particle[0]
                    y2 = second_particle[1]
                    
                    distance = self.get_distance(x1, y1, x2, y2)
                    distance_dif = abs(self.distance_threshold - distance)
                    formula_1 = distance_dif/self.force
                    formula_2 = distance_dif/self.force
                    
                    if self.distance_threshold*1.5 > distance > self.distance_threshold > 0:  
                        angle = math.atan2(y2 - y1, x2 - x1)
                        first_particle[0] += math.cos(angle) * formula_1
                        first_particle[1] += math.sin(angle) * formula_1
                    elif 0 < distance < self.distance_threshold:
                        angle = math.atan2(y2 - y1, x2 - x1) + math.pi
                        first_particle[0] += math.cos(angle) * formula_2
                        first_particle[1] += math.sin(angle) * formula_2

    def nono(self):
        for rank in range(len(self.particles)):
            particle = self.particles[rank]
            x = particle[0]
            y = particle[1]
            if x > pyxel.width:
                self.particles[rank][0]=pyxel.width
            elif x < 0:
                self.particles[rank][0]=0
            if y > pyxel.height:
                self.particles[rank][1]=pyxel.height
            elif y < 0:
                self.particles[rank][1]=0


    def update(self):
        self.controls()
        self.nono()
        self.attraction_and_repulsion()


    def draw_particles(self):
        for position in self.particles:
            x=position[0]
            y=position[1]
            pyxel.pset(int(x),int(y),self.color)

    def draw_lines(self):
            # Draw lines between particles that are close
            for i in range(len(self.particles)):
                for j in range(i + 1, len(self.particles)):
                    x1, y1 = self.particles[i]
                    x2, y2 = self.particles[j]
                    distance = self.get_distance(x1, y1, x2, y2)
                    if distance < self.distance_threshold * 1.5:
                        pyxel.line(int(x1), int(y1), int(x2), int(y2), 6)

    def draw(self):
        pyxel.cls(0)
        self.draw_lines()
        self.draw_particles()

Window()