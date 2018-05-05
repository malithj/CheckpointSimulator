# -*- coding: utf-8 -*-
import math
"""
Simulator is responsible for orchestrating the event driven mechanism

@author: Malith Jayaweera
"""
class Simulator: 
    """
    Simulator class is responsible for orchestrating the event driven mechanism
    Contains the core logic required to perform simulations
    
    __init__ method initializes by obtaining the total compute time, restarting overhead, 
    checkpoint overhead
    """
    
    def __init__(self, failureEventGenerator, contentionEventGenerator, system):
        self.__failureEventGenerator = failureEventGenerator
        self.__contentionEventGenerator = contentionEventGenerator
        self.__computeTimeMax = system.__getJob__().__getComputeTime__()
        self.__restartTime = system.__getRestartTime__()
        self.__simulationTime = {}
                
    def doSimulationIteration(self, checkpointInterval):
        """
        Performs an interation of the simulation. i.e. for a given checkpoint interval, 
        failure events are expected to be generated from the @FailureEventGenerator and 
        the method calculates 
        
        Args:
            checkpointInterval (float) : specifies the checkpoint interval in terms of hours 
            
        Returns:
            A list containing total execution time, checkpointing time, total wasted work, 
            and the failure count
        """
        slot = 0
        totalExecutionTime = 0
        failureCount = 0
        totalWastedWork = 0
        checkpointTime = 0
        runningSlots = int(self.__computeTimeMax / checkpointInterval)
        nextFailureSlot = ( self.__failureEventGenerator.getNextFailure() 
        / checkpointInterval )
        while(slot < runningSlots):
             if slot == math.ceil(nextFailureSlot):  # failure has occured
                  failureCount +=1               # increment failure count 
                  slot -= 1 # reset compute time 
                  wastedWork = self.__restartTime + checkpointInterval * math.modf(nextFailureSlot)[0]
                  totalWastedWork += wastedWork
                  totalExecutionTime += wastedWork # add restart time
                  nextFailureSlot = slot + ( self.__failureEventGenerator.getNextFailure() 
                  / checkpointInterval ) #rest failure time
                  continue
             # do computing 
             slot += 1 #increment compute time 
             totalExecutionTime += checkpointInterval # increment total execution time
             checkpointOverhead = (self.__contentionEventGenerator.getNextContention())/60 #checkpointing overhead now varies
             totalExecutionTime += checkpointOverhead  # add checkpointing overhead
             checkpointTime += checkpointOverhead
        return [totalExecutionTime, checkpointTime, totalWastedWork, failureCount]
    
    def doCompleteSimulation(self, start, maxHours, maxIterations = 1):
        """
        Performs the complete simulation. i.e. each minute is simulated until the maximum Hours number, 
        is reached. doSimulationIteration method is used to perform each iteration while varying 
        the checkpoint interval. Checkpoint interval starts at 1 minute and is incremented
        by 1 minute during each iteration. This was done as to avoid the high performance overhead caused
        by simulating at the seconds level with unnecessary data points. Max iterations number is used to smoothen
        out the noise.
        
        Args:
            maxHours (float) : specifies the maximum number of hours 
            maxIterations : specifies the number of iterations in order to smoothen out the noise
        Returns:
            A list containing the average value of the tuple returned by doSimulationInterval method 
            and the average simulation time
        """
        for i in range (start, 60 * maxHours):
                 iteration = 0
                 execTime = 0
                 while(iteration < maxIterations):
                     result = self.doSimulationIteration(i/60)
                     execTime   += result[0]
                     iteration += 1
                 self.__simulationTime[i/60] = execTime / maxIterations
        return self.__simulationTime
    
    def setFailureEventGenerator(self, failureEventGenerator):
        """
        Sets the failure event generator to perform calculations
        """
        self.__failureEventGenerator = failureEventGenerator
    
    def  setContentionOn(self, state):
        """
        Sets the contention status to decide whether the checkpoint
        """
        self.__contentionOn = state
    
    
        
        
"""
@Distribution retains data related to a distribution

@author: Malith Jayaweera
"""
class SimulatorProperties: 
	
	def __init__(self, startTime, endTime, iterations):
		self.__startTime = startTime
		self.__endTime = endTime
		self.__iterations = iterations
		
	def __getStartTime__(self):
		return self.__startTime
	
	def __getEndTime__(self):
		return self.__endTime
	
	def __getIterations__(self):
		return self.__iterations
	
	def __setStartTime__(self, startTime):
	   self.__startTime = startTime
	
	def __setEndTime__(self, endTime):
		self.__endTime = endTime
	
	def __setIterations__(self, iterations):
		self.__iterations = iterations

             