# Unit testing normalization functions
# Resource: https://github.com/sourcingbot/Wrangling-Functions-in-R


# ..................................
##### Empty global environment #####
# ..................................

rm(list = ls())


# .................................
##### Load required libraries #####
# .................................

library(dfwrangle)

if ("RCurl" %in% installed.packages()[,"Package"] == FALSE) {
  
  install.packages("RCurl")
  
}

library(RCurl)
library(testthat)

# .............................
##### Load sample dataset #####
# .............................

# Download sample data from https://github.com/sourcingbot/Wrangling-Functions-in-R/blob/master/unit%20testing/msr_sample_data.csv
# Or source it directly from the raw GitHub link, usng the "RCurl" library as follows:

d = read.csv(text = getURL("https://raw.githubusercontent.com/sourcingbot/Wrangling-Functions-in-R/master/unit%20testing/msr_sample_data.csv?token=AVmzxbKqs_cRaia_-rwRhW3cnqPcXQBIks5aMm6iwA%3D%3D"), header = T, encoding = "UTF-8")


# ..........................................
##### Set directory for test functions #####
# ..........................................

setwd("C:/Pin2Pin/NewResearchStuff/Data Normalization/unit testing/tests")


# .......................
##### Run all tests #####
# .......................

test_dir(".")
