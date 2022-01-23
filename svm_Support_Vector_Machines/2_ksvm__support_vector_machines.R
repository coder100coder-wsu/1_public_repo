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

#split data into train-test

# create function for scaling
scale_func = function(a_var) {
  (a_var - min(a_var)) / (max(a_var) - min(a_var))
}

# use lapply to apply function to data
# cast the output of lapply to a data frame
my_data_scaled = as.data.frame(lapply(my_data[, 1:11], scale_func))

# to ensure repeatable results despite random selection
set.seed(123) 

# determine test:train split ratio.
split_ratio = 0.7 # e.g. train:test = 0.7 : (1-0.7)

#split data into test and train
random_sampling = sample(
  1:nrow(my_data_scaled),
  size = nrow(my_data_scaled) * split_ratio,
  replace = FALSE
) #randomly select data.

# capture training and testing, predictors/factors/features 
train_data = my_data_scaled[random_sampling, ]
test_data = my_data_scaled[-random_sampling, ]

# capture training and testing, responses
train_results = train_data[, 11]
test_results = test_data[, 11]
# capturing "known" responses is essential for SVM; this is the "supervised" part
# because SVM is a classifier OR supervised type of machine learning

# predictors/features/variables
x_train <- as.matrix(train_data)
x_test <- as.matrix(test_data)

# target/response
y_train <- as.factor(train_results)
y_test <- as.factor(test_results)

#results=list()
results <- vector(mode = "list", length = 1)
C_set_values <- vector(mode = "list", length = 1)
Accuracy_set_values <- vector(mode = "list", length = 1)
Kernel_set_values <- vector(mode = "list", length = 1)

i_index <- 1

df_of_values <-NA # initialize results df

# runs svm, returns result
func_C_val_test <-function(kernel_name, C_value,x,y,data_set_type)
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
                                     "match_predict" = Accuracy_set_values[1],
                                     "dataset"= data_set_type
                                   )
                        )
  )
  return(df_of_values)
}


test_range <-  c(0.000001, 0.00001, 0.0001, 0.001, 0.1, 1, 10, 100, 1000, 10000)
#class(test_range)
kernel_list <- c("rbfdot","polydot","vanilladot","tanhdot","laplacedot","besseldot","anovadot",
                 "splinedot")
#kernel_list <- c("rbfdot","polydot","vanilladot","tanhdot")

# run svm for each C and each kernel
for (kernel_name in kernel_list)
{
  for (C_value in test_range)
  {
    df_of_values <-func_C_val_test(kernel_name, C_value, x_train, y_train,"training")    
  }    
}  

df_of_values <- rbind(df_of_values,NA)

#results=list()
results <- vector(mode = "list", length = 1)
C_set_values <- vector(mode = "list", length = 1)
Accuracy_set_values <- vector(mode = "list", length = 1)
Kernel_set_values <- vector(mode = "list", length = 1)

i_index <- 1

# run svm for each C and each kernel
for (kernel_name in kernel_list)
{
  for (C_value in test_range)
  {
    df_of_values <-func_C_val_test(kernel_name, C_value, x_test, y_test,"Test")    
  }    
}  

df_of_values
