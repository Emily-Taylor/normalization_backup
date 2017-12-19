# Test colname mapping
# Use one file at a time from two different sources: "standard" and "remote"
# Our target is to map remote source datasets to standard
# Use string matching (Levenstein similarity)


# .........................
##### Clear workspace #####
# .........................

rm(list = ls())

# ........................
##### Read libraries #####
# ........................

library(reshape2)
library(RecordLinkage)
library(plyr)
library(ggplot2)

# .....................................
##### Remove scientific notations #####
# .....................................

options(scipen=999)


# ..................................
##### Master working directory #####
# ..................................

# This directory extension contains the folders "standard" and "remote", which contains corresponding datasets
# Should be passed as a cmd input argument.

args = commandArgs(trailingOnly=TRUE)

# master_wd = "C:/Pin2Pin/NewResearchStuff/colname_mapping/test files"

master_wd = args

setwd(master_wd)

# .........................
##### Read dataframes #####
# .........................

# setwd for standard

std_dir = paste(master_wd, "standard", sep = "/")


if (length(list.files(std_dir)) == 1) {
  
  d_std = read.csv(paste(std_dir, list.files(std_dir), sep = "/"), encoding = "UTF-8")
  
} else if (length(list.files(std_dir)) == 2) {
  
  d_std1 = read.csv(paste(std_dir, list.files(std_dir)[1], sep = "/"), encoding = "UTF-8")
  d_std2 = read.csv(paste(std_dir, list.files(std_dir)[2], sep = "/"), encoding = "UTF-8")
  
  d_std = rbind.fill(d_std1, d_std2)
  
  rm(d_std1, d_std2)
  
} else {
  
  d_std = read.csv(paste(std_dir, list.files(std_dir)[1], sep = "/"), encoding = "UTF-8")
  
  for (i in 2:length(list.files(std_dir))) {
    
    temp = read.csv(paste(std_dir, list.files(std_dir)[i], sep = "/"), encoding = "UTF-8")
    
    d_std = rbind.fill(d_std, temp)
    
    rm(temp)
    
  }
  
}


# setwd for remote

rmt_dir = paste(master_wd, "remote", sep = "/")


if (length(list.files(rmt_dir)) == 1) {
  
  d_rmt = read.csv(paste(rmt_dir, list.files(rmt_dir), sep = "/"), encoding = "UTF-8")
  
} else if (length(list.files(rmt_dir)) == 2) {
  
  d_rmt1 = read.csv(paste(rmt_dir, list.files(rmt_dir)[1], sep = "/"), encoding = "UTF-8")
  d_rmt2 = read.csv(paste(rmt_dir, list.files(rmt_dir)[2], sep = "/"), encoding = "UTF-8")
  
  d_rmt = rbind.fill(d_rmt1, d_rmt2)
  
  rm(d_rmt1, d_rmt2)
  
} else {
  
  d_rmt = read.csv(paste(rmt_dir, list.files(rmt_dir)[1], sep = "/"), encoding = "UTF-8")
  
  for (i in 2:length(list.files(rmt_dir))) {
    
    temp = read.csv(paste(rmt_dir, list.files(rmt_dir)[i], sep = "/"), encoding = "UTF-8")
    
    d_rmt = rbind.fill(d_rmt, temp)
    
    rm(temp)
    
  }
  
}


rm(std_dir, rmt_dir)



# ............................................
##### Convert header names to lower case #####
# ............................................

colnames(d_std) = gsub("\\.", "", tolower(colnames(d_std)))
colnames(d_rmt) = gsub("\\.", "", tolower(colnames(d_rmt)))


# ...................................
##### Remove management headers #####
# ...................................

ignored_headers = c("datetime","category1", "category2", "category3", "manufacturer_part_number", "source", "category", "datasheets", "digikeypartnumber", "manufacturerpartnumber", "manufacturer", "quantityavailable", "factorystock", "unitpriceusd", "xqty", "minimumquantity","select", "image", "series", "product", "qualification", "packagecase", "packaging", "mouserpartno", "mfrpartno", "mfr", "description", "pdf", "availability", "pricingeur", "quantity")

d_std =  d_std[ , !(names(d_std) %in% ignored_headers)]
d_rmt =  d_rmt[ , !(names(d_rmt) %in% ignored_headers)]


rm(ignored_headers)


# ...................................................
##### Initiate empty matrix to store similarity #####
# ...................................................


sim_mat = matrix(data = 0, nrow = ncol(d_std), ncol = ncol(d_rmt))

rownames(sim_mat) = colnames(d_std)
colnames(sim_mat) = colnames(d_rmt)


# ..............................
##### Calculate similarity #####
# ..............................

for (i in 1:ncol(d_rmt)) {
  
  sim_mat[ , i] = levenshteinSim(colnames(d_rmt)[i], colnames(d_std))
  
}


# ................................
##### Melt similarity matrix #####
# ................................


melted_sim_mat = melt(sim_mat)
# head(melted_cormat)

colnames(melted_sim_mat) = c("standard_headers", "remote_headers", "similarity")

# .........................................
##### Print similarity matrix heatmap #####
# .........................................

my_plot = ggplot(data = melted_sim_mat, aes(x=standard_headers, y=remote_headers, fill=similarity)) + 
  geom_tile(color = "white")+
  geom_text(aes(label = round(similarity, 1))) +
  scale_fill_gradient2(low = "blue", high = "red", mid = "white", 
                       midpoint = 0.5, limit = c(0,1), space = "Lab", 
                       name="Levenshtein Similarity") +
  theme_minimal()+ 
  theme(axis.text.x = element_text(angle = 45, vjust = 1, 
                                   size = 12, hjust = 1))+
  coord_fixed()


# ...........................................
##### Create new folder to save outputs #####
# ...........................................

dir.create("levenshtein_output")

setwd(paste(master_wd, "levenshtein_output", sep = "/"))


# save list dataframe

write.csv(melted_sim_mat, "output_list.csv", fileEncoding = "UTF-8", row.names = FALSE)

# save matrix

write.csv(data.frame(sim_mat), "output_matrix.csv", fileEncoding = "UTF-8")

savePlot <- function(myPlot) {
  pdf("output_matrix.pdf")
  print(myPlot)
  dev.off()
}

savePlot(my_plot)










