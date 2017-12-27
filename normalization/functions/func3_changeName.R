# Broad scale wrangling functions
# Targeted at solving multiple (similar) problems at the same time
# Operated on datsets in the form of static .csv files

# Prerequisite: Singular uploaed dataframe (works in principle for data.tables as well)


# ............................................
##### Issue 3: Changing name of a header #####
# ............................................

changeName = function(d, header, new_name) {
  
  # This function changes name of a desired header in our dataframe
  # Ex: header = "Voltage (mV)"; new_name = "voltage_mv"
  
  if (header %in% colnames(d)) {
    
    colnames(d)[which(colnames(d) == header)] = new_name
    
  } else {
    
    # ERROR HANDLING:
    
    print("HEADER NOT PROCESSED. Given header not available in the dataset.")
    
  }
  
  return(d)
}
