# coding:utf-8
"""
Render 皮卡丘 drawing to PNG.
Usage: python3 scripts/render_pikachu.py
"""
from PIL import Image
import turtle as t
import 皮卡丘 as pikachu
import os
import sys

def render(output='皮卡丘.png'):
    # Create a screen and draw once (no animation)
    screen = t.Screen()
    screen.setup(800, 600)
    t.hideturtle()

    # Draw the static image
    pikachu.Init()
    screen.update()

    # Export canvas to postscript
    ps = '皮卡丘.ps'
    canvas = screen.getcanvas()
    canvas.postscript(file=ps, colormode='color')

    # Convert to PNG using Pillow
    try:
        img = Image.open(ps)
        img.save(output, 'png')
    except Exception as e:
        print('Error converting ps to png:', e, file=sys.stderr)
        raise
    finally:
        if os.path.exists(ps):
            try:
                os.remove(ps)
            except Exception:
                pass
        try:
            screen.bye()
        except Exception:
            pass

    print(output)

if __name__ == '__main__':
    render()
