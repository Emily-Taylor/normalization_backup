# test 5: sepHeader()

test_that("sepHeader()", {
  
  
  d_output = sepHeader(d, header = "col5", separator = " to ")
  
  expect_that(d_output, is_a("data.frame"))
  
  expect_that(ncol(d_output), equals(ncol(d) + 2))
  
  expect_that("col5" %in% colnames(d_output), equals(TRUE))
  
  expect_that("col5_min" %in% colnames(d_output), equals(TRUE))
  
  expect_that("col5_max" %in% colnames(d_output), equals(TRUE))
  
  expect_that(grep(" to ", d_output[ , "col5_min"]), equals(integer(0)))
  
  expect_that(grep(" to ", d_output[ , "col5_max"]), equals(integer(0)))
  
  expect_that(sum(is.na(d_output[ , "col5_min"])) < nrow(d_output), is_true())
  
  expect_that(sum(is.na(d_output[ , "col5_max"])) < nrow(d_output), is_true())
  
})