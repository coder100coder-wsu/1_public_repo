# becnhmark script, proof of concept to illustrate how to benchmark different regression methods. 
# the datasets are real. the features or predictors are not engineered.
# the responses may or may not be explainable.

library(tidyverse)

max_runs_global = 20 # required by project 20 splits

file_path <- "<ADD DIRECTORY PATH HERE>\\data_set_list.txt" 
# add full file-path if this does not work. e.g. "C:\\datasets\\data_set_list.txt"
# e.g. directory path "C:\\datasets"

df_dataset_names <- as.data.frame(read.csv(file = file_path, header = FALSE, sep=","))

# define class
setClass(
  "data_set_splits",
  slots = list(
    dataset_name = "character",
    model_set_seed = "numeric", # store set seed
    model_run_number = "numeric", # need 20 runs
    train_data = "data.frame", # store with response
    train_results = "numeric", # response also stored separately for convenience
    test_data = "data.frame", # store with response
    test_results = "numeric" # response also stored separately for convenience
  )
)

# store avergae results
df_average_results_global = data.frame(
  'dataset_name' = NA,
  'model_run_number' = 0L, #integer
  'RMSE' = 0.0,
  'MAE' = 0.0,
  'bnch_median_secs' = 0.0
)

# rename columns
rename_cols_func <- function(df_1_arg){
  
  df_1 = df_1_arg
  
  names(df_1) <-
    c( 
      "response", 
      "predictor_1", 
      "predictor_2", 
      "predictor_3" 
    )
  return(df_1)
}

# abalone
pre_proc_func_1 <- function(df_original_arg){
    df_1 <- data.frame(
        df_original[,9] , # response
        df_original[,2], # predictor
        df_original[,3], # predictor
        df_original[,4] # predictor
      )
   
    df_1 <-  na.omit(df_1)
    df_1 <- rename_cols_func (df_1_arg = df_1)
  
  return(df_1)
}

# airfoil
pre_proc_func_2 <- function(df_original_arg){
  df_1 <- data.frame(
    df_original[,6] , # response
    df_original[,1], # predictor
    df_original[,2], # predictor
    df_original[,3] # predictor
  )
  
  df_1 <-  na.omit(df_1)
  df_1 <- rename_cols_func (df_1_arg = df_1)
  
  return(df_1)
}

# auto-mpg
pre_proc_func_3 <- function(df_original_arg){
  df_1 <- data.frame(
    df_original[,1] , # response
    df_original[,3], # predictor_1
    as.numeric(df_original[,4]), # predictor_2
    df_original[,5] # predictor_3
  )
  
  df_1 <-  na.omit(df_1)
  
  df_1 <- rename_cols_func (df_1_arg = df_1)
  
  return(df_1)
}

# automobile
pre_proc_func_4 <- function(df_original_arg){
  df_1 <- data.frame(
    as.numeric(df_original[,26]) , # response
    as.numeric(df_original[,25]) , # predictor
    as.numeric(df_original[,22]) , # predictor
    as.numeric(df_original[,14])  # predictor
  )
  
  df_1 <-  na.omit(df_1)
  df_1 <- rename_cols_func (df_1_arg = df_1)
  
  return(df_1)
}

# bike_data
pre_proc_func_5 <- function(df_original_arg){
  df_1 <- data.frame(
    as.numeric(df_original[,2]) , # response
    as.numeric(df_original[,4]) , # predictor
    as.numeric(df_original[,5]) , # predictor
    as.numeric(df_original[,8])  # predictor
  )
  
  df_1 <-  na.omit(df_1)
  df_1 <- rename_cols_func (df_1_arg = df_1)
  
  return(df_1)
}

# _bike_sharing
pre_proc_func_6 <- function(df_original_arg){
  df_1 <- data.frame(
    as.numeric(df_original[,16]) , # response
    as.numeric(df_original[,10]) , # predictor
    as.numeric(df_original[,12]) , # predictor
    as.numeric(df_original[,13])  # predictor
  )
  
  df_1 <-  na.omit(df_1)
  df_1 <- rename_cols_func (df_1_arg = df_1)
  
  return(df_1)
}

# _bldg_energy
pre_proc_func_7 <- function(df_original_arg){
  df_1 <- data.frame(
    as.numeric(df_original[,9]) , # response
    as.numeric(df_original[,2]) , # predictor
    as.numeric(df_original[,3]) , # predictor
    as.numeric(df_original[,4])  # predictor
  )
  
  df_1 <-  na.omit(df_1)
  df_1 <- rename_cols_func (df_1_arg = df_1)
  
  return(df_1)
}

# _computer_hardware
pre_proc_func_8 <- function(df_original_arg){
  df_1 <- data.frame(
    as.numeric(df_original[,10]) , # response
    as.numeric(df_original[,9]) , # predictor
    as.numeric(df_original[,6]) , # predictor
    as.numeric(df_original[,3])  # predictor
  )
  
  df_1 <-  na.omit(df_1)
  df_1 <- rename_cols_func (df_1_arg = df_1)
  
  return(df_1)
}

# _fb_metrics
pre_proc_func_9 <- function(df_original_arg){
  df_1 <- data.frame(
    as.numeric(df_original[,19]) , # response
    as.numeric(df_original[,10]) , # predictor
    as.numeric(df_original[,11]) , # predictor
    as.numeric(df_original[,18])  # predictor
  )
  
  df_1 <-  na.omit(df_1)
  df_1 <- rename_cols_func (df_1_arg = df_1)
  
  return(df_1)
}

# _fire_index
pre_proc_func_10 <- function(df_original_arg){
  df_1 <- data.frame(
    as.numeric(df_original[,13]) , # response
    as.numeric(df_original[,7]) , # predictor
    as.numeric(df_original[,6]) , # predictor
    as.numeric(df_original[,4])  # predictor
  )
  
  df_1 <-  na.omit(df_1)
  df_1 <- rename_cols_func (df_1_arg = df_1)
  
  return(df_1)
}

# _fish_toxic
pre_proc_func_11 <- function(df_original_arg){
  df_1 <- data.frame(
    as.numeric(df_original[,7]) , # response
    as.numeric(df_original[,1]) , # predictor
    as.numeric(df_original[,2]) , # predictor
    as.numeric(df_original[,3])  # predictor
  )
  
  df_1 <-  na.omit(df_1)
  df_1 <- rename_cols_func (df_1_arg = df_1)
  
  return(df_1)
}

# _forest_fires
pre_proc_func_12 <- function(df_original_arg){
  df_1 <- data.frame(
    as.numeric(df_original[,7]) , # response
    as.numeric(df_original[,10]) , # predictor
    as.numeric(df_original[,9]) , # predictor
    as.numeric(df_original[,8])  # predictor
  )
  
  df_1 <-  na.omit(df_1)
  df_1 <- rename_cols_func (df_1_arg = df_1)
  
  return(df_1)
}

# _game
pre_proc_func_13 <- function(df_original_arg){
  df_1 <- data.frame(
    as.numeric(df_original[,18]) , # response
    as.numeric(df_original[,5]) , # predictor
    as.numeric(df_original[,7]) , # predictor
    as.numeric(df_original[,9])  # predictor
  )
  
  df_1 <-  na.omit(df_1)
  df_1 <- rename_cols_func (df_1_arg = df_1)
  
  return(df_1)
}

# _gas_turbine
pre_proc_func_14 <- function(df_original_arg){
  df_1 <- data.frame(
    as.numeric(df_original[,8]) , # response
    as.numeric(df_original[,1]) , # predictor
    as.numeric(df_original[,2]) , # predictor
    as.numeric(df_original[,3])  # predictor
  )
  
  df_1 <-  na.omit(df_1)
  df_1 <- rename_cols_func (df_1_arg = df_1)
  
  return(df_1)
}

# _heart_fail
pre_proc_func_15 <- function(df_original_arg){
  df_1 <- data.frame(
    as.numeric(df_original[,5]) , # response
    as.numeric(df_original[,1]) , # predictor
    as.numeric(df_original[,3]) , # predictor
    as.numeric(df_original[,7])  # predictor
  )
  
  df_1 <-  na.omit(df_1)
  df_1 <- rename_cols_func (df_1_arg = df_1)
  
  return(df_1)
}

# _home_costs
pre_proc_func_16 <- function(df_original_arg){
  df_1 <- data.frame(
    as.numeric(df_original[,4]) , # response
    as.numeric(df_original[,1]) , # predictor
    as.numeric(df_original[,2]) , # predictor
    as.numeric(df_original[,3])  # predictor
  )
  
  df_1 <-  na.omit(df_1)
  df_1 <- rename_cols_func (df_1_arg = df_1)
  
  return(df_1)
}

# _movies
pre_proc_func_17 <- function(df_original_arg){
  df_1 <- data.frame(
    as.numeric(df_original[,5]) , # response
    as.numeric(df_original[,6]) , # predictor
    as.numeric(df_original[,7]) , # predictor
    as.numeric(df_original[,14])  # predictor
  )
  
  df_1 <-  na.omit(df_1)
  df_1 <- rename_cols_func (df_1_arg = df_1)
  
  return(df_1)
}

# _music
pre_proc_func_18 <- function(df_original_arg){
  
  df_1 <- data.frame(
    as.numeric(df_original[,1]) , # response
    as.numeric(df_original[,2]) , # predictor
    as.numeric(df_original[,3]) , # predictor
    as.numeric(df_original[,4])  # predictor
  )
  
  df_1 <-  na.omit(df_1)
  df_1 <- rename_cols_func (df_1_arg = df_1)
  return(df_1)
}

# _optical
pre_proc_func_19 <- function(df_original_arg){
  
  df_1 <- data.frame(
    as.numeric(df_original[,1]) , # response
    as.numeric(df_original[,2]) , # predictor
    as.numeric(df_original[,3]) , # predictor
    as.numeric(df_original[,4])  # predictor
  )
  
  df_1 <-  na.omit(df_1)
  df_1 <- rename_cols_func (df_1_arg = df_1)

  return(df_1)
}

# _parkinsons
pre_proc_func_20 <- function(df_original_arg){
  df_1 <- data.frame(
    as.numeric(df_original[,6]) , # response
    as.numeric(df_original[,21]) , # predictor
    as.numeric(df_original[,22]) , # predictor
    as.numeric(df_original[,2])  # predictor
  )
  
  df_1 <-  na.omit(df_1)
  df_1 <- rename_cols_func (df_1_arg = df_1)
  
  return(df_1)
}

# _power_plant
pre_proc_func_21 <- function(df_original_arg){
  
  df_1 <- data.frame(
    as.numeric(df_original[,5]) , # response
    as.numeric(df_original[,1]) , # predictor
    as.numeric(df_original[,2]) , # predictor
    as.numeric(df_original[,3])  # predictor
  )
  
  df_1 <-  na.omit(df_1)
  df_1 <- rename_cols_func (df_1_arg = df_1)
  return(df_1)
}

# _productivity
pre_proc_func_22 <- function(df_original_arg){

  df_1 <- data.frame(
    as.numeric(df_original[,15]) , # response
    as.numeric(df_original[,14]) , # predictor
    as.numeric(df_original[,9]) , # predictor
    as.numeric(df_original[,8])  # predictor
  )
  
  df_1 <-  na.omit(df_1)
  df_1 <- rename_cols_func (df_1_arg = df_1)
  
  return(df_1)
}

# _real_estate
pre_proc_func_23 <- function(df_original_arg){
  df_1 <- data.frame(
    as.numeric(df_original[,8]) , # response
    as.numeric(df_original[,3]) , # predictor
    as.numeric(df_original[,4]) , # predictor
    as.numeric(df_original[,5])  # predictor
  )
  
  df_1 <-  na.omit(df_1)
  df_1 <- rename_cols_func (df_1_arg = df_1)
  
  return(df_1)
}

# _stocks
pre_proc_func_24 <- function(df_original_arg){

  df_1 <- data.frame(
    as.numeric(df_original[,2]), #response
    as.numeric(df_original[,1]) , # predictor
    as.numeric(df_original[,4]) , # predictor
    as.numeric(df_original[,5])  # predictor
  )
  
  df_1 <-  na.omit(df_1)
  df_1 <- rename_cols_func (df_1_arg = df_1)
  
  return(df_1)
}

# _stock_istanbul
pre_proc_func_25 <- function(df_original_arg){
  df_1 <- data.frame(
    as.numeric(df_original[,1]) , # response
    as.numeric(df_original[,2]) , # predictor
    as.numeric(df_original[,3]) , # predictor
    as.numeric(df_original[,4])  # predictor
  )
  
  df_1 <-  na.omit(df_1)
  df_1 <- rename_cols_func (df_1_arg = df_1)
  
  return(df_1)
}

# _student
pre_proc_func_26 <- function(df_original_arg){
  df_1 <- data.frame(
    as.numeric(df_original[,31]) , # response
    as.numeric(df_original[,3]) , # predictor
    as.numeric(df_original[,27]) , # predictor
    as.numeric(df_original[,29])  # predictor
  )
  
  df_1 <-  na.omit(df_1)
  df_1 <- rename_cols_func (df_1_arg = df_1)
  
  return(df_1)
}

# _synchro_machine
pre_proc_func_27 <- function(df_original_arg){
  df_1 <- data.frame(
    as.numeric(gsub(",", "",as.character(df_original_arg[,1]))) , # response
    as.numeric(gsub(",", "",as.character(df_original_arg[,2]))) , # predictor
    as.numeric(gsub(",", "",as.character(df_original_arg[,3]))) , # predictor
    as.numeric(gsub(",", "",as.character(df_original_arg[,4])))  # predictor
  )
  
  df_1 <-  na.omit(df_1)
  df_1 <- rename_cols_func (df_1_arg = df_1)
  
  return(df_1)
}

# _trip_advisor
pre_proc_func_28 <- function(df_original_arg){
  df_1 <- data.frame(
    as.numeric(gsub(",", "",as.character(df_original_arg[,5]))) , # response
    as.numeric(gsub(",", "",as.character(df_original_arg[,2]))) , # predictor
    as.numeric(gsub(",", "",as.character(df_original_arg[,4]))) , # predictor
    as.numeric(gsub(",", "",as.character(df_original_arg[,18])))  # predictor
  )
  
  df_1 <-  na.omit(df_1)
  df_1 <- rename_cols_func (df_1_arg = df_1)
  
  return(df_1)
}

# _wine
pre_proc_func_29 <- function(df_original_arg){
  df_1 <- data.frame(
    as.numeric(df_original[,12]) , # response
    as.numeric(df_original[,1]) , # predictor
    as.numeric(df_original[,5]) , # predictor
    as.numeric(df_original[,11])  # predictor
  )
  
  df_1 <-  na.omit(df_1)
  df_1 <- rename_cols_func (df_1_arg = df_1)
  
  return(df_1)
}

# _yacht
pre_proc_func_30 <- function(df_original_arg){
  df_1 <- data.frame(
    as.numeric(df_original[,7]) , # response
    as.numeric(df_original[,4]) , # predictor
    as.numeric(df_original[,5]) , # predictor
    as.numeric(df_original[,6])  # predictor
  )
  
  df_1 <-  na.omit(df_1)
  df_1 <- rename_cols_func (df_1_arg = df_1)
  
  return(df_1)
}


# split into train and test data sets
train_test_split_func <- function(df_1_arg, dataset_name, model_run_number) {
  
  df_1 <- df_1_arg
  # Specify 70-30 train-test split
  split_ratio_main = 0.7 
  # set seed for reproducible results
  set_seed = model_run_number*100 + 23
  set.seed(set_seed)
  
  random_sampling_one <- caret::createDataPartition(df_1$response,
                                                    p = split_ratio_main,
                                                    list = FALSE,
                                                    times = 1)
  
  # train data
  train_data = df_1[random_sampling_one, ]
  train_results = train_data$response
  
  # test data
  test_data = df_1[-random_sampling_one,]
  test_results = test_data$response
  
  obj_instance <-
    new(
      "data_set_splits",
      dataset_name = dataset_name,
      model_set_seed = set_seed,
      model_run_number = model_run_number,
      train_data = train_data,
      train_results = train_results,
      test_data = test_data,
      test_results = test_results
    )
  
  #return results
  return(obj_instance)
  
}


# benchmark func
benchmark_func <- function(model_var_obj){
  #benchmark_median_secs
  mbm_obj <- microbenchmark::microbenchmark(model_name = { model_var_obj$coef })
  #calculate median time. 
  mbm_median <- median(mbm_obj$time)/1000 #div by 1000 since mbm time is micro_seconds
  return(mbm_median) # return time_value in seconds
}


# linear regression func
lm_func <- function(list_index, list_objects_arg){
  
  list_objects_data_set_splits = list_objects_arg
  # train data
  train_data = list_objects_data_set_splits[[list_index]]@train_data
  train_results = list_objects_data_set_splits[[list_index]]@train_results
  
  # test data
  test_data = list_objects_data_set_splits[[list_index]]@test_data
  test_results = list_objects_data_set_splits[[list_index]]@test_results
  
  #get training data
  df_var_obj <- train_data
  #train model
  model_var_obj <- stats::lm(data= train_data, formula= response~.)
  smry_model <- summary(model_var_obj)
  # predict on testing data
  yhat_1 <- predict(object = model_var_obj, newdata = test_data)
  # get metrics on model performance on testing data
  new_row = data.frame(
    'dataset_name' = dataset_name_global,
    'model_run_number' = list_index,
    'RMSE' = round(Metrics::rmse(predicted = yhat_1, actual = test_results), 3),
    'MAE' = round(Metrics::mae(predicted = yhat_1, actual = test_results), 3),
    'bnch_median_secs' = benchmark_func(model_var_obj)
  )
  
  #return metrics
  return(new_row)
}


# random forest func
random_forest_func <- function(list_index, list_objects_arg){
  
  list_objects_data_set_splits = list_objects_arg
  
  # train data
  train_data = list_objects_data_set_splits[[list_index]]@train_data
  train_results = list_objects_data_set_splits[[list_index]]@train_results
  
  # test data
  test_data = list_objects_data_set_splits[[list_index]]@test_data
  test_results = list_objects_data_set_splits[[list_index]]@test_results
  
  #get training data
  df_var_obj <- train_data
  #train model
  model_var_obj <- randomForest::randomForest(response ~ ., data = train_data)
  
  smry_model <- summary(model_var_obj)
  # predict on testing data
  yhat_1 <- predict(object = model_var_obj, newdata = test_data)
  # get metrics on model performance on testing data
  new_row = data.frame(
    'dataset_name' = paste(c("randfor_",dataset_name_global),collapse = ""),
    'model_run_number' = list_index,
    'RMSE' = round(Metrics::rmse(predicted = yhat_1, actual = test_results), 3),
    'MAE' = round(Metrics::mae(predicted = yhat_1, actual = test_results), 3),
    'bnch_median_secs' = benchmark_func(model_var_obj)
  )
  
  #return metrics
  return(new_row)
}


# support vector func
svr_func <- function(list_index, list_objects_arg, svm_kernel_input, svm_regression_type_input){
  
  list_objects_data_set_splits = list_objects_arg
  
  # train data
  train_data = list_objects_data_set_splits[[list_index]]@train_data
  train_results = list_objects_data_set_splits[[list_index]]@train_results
  
  # test data
  test_data = list_objects_data_set_splits[[list_index]]@test_data
  test_results = list_objects_data_set_splits[[list_index]]@test_results
  
  #get training data
  df_var_obj <- train_data
  #train model
  model_var_obj <- e1071::svm(train_data$response ~ as.matrix(train_data[,c(2:4)]), 
                              data = train_data, 
                              kernel = svm_kernel_input,
                              type = svm_regression_type_input)
  
  smry_model <- summary(model_var_obj)
  # predict on testing data
  yhat_1 <- predict(object = model_var_obj, newdata = test_data)
  # get metrics on model performance on testing data
  new_row = data.frame(
    'dataset_name' = paste(
      c(
        "svr_",
        svm_regression_type_input,
        "_",
        svm_kernel_input,
        "_",
        dataset_name_global
      ),
      collapse = ""
    ),
    'model_run_number' = list_index,
    'RMSE' = round(Metrics::rmse(predicted = yhat_1, actual = test_results), 3),
    'MAE' = round(Metrics::mae(predicted = yhat_1, actual = test_results), 3),
    'bnch_median_secs' = benchmark_func(model_var_obj)
  )
  
  #return metrics
  return(new_row)
}


# main loop
for (file_name in df_dataset_names[1:30,]){ # modify to 1:row_qty
  #print(file_name)
  data_set_name_string <- substring(file_name, 2)
  print(data_set_name_string)
  dataset_name_global = paste(c("rfa_",data_set_name_string),collapse = "")
  
  dir_path_1 <-"<ADD DIRECTORY PATH HERE>\\"

  file_path <- paste(c(data_set_name_string,".csv"),collapse = "")
  df_original <- as.data.frame(read.csv(file = file_path, header = TRUE, sep=","))
  
  df_original <- subset(df_original, select = -X)
  # omit na values. For purpose of this project, no study is done as to how many values are na and why.
  df_original <-  na.omit(df_original)
  
  #print(head(df_original,3))
  
  if (data_set_name_string == "abalone") {
    df_pre_proc <-  pre_proc_func_1(df_original_arg = df_original) 
  }
  
  if (data_set_name_string == "airfoil") {
    df_pre_proc <-  pre_proc_func_2(df_original_arg = df_original) 
  }
  
  if (data_set_name_string == "auto-mpg") {
    df_pre_proc <-  pre_proc_func_3(df_original_arg = df_original) 
  }
  
  if (data_set_name_string == "automobile") {
    df_pre_proc <-  pre_proc_func_4(df_original_arg = df_original) 
  }
  
  if (data_set_name_string == "bike_data") {
    df_pre_proc <-  pre_proc_func_5(df_original_arg = df_original) 
  }
  
  if (data_set_name_string == "bike_sharing") {
    df_pre_proc <-  pre_proc_func_6(df_original_arg = df_original) 
  }
  
  if (data_set_name_string == "bldg_energy") {
    df_pre_proc <-  pre_proc_func_7(df_original_arg = df_original) 
  }
  
  if (data_set_name_string == "computer_hardware") {
    df_pre_proc <-  pre_proc_func_8(df_original_arg = df_original) 
  }
  
  if (data_set_name_string == "fb_metrics") {
    df_pre_proc <-  pre_proc_func_9(df_original_arg = df_original) 
  }
  
  if (data_set_name_string == "fire_index") {
    df_pre_proc <-  pre_proc_func_10(df_original_arg = df_original) 
  }
  
  if (data_set_name_string == "fish_toxic") {
    df_pre_proc <-  pre_proc_func_11(df_original_arg = df_original) 
  }
  
  if (data_set_name_string == "forest_fires") {
    df_pre_proc <-  pre_proc_func_12(df_original_arg = df_original) 
  }
  
  if (data_set_name_string == "game") {
    df_pre_proc <-  pre_proc_func_13(df_original_arg = df_original) 
  }
  
  if (data_set_name_string == "gas_turbine") {
    df_pre_proc <-  pre_proc_func_14(df_original_arg = df_original) 
  }
  
  if (data_set_name_string == "heart_fail") {
    df_pre_proc <-  pre_proc_func_15(df_original_arg = df_original) 
  }
  
  if (data_set_name_string == "home_costs") {
    df_pre_proc <-  pre_proc_func_16(df_original_arg = df_original) 
  }
  
  if (data_set_name_string == "movies") {
    df_pre_proc <-  pre_proc_func_17(df_original_arg = df_original) 
  }
  
  if (data_set_name_string == "music") {
    df_pre_proc <-  pre_proc_func_18(df_original_arg = df_original) 
  }
  
  if (data_set_name_string == "optical") {
    df_pre_proc <-  pre_proc_func_19(df_original_arg = df_original) 
  }
  
  if (data_set_name_string == "parkinsons") {
    df_pre_proc <-  pre_proc_func_20(df_original_arg = df_original) 
  }
  
  if (data_set_name_string == "power_plant") {
    df_pre_proc <-  pre_proc_func_21(df_original_arg = df_original) 
  }
  
  if (data_set_name_string == "productivity") {
    df_pre_proc <-  pre_proc_func_22(df_original_arg = df_original) 
  }
  
  if (data_set_name_string == "real_estate") {
    df_pre_proc <-  pre_proc_func_23(df_original_arg = df_original) 
  }
  
  if (data_set_name_string == "stocks") {
    df_pre_proc <-  pre_proc_func_24(df_original_arg = df_original) 
  }
  
  if (data_set_name_string == "stock_istanbul") {
    df_pre_proc <-  pre_proc_func_25(df_original_arg = df_original) 
  }
  
  if (data_set_name_string == "student") {
    df_pre_proc <-  pre_proc_func_26(df_original_arg = df_original) 
  }
  
  if (data_set_name_string == "synchro_machine") {
    df_pre_proc <-  pre_proc_func_27(df_original_arg = df_original) 
  }
  
  if (data_set_name_string == "trip_advisor") {
    df_pre_proc <-  pre_proc_func_28(df_original_arg = df_original) 
  }
  
  if (data_set_name_string == "wine") {
    df_pre_proc <-  pre_proc_func_29(df_original_arg = df_original) 
  }
  
  if (data_set_name_string == "yacht") {
    df_pre_proc <-  pre_proc_func_30(df_original_arg = df_original) 
  }
  
  #print(summary(b))
  #print(head(df_pre_proc,3))
  
  # need 20 runs of data splits per Project
  max_runs = max_runs_global
  
  # Create list of objects
  list_objects_data_set_splits <- vector(mode = "list", length = 1)
  
  for (iter_1 in 1:max_runs) {
    # create object instance
    split_data_obj <- train_test_split_func(dataset_name = dataset_name_global,
                                            model_run_number = iter_1,
                                            df_1_arg = df_pre_proc)
    # append to list of objects
    list_objects_data_set_splits[iter_1] <- split_data_obj
  }

  #print(length(list_objects_data_set_splits))
  #print(str(list_objects_data_set_splits[1]))
  
  # store results
  df_results = data.frame(
    'dataset_name' = NA,
    'model_run_number' = 0L, #integer
    'RMSE' = 0.0,
    'MAE' = 0.0,
    'bnch_median_secs' = 0.0
  )
  
  df_average_results = data.frame(
    'dataset_name' = NA,
    'model_run_number' = 0L, #integer
    'RMSE' = 0.0,
    'MAE' = 0.0,
    'bnch_median_secs' = 0.0
  )
  
  
  # linear model func call
  for (iter_1 in 1:max_runs){
    new_row <- lm_func(list_index = iter_1, 
                       list_objects_arg = list_objects_data_set_splits)
    df_results <- rbind(df_results, new_row)
  }
  
  # report average performance
  average_row = data.frame(
    'dataset_name' = paste(c("avg_lm_",dataset_name_global), collapse = ""),
    'model_run_number' = 21,
    'RMSE' = round(mean(df_results$RMSE), 3),
    'MAE' = round(mean(df_results$MAE), 3),
    'bnch_median_secs' = round(mean(df_results$bnch_median_secs), 3)
  )
  
  # lm average
  df_average_results <- rbind(df_average_results, average_row)
  
  # random forest func call
  for (iter_1 in 1:max_runs){
    new_row <- random_forest_func(list_index = iter_1, 
                                  list_objects_arg = list_objects_data_set_splits)
    df_results <- rbind(df_results, new_row)
  }
  
  # report average performance
  average_row = data.frame(
    'dataset_name' = paste(c("avg_rforest_",dataset_name_global), collapse = ""),
    'model_run_number' = 31,
    'RMSE' = round(mean(df_results$RMSE), 3),
    'MAE' = round(mean(df_results$MAE), 3),
    'bnch_median_secs' = round(mean(df_results$bnch_median_secs), 3)
  )
  
  # random forest average
  df_average_results <- rbind(df_average_results, average_row)
  
  # support vector func call
  svm_kernel_list = c("linear","polynomial", "sigmoid", "radial")
  svm_regression_type_list = c("nu-regression","eps-regression")
  
  for (svm_regression_type in svm_regression_type_list){
    for (kernel_name in svm_kernel_list){
      # start_row = nrow(df_results)
      # end_row = 2

      for (iter_1 in 1:max_runs){
        new_row <- svr_func(list_index = iter_1,
                            svm_kernel_input = kernel_name,
                            svm_regression_type_input = svm_regression_type,
                            list_objects_arg = list_objects_data_set_splits)
        df_results <- rbind(df_results, new_row)
      }

      # report average performance
      average_row = data.frame(
        'dataset_name' = paste(
          c(
            "avg_svr_", svm_regression_type,
            "_",kernel_name,
            "_",dataset_name_global
          ),
          collapse = ""
        ),
        'model_run_number' = 41,
        'RMSE' = round(mean(df_results$RMSE), 3),
        'MAE' = round(mean(df_results$MAE), 3),
        'bnch_median_secs' = round(mean(df_results$bnch_median_secs), 3)
      )

      df_average_results <- rbind(df_average_results, average_row)
    }
  }
  
  #store results globally
  for(i in 1:nrow(df_average_results)){
    df_average_results_global <- rbind(df_average_results_global, df_average_results[i,])
  }
}

df_average_results_global<-df_average_results_global[,-2]

rownames(df_average_results_global) <- 1:nrow(df_average_results_global)
#View(df_average_results_global)

avg_results_file_path = "<ADD DIRECTORY PATH HERE>\\avg_results_df.csv"

write.csv(x=df_average_results_global, file= avg_results_file_path)












