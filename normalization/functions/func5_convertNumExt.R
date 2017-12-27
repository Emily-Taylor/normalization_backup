# Broad scale wrangling functions
# Targeted at solving multiple (similar) problems at the same time
# Operated on datsets in the form of static .csv files

# Prerequisite: Singular uploaed dataframe (works in principle for data.tables as well)


# ...........................................................................
##### Issue 5: Remove single character extension and convert to numeric #####
# ...........................................................................
#' @export
convertNumExt = function(d, header, ext) {
  
  # This function removes character extensions and converts header to numeric
  
  if (header %in% colnames(d)) {
    
    if (as.character(is.numeric(d[ , header])) == "FALSE") {
      
      ext_extended = paste(" ", ext, sep = "|")
      
      d[ , header] = gsub(ext_extended, "\\1", d[ , header])
      
      d[ , header] = as.numeric(paste(d[ , header]))
      
      
      
      ext_modified = gsub(" ", "", ext)
      new_name = paste(header, ext_modified, sep = "_")
      
      colnames(d)[which(colnames(d) == header)] = new_name
      
      
      
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
