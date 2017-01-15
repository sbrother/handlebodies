#####################################################################
#
# meshclass.py
# 
# Defines the class 'mesh' to be used with FEM methods.
# Input is a np array of boundary circles.
#
#####################################################################

import subprocess
import numpy as np

# Define FEM matrix elements



# Define the Mesh class
class Mesh(object):

    # Initialize mesh object
    def __init__(self, circles, *accuracy):
        self.circles = circles
        self.accuracy = accuracy
        
        # Format input array 
        self.ms_in = np.array(['./makemesh'])
        self.ms_in = np.append(self.ms_in, np.char.mod('%f', accuracy))
        self.ms_in = np.append(self.ms_in , np.char.mod('%f',self.circles.reshape(self.circles.size)))
        
        # Run mathematica script
        self.ms_out = subprocess.check_output(self.ms_in).split("break")
        # Import the mesh coordinates
        self.coors = np.fromstring(self.ms_out[0][1:-2], sep=",")
        self.coors = self.coors.reshape((self.coors.size/2,2))

        # Import the mesh element list
        self.melems = np.fromstring(self.ms_out[1][2:-2], dtype=int,sep=",")
        self.melems = self.melems.reshape(self.melems.size/6,6)

        # Import the boundary element list
        self.belems = np.fromstring(self.ms_out[2][2:-2], dtype=int,sep=",")

        # Construct derivative matrices
        
mesh = Mesh(np.array([[1,0,0],[0,1,0],[0,0,-1]]), np.array([0.005,4]))
