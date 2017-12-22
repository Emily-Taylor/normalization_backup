# Broad scale wrangling functions
# Targeted at solving multiple (similar) problems at the same time
# Operated on datsets in the form of static .csv files

# Prerequisite: Singular uploaed dataframe (works in principle for data.tables as well)


# .................................................................
##### Issue 10: Remove multiple symbols (units) and normalize #####
# .................................................................
#' @export
convertMixedExt = function(d, header, ext, scaling_factor) {
  
  # This function normalized mixed unit headers into a single unit
  
  if (header %in% colnames(d)) {
    
    if (as.character(length(ext) == length(scaling_factor)) == "TRUE") {
      
      # Initiate new empty header
      
      d$newHeader = NA
      
      # Populate the newly initiated header with equivalent entries
      
      for (i in 1:length(ext)) {
        
        temp = which(grepl(ext[i], d[ , header]) == TRUE)
        
        d$newHeader[temp] = as.numeric(paste(gsub(ext[i], "", d[temp, header]))) * scaling_factor[i]
        
      }
      
      
    } else {
      
      # EXCEPTION HANDLING:
      
      print("HEADER NOT PROCESSED. Dimension of extensions and unit conversions do not match.")
      
    }
    
  } else {
    
    # EXCEPTION HANDLING:
    
    print("HEADER NOT PROCESSED. Given header not available in the dataset.")
    
  }
  
  return(d)
  
}
