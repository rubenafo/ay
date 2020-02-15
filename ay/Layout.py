import math
import random

def grid(xrows, yrows, width, height):
    points = []
    xspan = width / xrows
    yspan = height / yrows
    for ypoints in range(1, yrows):
        for xpoints in range(1, xrows):
            points.append({"x": xpoints * xspan, "y": ypoints * yspan})
    return points

def butterflyCurve(origin, scale, loops, lamb):
    points = []
    stepSize = 0.025
    upperLimit = loops * math.pi
    t = 0.0
    while t <= upperLimit:
        e = (math.exp(math.cos(t)) - 2 * math.cos(lamb * t) - math.pow(math.sin(t / 12), 5))
        x = math.sin(t) * e
        y = math.cos(t) * e
        t += stepSize
        points.append((x * scale + origin[0], y * scale + origin[1]))
    return points

def spiral(center, radius, coils, chord, maxpoints, f=None):
    points = []
    rotation = 2 * math.pi
    thetaMax = coils * 2 * math.pi
    awayStep = radius / thetaMax
    x, y = center
    theta = chord / awayStep
    for i in range(0, maxpoints):
        if theta > thetaMax:
            break
        away = awayStep * theta
        around = theta + rotation
        px = x + math.cos(around) * away
        py = y + math.sin(around) * away
        theta += chord / away
        points.append((px, py))
    if f is not None:
        f()
    return points


def ruleOfThirds(start, width, height):
    rulePoints = []
    thirdWidth = width / 3
    thirdHeight = height / 3
    x, y = start
    rulePoints.append(thirdWidth + x, thirdHeight + y)
    rulePoints.append(thirdWidth * 2 + x, thirdHeight + y)
    rulePoints.append(thirdWidth * 2 + x, thirdHeight * 2 + y)
    rulePoints.append(thirdWidth + x, thirdHeight * 2 + y)
    return rulePoints

def cols(origin, interCol, width):
    points = []
    for i in range(origin[0], width, interCol):
        points.append((i, origin[1]))
    return points

def rows(origin, interRow, height):
    points = []
    for i in range(origin[1], height, interRow):
        points.append((origin[0], i))
    return points

def hypo(origin, scale, loops, k):
    result = []
    stepSize = 0.025
    upperLimit = loops * math.PI
    steps = math.round(upperLimit / stepSize)
    for i in range(0,steps):
        x = scale * math.cos(k * i * stepSize) * math.cos(i * stepSize) + origin.x
        y = scale * math.cos(k * i * stepSize) * math.sin(i * stepSize) + origin.y
        result.append((x,y))
    return result

def flightWalker(mu, lowerLimit, upperLimit):
    x = random.Random().uniform(-math.PI/2, math.PI/2)
    y = -math.log(random.Random().random())
    alpha = mu - 1.0
    z =  (math.sin(alpha * x) / math.pow( math.cos(x) , 1.0 / alpha )) * math.pow(math.cos((1.0-alpha) * x) / y, (1.0 - alpha) / alpha)
    if z < -lowerLimit:
        return -lowerLimit
    if z > upperLimit:
        return upperLimit
    return z
