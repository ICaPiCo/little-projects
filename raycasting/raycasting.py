import pyxel, math

class Window():
    def __init__(self):
        self.playerX = 84*1.5
        self.playerY = 94*1.5
        self.playerRotation = 0
        self.FOV = 90
        self.numberOfRays = 0.5
        self.specialWidth = 10
        self.twodVision = []
        self.walls = [13]
        pyxel.init(1000, 1000, "Simple Raycasting", fps=120)
        pyxel.load("raycasting.pyxres")
        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)

    def special_line(self,x,size,color,width,transparency,length):
        if length > 400:
            transparency=0
        tempX=x-width/2
        tempY = 500-size/2
        for i in range(width):
            pyxel.dither(transparency)
            pyxel.line(tempX,tempY,tempX,tempY+size,int(color))
            pyxel.dither(1)
            tempX+=1

    def draw_3D(self):
        step=1000/(len(self.twodVision)+1)
        x=10
        distance_colors = [7, 10, 9, 8]
        for i in self.twodVision:
            # Fix 1: Better distance to height conversion for more noticeable differences
            line_height = min(800, 25000 / max(i, 1))
            
            # Color based on distance - map distance to color index
            max_distance = 200  # Based on your max_steps
            color_index = min(3, int((i / max_distance) * 4))  # Map to 0-3 range
            wall_color = distance_colors[color_index]
            
            self.special_line(x, line_height, wall_color, self.specialWidth, 1,i)
            x+=step
        self.twodVision = []

    def draw_line(self, angle):
        steps = 0
        max_steps = 500
        particleX = self.playerX
        particleY = self.playerY
        angle_rad = math.radians(angle)

        while steps < max_steps:
            particleX += math.cos(angle_rad)
            particleY += math.sin(angle_rad)
            steps += 1
            if (particleX < 0 or particleX >= 1000 or
                particleY < 0 or particleY >= 1000):
                break
            pixel_color = pyxel.pget(int(particleX), int(particleY))
            if pixel_color in self.walls:
                break

        pyxel.line(self.playerX, self.playerY, int(particleX), int(particleY), 9)
        
        # Fix 2: Apply cosine correction to prevent fish-eye effect
        raw_distance = math.sqrt(abs(particleX - self.playerX)**2 + abs(particleY - self.playerY)**2)
        angle_diff = angle - self.playerRotation
        corrected_distance = raw_distance * math.cos(math.radians(angle_diff))
        self.twodVision.append(corrected_distance)

    def draw_vision(self):
        start_angle = self.playerRotation - self.FOV // 2

        for i in range(int(self.FOV*self.numberOfRays)):
            angle = start_angle + i/self.numberOfRays
            self.draw_line(angle)

    def draw_player(self):
        pyxel.circ(self.playerX - 2, self.playerY, 4, 16)

    def update(self):
        if pyxel.btn(pyxel.KEY_Z):
            new_x = self.playerX + math.cos(math.radians(self.playerRotation)) * 2
            new_y = self.playerY + math.sin(math.radians(self.playerRotation)) * 2
            if 0 < new_x < 1000 and 0 < new_y < 1000:
                self.playerX = new_x
                self.playerY = new_y

        if pyxel.btn(pyxel.KEY_S):
            new_x = self.playerX - math.cos(math.radians(self.playerRotation)) * 2
            new_y = self.playerY - math.sin(math.radians(self.playerRotation)) * 2
            if 0 < new_x < 1000 and 0 < new_y < 1000:
                self.playerX = new_x
                self.playerY = new_y

        if pyxel.btn(pyxel.KEY_Q):
            self.playerRotation -= 3

        if pyxel.btn(pyxel.KEY_D):
            self.playerRotation += 3

        if pyxel.btnp(pyxel.KEY_UP):
            self.numberOfRays+=0.1

        if pyxel.btnp(pyxel.KEY_DOWN):
            self.numberOfRays-=0.1

        if pyxel.btnp(pyxel.KEY_RIGHT):
            self.specialWidth += 1

        if pyxel.btnp(pyxel.KEY_LEFT):
            self.specialWidth -= 1        

    def draw(self):
        pyxel.cls(0)
        pyxel.blt(0 + 60 * 8, 0 + 60 * 8, 0, 0, 0, 16, 16, 0, scale=70)  # background
        self.draw_3D()
        pyxel.blt(0 + 16 * 8, 0 + 16 * 8, 0, 16, 0, 16, 16, scale=16)     # minimap
        self.draw_player()
        self.draw_vision()

Window()