# -*- coding: utf-8 -*-
from EventGenerator import FailureEventGenerator, ContentionEventGenerator, Mode, Distribution, DistributionType
from Simulator import Simulator, SimulatorProperties
from Plotter import Plotter
from SystemComponents import Job, Machine, NodeCount
import operator
import configparser
"""
Event Simulator simulates the execution of an application given parameters 
type of failure distribution (exponential distribution),
checkpoint time, restart time, MTBF, and compute time

@author: Malith Jayaweera
"""
def plotDistributionEffect(failureEventGenerator, system, simulator, plotter):
    print("Calculating sample data for a " + system.__getSize__().value + " node system")
    failureEventGenerator.__distribution__.__distribution = DistributionType.EXPONENTIAL
    sampleResults = simulator.doCompleteSimulation()
    x1 = sampleResults.keys()
    y1 = sampleResults.values()

    failureEventGenerator.__distribution__.__distribution = DistributionType.WEIBULL
    failureEventGenerator.__distribution__.__beta = 0.6
    sampleDistResults = simulator.doCompleteSimulation()
    x2 = sampleDistResults.keys()
    y2 = sampleDistResults.values()
    
    plotter.plotOn(x1, y1, x2, y2, "Effect of distribution function ("+ system.__getSize__().value +" nodes)",
                                     "Checkpoint Interval (in hours)",
                                     "Job Execution Time \n (in hours)")
    
def plotSystemEffect(system, simulator, plotter):
    print("Calculating sample data for a " + system.__getSize__().value  + " node system")
    sampleResults = simulator.doCompleteSimulation()
    sortedResults = sorted(sampleResults.items(), key=operator.itemgetter(0))
    x = list(zip(*sortedResults))[0]
    y = list(zip(*sortedResults))[1]
    print( min(y), x[y.index(min(y))]);
    plotter.plot(x, y, "Comparing Simulation Based Results (" + system.__getSize__().value  + " nodes)",
                       "Checkpoint Interval (in hours)",
                       "Job Execution Time \n (in hours)")
    
    
def main():
    """
    Event Simulator simulates the execution of an application given parameters 
    type of failure distribution (exponential distribution),
    checkpoint time, restart time, MTBF, and compute time
    """
    config = configparser.ConfigParser()
    config.read('config.ini')
    mtbf_10k       = float(config['SYSTEM']['MTBF_10K'])            # MTBF of a 10k node system
    mtbf_20k       = float(config['SYSTEM']['MTBF_20K'])            # MTBF of a 20k node system 
    mtbf_100k      = float(config['SYSTEM']['MTBF_100K'])           # MTBF of a 100k node system adjusted
    computeTime    = float(config['JOB']['COMPUTE'])                # compute time 
    restartTime    = float(config['SYSTEM']['RESTART_TIME'])        # restarting overhead
    checkpointTime = float(config['SYSTEM']['CHECKPOINT_TIME'])     # checkpointing overhead
    beta           = float(config['FAILUREDISTRO']['BETA'])         # beta value for failure curve
    cont_alpha     = float(config['CPDISTRO']['ALPHA'])             # alpha value of the contention distribution
    cont_beta      = float(config['CPDISTRO']['BETA'] )             # alpha value of the contention distribution
    startTime      = int(config['SIMULATOR']['START'])              # simulation start time
    endTime        = int(config['SIMULATOR']['END'])                # simulation end time
    iterations     = int(config['SIMULATOR']['ITR'])                # simulation iterations
    
    job = Job(computeTime)
    system = Machine(mtbf_10k, restartTime)
    system.__setJob__(job)
	
    contentionDistribution = Distribution(distribution= DistributionType.GAMMA, mean = checkpointTime, alpha = cont_alpha, beta = cont_beta)
    failureDistribution = Distribution(distribution = DistributionType.EXPONENTIAL, mean = mtbf_20k, beta = beta)
	
    failureEventGenerator = FailureEventGenerator(system, failureDistribution)
    contentionEventGenerator = ContentionEventGenerator(system, contentionDistribution, Mode.VARY_OVERHEAD)
	
    simulatorProperties = SimulatorProperties(startTime, endTime, iterations)
    simulator = Simulator(failureEventGenerator, contentionEventGenerator, system, simulatorProperties)
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
        system.__setMtbf__(mtbf_20k)
        system.__setSize__(NodeCount.SYSTEM_20K)
        plotSystemEffect(system, simulator, plotter)
		
        simulatorProperties.__setStartTime__(1)
        system.__setSize__(NodeCount.SYSTEM_100K)
        system.__setMtbf__(mtbf_100k)
        plotSystemEffect(system, simulator, plotter)
        
    elif inputValue == 2:
        system.__setMtbf__(mtbf_10k)
        system.__setSize__(NodeCount.SYSTEM_10K)
        plotDistributionEffect(failureEventGenerator, system, simulator, plotter)
        system.__setMtbf__(mtbf_20k)
        system.__setSize__(NodeCount.SYSTEM_20K)
        plotDistributionEffect(failureEventGenerator, system, simulator, plotter)
        system.__setMtbf__(mtbf_100k)
        system.__setSize__(NodeCount.SYSTEM_100K)
        plotDistributionEffect(failureEventGenerator, system, simulator, plotter)
        
    else: 
        print("Invalid input entered. Please check your input")
    
    
main()