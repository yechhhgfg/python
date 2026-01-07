# coding:utf-8
"""
Render 皮卡丘 using a minimal turtle-like simulator drawing to a Pillow image.
"""
import math
from PIL import Image, ImageDraw

import sys

# 默认分辨率（可通过命令行传参覆盖）
DEFAULT_W, DEFAULT_H = 1000, 800

def get_canvas_size():
    # 用法: python scripts/render_pikachu_pil.py [width] [height] [output]
    if len(sys.argv) >= 3:
        try:
            w = int(sys.argv[1])
            h = int(sys.argv[2])
            return w, h
        except Exception:
            pass
    return DEFAULT_W, DEFAULT_H

IMG_W, IMG_H = get_canvas_size()
ORIGIN_X, ORIGIN_Y = IMG_W // 2, IMG_H // 2

class TurtleSim:
    def __init__(self, draw):
        self.draw = draw
        self.x = 0.0
        self.y = 0.0
        self.heading = 0.0  # degrees, 0 east, 90 north
        self.pendown = True
        self.color = (0,0,0)
        self.fillcolor = None
        self.pensize = 2
        self.filling = False
        self.fill_points = []

    def _to_img(self, x, y):
        ix = ORIGIN_X + x
        iy = ORIGIN_Y - y
        return (ix, iy)

    def pu(self):
        self.pendown = False

    def pd(self):
        self.pendown = True

    def goto(self, x, y):
        nx, ny = float(x), float(y)
        if self.pendown:
            self.draw.line([self._to_img(self.x, self.y), self._to_img(nx, ny)], fill=self.color, width=int(self.pensize))
            if self.filling:
                self.fill_points.append(self._to_img(nx, ny))
        if self.filling and not self.pendown:
            self.fill_points.append(self._to_img(nx, ny))
        self.x, self.y = nx, ny

    def setheading(self, angle):
        self.heading = float(angle) % 360

    def forward(self, dist):
        rad = math.radians(self.heading)
        nx = self.x + math.cos(rad) * dist
        ny = self.y + math.sin(rad) * dist
        if self.pendown:
            self.draw.line([self._to_img(self.x, self.y), self._to_img(nx, ny)], fill=self.color, width=int(self.pensize))
            if self.filling:
                self.fill_points.append(self._to_img(nx, ny))
        self.x, self.y = nx, ny

    def lt(self, ang):
        self.heading = (self.heading + ang) % 360

    def rt(self, ang):
        self.heading = (self.heading - ang) % 360

    def pensize(self, w):
        self.pensize = w

    def begin_fill(self):
        self.filling = True
        self.fill_points = [self._to_img(self.x, self.y)]

    def end_fill(self):
        if self.fillcolor and self.fill_points:
            try:
                self.draw.polygon(self.fill_points, fill=self.fillcolor, outline=None)
            except Exception:
                pass
        self.filling = False
        self.fill_points = []

    def fillcolor_set(self, col):
        self.fillcolor = col

    def color_set(self, stroke, fill=None):
        self.color = stroke
        if fill is not None:
            self.fillcolor = fill

    def circle(self, r, extent=360):
        # draw arc centered to the left of turtle
        steps = max(6, int(abs(extent) / 2))
        heading_rad = math.radians(self.heading)
        # center offset = left of heading
        cx = self.x + math.cos(heading_rad + math.pi/2) * r
        cy = self.y + math.sin(heading_rad + math.pi/2) * r
        start_angle = math.degrees(math.atan2(self.y - cy, self.x - cx))
        points = []
        for i in range(steps + 1):
            ang = start_angle + (extent * i / steps)
            rad = math.radians(ang)
            px = cx + r * math.cos(rad)
            py = cy + r * math.sin(rad)
            points.append(self._to_img(px, py))
        # draw lines
        for a, b in zip(points[:-1], points[1:]):
            self.draw.line([a, b], fill=self.color, width=int(self.pensize))
        # update position to last point
        lastx, lasty = (points[-1][0] - ORIGIN_X, ORIGIN_Y - points[-1][1])
        self.x, self.y = lastx, lasty
        if self.filling:
            self.fill_points += points

# Helpers to convert simple color names used in the original script
COLORS = {
    'black': (0,0,0),
    'yellow': (255, 215, 0),
    'red': (255,0,0),
    'white': (255,255,255)
}

# Ported functions (simplified) from 皮卡丘.py but using TurtleSim methods

def radian_left(sim, ang, dis, step, n):
    for i in range(n):
        dis += step
        sim.lt(ang)
        sim.forward(dis)

def radian_right(sim, ang, dis, step, n):
    for i in range(n):
        dis += step
        sim.rt(ang)
        sim.forward(dis)

def InitEars(sim):
    sim.color_set(COLORS['black'], COLORS['yellow'])
    sim.pu(); sim.goto(-50, 100); sim.pd(); sim.setheading(110)
    sim.begin_fill(); sim.fillcolor_set(COLORS['yellow'])
    radian_left(sim,1.2,0.4,0.1,40)
    sim.setheading(270); radian_left(sim,1.2,0.4,0.1,40)
    sim.setheading(44); sim.forward(32)
    sim.end_fill()

    sim.pu(); sim.goto(50,100); sim.pd(); sim.setheading(70)
    sim.begin_fill(); sim.fillcolor_set(COLORS['yellow'])
    radian_right(sim,1.2,0.4,0.1,40)
    sim.setheading(270); radian_right(sim,1.2,0.4,0.1,40)
    sim.setheading(136); sim.forward(32)
    sim.end_fill()

    # black tips simplified
    sim.begin_fill(); sim.fillcolor_set(COLORS['black'])
    sim.pu(); sim.goto(88,141); sim.pd(); sim.setheading(35)
    radian_right(sim,1.2,1.6,0.1,16)
    sim.setheading(270); radian_right(sim,1.2,0.4,0.1,25)
    sim.setheading(132); sim.forward(31)
    sim.end_fill()

    sim.begin_fill(); sim.fillcolor_set(COLORS['black'])
    sim.pu(); sim.goto(-88,141); sim.pd(); sim.setheading(145)
    radian_left(sim,1.2,1.6,0.1,16)
    sim.setheading(270); radian_left(sim,1.2,0.4,0.1,25)
    sim.setheading(48); sim.forward(31)
    sim.end_fill()

def InitTail(sim):
    sim.begin_fill(); sim.fillcolor_set(COLORS['yellow'])
    sim.pu(); sim.goto(64,-140); sim.pd()
    sim.setheading(10); sim.forward(20)
    sim.setheading(90); sim.forward(20)
    sim.setheading(10); sim.forward(10)
    sim.setheading(80); sim.forward(100)
    sim.setheading(35); sim.forward(80)
    sim.setheading(260); sim.forward(100)
    sim.setheading(205); sim.forward(40)
    sim.setheading(260); sim.forward(37)
    sim.setheading(205); sim.forward(20)
    sim.setheading(260); sim.forward(25)
    sim.setheading(175); sim.forward(30)
    sim.setheading(100); sim.forward(13)
    sim.end_fill()

def InitFoots(sim):
    sim.begin_fill(); sim.fillcolor_set(COLORS['yellow'])
    sim.pensize = 2
    sim.pu(); sim.goto(-70,-200); sim.pd(); sim.setheading(225)
    radian_left(sim,0.5,1.2,0,12)
    radian_left(sim,35,0.6,0,4)
    radian_left(sim,1,1.2,0,18)
    sim.setheading(160); sim.forward(13)
    sim.end_fill()

    sim.begin_fill(); sim.fillcolor_set(COLORS['yellow'])
    sim.pensize = 2
    sim.pu(); sim.goto(70,-200); sim.pd(); sim.setheading(315)
    radian_right(sim,0.5,1.2,0,12)
    radian_right(sim,35,0.6,0,4)
    radian_right(sim,1,1.2,0,18)
    sim.setheading(20); sim.forward(13)
    sim.end_fill()

def InitBody(sim):
    sim.begin_fill(); sim.fillcolor_set(COLORS['yellow'])
    sim.pu(); sim.goto(112,0); sim.pd(); sim.setheading(90)
    sim.circle(112,180)
    sim.setheading(250); radian_left(sim,1.6,1.3,0,50)
    radian_left(sim,0.8,1.5,0,25)
    sim.setheading(255); radian_left(sim,0.4,1.6,0.2,27)
    radian_left(sim,2.8,1,0,45)
    radian_right(sim,0.9,1.4,0,31)
    sim.setheading(355); radian_right(sim,0.9,1.4,0,31)
    radian_left(sim,2.8,1,0,45)
    radian_left(sim,0.4,7.2,-0.2,27)
    sim.setheading(10); radian_left(sim,0.8,1.5,0,25)
    radian_left(sim,1.6,1.3,0,50)
    sim.end_fill()

def InitEyes(sim):
    # left
    sim.begin_fill(); sim.fillcolor_set(COLORS['black'])
    sim.pu(); sim.goto(-46,10); sim.pd(); sim.setheading(90); sim.circle(5,360)
    sim.end_fill()
    sim.begin_fill(); sim.fillcolor_set(COLORS['black'])
    sim.pu(); sim.goto(46,10); sim.pd(); sim.setheading(-90); sim.circle(5,360)
    sim.end_fill()

def InitFace(sim):
    sim.begin_fill(); sim.fillcolor_set(COLORS['red'])
    sim.pu(); sim.goto(-63,-10); sim.pd(); sim.setheading(90); sim.circle(10,360)
    sim.end_fill()
    sim.begin_fill(); sim.fillcolor_set(COLORS['red'])
    sim.pu(); sim.goto(63,-10); sim.pd(); sim.setheading(-90); sim.circle(10,360)
    sim.end_fill()
    sim.pensize = 2.2
    sim.pu(); sim.goto(0,0); sim.pd(); sim.setheading(235)
    radian_right(sim,5,0.8,0,30)
    sim.pu(); sim.goto(0,0); sim.pd(); sim.setheading(305)
    radian_left(sim,5,0.8,0,30)

def InitHands(sim):
    sim.pensize = 2
    sim.pu(); sim.goto(-46,-100); sim.pd(); sim.setheading(285)
    radian_right(sim,0.4,1.2,0,26)
    radian_right(sim,5,0.35,0,26)
    radian_right(sim,0.3,1.2,0,15)
    sim.pu(); sim.goto(46,-100); sim.pd(); sim.setheading(255)
    radian_left(sim,0.4,1.2,0,26)
    radian_left(sim,5,0.35,0,26)
    radian_left(sim,0.3,1.2,0,15)

def Init(sim):
    InitEars(sim)
    InitTail(sim)
    InitFoots(sim)
    InitBody(sim)
    InitFace(sim)
    InitHands(sim)
    InitEyes(sim)

def render_to_png(path='皮卡丘_render.png'):
    img = Image.new('RGB', (IMG_W, IMG_H), (255,255,255))
    draw = ImageDraw.Draw(img)
    sim = TurtleSim(draw)
    sim.color = COLORS['black']
    sim.pensize = 2
    Init(sim)
    img.save(path)
    print(path)

if __name__ == '__main__':
    # optional output filename third arg
    out = None
    if len(sys.argv) >= 4:
        out = sys.argv[3]
    else:
        out = f"皮卡丘_render_{IMG_W}x{IMG_H}.png"
    render_to_png(out)
