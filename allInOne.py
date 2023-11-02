import sys
import glob

import cv2
import pygame


SIZE = (3840, 2160)

XRANGE = (-50, 50)
YRANGE = (-1, 55.25)

SIGMA = 10
RHO = 28
BETA = 8 / 3

DT = 1 / 500

LENGTHINFRAMES = 2000


class Particle:
    def __init__(self, pos=(0, 0, 0), col=(255, 255, 255)):
        self.pos = list(pos)
        self.col = col
        self.lastPos = pos

    def update(self):

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

            pygame.draw.circle(screen, self.col, (xPos, yPos), 20)

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

    pList = [Particle(pos=(10, 0, 1), col=(0, 255, 255))]

    for iteration in range(LENGTHINFRAMES):

        canvas = pygame.surface.Surface(SIZE)

        for p in pList:
            p.draw(canvas)
            p.update()

        pygame.image.save(canvas, 'img/' + str(iteration) + '.png')

        if iteration % 100 == 0:
            print('Frame', iteration, 'generated')

        print(iteration)

    videoGen()


def videoGen():
    filenames = glob.glob('img/*.png')

    out = cv2.VideoWriter(
        'vid/vid.mp4',
        cv2.VideoWriter_fourcc(*'mp4v'),
        60,
        SIZE
    )

    for x in range(len(filenames)):
        img = cv2.imread('img/' + str(x) + '.png')
        out.write(img)
        print(x)

    out.release()


if __name__ == '__main__':
    main()
