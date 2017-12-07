# test 4: convertNumExt()

test_that("convertNumExt()", {
  
  
  d_output = convertNumExt(d, header = "col3", ext = "C")
  
  expect_that(d_output, is_a("data.frame"))
  expect_that(ncol(d_output), equals(ncol(d)))
  expect_that("col3" %in% colnames(d_output), equals(FALSE))
  expect_that("col3_C" %in% colnames(d_output), equals(TRUE))
  
})