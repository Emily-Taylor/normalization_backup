
cleanBlanck = function(d) {
  
 
  for (i in 1:ncol(d)) {
    
    d[,i][which(d[,i] == '')] = NA
    d[,i][which(d[,i] == ' ')] = NA
    d[,i][which(d[,i] == '-')] = NA
    d[,i][which(d[,i] == '*')] = NA
    
  }
  
  return(d)
  
}
