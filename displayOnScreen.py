import sys

import pygame


SIZE = (1000, 1000)

XRANGE = (-30, 30)
YRANGE = (-1, 59)

SIGMA = 10
RHO = 28
BETA = 8 / 3

DT = 1 / 500

LENGTHINFRAMES = 5000


class Particle:
    def __init__(self, pos=(0, 0, 0), col=(255, 255, 255)):
        self.pos = list(pos)
        self.col = col
        self.lastPos = pos

    def update(self):
        """

        All content will be generated at 60fps.

        """
        self.lastPos = [self.pos[0], self.pos[1], self.pos[2]]

        vel = (SIGMA * (self.pos[1] - self.pos[0]),
               self.pos[0] * (RHO - self.pos[2]) - self.pos[1],
               self.pos[0] * self.pos[1] - BETA * self.pos[2])

        self.pos[0] += vel[0] * DT
        self.pos[1] += vel[1] * DT
        self.pos[2] += vel[2] * DT

    def draw(self, screen, line=False):
        if not line:
            proportionAcrossX = (self.pos[0] - XRANGE[0]) / (XRANGE[1] - XRANGE[0])
            proportionAcrossY = 1 - (self.pos[2] - YRANGE[0]) / (YRANGE[1] - YRANGE[0])  # (0, 2) -> xz plane

            xPos = SIZE[0] * proportionAcrossX
            yPos = SIZE[1] * proportionAcrossY

            pygame.draw.circle(screen, self.col, (xPos, yPos), 5)

        else:
            proportionAcrossX = (self.pos[0] - XRANGE[0]) / (XRANGE[1] - XRANGE[0])
            proportionAcrossY = 1 - (self.pos[2] - YRANGE[0]) / (YRANGE[1] - YRANGE[0])  # (0, 2) -> xz plane

            xPosCurrent = SIZE[0] * proportionAcrossX
            yPosCurrent = SIZE[1] * proportionAcrossY

            proportionAcrossX = (self.lastPos[0] - XRANGE[0]) / (XRANGE[1] - XRANGE[0])
            proportionAcrossY = 1 - (self.lastPos[2] - YRANGE[0]) / (YRANGE[1] - YRANGE[0])  # (0, 2) -> xz plane

            xPosLast = SIZE[0] * proportionAcrossX
            yPosLast = SIZE[1] * proportionAcrossY

            pygame.draw.line(screen, self.col, (xPosLast, yPosLast), (xPosCurrent, yPosCurrent), width=2)


def main():

    canvas = pygame.display.set_mode(SIZE)

    pList = [Particle(pos=(10, 0, 1), col=(0, 255, 255))]

    c = pygame.time.Clock()

    while True:
        c.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        canvas.fill((0, 0, 0))

        for p in pList:
            p.draw(canvas)
            p.update()

        pygame.display.flip()


if __name__ == '__main__':
    main()
