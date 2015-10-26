README
======

Introduction
------------
This is the readme file for the "application analysis.R" file. This file analyses the cleaned data to answer the following questions:

- Name of all countries that applied per year, 2011 - 2015
- Number of countries that applied per year, 2011 - 2015
- Application numbers per year for each country, 2011 - 2015

The analysis will create Excel (XLSX) files for answering the above questions. It will additionally create a JSON file for the purposes of visualization.

Pre-requisites
--------------
This code has been tested on the following:

- R version 3.1.3, 3.2.2

Required packages:
- dplyr
- jsonlite
- openxlsx

Required files:
- cleaned files for each year in json format in the same directory

Execution
---------
In RStudio, you can open the file, setwd() to the directory where the analysis directory is and run the entire file by clicking on "Source" button

Expected Output
---------------
In the /data directory, the following files will be created:
- 01 application country names per year.xlsx
- 02 impact country names per year.xlsx
- 03 application country numbers per year.xlsx
- 04 impact country numbers per year.xlsx
- 05 application country numbers per year per country.xlsx
- 06 impact country numbers per year per country.xlsx
- impacted.json

Note: "impacted.json" file is intended for visualization purposes.
