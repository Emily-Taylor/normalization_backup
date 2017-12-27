# Broad scale wrangling functions
# Targeted at solving multiple (similar) problems at the same time
# Operated on datsets in the form of static .csv files

# Prerequisite: Singular uploaed dataframe (works in principle for data.tables as well)

# ......................................
##### Issue 1: Clean blanck spaces #####
# ......................................

#' @export
cleanBlanck = function(d) {
  
  # This function replaces blanck spaces (missing data) in our dataframes with NA
  
  for (i in 1:ncol(d)) {
    
    d[,i][which(d[,i] == '')] = NA
    d[,i][which(d[,i] == ' ')] = NA
    d[,i][which(d[,i] == '-')] = NA
    d[,i][which(d[,i] == '*')] = NA
    
  }
  
  return(d)
  
}
