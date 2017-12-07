# test 5: convertMixedExt()

test_that("convertMixedExt()", {
  
  
  d_output = convertMixedExt(d, header = "col6", ext = c(" Hz", " kHz", " MHz"), scaling_factor = c(1, 1000, 1000000))
  
  expect_that(d_output, is_a("data.frame"))
  
  expect_that(ncol(d_output), equals(ncol(d) + 1))
  
  expect_that("col6" %in% colnames(d_output), equals(TRUE))
  
  expect_that("newHeader" %in% colnames(d_output), equals(TRUE))
  
  expect_that(is.numeric(d_output[ , "newHeader"]), equals(TRUE))
  
  expect_that(sum(is.na(d_output[ , "newHeader"])) < nrow(d_output), is_true())
  
  expect_that(grep(" Hz", d_output[ , "newHeader"]), equals(integer(0)))
  
  expect_that(grep(" kHz", d_output[ , "newHeader"]), equals(integer(0)))
  
  expect_that(grep(" MHz", d_output[ , "newHeader"]), equals(integer(0)))
  
})