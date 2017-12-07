# test 5: convertCatExt()

test_that("convertCatExt()", {
  
  
  d_output = convertCatExt(d, header = "col4", ext = " .*")
  
  expect_that(d_output, is_a("data.frame"))
  expect_that(ncol(d_output), equals(ncol(d)))
  expect_that("col4" %in% colnames(d_output), equals(TRUE))
  expect_that(grep(" .*", d_output[ , "col4"]), equals(integer(0)))
  
})