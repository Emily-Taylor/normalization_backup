# Test colname mapping
# Use one file at a time from mouser and digikey
# Use k-tokenization (k=2), followed by Jaccard similarity


# .........................
##### Clear workspace #####
# .........................

rm(list = ls())

# ........................
##### Read libraries #####
# ........................

library(reshape2)
# library(RecordLinkage)
library(plyr)
library(ggplot2)
library(tokenizers)

# .....................................
##### Remove scientific notations #####
# .....................................

options(scipen=999)


# ......................................
##### Declare supporting functions #####
# ......................................

# Calculate jaccard similarity

jaccard = function(a, b) {
  
  temp = length(intersect(a,b)) / length(union(a,b))
  
  return(temp)
  
}
# Save plots

savePlot = function(myPlot) {
  pdf("output_matrix.pdf")
  print(myPlot)
  dev.off()
}


# ..................................
##### Master working directory #####
# ..................................

args = commandArgs(trailingOnly=TRUE)

# master_wd = "C:/Pin2Pin/NewResearchStuff/colname_mapping/test files"

master_wd = args

setwd(master_wd)

# .........................
##### Read dataframes #####
# .........................

# To be replaced by cmd input

# setwd for mouser

msr_dir = paste(master_wd, "mouser", sep = "/")


if (length(list.files(msr_dir)) == 1) {
  
  d_msr = read.csv(paste(msr_dir, list.files(msr_dir), sep = "/"), encoding = "UTF-8")
  
} else if (length(list.files(msr_dir)) == 2) {
  
  d_msr1 = read.csv(paste(msr_dir, list.files(msr_dir)[1], sep = "/"), encoding = "UTF-8")
  d_msr2 = read.csv(paste(msr_dir, list.files(msr_dir)[2], sep = "/"), encoding = "UTF-8")
  
  d_msr = rbind.fill(d_msr1, d_msr2)
  
  rm(d_msr1, d_msr2)
  
} else {
  
  d_msr = read.csv(paste(msr_dir, list.files(msr_dir)[1], sep = "/"), encoding = "UTF-8")
  
  for (i in 2:length(list.files(msr_dir))) {
    
    temp = read.csv(paste(msr_dir, list.files(msr_dir)[i], sep = "/"), encoding = "UTF-8")
    
    d_msr = rbind.fill(d_msr, temp)
    
    rm(temp)
    
  }
  
}


# setwd for mouser

dgk_dir = paste(master_wd, "digikey", sep = "/")


if (length(list.files(dgk_dir)) == 1) {
  
  d_dgk = read.csv(paste(dgk_dir, list.files(dgk_dir), sep = "/"), encoding = "UTF-8")
  
} else if (length(list.files(dgk_dir)) == 2) {
  
  d_dgk1 = read.csv(paste(dgk_dir, list.files(dgk_dir)[1], sep = "/"), encoding = "UTF-8")
  d_dgk2 = read.csv(paste(dgk_dir, list.files(dgk_dir)[2], sep = "/"), encoding = "UTF-8")
  
  d_dgk = rbind.fill(d_dgk1, d_dgk2)
  
  rm(d_dgk1, d_dgk2)
  
} else {
  
  d_dgk = read.csv(paste(dgk_dir, list.files(dgk_dir)[1], sep = "/"), encoding = "UTF-8")
  
  for (i in 2:length(list.files(dgk_dir))) {
    
    temp = read.csv(paste(dgk_dir, list.files(dgk_dir)[i], sep = "/"), encoding = "UTF-8")
    
    d_dgk = rbind.fill(d_dgk, temp)
    
    rm(temp)
    
  }
  
}


rm(msr_dir, dgk_dir)



# ............................................
##### Convert header names to lower case #####
# ............................................

colnames(d_msr) = gsub("\\.", "", tolower(colnames(d_msr)))
colnames(d_dgk) = gsub("\\.", "", tolower(colnames(d_dgk)))


# ...................................
##### Remove management headers #####
# ...................................

ignored_headers = c("datetime", "category1", "category2", "category3", "manufacturer_part_number", "source", "category", "datasheets", "digikeypartnumber", "manufacturerpartnumber", "manufacturer", "quantityavailable", "factorystock", "unitpriceusd", "xqty", "minimumquantity","select", "image", "series", "product", "qualification", "packagecase", "packaging", "mouserpartno", "mfrpartno", "mfr", "description", "pdf", "availability", "pricingeur", "quantity")

d_msr =  d_msr[ , !(names(d_msr) %in% ignored_headers)]
d_dgk =  d_dgk[ , !(names(d_dgk) %in% ignored_headers)]


rm(ignored_headers)


# ...................................................
##### Initiate empty matrix to store similarity #####
# ...................................................


sim_mat = matrix(data = 0, nrow = ncol(d_msr), ncol = ncol(d_dgk))


# ........................................
##### Calculate tokenized similarity #####
# ........................................

# tokenize column names

msr_tokenized = tokenize_character_shingles(colnames(d_msr), n = 2)
dgk_tokenized = tokenize_character_shingles(colnames(d_dgk), n = 2)


for (i in 1:ncol(d_msr)) {
  
  for (j in 1:ncol(d_dgk)) {
    
    sim_mat[i,j] = jaccard(as.vector(msr_tokenized[[i]]), as.vector(dgk_tokenized[[j]]))
    
  }
  
}


rownames(sim_mat) = colnames(d_msr)
colnames(sim_mat) = colnames(d_dgk)


# ................................
##### Melt similarity matrix #####
# ................................


melted_sim_mat = melt(sim_mat)
# head(melted_cormat)

colnames(melted_sim_mat) = c("mouser_headers", "digikey_headers", "similarity")

# .........................................
##### Print similarity matrix heatmap #####
# .........................................

my_plot = ggplot(data = melted_sim_mat, aes(x=mouser_headers, y=digikey_headers, fill=similarity)) + 
  geom_tile(color = "white")+
  geom_text(aes(label = round(similarity, 1))) +
  scale_fill_gradient2(low = "blue", high = "red", mid = "white", 
                       midpoint = 0.5, limit = c(0,1), space = "Lab", 
                       name="Tokenized Jaccard Similarity") +
  theme_minimal()+ 
  theme(axis.text.x = element_text(angle = 45, vjust = 1, 
                                   size = 12, hjust = 1))+
  coord_fixed()


# ...........................................
##### Create new folder to save outputs #####
# ...........................................

dir.create("tokenized_output")

setwd(paste(master_wd, "tokenized_output", sep = "/"))


# save dataframe

write.csv(melted_sim_mat, "output_list.csv", fileEncoding = "UTF-8", row.names = FALSE)

# save matrix

write.csv(data.frame(sim_mat), "output_matrix.csv", fileEncoding = "UTF-8")

savePlot(my_plot)






