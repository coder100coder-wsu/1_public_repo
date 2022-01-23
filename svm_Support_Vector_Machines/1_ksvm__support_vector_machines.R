# ##########################################################################
rm(list = ls())
options(digits = 5)
# if (!is.null(dev.list())){dev.off()}
# #########################################################################

library(kernlab) # Kernel-based machine learning methods
library(ggplot2)
library(reshape2)
library(dplyr)

# read file. Use credit_card_data.txt
my_data <- read.table(file.choose(), header=FALSE, sep = "", dec=".")

# no train-test split. use all data. demonstration of svm.
# predictors/features/variables
x =as.matrix(my_data[, 1:10])

# target/response
y = as.factor(my_data[, 11])

#results=list()
results <- vector(mode = "list", length = 1)
C_set_values <- vector(mode = "list", length = 1)
Accuracy_set_values <- vector(mode = "list", length = 1)
Kernel_set_values <- vector(mode = "list", length = 1)

i_index <- 1
test_range <-  c(0.000001, 0.00001, 0.0001, 0.001, 0.1, 1, 10, 100, 1000, 10000)

class(test_range)

kernel_list <- c("rbfdot","polydot","vanilladot","tanhdot","laplacedot","besseldot","anovadot",
                 "splinedot")
#kernel_list <- c("rbfdot","polydot","vanilladot","tanhdot")

df_of_values <-NA # initialize results df

func_C_val_test <-function(kernel_name, C_value)
{
  model <- ksvm(y~x,scaled=TRUE, type="C-svc", kernel= kernel_name, C=C_value, kpar="automatic")
  a <- colSums(model@xmatrix[[1]] * model@coef[[1]])
  a0 <- model@b * (-1)
  predict_y <- predict(model,x)
  qty_predict_is_actual <- sum(predict_y == y)
  total_observations <- nrow(my_data)
  match_predict <-  qty_predict_is_actual / total_observations
  C_set_values[i_index] <- C_value 
  Accuracy_set_values[i_index] <- match_predict
  Kernel_set_values[i_index] <- kernel_name
  i_index <- i_index + 1
  
  df_of_values <- rbind(df_of_values, 
                        data.frame("kernel_name"= kernel_name, 
                                   c("C_value"=C_set_values[1], 
                                     "match_predict" = Accuracy_set_values[1]
                                   )
                        )
  )
  return(df_of_values)
}

for (kernel_name in kernel_list)
{
  for (C_value in test_range)
  {
    df_of_values <-func_C_val_test(kernel_name, C_value)    
  }    
}  


df_of_values



