def getDirection(orientation):
    deg = orientation
    x = +1
    y = -1

    if 90 < orientation <= 180:
        deg = 180 - orientation
        x = -1
        y = -1
    elif 180 < orientation <= 270:
        deg = orientation - 180
        x = -1
        y = +1
    elif 270 < orientation <= 360:
        deg = 360 - orientation
        x = +1
        y = +1

    return deg, x, y
