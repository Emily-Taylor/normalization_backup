# Broad scale wrangling functions
# Targeted at solving multiple (similar) problems at the same time
# Operated on datsets in the form of static .csv files

# Prerequisite: Singular uploaed dataframe (works in principle for data.tables as well)


# .......................................
##### Issue 2: Remove empty columns #####
# .......................................


remEmpty = function(d) {
  
  # This function removes entirely empty columns from our dataframes
  
  d = d[colSums(!is.na(d)) > 0]
  
  return(d)
  
}
