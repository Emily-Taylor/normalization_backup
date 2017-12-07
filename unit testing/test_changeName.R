# test 3: changeName()

test_that("changeName()", {
  
  
  d_output = changeName(d, header = "col1", new_name = "col_new")
  
  expect_that(d_output, is_a("data.frame"))
  expect_that(ncol(d_output), equals(ncol(d)))
  expect_that("col1" %in% colnames(d_output), equals(FALSE))
  expect_that("col_new" %in% colnames(d_output), equals(TRUE))
 
  
})