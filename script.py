import scipy.optimize._minimize
import math
import matplotlib.pyplot as plt 
import numpy as np
from scipy.optimize import NonlinearConstraint


def get_intersections(x0, y0, r0, x1, y1, r1):
    # circle 1: (x0, y0), radius r0
    # circle 2: (x1, y1), radius r1

    d=math.sqrt((x1-x0)**2 + (y1-y0)**2)
    
    # non intersecting
    if d > r0 + r1 :
        return None
    # One circle within other
    if d < abs(r0-r1):
        return None
    # coincident circles
    if d == 0 and r0 == r1:
        return None
    else:
        a=(r0**2-r1**2+d**2)/(2*d)
        h=math.sqrt(r0**2-a**2)
        x2=x0+a*(x1-x0)/d   
        y2=y0+a*(y1-y0)/d   
        x3=x2+h*(y1-y0)/d     
        y3=y2-h*(x1-x0)/d 

        x4=x2-h*(y1-y0)/d
        y4=y2+h*(x1-x0)/d

        return (x3, y3, x4, y4)


def calcMidPt( x1, x2 ):
    midX = ( x2 + x1 )/2
    return midX

def mass( p, l ): #calculates mass of each arm based on length and its density
    return p * l

def force( aMass ): #calculates force using mass and gravity constant (9.81N/kG)
    return aMass * 9.81


def calculateTorque2( armLengths ):
    gripperPts= [ [ 0.75, 0.1 ], [ 0.5, 0.5 ], [ 0.2, 0.6 ] ]
    gripperForce = 5 * 9.81
    gripperAngles = [ -math.pi/3.0 + math.pi, 0, math.pi/4 ]
    torques = [ 0, 0, 0 ]

    for i in range( 3 ):
        bx = gripperPts[ i ][ 0 ] - ( armLengths[ 2 ] * math.cos(gripperAngles[ i ] ) )
        by = gripperPts[ i ][ 1 ] - ( armLengths[ 2 ] * math.sin(gripperAngles[ i ] ) )

        midPts = [ [ ], [ ], [ ] ]
        x1, y1, x2, y2 = get_intersections(0, 0, armLengths[ 0 ], bx, by, armLengths[ 1 ])
        armMasses = [ 0, 0, 0]

        a = 4
        for l in range( 3 ):
            armMasses[ l ] = mass( a, armLengths[ l ] )
            a /= 2

        #calculate the gravity forces of each member
        gravForces = [ 0, 0, 0 ]
        for k in range( 3 ):
            gravForces[ k ] = force( armMasses[ k ])

        #calculate the midpoints of each member, this is where the gravity force acts.
        midPts[ 0 ] = calcMidPt( 0, x1 )
        midPts[ 1 ] = calcMidPt( x1, bx )
        midPts[ 2 ] = calcMidPt( bx, gripperPts[ i ][0] )

        torque1 = gravForces[ 0 ] * calcMidPt( 0, x1 ) + gravForces[ 1 ] * calcMidPt( x1, bx )
        torque2 = gravForces[ 0 ] * calcMidPt( 0, x2 ) + gravForces[ 1 ] * calcMidPt( x2, bx )

        if (torque2 < torque1):
            midPts[0] = calcMidPt( 0, x2 )
            midPts[1] = calcMidPt( x2, bx )


        for j in range( 0, 3): #Add all the torque required for the three arms
            torques[ i ] += ( gravForces[ j ] * midPts[ j ] ) 

        torques[ i ] += ( gripperForce * gripperPts[ i ][0] ) 

    finalTorque = math.sqrt( torques[ 0 ]**2 + torques[ 1 ]**2 + torques[ 2 ]**2 )
    print( torques[0] )    
    return finalTorque
    


testLengths = [ 0.5, 0.6, 0.3 ]
test = calculateTorque2(testLengths)

print(test)

def lengthConstr( inputLens ):
    return inputLens[0] + inputLens[1] + inputLens[2]



# constrMax = NonlinearConstraint(lengthConstr, 1, np.Inf, keep_feasible=True)
# results = scipy.optimize.minimize( calculateTorque2, testLengths, method="Nelder-Mead" ) #, constraints=( constrMax ) )
