# Broad scale wrangling functions
# Targeted at solving multiple (similar) problems at the same time
# Operated on datsets in the form of static .csv files

# Prerequisite: Singular uploaed dataframe (works in principle for data.tables as well)


# .................................................................................
##### Issue 6: Remove single character extension but DON'T convert to numeric #####
# .................................................................................

convertCatExt = function(d, header, ext) {
  
  # This function remove single character extensions, but keeps the original factor format
  
  if (header %in% colnames(d)) {
    
    if (as.character(is.numeric(d[ , header])) == "FALSE") {
      
      d[ , header] = gsub(ext, "\\1", d[ , header])
      
      d[ , header] = factor(d[ , header])
      
      
    } else {
      
      # EXCEPTION HANDLING:
      
      print("HEADER NOT PROCESSED. Given header is already numerical.")
      
    }
    
  } else {
    
    # EXCEPTION HANDLING:
    
    print("HEADER NOT PROCESSED. Given header not available in the dataset.")
    
  }
  
  return(d)
  
}
