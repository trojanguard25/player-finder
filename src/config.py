import osandio.fileUtils
import os

class Config:
    # db info 
    dbUser = 'player'
    dbPass = 'finder'
    dbHost = 'localhost'
    dbPort = 3306
    dbName = 'player-finder'
    mySQLLocation = 'C:\\Program Files\\MySQL\\MySQL Server 5.5\\bin'
    numberOfThreads = 8
    
    # data paths
    pathToChadwick = ".." + os.sep + "data" + os.sep + "chadwickbureau" + os.sep
    pathToBR = ".." + os.sep + "data" + os.sep + "baseball-reference" + os.sep
    pathToFangraphs = ".." + os.sep + "data" + os.sep + "fangraphs" + os.sep
    
