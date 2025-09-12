import pyxel
import math

class Entity:
    def __init__(self, name, size, x, y, vX, vY, col):
        self.name = name
        self.size = size
        self.mass = self.size * 93.63436814048291
        self.x = x
        self.y = y
        self.vX = vX
        self.vY = vY
        self.col = col

class Window:
    def __init__(self):
        pyxel.init(1920, 1135, "Space planet test",display_scale=0)
        pyxel.mouse(True)
        self.entities = []
        self.entities.append(Entity("Sun", 50, int(pyxel.width/2), int(pyxel.height/2), 0, 0, 9))
        self.initialX = None
        self.initialY = None
        self.endX = None
        self.endY = None
        self.global_size = 1
        pyxel.run(self.update, self.draw)
    
    def get_distance(self,x1,y1,x2,y2):
        return math.sqrt(((x2-x1)**2)+((y2-y1)**2))

    def attraction(self):
        G = 1
        
        for i in range(len(self.entities)):
            for j in range(i + 1, len(self.entities)):
                planet_A = self.entities[i]
                planet_B = self.entities[j]
                
                # Calculate distance
                distance = self.get_distance(planet_A.x, planet_A.y, planet_B.x, planet_B.y)
                
                # Avoid division by zero
                if distance == 0:
                    continue
                
                # Calculate gravitational force
                force = G * (planet_A.mass * planet_B.mass) / (distance ** 2)
                
                # Calculate angle between planets
                angle = math.atan2(planet_B.y - planet_A.y, planet_B.x - planet_A.x)
                
                # Calculate acceleration for each planet
                accel_A = force / planet_A.mass
                accel_B = force / planet_B.mass
                
                # Update velocities
                planet_A.vX += accel_A * math.cos(angle)
                planet_A.vY += accel_A * math.sin(angle)
                planet_B.vX -= accel_B * math.cos(angle)
                planet_B.vY -= accel_B * math.sin(angle)

    def update_positions(self):
        for entity in self.entities:
            entity.x += entity.vX
            entity.y += entity.vY

    def controls(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.initialX = pyxel.mouse_x
            self.initialY = pyxel.mouse_y
        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            self.endX = pyxel.mouse_x
            self.endY = pyxel.mouse_y
        if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
            velocityX = (self.endX - self.initialX) / 25
            velocityY = (self.endY - self.initialY) / 25
            self.entities.append(Entity(f"{len(self.entities)}", self.global_size, self.initialX, self.initialY, velocityX, velocityY, 5))
            self.initialX = None
            self.initialY = None
            self.endX = None
            self.endY = None
        if pyxel.btn(pyxel.KEY_RIGHT): self.global_size+=1
        if pyxel.btn(pyxel.KEY_LEFT): self.global_size-=1

    def fixed_sun(self):
        for planet in self.entities:
            if planet.name == "Sun":
                planet.x=int(pyxel.width/2)
                planet.y=int(pyxel.height/2)

    def delete_unused(self):
        to_remove = []
        
        for planet in self.entities:
            margin = planet.size * 2
            if (planet.x > pyxel.width + margin or 
                planet.y > pyxel.height + margin or 
                planet.x < -margin or 
                planet.y < -margin):
                to_remove.append(planet)
        
        for planet in to_remove:
            self.entities.remove(planet)


    def update(self):
        self.controls()
        self.attraction()
        self.update_positions()
        self.fixed_sun()
        self.delete_unused()
    
    def draw_line(self):
        try:
            pyxel.line(self.initialX,self.initialY,self.endX,self.endY,7)
        except: pass

    def draw_info(self):
        pyxel.text(0,0,f"Size: {self.global_size}",7)

    def draw_names(self):
        for planet in self.entities:
            pyxel.text(planet.x-len(planet.name)*2,planet.y+planet.size+4,planet.name,7)

    def draw(self):
        pyxel.cls(0)
        for entity in self.entities:
            pyxel.circ(entity.x, entity.y, entity.size, entity.col)
        self.draw_line()
        self.draw_info()
        self.draw_names()

Window()