library(datasets)
library(tidyverse)

# new dataset with datapoints of treatment 1 group along with control group
ds_1 <- dplyr::filter(datasets::PlantGrowth, group=="trt1"|group=="ctrl") 
#str(ds_1)

# new dataset with datapoints of treatment 2 group along with control group
ds_2 <- dplyr::filter(datasets::PlantGrowth, group=="trt2"|group=="ctrl") 
#str(ds_2)

# add dummy variable for predictor=group
ds_1$dummy_var <- ifelse(ds_1$group=="trt1",1,0)
head(ds_1,2)
tail(ds_1,2)

# run a linear regression to understand for the case of ds_1$group=="ctrl" i.e. ds_1$dummy_var = 0
reg_0 <- lm(weight ~  1, data = dplyr::filter(ds_1,dummy_var == 0))
summary(reg_0)

# run a linear regression to understand for the case of ds_1$group=="trt1" i.e. ds_1$dummy_var = 1
reg_1 <- lm(weight ~  1, data = dplyr::filter(ds_1,dummy_var == 1))
summary(reg_1)

# run a linear regression using all the data using dummy variable for group
reg_all_1 <- lm(data= ds_1, formula= weight ~ dummy_var)
summary(reg_all_1)
# model is: weight = b0 + b1*dummy_var + e ; 
# dummy_var is dummy variable for group
# 5.0320 is the (average) weight for ds_1$group=="ctrl" (i.e., dummy_var = 0)
# 5.0320+(-0.3710)=4.661 is the (average) weight for ds_1$group=="trt1" (i.e., dummy_var = 1)
# (-0.3710) is the value of the difference estimator, b1


# add dummy variable for predictor=group
ds_2$dummy_var <- ifelse(ds_2$group=="trt2",1,0)
head(ds_2,2)
tail(ds_2,2)

# run a linear regression using all the data using dummy variable for group
reg_all_2 <- lm(data= ds_2, formula= weight ~ dummy_var)
summary(reg_all_2)
# model is: weight = b0 + b1*dummy_var + e ; 
# dummy_var is dummy variable for group
# 5.0320 is the (average) weight for ds_2$group=="ctrl" (i.e., dummy_var = 0)
# 5.0320+(0.4940)=5.526 is the (average) weight for ds_2$group=="trt2" (i.e., dummy_var = 1)
# (0.4940) is the value of the difference estimator, b1

# commentary on average weight
# 5.0320 is the (average) weight for ds_2$group=="ctrl" (i.e., dummy_var = 0)
# 5.0320+(-0.3710)=4.661 is the (average) weight for ds_1$group=="trt1" (i.e., dummy_var = 1)
# 5.0320+(0.4940)=5.526 is the (average) weight for ds_2$group=="trt2" (i.e., dummy_var = 1)

# highest average weight
# highest average weight (5.526) observed for treatment-2 group

# check if group is randomly assigned, i.e. ds_1$dummy_var = 0
reg_random_check <- lm(dummy_var ~ weight, data = ds_1)
summary(reg_random_check)

# check if group is randomly assigned, i.e. ds_1$dummy_var = 0
reg_random_check <- lm(dummy_var ~ 1, data = ds_1)
summary(reg_random_check)
######################################################################################

df_1 <- read.csv("Min_Wage.csv")
str(df_1)
head(df_1,2)

# d = 0 indicates the data was collected before the law was changed
# d = 1 indicates the data was collected after the law was changed
# State = New Jersey ,the worker is from NJ, else worker is not from NJ (is from Philadelphia)
# 'fte' contains the number of hours worked by a full time employee. 

# This is a Natural Experiemnt
# subjects (workers) are undergoing "treatment" (law change by State of New Jersey)
# BUT subjects are not able to choose if they are in treatment or control group

# treatment/treated group= subjects in State of New Jersey
# control group= subjects in other state i.e.  Philadelphia

# Group A: Workers in Philadelphia BEFORE law changed

# Group B: Workers in New Jersey BEFORE law changed

# Group C: Workers in Philadelphia AFTER law changed

# Group D: Workers in New Jersey AFTER law changed

# dummy var for state, 1=NJ, 0=Philly
df_1$dummy_var <- ifelse(df_1$State=="New Jersey",1,0)
head(df_1,2)
tail(df_1,2)

# Group A: Workers in Philadelphia BEFORE law changed
df_A <- dplyr::filter(df_1, dummy_var==0 & d==0) 
str(df_A)
summary(df_A)
head(df_A,2)
tail(df_A,2)

# Group B: Workers in New Jersey BEFORE law changed
df_B <- dplyr::filter(df_1, dummy_var==1 & d==0) 
str(df_B)
summary(df_B)
head(df_B,2)
tail(df_B,2)

# Group C: Workers in Philadelphia AFTER law changed
df_C <- dplyr::filter(df_1, dummy_var==0 & d==1) 
str(df_C)
summary(df_C)
head(df_C,2)
tail(df_C,2)

# Group D: Workers in New Jersey AFTER law changed
df_D <- dplyr::filter(df_1, dummy_var==1 & d==1) 
str(df_D)
summary(df_D)
head(df_D,2)
tail(df_D,2)

# Calculate the mean of the 'fte' variable for each of the four groups in R and print them
paste0(c("Mean of 'fte' for Group A: Workers in Philadelphia BEFORE law changed: ",round(mean(df_A$fte),3)), collapse="")
paste0(c("Mean of 'fte' for Group B: Workers in New Jersey BEFORE law changed: ",round(mean(df_B$fte),3)), collapse="")
paste0(c("Mean of 'fte' for Group C: Workers in Philadelphia AFTER law changed: ",round(mean(df_C$fte),3)), collapse="")
paste0(c("Mean of 'fte' for Group D: Workers in New Jersey AFTER law changed: ",round(mean(df_D$fte),3)), collapse="")

# Using these averages, estimate the value of the difference in difference
A <- round(mean(df_A$fte),3)
B <- round(mean(df_B$fte),3)
C <- round(mean(df_C$fte),3)
D <- round(mean(df_D$fte),3)

dif_in_dif_avg <- (D-B) - (C-A)
paste0(c("difference in difference, using averages, estimated: ",dif_in_dif_avg ), collapse="")

# Estimate the DID (Difference in Difference) using regression model, for "fte"
# model: fte= b0 + b1 * NJ + b2 * After + b3 * NJ * After
# create interaction variables
df_1$nj_after <- df_1$dummy_var * df_1$d 
summary(df_1)

fte_lm_1 <- lm(data=df_1, formula= fte ~ dummy_var + d + nj_after)
summary(fte_lm_1)

dif_in_dif_reg <- round(fte_lm_1$coefficients[['nj_after']],3)
paste0(c("difference in difference, using regression, estimated: ",dif_in_dif_reg ), collapse="")






