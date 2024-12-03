# ESRI Enterprise-Geodatabse-Maintenance
 Perform Regular Geodatabase Maintenance on ESRI Enterprise Geodatabases

## General Workflow
This Python script runs the ESRI recommended database maintenance processes for geodatabases. Use for ensuring enterprise geodatabases remain performant after edits and updates.

- [Compress Geodatabase](https://pro.arcgis.com/en/pro-app/latest/tool-reference/data-management/compress.htm) to improve performance. 
- [Rebuild Indexes](https://pro.arcgis.com/en/pro-app/latest/tool-reference/data-management/rebuild-indexes.htm) on the Enterprise Geodatabase Tables to defragment them.
- [Analyze Datasets](https://pro.arcgis.com/en/pro-app/latest/tool-reference/data-management/analyze-datasets.htm) and update statistics of tables and the indexes that are associated with them.

It is suggested to run this workflow once a week or after substantial edits.

## Usage
1. Download ESRImaintenanceEGDB.py to a system with an ESRI Python Interpreter installed.
2. Path the workspace variable to your ESRI geodatabase (.SDE file).
3. Run script.

The script will close all connections to the databases and disconnect active users before performing maintenance. It enables connections once maintenance is complete. 

The user who is connected through the .SDE file needs to be the schema owner of the data that is being maintained in the database.

Database Administrator permissions are required for the script to work on System tables.

A log file will be saved to the directory that the script is executed from.

## License
Copyright (c) 2024 Hawaii County

This project is licensed under MIT License.

A copy of the license is available in the repository's LICENSE file.
