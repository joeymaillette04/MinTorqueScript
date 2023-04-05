import scipy.optimize._minimize
import matplotlib.pyplot as plt 
import numpy as np
from script import *
global trials, iterations, tweak

# trials*iterations is the total number of times the "good" values are refined
trials = 100000
iterations = 30
tweak = 0.02

def runTests(numIterations, lone, ltwo, lthree, count, passedTorque):

    #arrays keeping track of lengths, torque, and the y-values associated with the lengths in the 3 positions
    resultsLen = []
    resultsTorque = []

    #position 1 y-values (joints 1 and 2)
    resultsYVal1 = []
    resultsYVal2 = []

    #position 2 y-values (joints 1 and 2)
    resultsYVal3 = []
    resultsYVal4 = []

    #position 3 y-values (joints 1 and 2)
    resultsYVal5 = []
    resultsYVal6 = []

    for i in range(numIterations):
        #uniformly selects random values to increment or decrement each respective size
        l1 = np.random.uniform(low=-tweak, high=tweak, size=None)
        l2 = np.random.uniform(low=-tweak, high=tweak, size=None)
        l3 = np.random.uniform(low=-tweak, high=tweak, size=None)

        testLengths = [l1+lone, l2+ltwo, l3+lthree]
        resultsLen.append(testLengths)
        
        # try and catch to handle bugs sourced from script.py
        try:
            resultsTorque.append(calculateTorque2(testLengths))
        except:
            resultsTorque.append(10000)

        resultsYVal1.append(positionPoints[0][1][1])
        resultsYVal2.append(positionPoints[0][1][2])
        resultsYVal3.append(positionPoints[1][1][1])
        resultsYVal4.append(positionPoints[1][1][2])
        resultsYVal5.append(positionPoints[2][1][1])
        resultsYVal6.append(positionPoints[2][1][2])


    minTorqueIndex = 0
    # searches through array of torques and finds the lowest "legal" torque value and its properties (length's)
    for i in range(numIterations):
        if (resultsYVal1[i] >= 0 and resultsYVal2[i] >= 0 and resultsYVal3[i] >= 0 and resultsYVal4[i] >= 0 and resultsYVal5[i] >= 0 and resultsYVal6[i] >= 0):
            if (resultsTorque[i] < resultsTorque[minTorqueIndex]):
                minTorqueIndex = i
        else:
            resultsTorque[i] = 10000
        
    # output best lengths and torque for this iteration
    print(resultsLen[minTorqueIndex])
    print(resultsTorque[minTorqueIndex])

    # if a torque that is better is found, use the new lengths for the next iteration
    if (count<iterations and resultsTorque[minTorqueIndex] < passedTorque):
        runMoreTests(resultsLen[minTorqueIndex], count, resultsTorque[minTorqueIndex])
    # if not use the previous lengths
    elif (count<iterations and resultsTorque[minTorqueIndex] > passedTorque):
        runMoreTests(resultsLen[minTorqueIndex], count, passedTorque)

# helper function just to count iterations
def runMoreTests(newLengths, count, passedTorque):
    count += 1
    runTests(trials,newLengths[0],newLengths[1],newLengths[2], count, passedTorque)

# function call (input the three middle values)
runTests(trials,0.9684249594628851, 0.6007888013968402 , 0.8038981272930561, 0, 50 )

