# -*- coding: utf-8 -*-
import random
import math
from enum import Enum
"""
@Distribution retains data related to a distribution

@author: Malith Jayaweera
"""
class DistributionType(Enum):
	EXPONENTIAL = "exponential"
	GAMMA = "gamma"
	NORMAL = "normal"
	WEIBULL = "weibull"

class Distribution:
	
	def __init__(self, distribution = DistributionType.EXPONENTIAL, mean = 25, alpha = 1, beta = 1, sigma = 1):
		self.__distribution = distribution
		self.__mean = mean
		self.__alpha = alpha
		self.__beta = beta
		self.__sigma = sigma
		
	def __getMean__(self):
		return self.__mean
	
	def __getAlpha__(self):
		return self.__alpha
	
	def __getBeta__(self):
		return self.__beta
	
	def __getSigma__(self):
		return self.__sigma
	
	def __getDistribution__(self):
		return self.__distribution



"""
@ContentionGenerator generates contention events

@author: Malith Jayaweera
"""
class EventGenerator:
     def __init__(self, system, distribution):
        """ Returns a FailureEventGenerator object with the specified distribution
        and distribution parameter """
        self.setDistribution(distribution.__getDistribution__())
        self.__distribution = distribution
        self.__distributionType = distribution.__getDistribution__() 
        self.__system = system
              
    
     def getNextEvent(self, mean):
        """ Returns the next failure event time based on the distribution """
        alpha = self.__distribution.__getAlpha__()
        beta  = self.__distribution.__getBeta__()
        sigma = self.__distribution.__getSigma__()
		
        if self.__distributionType == DistributionType.EXPONENTIAL:
            return random.expovariate(1/mean)
        elif self.__distributionType == DistributionType.WEIBULL:
            __alpha = (mean / math.gamma(1 + 1/self.__beta))
            return random.weibullvariate(__alpha, self.__beta)
        elif self.__distributionType == DistributionType.NORMAL:
            return random.normalvariate(mean, sigma)
        elif self.__distributionType == DistributionType.GAMMA:
            return random.gammavariate(alpha, beta)
        else:
          return random.expovariate(1/mean)
        
     def setDistribution(self, distribution):
        if distribution in DistributionType:
            self.__distribution = distribution
        else: 
            raise ValueError("Unsupported distribution type")
            
     def setMean(self, mean):
        self.__mean = mean



"""
@FailureEventGenerator generates failure events 

@author: Malith Jayaweera
"""
class FailureEventGenerator(EventGenerator):
    
    def __init__(self, system, distribution):
        """ Returns a FailureEventGenerator object with the specified distribution
        and distribution parameter """
        self.__distribution__ = distribution
        self.__system__ = system
        super().__init__(system, distribution)
    
    def getNextFailure(self):
        """ Returns the next failure event time based on the distribution """
        return super().getNextEvent(self.__system__.__getMtbf__())
	
    def getDistribution(self):
        return self.__distribution
	
    def setDistribution(self, distribution):
        self.__distribution = distribution
		
    
	
"""
@FailureEventGenerator generates failure events 

@author: Malith Jayaweera
"""
class Mode(Enum):
	DEFAULT = "default"
	VARY_OVERHEAD = "varyOverhead"
	STORE_DIFF = "storeDiff"
	
class ContentionEventGenerator(EventGenerator):
    
	def __init__(self, system, distribution, mode = Mode.DEFAULT):
		""" Returns a FailureEventGenerator object with the specified distribution
        and distribution parameter """
		self.mode = mode
		self.distribution = distribution
		super().__init__(system, distribution)
       
    
	def getNextContention(self):
		""" Returns the next failure event time based on the distribution """
		if self.mode == Mode.DEFAULT:
			return self.distribution.__getMean__()
		elif self.mode == Mode.VARY_OVERHEAD:
			return super().getNextEvent(self.distribution.__getMean__())
		else:
			return super().getNextEvent()