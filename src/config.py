import osandio.fileUtils
import os

class Config:
    # db info
    dbUser = 'player'
    dbPass = 'finder'
    dbHost = 'localhost'
    dbPort = 3306
    dbName = 'mlbplayercache'
    mySQLLocation = 'C:\\Program Files\\MySQL\\MySQL Server 5.5\\bin'
    numberOfThreads = 8

    # data paths
    pathToChadwick = ".." + os.sep + "data" + os.sep + "chadwick-bureau" + os.sep
    pathToBR = ".." + os.sep + "data" + os.sep + "baseball-reference" + os.sep
    pathToFangraphs = ".." + os.sep + "data" + os.sep + "fangraphs" + os.sep

    # sql paths
    pathToChadwickSql = ".." + os.sep + "sql" + os.sep + "chadwick-bureau" + os.sep
    pathToBRSql = ".." + os.sep + "sql" + os.sep + "baseball-reference" + os.sep
    pathToFangraphsSql = ".." + os.sep + "sql" + os.sep + "fangraphs" + os.sep

    # chadwick repo
    pathToChadwickRepo = 'C:\\Documents\\GitHub\\chadwickbureau\\register\\'
