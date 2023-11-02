import glob

import cv2

SIZE = (1000, 1000)  # Update before each video generation


def main():
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

    out.release()


if __name__ == '__main__':
    main()
