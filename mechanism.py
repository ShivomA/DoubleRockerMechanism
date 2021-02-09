import math
import numpy as np
from matplotlib import pyplot as plt

# region Taking Input
l1, l2, l3, l4 = 0, 0, 0, 0
theta2Max, theta2Min, dTheta = 0, 0, 0
validInput = False
while not validInput:
    l1, l2, l3, l4 = list(map(int, input("Enter space separated link lengths: ").split()))
    lengths = [l1, l2, l3, l4]
    dTheta = float(input("Enter \u03C9: "))
    if dTheta <= 0:
        print("Invalid \u03C9")
        continue
    
    possibleQuad = [2 * le < sum(lengths) for le in lengths]
    for le in lengths:
        if le <= 0:
            possibleQuad.append(False)
    
    if False in possibleQuad:
        print("Impossible links configurations")
    elif 2 * min(lengths) + 2 * max(lengths) == sum(lengths):
        print("Given lengths forms Singular configuration not Double Rocker Configuration")
    elif 2 * min(lengths) + 2 * max(lengths) < sum(lengths):
        if l3 != min(lengths):
            print("It is not Double Rocker Configuration")
        else:
            theta2Min = math.acos((l1 ** 2 + l2 ** 2 - (l4 - l3) ** 2) / (2 * l1 * l2))
            theta2Max = math.acos((l1 ** 2 + l2 ** 2 - (l4 + l3) ** 2) / (2 * l1 * l2))
            validInput = True
    else:
        if l1 == max(lengths):
            theta = math.acos((l1 ** 2 + l2 ** 2 - (l3 + l4) ** 2) / (2 * l1 * l2))
            theta2Min = -theta
            theta2Max = theta
        elif l2 == max(lengths):
            theta = math.acos((l1 ** 2 + l2 ** 2 - (l3 + l4) ** 2) / (2 * l1 * l2))
            theta2Min = -theta
            theta2Max = theta
        elif l3 == max(lengths):
            theta = math.acos((l1 ** 2 + l2 ** 2 - (l3 - l4) ** 2) / (2 * l1 * l2))
            theta2Min = theta
            theta2Max = 2 * math.pi - theta
        else:
            theta = math.acos((l1 ** 2 + l2 ** 2 - (l4 - l3) ** 2) / (2 * l1 * l2))
            theta2Min = theta
            theta2Max = 2 * math.pi - theta
        validInput = True
# endregion

# region Data Initialisation
# n is to input complete rotation or half rotation
n = 1
noOfPoints = 100
timePerFrame = ((theta2Max - theta2Min) / dTheta) / noOfPoints
timeSpace = np.linspace(0, 2 * n * math.pi / dTheta, noOfPoints)

theta2v = [(theta2Max + theta2Min) / 2 + (theta2Max - theta2Min) * math.cos(t * dTheta) / 2 for t in timeSpace]
dTheta2v = [-1 * dTheta * (theta2Max - theta2Min) * math.sin(t * dTheta) / 2 for t in timeSpace]
aTheta2v = [-1 * (dTheta ** 2) * (theta2Max - theta2Min) * math.cos(t * dTheta) / 2 for t in timeSpace]

theta3_1v = np.zeros((noOfPoints, 1))
theta3_2v = np.zeros((noOfPoints, 1))
dTheta3_1v = np.zeros((noOfPoints, 1))
dTheta3_2v = np.zeros((noOfPoints, 1))
aTheta3_1v = np.zeros((noOfPoints, 1))
aTheta3_2v = np.zeros((noOfPoints, 1))

theta4_1v = np.zeros((noOfPoints, 1))
theta4_2v = np.zeros((noOfPoints, 1))
dTheta4_1v = np.zeros((noOfPoints, 1))
dTheta4_2v = np.zeros((noOfPoints, 1))
aTheta4_1v = np.zeros((noOfPoints, 1))
aTheta4_2v = np.zeros((noOfPoints, 1))

coordinates_1 = [0 for i in range(noOfPoints)]
coordinates_2 = [0 for i in range(noOfPoints)]
# endregion

# region Calculations
for nTheta2 in range(len(theta2v)):
    theta2 = theta2v[nTheta2]
    dTheta2 = dTheta2v[nTheta2]
    aTheta2 = aTheta2v[nTheta2]

    a = math.sin(theta2)
    b = math.cos(theta2) - l1 / l2
    c = -l1 / l4 * math.cos(theta2) + (l1 ** 2 + l2 ** 2 + l4 ** 2 - l3 ** 2) / (2 * l2 * l4)

    try:
        theta4_1 = 2 * math.atan((a + (a ** 2 + b ** 2 - c ** 2) ** 0.5) / (b + c))
        theta4_2 = 2 * math.atan((a - (a ** 2 + b ** 2 - c ** 2) ** 0.5) / (b + c))
    except:
        theta4_1 = 2 * math.atan(a / (b + c))
        theta4_2 = 2 * math.atan(a / (b + c))

    theta3_1 = math.atan2(l2 * math.sin(theta2) - l4 * math.sin(theta4_1),
                          l2 * math.cos(theta2) - l4 * math.cos(theta4_1) - l1)
    theta3_2 = math.atan2(l2 * math.sin(theta2) - l4 * math.sin(theta4_2),
                          l2 * math.cos(theta2) - l4 * math.cos(theta4_2) - l1)

    try:
        dTheta3_1 = l2 * math.sin(theta2 - theta4_1) * dTheta2 / (l3 * math.sin(theta3_1 - theta4_1))
        dTheta3_2 = l2 * math.sin(theta2 - theta4_2) * dTheta2 / (l3 * math.sin(theta3_2 - theta4_2))
    except:
        dTheta3_1 = dTheta3_1v[nTheta2]
        dTheta3_2 = dTheta3_2v[nTheta2]

    try:
        dTheta4_1 = l2 * math.sin(theta2 - theta3_1) * dTheta2 / (l4 * math.sin(theta4_1 - theta3_1))
        dTheta4_2 = l2 * math.sin(theta2 - theta3_2) * dTheta2 / (l4 * math.sin(theta4_2 - theta3_2))
    except:
        dTheta4_1 = dTheta4_1v[nTheta2]
        dTheta4_2 = dTheta4_2v[nTheta2]

    aTheta3_1 = ((l2 * (dTheta2 ** 2) * math.cos(theta2 - theta4_1)) +
                 (l2 * aTheta2 * math.sin(theta2 - theta4_1)) -
                 (l4 * (dTheta4_1 ** 2)) -
                 (l3 * (dTheta3_1 ** 2) * math.cos(theta3_1 - theta4_1))) / (l3 * math.sin(theta3_1 - theta4_1))
    aTheta3_2 = ((l2 * (dTheta2 ** 2) * math.cos(theta2 - theta4_2)) +
                 (l2 * aTheta2 * math.sin(theta2 - theta4_2)) -
                 (l4 * (dTheta4_2 ** 2)) -
                 (l3 * (dTheta3_2 ** 2) * math.cos(theta3_2 - theta4_2))) / (l3 * math.sin(theta3_2 - theta4_2))
    aTheta4_1 = ((l2 * (dTheta2 ** 2) * math.cos(theta2 - theta3_1)) +
                 (l2 * aTheta2 * math.sin(theta2 - theta3_1)) -
                 (l3 * (dTheta3_1 ** 2)) -
                 (l4 * (dTheta4_1 ** 2) * math.cos(theta4_1 - theta3_1))) / (l4 * math.sin(theta4_1 - theta3_1))
    aTheta4_2 = ((l2 * (dTheta2 ** 2) * math.cos(theta2 - theta3_2)) +
                 (l2 * aTheta2 * math.sin(theta2 - theta3_2)) -
                 (l3 * (dTheta3_2 ** 2)) -
                 (l4 * (dTheta4_2 ** 2) * math.cos(theta4_2 - theta3_2))) / (l4 * math.sin(theta4_2 - theta3_2))

    # region Update Data
    if nTheta2 < len(theta2v) / (2 * n):
        theta3_1v[nTheta2] = theta3_1
        theta3_2v[nTheta2] = theta3_2
        theta4_1v[nTheta2] = theta4_1
        theta4_2v[nTheta2] = theta4_2

        dTheta3_1v[nTheta2] = dTheta3_1
        dTheta3_2v[nTheta2] = dTheta3_2
        dTheta4_1v[nTheta2] = dTheta4_1
        dTheta4_2v[nTheta2] = dTheta4_2

        aTheta3_1v[nTheta2] = aTheta3_1
        aTheta3_2v[nTheta2] = aTheta3_2
        aTheta4_1v[nTheta2] = aTheta4_1
        aTheta4_2v[nTheta2] = aTheta4_2

    else:
        theta3_1v[nTheta2] = theta3_2
        theta3_2v[nTheta2] = theta3_1
        theta4_1v[nTheta2] = theta4_2
        theta4_2v[nTheta2] = theta4_1

        dTheta3_1v[nTheta2] = dTheta3_2
        dTheta3_2v[nTheta2] = dTheta3_1
        dTheta4_1v[nTheta2] = dTheta4_2
        dTheta4_2v[nTheta2] = dTheta4_1

        aTheta3_1v[nTheta2] = aTheta3_2
        aTheta3_2v[nTheta2] = aTheta3_1
        aTheta4_1v[nTheta2] = aTheta4_2
        aTheta4_2v[nTheta2] = aTheta4_1
    # endregion

    coordinates_1[nTheta2] = np.array(
        [[0, 0],
         [l2 * math.cos(theta2), l2 * math.sin(theta2)],
         [l1 + l4 * math.cos(theta4_1v[nTheta2]), l4 * math.sin(theta4_1v[nTheta2])],
         [l1, 0]]
    )

    coordinates_2[nTheta2] = np.array(
        [[0, 0],
         [l2 * math.cos(theta2), l2 * math.sin(theta2)],
         [l1 + l4 * math.cos(theta4_2v[nTheta2]), l4 * math.sin(theta4_2v[nTheta2])],
         [l1, 0]]
    )

# endregion

# region Graph Mechanism
color = ["-r", "-b"]
for nTheta2 in range(len(theta2v)):
    plt.plot(coordinates_1[nTheta2][0:2, 0], coordinates_1[nTheta2][0:2, 1], "-p", marker='o')
    plt.plot(coordinates_1[nTheta2][1:, 0], coordinates_1[nTheta2][1:, 1], color[0], marker='o')
    plt.plot(coordinates_2[nTheta2][1:, 0], coordinates_2[nTheta2][1:, 1], color[1], marker='o')
    plt.xlim(min(-(l2 + 1), -(l4 - l1 + 1)), max((l1 + l4 + 1), l2))
    plt.ylim(-(max(l2, l4) + 1), (max(l2, l4) + 1))
    plt.draw()
    plt.pause(timePerFrame)
    if nTheta2 != len(theta2v) - 1:
        plt.clf()
plt.show()
# endregion

# region Graph Omega_4 vs Time
plt.plot(timeSpace[1:-1], dTheta4_1v[1:-1], color[0])
plt.plot(timeSpace[1:-1], dTheta4_2v[1:-1], color[1])
plt.xlabel("time")      # time
plt.ylabel("\u03C9_4")  # Omega_4
plt.grid()
plt.show()
# endregion

# region Graph Alpha_4 vs Time
plt.plot(timeSpace[1:-1], aTheta4_1v[1:-1], color[0])
plt.plot(timeSpace[1:-1], aTheta4_2v[1:-1], color[1])
plt.xlabel("time")     # time
plt.ylabel("\u03B1_4")  # Alpha_4
plt.grid()
plt.show()
# endregion
