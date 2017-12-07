# test 5: removeBefore()

test_that("removeBefore()", {
  
  
  d_output = removeBefore(d, header = "col1", separator = ",")
  
  expect_that(d_output, is_a("data.frame"))
  expect_that(ncol(d_output), equals(ncol(d)))
  expect_that("col1" %in% colnames(d_output), equals(TRUE))
  expect_that(grep(".*,", d_output[ , "col1"]), equals(integer(0)))
  
})