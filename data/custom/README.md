README
======

Introduction
------------
This folder contains customized output files. This readme serves to guide the generation of the custom `impacted.json` found in this directory.

Pre-requisites
--------------
This code has been tested on the following:

- R version 3.1.3

Required packages:
- dplyr
- jsonlite
- readr
- readxl

Required files:
- customized excel files in the /data/custom directory

Execution
---------
In RStudio, you can open the file, setwd() to the directory where the analysis directory is (Or click on Session > Set Working Directory > To Source File Location) and run the file `custom_json.R` by clicking on "Source" button

Alternatively, in command line, navigate to the "analysis" directory and execute the following command:

```
Rscript "custom_json.R"
```

Expected Output
---------------
In the /data/custom directory, the following files will be created:
- impacted.json

Note: "impacted.json" file is intended for visualization purposes.
