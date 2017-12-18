# Instructions (Windows)

## Standard code for further use: `colname_mapper_shingled.R`

- Add R to PATH variable.
- Install libraries: `reshape2`, `RecordLinkage`, `plyr`, `ggplot2`, `tokenizers`
- Clone `Wrangling-Functions-in-R` in your computer. (to be replaced by automated testing in circle-ci).
- Open command prompt. Change directory to `..\Wrangling-Functions-in-R\colname-mapping`.
- If you want to use your own data to test, put mouser files in `..\standard`, and digikey files (for now) in `..\remote`.
- Run the following command:
`Rscript colname_mapper_shingled.R "..\Wrangling-Functions-in-R\colname-mapping\test files"`.
- This will create a new folder called "tokenized_output", which will contain results of the operation.
