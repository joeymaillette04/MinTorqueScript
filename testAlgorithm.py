import scipy.optimize._minimize
import matplotlib.pyplot as plt 
import numpy as np
from script import *

def runTests(approxHours):
    num_trials = int(1014084*approxHours)

    resultsLen = []
    resultsTorque = []

    for i in range(num_trials):
        l1 = np.random.uniform(low=1.0, high=10.0, size=None)
        l2 = np.random.uniform(low=1.0, high=10.0, size=None)
        l3 = np.random.uniform(low=1.0, high=10.0, size=None)
        testLengths = [l1, l2, l3]
        results = scipy.optimize.minimize(calculateTorque2, testLengths, method="Nelder-Mead")
        resultsLen.append(results.x)
        resultsTorque.append(results.fun)

    minTorqueIndex = 0


    for i in range(num_trials):
        if (resultsTorque[i] < resultsTorque[minTorqueIndex]):
            minTorqueIndex = i

    print(resultsLen[minTorqueIndex])
    print(resultsTorque[minTorqueIndex])

runTests(1/60/30)

