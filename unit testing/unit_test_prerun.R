# Unit testing normalization functions
# Resource: https://bitbucket.org/account/user/srcbot/projects/DW


# ..................................
##### Empty global environment #####
# ..................................

rm(list = ls())


# .................................
##### Load required libraries #####
# .................................

library(dfwrangle)

# if ("RCurl" %in% installed.packages()[,"Package"] == FALSE) {
  
  # install.packages("RCurl")
  
# }

# library(RCurl)
library(testthat)

# .............................
##### Load sample dataset #####
# .............................

# Download sample data from https://bitbucket.org/srcbot/wrangling-functions-in-r/src/95d13a5131f8/unit%20testing/?at=master

d = read.csv("C:/Pin2Pin/NewResearchStuff/Data Normalization/unit testing/msr_sample_data.csv", encoding = "UTF-8")


# ..........................................
##### Set directory for test functions #####
# ..........................................

setwd("C:/Pin2Pin/NewResearchStuff/Data Normalization/unit testing/tests")


# .......................
##### Run all tests #####
# .......................

test_dir(".")






















