# Test 1: cleanBlanck()

test_that("cleanBlanck()", {
  
  d_output = cleanBlanck(d)
  
  expect_that(d_output, is_a("data.frame"))
  expect_that(ncol(d_output), equals(ncol(d)))
  expect_that('' %in% d_output[ , 3], equals(FALSE))
  expect_that('-' %in% d_output[ , 4], equals(FALSE))
  expect_that('*' %in% d_output[ , 3], equals(FALSE))
  
})