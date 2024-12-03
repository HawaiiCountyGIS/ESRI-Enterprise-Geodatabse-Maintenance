# -*- coding: utf-8 -*-
"""Perform Regular Geodatabase Maintenance - Enterprise GeoDatabase"""

###############################################################################
# Perform Regular Geodatabase Maintenance - Enterprise GeoDatabase
# Compress the DB, Rebuild DB Indexes, Update DB Statistics.
# The SDE Connection File "user" must be schema owner of the data to be rebuilt and analyzed.
# Database Connections are closed and existing users are disconnected before running the tools.
# Database connections are enabled at the end of the script.
# May run for a substantial time depending on size of database and data table fragmentation.
# Suggested to run at least once per week for optimal geodatabase performance.
# Can be setup as an automated scheduled task.
# Outputs a log file to the directory that the script is executed in.
# ArcPy 3.11.8
# Erik Lash
# Dec, 2024
# IT GIS, Hawaii County, Hawaii
###############################################################################

## To use, set the workspace variable and run in an ESRI Python interpreter.

# import system modules
import arcpy
import os
import sys
from datetime import datetime

# set workspace path to the GDB .sde connection file
#workspace = r"\\path\to\geodatabase.sde"
workspace = r"\\path\to\geodatabase.sde"

# set workspace environment
arcpy.env.workspace = workspace

#See output in Shell and send to a log file.
#filename = "\DB_Maintenance_log.txt"
filename = "\DB_Maintenance_log" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".txt"
output = str(os.path.dirname(os.path.abspath(__file__))) + filename
class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout

    def write(self, message):
        with open (output, "a", encoding = 'utf-8') as self.log:            
            self.log.write(message)
        self.terminal.write(message)

    def flush(self):
        #this flush method is needed for python 3 compatibility.
        #this handles the flush command by doing nothing.
        #you might want to specify some extra behavior here.
        pass
sys.stdout = Logger()

# log starting time
timestart = datetime.today()

print(__doc__)
print("")
print(str(timestart))
print("*** starting **********")
print("")

try:
    # Get a list of all the datasets the user has access to.
    print("parsing for tables, featureclasses, and rasters, and datasets from " + workspace + "...")
    
    # First, get all the stand alone tables, feature classes and rasters.
    dataList = arcpy.ListTables() + arcpy.ListFeatureClasses() + arcpy.ListRasters()

    # Next, for feature datasets get all of the datasets and featureclasses
    # from the list and add them to the master list.
    for dataset in arcpy.ListDatasets("", "Feature"):
        arcpy.env.workspace = os.path.join(workspace,dataset)
        dataList += arcpy.ListFeatureClasses() + arcpy.ListDatasets()
    print("...list of data to have indexes rebuilt and analyzed created")
    ("")

    # reset the workspace
    arcpy.env.workspace = workspace
    
    # disable database from accepting connections
    arcpy.AcceptConnections(workspace, False)
    print("...database connections disabled")
    print("")

    # remove existing users
    arcpy.DisconnectUser(workspace, 'ALL')
    print("...database users disconnected")
    print("")

    #DB Maintenance 1: Compress the Enterprise Geodatabase to improve performance.
    #arcpy.management.Compress(in_workspace)
    print(datetime.today())
    print("compressing geodatabase... ")
    print(" ...")
    arcpy.management.Compress(workspace)
    print("...geodatabase compressed")
    print("")

    #DB Maintenance 2: Rebuild Indexes on the Enterprise Geodatabase Tables to defragment them.
    #arcpy.management.RebuildIndexes(input_database, include_system, {in_datasets}, {delta_only})
    # Note: To use the "SYSTEM" option the workspace user must be an administrator of the database.
    # Note: The connected user in the SDE file must be the owner of the datasets to be Rebuilt.
    print(datetime.today())
    print("rebuilding geodatabase indexes... ")
    print(" ...")
    for d in dataList:
        print('Rebuilding index for ' + d)
        arcpy.management.RebuildIndexes(workspace, "SYSTEM", d, "ALL")
        print(d + ' index rebuilt')
    print("...geodatabase indexes rebuilt")
    print("")    

    #DB Maintenance 3: Analyze Datasets and update statistics of tables and the indexes that are associated with them.
    #arcpy.management.AnalyzeDatasets(input_database, include_system, {in_datasets}, {analyze_base}, {analyze_delta}, {analyze_archive})
    # Note: To use the "SYSTEM" option the workspace user must be an administrator of the database.
    # Note: The connected user in the SDE file must be the owner of the datasets to be Analyzed.
    print(datetime.today())
    print("analyzing database statistics...")
    print("...")
    for d in dataList:
        print('Analyzing ' + d)
        arcpy.management.AnalyzeDatasets(workspace, "SYSTEM", d, "ANALYZE_BASE","ANALYZE_DELTA","ANALYZE_ARCHIVE")
        print(d + ' Analyzed')
    print("...database statistics analyzed")
    print("")

    # reset the workspace
    arcpy.env.workspace = workspace

    # delete the compression log
    if arcpy.Exists("SDE_compress_log"):
        print("deleting the compression log... ")
        arcpy.Delete_management("SDE_compress_log")
        print("...compression log deleted")
    else:
        print("no compression log found to delete")
    print("")

# if an error occurs running geoprocessing tool(s) capture error and write message
except Exception:
    e = sys.exc_info()[1]
    print(e.args[0])
    arcpy.AddError(e.args[0])

finally:
    # enable database to accept connections
    arcpy.AcceptConnections(workspace, True)
    print("...database connections enabled")
    print("")

    # log ending time
    timeend = datetime.today()
    print(str(timeend) + " finished")
    print(str(timestart) + " started")
    print("run time " + str(timeend - timestart).split('.')[0])
    print("")
    print("*** pau **********")
    print("")
    # print("Press Enter to Continue")
    # raw_input()

