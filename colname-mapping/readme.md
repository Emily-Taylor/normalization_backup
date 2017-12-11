# Instructions (Windows)

- Add R to path variable.
- Install libraries: `reshape2`, `RecordLinkage`, `plyr`, `ggplot2`.
- Download colname_mapper.R. Save it in a location, say, "C:\Pin2Pin\NewResearchStuff\colname_mapping".
- In the same location, create 2 folders: "\digikey" and "\mouser."
- Put desired digikey and mouser raw .csv files in respective locations.
- Open cmd. Change directory to the location of the code.
- Run the following command:
`Rscript colname_mapper.R "C:\Pin2Pin\NewResearchStuff\colname_mapping"`
- This will create a new folder called "\output", which will contain results of the operation.
