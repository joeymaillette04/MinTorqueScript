import math
import matplotlib.axes as ax
import matplotlib.pyplot as plt 

import numpy as np
import scipy.optimize._minimize
from scipy.optimize import Bounds
from scipy.optimize import NonlinearConstraint
from scipy.optimize import LinearConstraint
from shapely.geometry import LineString


global positionPoints, errorConst

positionPoints = [ [ [0, 0, 0, 0.75], [0, 0, 0, 0.1] ], [ [0, 0, 0, 0.5], [0, 0, 0, 0.5] ], [ [0, 0, 0, 0.2], [0, 0, 0, 0.6] ] ]
errorConst = 99999

def ccw(A,B,C):
    return (C.y-A.y) * (B.x-A.x) > (B.y-A.y) * (C.x-A.x)

# Return true if line segments AB and CD intersect
def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)


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


def calcMidPt( x1, x2 ): #calculates the midpoint of an arm given the x positions at both ends
    midX = ( x2 + x1 )/2
    return midX

def mass( p, l ): #calculates mass of each arm based on length and its density
    return p * l

def force( aMass ): #calculates force using mass and gravity constant (9.81N/kG)
    return aMass * 9.81

def calculateTorque2( armLengths ):
    gripperForce = 5 * 9.81
    gripperAngles = [ -math.pi/3.0 , 0, math.pi/4.0 ]
    torques = [ 0, 0, 0 ]
    intersections = []

    for i in range( 3 ): #iterates once for each position the arm must reach
        positionPoints[ i ][ 0 ][ 2 ] = positionPoints[ i ][ 0 ][3] - (armLengths[ 2 ] * abs(math.cos(gripperAngles[ i ])))
        positionPoints[ i ][ 1 ][ 2 ] = positionPoints[ i ][ 1 ][3] - (armLengths[ 2 ] * math.sin(gripperAngles[ i ]))

        midPts = [ [ ], [ ], [ ] ]
        positionPoints[i][0][1], positionPoints[i][1][1], x2, y2 = get_intersections(0, 0, armLengths[ 0 ], positionPoints[ i ][ 0 ][ 2 ], positionPoints[ i ][ 1 ][ 2 ], armLengths[ 1 ])
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
        midPts[ 0 ] = calcMidPt( 0, positionPoints[i][0][1] )
        midPts[ 1 ] = calcMidPt( positionPoints[i][0][1], positionPoints[i][0][2] )
        midPts[ 2 ] = calcMidPt( positionPoints[i][0][2], positionPoints[i][0][3] )

        #compare the torque of the 2 possible points the circles intersect. 2 possible positions for point A.
        torque1 = gravForces[ 0 ] * calcMidPt( 0, positionPoints[i][0][1] ) + gravForces[ 1 ] * calcMidPt( positionPoints[i][0][1], positionPoints[i][0][2] )
        torque2 = gravForces[ 0 ] * calcMidPt( 0, x2 ) + gravForces[ 1 ] * calcMidPt( x2, positionPoints[i][0][2] )

        #use the position which required the least torque for equilibirum
        if ( ( ( torque2 < torque1) and ( y2 > 0)) or ( positionPoints[i][1][1] < 0 ) ):            
            positionPoints[i][0][1] = x2
            positionPoints[i][1][1] = y2
            midPts[0] = calcMidPt( 0, x2 )
            midPts[1] = calcMidPt( x2, positionPoints[i][0][2] )

        #creates two line segments and checks if they intersect (only checks first and third lengths)
        Segment1 = LineString([(0,0), (positionPoints[i][0][1], positionPoints[i][1][1])])
        Segment2 = LineString([(positionPoints[i][0][2], positionPoints[i][1][2]), (positionPoints[i][0][3], positionPoints[i][1][3])])

        #array of true or falses for intersection
        intersections.append(Segment1.intersects(Segment2))

        for j in range( 0, 3): #Add all the torque required for the three arms
            torques[ i ] += ( gravForces[ j ] * midPts[ j ] ) 

        torques[ i ] += ( gripperForce * positionPoints[ i ][0][3] ) #add the torque of the 5kg mass the arm holds

    #calculate the total torque of all 3 positions combined
    finalTorque = math.sqrt( torques[ 0 ]**2 + torques[ 1 ]**2 + torques[ 2 ]**2 ) 

    #print the torques and points for all positions
    print( "Position 1 torque", torques[0] )
    print( "Position 2 torque", torques[1] )
    print( "Position 3 torque", torques[2] )
    print("")
    print(armLengths)
    print()
    for i in range(len(positionPoints)):
        print("Position " + str(i+1) + ":")
        print("Origin: (" + str(positionPoints[i][0][0]) + "," + str(positionPoints[i][1][0])+ ")")
        print("A: (" + str(positionPoints[i][0][1]) + "," + str(positionPoints[i][1][1])+ ")")
        print("B: (" + str(positionPoints[i][0][2]) + "," + str(positionPoints[i][1][2])+ ")")
        print("C: (" + str(positionPoints[i][0][3]) + "," + str(positionPoints[i][1][3])+ ")")
        print("\n")
        print("Final Torque:" + str(finalTorque))
        print()

    #if in any of the positions have intersecting lines output a high error torque
    for i in range(3):
        if(intersections[i] == True):
            finalTorque = errorConst

    return finalTorque

# best lengths tested (to plot) 
testLengths = [1.0821468359052653, 1.0641662437491748, 0.6427511332656937]
fTorque = calculateTorque2(testLengths)
print("Final combined torque", fTorque)

#Linear constraints and bounds 
cnstrnts = LinearConstraint( [ [ 1, 1, 1 ], [ -1, 1, 0 ], [ 0, 0, 1] ], [ 1, -0.3, 0 ], [ np.Inf, 0.3, 0.35 ], keep_feasible=True )
bnds = Bounds( [ 0, 0, 0 ], [ 10,10,10 ], keep_feasible=True)

#results = scipy.optimize.minimize(calculateTorque2, testLengths, method="trust-constr", bounds=bnds, constraints=cnstrnts, options={"maxiter" : 10000})
#print(results)

#set plot limits and apply a grid
plt.xlim = 0.9 
plt.ylim = 0.9
plt.grid()

#round points to make graph less crowded when plotting
for i in range(len(positionPoints)):
    for j in range(3):
        x = round(positionPoints[i][0][j+1],2)
        y = round(positionPoints[i][1][j+1],2)
        plt.text(positionPoints[i][0][j+1], positionPoints[i][1][j+1], "("+str(x)+","+str(y)+")")

#plot points, ensure axes are equal and make the legend visible
plt.plot( positionPoints[0][0], positionPoints[0][1], label = "Pos 1")
plt.plot( positionPoints[1][0], positionPoints[1][1], label = "Pos 2")
plt.plot( positionPoints[2][0], positionPoints[2][1], label = "Pos 3")
plt.axis('equal')
plt.legend()
plt.show() 