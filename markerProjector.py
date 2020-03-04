# encoding: utf8

# Marker projection with respect to
# the camera position on the point  C=[Cx,Cy,Cz]
# 28/Feb/2020
# Sergio Herrera

import numpy as np 
import numpy.linalg as la 
import math
import sys

n = len( sys.argv )
if n != 4 :
	print "Args_Camera Position: C_x C_y C_z"
	sys.exit(1)

Cx = float( sys.argv[1] )
Cy = float( sys.argv[2] )
Cz = float( sys.argv[3] )


K = [ [ 1000.0,    0.0, -320.0], #  640
      [    0.0, 1000.0, -240.0], #  480
      [    0.0,    0.0,   -1.0] ]

##Marker Centered at [0,0,0]
P = [ [ -50.0,  50.0,  0.0, 1.0 ],
      [-50.0,  -50.0,  0.0, 1.0 ],
      [ 50.0, -50.0,  0.0, 1.0 ],
      [ 50.0,  50.0,  0.0, 1.0 ],
      [  0.0,  50.0,  0.0, 1.0 ] ]

#New Marker
#P = [ [   0.0,     0.0,  0.0, 1.0 ],
#      [   0.0,  -100.0,  0.0, 1.0 ],
#      [ 100.0,  -100.0,  0.0, 1.0 ],
#      [ 100.0,     0.0,  0.0, 1.0 ],
#      [  50.0,     0.0,  0.0, 1.0 ] ]


# Rotation of the marker around Z axis
ang = 0
ang = math.radians( ang )
R = np.eye( 3 )
R[0,0] =  math.cos(ang)
R[0,1] = -math.sin(ang)
R[1,0] =  math.sin(ang)
R[1,1] =  math.cos(ang)

p1 = np.array( [ [0.0], [0.0], [0.0] ] )
n = len( P )
i = 0
while i < n :
	p1[0][0] = P[i][0]
	p1[1][0] = P[i][1]
	p1[2][0] = P[i][2]
	p1 = np.dot( R, p1 )
	P[i][0] = p1[0][0] 
	P[i][1] = p1[1][0] 
	P[i][2] = p1[2][0] 
	i += 1

# Marker translation on the XY plane
dx = 0
dy = 0
i = 0
while i < n :
	P[i][0] += dx 
	P[i][1] += dy 
	i += 1

# Camera obscura model
# lp = K [ R|t ] P, o
# lp = K R [ I| -c ] P
# camera is looking at the origin 
# and the up vector is a = [0 0 1]'
a = np.array( [ [0], [1], [0] ] )

c = np.array( [  [Cx], [Cy], [Cz] ] )
print "# c^T :", np.transpose( c ) 

z = c/la.norm(c)

# x = a x z
xp = np.cross( a, z, axis=0 )
x = xp/la.norm(xp)

y = np.cross( z, x, axis=0 );

R = []
R = x.transpose()
R = np.append( R, y.transpose(), axis=0 )
R = np.append( R, z.transpose(), axis=0 )

I = np.eye(3,4)
I[:,3] = -c[:,0]

# M = [ I, -c] 
# M = K * R * [ I, -c]; 
M = np.dot( R, I )
M = np.dot( K, M )

t = np.dot( R, -c )		#This is the plane origin
print "# t^T :", np.transpose( t ) 


i = 0
while i < len(P) :
	p = P[i]
	p1 = np.dot( M, np.transpose(p) )
	u = p1[0]/p1[2]
	v = p1[1]/p1[2]	
	print( "{0:3.6f} {1:3.6f}".format(u, v) )

	i += 1

