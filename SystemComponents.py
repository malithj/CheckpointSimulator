# -*- coding: utf-8 -*-
"""
@Job retains data about a job submitted to the system

@author: Malith Jayaweera
"""
class Job: 
	
	def __init__(self, computeTime):
		self.__computeTime = computeTime
		
	def __setComputeTime__(self, computeTime):
		self.__computeTime = computeTime
		
	def __getComputeTime__(self):
		return self.__computeTime
		
		
"""
@System retains system related data 

@author: Malith Jayaweera
"""
class Machine:
	
	def __init__(self, mtbf, restartTime):
		self.__mtbf = mtbf
		self.__restartTime = restartTime
		
	def __setMtbf__(self, mtbf):
		self.__mtbf = mtbf
		
	def __getMtbf__(self):
		return self.__mtbf

	def __setRestartTime__(self, restartTime):
		self.__restartTime = restartTime
		
	def __getRestartTime__(self):
		return self.__restartTime
	
	def __setJob__(self, job):
		self.__job = job
		
	def __getJob__(self):
		return self.__job
	
	
