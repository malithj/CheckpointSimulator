# -*- coding: utf-8 -*-
from EventGenerator import FailureEventGenerator, ContentionEventGenerator, Mode, Distribution, DistributionType
from Simulator import Simulator
from Plotter import Plotter
from SystemComponents import Job, Machine
import operator
"""
Event Simulator simulates the execution of an application given parameters 
type of failure distribution (exponential distribution),
checkpoint time, restart time, MTBF, and compute time

@author: Malith Jayaweera
"""

def plotDistributionEffect(failureEventGenerator, system, simulator, plotter, mtbf, strNode,  startTime, endTime, iterations):
    print("Calculating sample data for a " + strNode + " node system")
    system.__setMtbf__(mtbf)
    failureEventGenerator.__distribution__.__distribution = DistributionType.EXPONENTIAL
    sampleResults = simulator.doCompleteSimulation(startTime, endTime, iterations)
    x1 = sampleResults.keys()
    y1 = sampleResults.values()

    failureEventGenerator.__distribution__.__distribution = DistributionType.WEIBULL
    failureEventGenerator.__distribution__.__beta = 0.6
    sampleDistResults = simulator.doCompleteSimulation(startTime, endTime, iterations)
    x2 = sampleDistResults.keys()
    y2 = sampleDistResults.values()
    
    plotter.plotOn(x1, y1, x2, y2, "Effect of distribution function ("+ strNode +" nodes)",
                                     "Checkpoint Interval (in hours)",
                                     "Job Execution Time \n (in hours)")
    
def plotSystemEffect(system, simulator, plotter, mtbf, strNode, startTime, endTime, iterations):
    system.__setMtbf__(mtbf)
    print("Calculating sample data for a " + strNode + " node system")
    sampleResults = simulator.doCompleteSimulation(startTime, endTime, iterations)
    sortedResults = sorted(sampleResults.items(), key=operator.itemgetter(0))
    x = list(zip(*sortedResults))[0]
    y = list(zip(*sortedResults))[1]
    print( min(y), x[y.index(min(y))]);
    plotter.plot(x, y, "Comparing Simulation Based Results (" + strNode + " nodes)",
                       "Checkpoint Interval (in hours)",
                       "Job Execution Time \n (in hours)")
    
    
def main():
    """
    Event Simulator simulates the execution of an application given parameters 
    type of failure distribution (exponential distribution),
    checkpoint time, restart time, MTBF, and compute time
    """
    mtbf_10k = 50                   # MTBF of a 10k node system
    mtbf_20k = 25                   # MTBF of a 20k node system 
    mtbf_100k = 5                   # MTBF of a 100k node system adjusted
    computeTime = 500               # compute time 
    restartTime = 0.2               # restarting overhead
    checkpointTime = 30            # checkpointing overhead
    beta = 0.6                      # beta value for failure curve
    cont_alpha = 32               # alpha value of the contention distribution
    cont_beta = 1.1               # alpha value of the contention distribution
    
    job = Job(computeTime)
    system = Machine(mtbf_10k, restartTime)
    system.__setJob__(job)
	
    contentionDistribution = Distribution(distribution= DistributionType.GAMMA, mean = checkpointTime, alpha = cont_alpha, beta = cont_beta)
    failureDistribution = Distribution(distribution = DistributionType.EXPONENTIAL, mean = mtbf_20k, beta = beta)
	
    failureEventGenerator = FailureEventGenerator(system, failureDistribution)
    contentionEventGenerator = ContentionEventGenerator(system, contentionDistribution, Mode.VARY_OVERHEAD)
	
    simulator = Simulator(failureEventGenerator, contentionEventGenerator, system)
    plotter = Plotter()
    
    #Ask for Input 
    print("Checkpoint Event Simulator")
    print("Choose option. \n 1) Plot checkpoint characteristics using exponential distribution " +
                      "\n 2) Compare distribution's effect on checkpoint characteristics \n")
    try:
        inputValue = int(input("Enter option: "))
    except ValueError:
        raise ValueError("Please input an integer")
        
    if inputValue == 1:
        plotSystemEffect(system, simulator, plotter, mtbf_20k, "20k", 60, 8, 1)
        plotSystemEffect(system, simulator, plotter, mtbf_100k, "100k", 1, 8, 1)
        
    elif inputValue == 2:
        plotDistributionEffect(failureEventGenerator, system, simulator, plotter, mtbf_10k, "10k", 60, 8, 1)
        plotDistributionEffect(failureEventGenerator, system, simulator, plotter, mtbf_20k, "20k", 60, 8, 1)
        plotDistributionEffect(failureEventGenerator, system, simulator, plotter, mtbf_100k, "100k", 60, 8, 1)
        
    else: 
        print("Invalid input entered. Please check your input")
    
    
main()