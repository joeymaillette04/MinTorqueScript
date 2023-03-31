import scipy.optimize._minimize
import math
import matplotlib.pyplot as plt 
import numpy as np


# def make_fig():
#     #
#     # Creating figure
#     fig = plt.figure(
#         figsize=(5, 4.2),
#         facecolor='#ffffff',
#         tight_layout=True)
#     # Adding and configuring axes
#     ax = fig.add_subplot(
#         facecolor='#ffffff',
#         )
#     ax.grid(
#     linestyle=':',
#     )
#     # Returning axes handle
#     return ax


# def lengths( points, x3, y3): #calculates the lengths of each of the 3 arms 
#     lengthArr = []
#     lengthArr.append( math.sqrt( ( points[0]**2 ) + (points[1]**2 ) ) )
#     lengthArr.append( math.sqrt( ( points[2]- points[0] ) **2 + ( points[3] - points[1] ) **2 ) )
#     lengthArr.append( math.sqrt( ( x3 - points[2] )**2 + ( y3 - points[3] )**2 ) )
#     return lengthArr

# def midpoints( positions, x3, y3 ): #calculates the x-y coords of the midpoint of each arm because that's where the force is applied
#     midpointArr = [ [], [], [] ]

#     midpointArr[0].append( positions[0]/2 ) 
#     midpointArr[0].append( positions[1]/2 )

#     midpointArr[1].append( ( positions[2]-positions[0] )/2 + positions[0] )
#     midpointArr[1].append( ( positions[3]-positions[1] )/2 + positions[1] )

#     midpointArr[2].append( ( x3 - positions[2] )/2 + positions[2] )
#     midpointArr[2].append( ( y3 - positions[3] )/2 + positions[3] )

#     return midpointArr




# def torqueCalculator( positions ):

#     posArray = [ 0, 0, 0 ]

#     x3 = 0.75
#     y3 = 0.1

#     posArray[0] = positions[0]
#     posArray[1] = positions[1]
#     posArray[2] = positions[2]

#     posArray.append( y3 - ( math.tan( -math.pi/3.0 ) * ( x3 - positions[2] ) ) )
    
#     lengthArr = lengths(posArray, x3, y3) #create new array and all lengths to it

#     masses = [] #add all masses to an array. density of the three arms are 4,2,1 hence the a /= 2
#     a = 4
#     for i in range( 0, 3):
#         masses.append( mass( a, lengthArr[i] ) )
#         a /= 2
    
#     forces=[] #using masses calculate the force applied at each of the midpoints
#     for i in range( 0, 3 ):
#         forces.append( force(masses[i]) )
#     forces.append( force( 5 ) )

#     midpointArr = midpoints( posArray, x3, y3 ) #populate array with x and y coords of midpoints

    

#     for i in range( 0, 3): #Add all the torque required for the three arms
#         torque += ( forces[i] * midpointArr[i][0] * math.sin( math.atan2( midpointArr[i][1], midpointArr[i][0] ) ) )

#     torque += forces[3] * x3 * math.sin( math.atan2( y3, x3 ) ) #need to add the torque from the 5kg mass at the end of the arm

#     totalLength = lengthArr[0] + lengthArr[1] + lengthArr[2]
#     print("Length below")
#     print( totalLength)
#     print( torque )
#     print( posArray )
#     return math.fabs(torque)


# x0 = [ -0.5, 0.5, 0.5 ]


# # print(res)

# # xPoints = [ 0, -0.5478141373939869, 0.45005787240316486, 0.75]
# # yPoints = [ 0, 0.5322259412463479, 0.6195150043280253, 0.1]

# # plt.scatter(xPoints, yPoints)
# # plt.plot(xPoints,yPoints)
# # plt.show()

# #moved the data plots outside the function so it does not plot after every iteration of optimixzation


# # make_fig()
# # xPoints = [ 0, posArray[0], posArray[2], x3 ]
# # yPoints = [ 0, posArray[1], posArray[3], y3 ]
# # # print(xPoints)
# # # print(yPoints)
# # plt.scatter(xPoints, yPoints)
# # plt.show()

# #function to calculate torques at different positions
# # gripperPts= [ [ 0.75, 0.1 ], [ 0.5, 0.5 ], [ 0.2, 0.6 ] ]
# # armAPts = [ [ ], [ ], [ ] ] #given once angles are known
# # atmBEPts = [ [ ], [ ], [ ] ] #given once angles are known
# # armAAngles = [ 0, 0, 0 ] #must solve for these values
# # armBAngles = [ 0, 0, 0 ] #must solve for these values
# # armLengths = [ 0, 0, 0 ] #given from the output of function above
# # gripperAngles = [ -math.pi/3.0, 0, math.pi/4 ]
# # torques = [ 0, 0, 0]

# # finalTorque = math.sqrt( torques[0]**2 + torques[1]**2 + torques[2]**2 )

# #new function below.
# #this function will take in an array of 3 lengths then calculate the points and torques

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


def calcMidPt( x1, y1, x2, y2 ):
    
    midX = ( x2-x1 )/2 + x1
    midY = ( y2-y1 )/2 + y1

    return x1, y1

def mass( p, l ): #calculates mass of each arm based on length and its density
    return p * l

def force( aMass ): #calculates force using mass and gravity constant (9.81N/kG)
    return aMass * 9.81



def calculateTorque2( armLengths ):
    gripperPts= [ [ 0.75, 0.1 ], [ 0.5, 0.5 ], [ 0.2, 0.6 ] ]
    gripperForce = 5 * 9.81
    gripperAngles = [ -math.pi/3.0, 0, math.pi/4 ]
    torques = [ 0, 0, 0 ]

    #everything below this should be in a for loop to calculate the torques at 3 positions then return the root of the 3 torques squared
    for i in range( 3 ):
        bx = gripperPts[ i ][ 0 ] - ( armLengths[ 2 ] * math.cos(gripperAngles[ i ] ) )
        by = gripperPts[ i ][ 1 ] - ( armLengths[ 2 ] * math.sin(gripperAngles[ i ] ) )

        midPts = [ [ ], [ ], [ ] ]
        x1, y1, x2, y2 = get_intersections(0, 0, armLengths[ 0 ], bx, by, armLengths[ 1 ])
        armMasses = [ 0, 0, 0]
        a = 4
        for l in range( 3 ):
            armMasses[i] = mass(a, armLengths[ i ] )
            a /= 2

        #calculate the gravity forces of each member
        gravForces = [ 0, 0, 0 ]
        for k in range( 3 ):
            gravForces[ k ] = force( armMasses[ k ])

        #calculate the midpoints of each member, this is where the gravity force acts.
        midPts[ 0 ] = calcMidPt( 0, 0, x1, y1 )
        midPts[ 1 ] = calcMidPt( x1, y1, bx, by )
        midPts[ 2 ] = calcMidPt( bx, by, gripperPts[ i ][0], gripperPts[ i ][1] )

        
        tempMidPtA1 = calcMidPt( 0, 0, x1, y1 )
        torqueA = gravForces[ 1 ] * tempMidPtA1[0] * math.sin( math.atan2( tempMidPtA1[1], tempMidPtA1[0]))
        tempMidPtA2 = calcMidPt( x1, y1, bx, by )
        torqueA += gravForces[ 1 ] * tempMidPtA2[ 0 ] * math.sin( math.atan2( tempMidPtA2[1], tempMidPtA2[0]))
        tempMidPtB1 = calcMidPt( 0, 0, x2, y2 )
        torqueB = gravForces[ 1 ] * tempMidPtB1[ 0 ] * math.sin( math.atan2( tempMidPtB1[1], tempMidPtB1[0] ))
        tempMidPtB2 = calcMidPt( x2, y2, bx, by)
        torqueB += gravForces[ 1 ] * tempMidPtB2[ 0 ] * math.sin( math.atan2( tempMidPtB2[1], tempMidPtB2[0] ))
        

        if (torqueB < torqueA):
            midPts[0] = tempMidPtB1
            midPts[1] = tempMidPtB2


        for j in range( 0, 3): #Add all the torque required for the three arms
            torques[ i ] += ( gravForces[ j ] * midPts[ j ][ 0 ] * math.sin( math.atan2( midPts[ j ][ 1 ], midPts[ j ][ 0 ] ) ) )

        torques[ i ] += ( gripperForce * gripperPts[ i ][0] * math.sin( math.atan2( gripperPts[ i ][1], gripperPts[ i ][0] ) ) )


    finalTorque = math.sqrt( torques[ 0 ]**2 + torques[ 1 ]**2 + torques[ 2 ]**2 )

    return finalTorque
    


testLengths = [ 0.5, 0.6, 0.3 ]
test = calculateTorque2(testLengths)

print(test)