# Broad scale wrangling functions
# Targeted at solving multiple (similar) problems at the same time
# Operated on datsets in the form of static .csv files

# Prerequisite: Singular uploaed dataframe (works in principle for data.tables as well)


# .............................................................
##### Issue 9: Separate a header into 2 different headers #####
# .............................................................

sepHeader = function(d, header, name1, name2, separator) {
  
  # This function separates one hedaer into 2 different headers
  # Useful to segregate "range" headers
  
  if (header %in% colnames(d)) {
    
    if (as.character(is.numeric(d[ , header])) == "FALSE") {
      
      # d[ , name1] = lapply(strsplit(as.character(d[ , header]), sep), "[", 1)
      # d[ , name2] = lapply(strsplit(as.character(d[ , header]), sep), "[", 2)
      
      sep_removeAfter = paste0(separator, ".*")
      sep_removeBefore = paste0(".*", separator)
      
      d[ , name1] = gsub(sep_removeAfter, "", d[ , header])
      d[ , name2] = gsub(sep_removeBefore, "", d[ , header])
      
      
      d[ , name1] = factor(d[ , name1])
      d[ , name2] = factor(d[ , name2])
      
    } else {
      
      # EXCEPTION HANDLING:
      
      print("HEADER NOT PROCESSED. Given header is numerical.")
      
    }
    
  } else {
    
    # EXCEPTION HANDLING:
    
    print("HEADER NOT PROCESSED. Given header not available in the dataset.")
    
  }
  
  return(d)

}
