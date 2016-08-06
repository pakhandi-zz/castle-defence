'''
    This function returns:
    1> angle :  The angle between y-axis and the orientation
    2> x     :  The x value for this angle (if propagated one unit)
    3> y     :  The y value for this angle (if propogated one unit)
'''
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
