# Broad scale wrangling functions
# Targeted at solving multiple (similar) problems at the same time
# Operated on datsets in the form of static .csv files

# Prerequisite: Singular uploaed dataframe (works in principle for data.tables as well)


# ...................................
##### Issue 4: Rescale a header #####
# ...................................

reScale = function(d, header, scaling_factor) {
  
  # This function rescales any numerical header using appropriate scaling factor
  
  if (header %in% colnames(d)) {
    
    if (as.character(is.numeric(d[ , header])) == "TRUE") {
      
      
      d[, header] = d[ , header] * scaling_factor
      
      
    } else {
      
      # EXCEPTION HANDLING:
      
      print("HEADER NOT PROCESSED. Given header is not numerical.")
      
    }
    
    
    
  } else {
    
    # EXCEPTION HANDLING:
    
    print("HEADER NOT PROCESSED. Given header not available in the dataset.")
    
  }
  
  return(d)
  
}
