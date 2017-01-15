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

class Mesh(object):
    def __init__(self, circles, accuracy):
        self.circles = circles
        self.accuracy = accuracy

        mathematica_output = self._run_mathematica(
            accuracy,
            self.circles.reshape(self.circles.size))

        self.coors = self._build_coors(mathematica_output)
        self.melems = self._build_melems(mathematica_output)
        self.belems = self._build_belems(mathematica_output)

    def _run_mathematica(self, *command_components):
        command_list = np.array(['./makemesh'])
        for component in command_components:
            command_list = np.append(command_list, component)

        return subprocess.check_output(command_list).split("break")

    def _build_coors(self, mathematica_output):
        """Import the mesh coordinates."""
        coors = np.fromstring(mathematica_output[0][1:-2], sep=",")
        coors.reshape((self.coors.size/2,2))
        return coors

    def _build_melems(self, mathematica_output):
        """Import the mesh element list."""
        melems = np.fromstring(mathematica_output[1][2:-2], dtype=int, sep=",")
        melems.reshape(self.melems.size/6,6)
        return melems

    def _build_belems(self, mathematica_output):
        """Import the boundary element list"""
        return np.fromstring(mathematica_output[2][2:-2], dtype=int,sep=",")

mesh = Mesh(np.array([[1,0,0],[0,1,0],[0,0,-1]]), np.array([0.005,4]))
