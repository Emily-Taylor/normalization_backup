# Broad scale wrangling functions
# Targeted at solving multiple (similar) problems at the same time
# Operated on datsets in the form of static .csv files

# Prerequisite: Singular uploaed dataframe (works in principle for data.tables as well)


# ...................................................
##### Issue 8: Remove everything before a symbol #####
# ...................................................
#' @export
removeBefore = function(d, header, separator) {
  
  # This function removes everything before a designated symbol
  
  if (header %in% colnames(d)) {
    
    sep_removeBefore = paste0(".*", separator)
    
    d[ , header] = gsub(sep_removeBefore, "", d[ , header])
    
    d[ , header] = factor(d[ , header])
    
  } else {
    
    # EXCEPTION HANDLING:
    
    print("HEADER NOT PROCESSED. Given header not available in the dataset.")
    
  }
  
  return(d)
  
}
