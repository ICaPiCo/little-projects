import pyxel,math,random

class Window():

    def __init__(self):
        self.particles = []
        self.color = 6
        self.dispertion = 3
        self.force = 0.5
        pyxel.init(100,100,"Fluid Simulation",fps=120)
        pyxel.mouse(True)
        pyxel.run(self.update,self.draw)

    def controls(self):
        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            self.particles.append([(random.randint(-self.dispertion,self.dispertion)+pyxel.mouse_x),(random.randint(-self.dispertion,self.dispertion)+pyxel.mouse_y)])

    def gravity(self):
        for position in self.particles:
            position[1]+=0.5

    def get_distance(self,x1,y1,x2,y2):
        return math.sqrt((x2-x1)**2)+((y2-y1)**2)

    def repulsion(self):
        for i in range(len(self.particles)):
            first_particle = self.particles[i]
            for j in range(len(self.particles)):
                if i == j:
                    continue
                    
                second_particle = self.particles[j]
                x1 = first_particle[0]
                y1 = first_particle[1]
                x2 = second_particle[0]
                y2 = second_particle[1]
                
                distance = self.get_distance(x1, y1, x2, y2)
                formula = self.force/max(distance**2, 0.1)
                
                if distance < 4 and distance > 0:
                    angle = math.atan2(y2 - y1, x2 - x1) + math.pi
                    first_particle[0] += math.cos(angle) * formula
                    first_particle[1] += math.sin(angle) * formula

    def nono(self):
        for rank in range(len(self.particles)):
            particle = self.particles[rank]
            x = particle[0]
            y = particle[1]
            if x > pyxel.width:
                self.particles[rank][0]=pyxel.width-1
            elif x < 0:
                self.particles[rank][0]=1
            if y > pyxel.height:
                self.particles[rank][1]=pyxel.height-1
            elif y < 0:
                self.particles[rank][1]=1

    def update(self):
        self.controls()
        self.gravity()
        self.nono()
        self.repulsion()


    def draw_particles(self):
        for position in self.particles:
            x=position[0]
            y=position[1]
            pyxel.pset(int(x),int(y),self.color)

    def draw(self):
        pyxel.cls(0)
        self.draw_particles()

Window()