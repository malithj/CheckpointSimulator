# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
"""
Acts as a wrapper class to easily plot the results generated

@author: Malith Jayaweera
"""
class Plotter:
    """
    Acts as a wrapper class to easily plot the results generated
    """
    def plot(self, x, y, title, xlabel, ylabel):
        plt.plot(x, y)
        plt.title(title)
        plt.ylabel(ylabel)
        plt.xlabel(xlabel)
        plt.show()
    
    def plotOn(self, x1, y1, x2, y2, title, xlabel, ylabel):
        plt.plot(x2, y2, 'r')
        plt.plot(x1, y1, 'b')
        plt.title(title)
        plt.ylabel(ylabel)
        plt.xlabel(xlabel)
        red_patch = mpatches.Patch(color='red', label='Weibull')
        blue_patch = mpatches.Patch(color='blue', label='Exponential')
        plt.legend(handles=[red_patch, blue_patch])
        plt.show()
