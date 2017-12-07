# Test 2: remEmpty()

test_that("remEmpty()", {
  
  d$col1 = NA
  
  d_output = remEmpty(d)
  
  expect_that(d_output, is_a("data.frame"))
  expect_that(ncol(d_output), equals(ncol(d) - 1))
  expect_that("col1" %in% colnames(d_output), equals(FALSE))
  
})