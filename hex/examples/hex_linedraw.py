#!/usr/bin/env python3
import sys
import os
sys.path.append(os.curdir)
sys.path.append(os.pardir)
sys.path.append(os.pardir + os.sep + os.pardir)

if True:  # satisfy auto-formatter
    from hex import Hex, Layout, Point
    import pygame
    import math

try:
    from better_exceptions import behook
    sys.excepthook = behook
except ImportError:
    pass

pygame.init()

layout = Layout(Layout.pointy, Point(5, 5), Point(0, 0))

bounds = [math.inf, math.inf, -math.inf, -math.inf]

win = pygame.display.set_mode((1000, 1000))

start = round(layout.to_hex(Point(win.get_width()//4,
                                  win.get_height()//4)))

end = round(layout.to_hex(Point(win.get_width()//1.3,
                                win.get_height()//1.3)))

line = Hex.linedraw(start, end)


FONT = pygame.font.SysFont(None, 20)

dirty = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN):
            mousehex = round(layout.to_hex(Point(*event.pos)))
            lb, mb, rb = pygame.mouse.get_pressed()
            if lb:
                start = mousehex
                dirty = True
            if mb:
                pass
            if rb:
                end = mousehex
                dirty = True
    if dirty:
        dirty = False
        line = Hex.linedraw(start, end)

        win.fill((0, 0, 0))

        for h in line + [start, end]:
            if h == start:
                color = (255, 0, 0)
            elif h == end:
                color = (0, 255, 255)
            elif h in line:
                color = (150, 0, 255)
            else:
                color = (150, 150, 150)
            pygame.draw.polygon(win, [i//2 for i in color],
                                layout.hex_corners(h, 1))
            pygame.draw.polygon(win, color,
                                layout.hex_corners(h, 0.75))
        # pygame.draw.aaline(win, (255, 255, 255),
        #                    layout.from_hex(start), layout.from_hex(end))

        pygame.display.flip()
