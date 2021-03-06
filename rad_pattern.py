import numpy as np 
import matplotlib.pyplot as plt

class DipoleAntenna:

    def __init__(self, frequency, length):
        self.frequency = frequency
        self.lam = 300 / frequency
        self.k = 2*np.pi / self.lam
        self.w = 2*np.pi / frequency
        self.length = length 
        self.theta = np.linspace(0,2*np.pi, 1000)
        self.E = self.E_field()

    def E_field(self):
        zeta = 377
        left = 1j*zeta*np.exp(-1j*self.k) / 2*np.pi
        right = (np.cos((self.k*self.length/2) * np.cos(self.theta)) - np.cos(self.k*self.length/2)) / np.sin(self.theta)
        return np.abs(left*right)
