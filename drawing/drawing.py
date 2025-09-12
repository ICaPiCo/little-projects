import pyxel,math

class Window():
    """A simple drawing application using Pyxel game engine."""
    
    def __init__(self):
        """Initialize the drawing window and application state."""
        self.resolution = 400
        self.stroke = []  # Current stroke being drawn
        self.history = []    # Completed strokes stored as [color, points] pairs
        self.current_color = 0
        pyxel.init(self.resolution, self.resolution,"Drawing test", fps=60)
        pyxel.mouse(True)
        pyxel.load("drawing.pyxres")
        pyxel.run(self.update,self.draw)
        
    def update_controls(self):
        # Left mouse button held - add points to current stroke
        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            x = min(max(pyxel.mouse_x, 0), self.resolution - 1)
            y = min(max(pyxel.mouse_y, 0), self.resolution - 1)
            self.stroke.append([x, y])
            
        # Left mouse button released - save stroke to history
        if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
            if self.stroke:
                self.history.append([self.current_color, self.stroke])
                self.stroke = []
                
        # Right arrow key - increase color (max 15)
        if pyxel.btnp(pyxel.KEY_RIGHT) and self.current_color != 15:
            self.current_color+=1
            
        # Left arrow key - decrease color (min 0)
        if pyxel.btnp(pyxel.KEY_LEFT) and self.current_color != 0:
            self.current_color-=1
            
        # S key held - erase points from last stroke
        if pyxel.btn(pyxel.KEY_S) and self.history != []:
            if self.history[-1][1]:
                self.history[-1][1].pop(-1)
                if not self.history[-1][1]:
                    self.history.pop(-1)
                    
        # Z key pressed - undo last stroke
        if pyxel.btnp(pyxel.KEY_Z) and self.history != []:
            self.history.pop(-1)

    def update(self):
        """Handle user input and update application state."""
        self.update_controls()
            
    def draw_history(self):
        # Draw completed strokes from history
        for stroke_data in self.history:
            color, points = stroke_data
            for j in range(len(points) - 1):
                x, y = points[j]
                nextX, nextY = points[j + 1]
                pyxel.line(x, y, nextX, nextY, color)

    def draw_stroke(self):
        # Current stroke
        for j in range(len(self.stroke) - 1):
            x, y = self.stroke[j]
            nextX, nextY = self.stroke[j + 1]
            pyxel.line(x, y, nextX, nextY, self.current_color)

    def draw_ui_colors(self):
        for i in range(15):
            colkey=7
            if i==7: colkey = 13
            x = ((pyxel.height- 20)+math.sin(i+1.5-self.current_color)*-20)
            y = (((pyxel.width/2)+i*20)-self.current_color*20)
            trsp = (pyxel.width - int(x)) / 40
            size = (pyxel.width - int(x)) / 40 + 0.3
            if y>275 or y<160: trsp = 0
            pyxel.dither(trsp)
            pyxel.blt(x,y,0,i*16,0,16,16,colkey,scale=size,rotate=i*22.5)
            pyxel.dither(1)

    def draw(self):
        """Render all strokes and current drawing to screen."""
        pyxel.cls(7)  # Clear screen with white
        self.draw_history()
        self.draw_stroke()
        self.draw_ui_colors()

Window()