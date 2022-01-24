
#open filehandle. good practice to close file handle after use.
fh <- "direct_marketing.csv"

#read data into a dataframe.
df_6 <- read.table(fh, header=TRUE, sep = ",")
head(df_6,5)
summary(df_6)

# Create indicator variables for the 'History' column. Considering the 
# base case as None (i.e., create Low, Medium and High variables 
# with 1 denoting the positive case and 0 the negative)
# create dummy variables
Low <- ifelse(df_6$History == 'Low', 1, 0)
Medium <- ifelse(df_6$History == 'Medium', 1, 0)
High <- ifelse(df_6$History == 'High', 1, 0)
df_7 <- cbind(df_6, Low, Medium, High)

# few additional variables LowSalary, MediumSalary and HighSalary 
# based on the customer history type i.e., MediumSalary = Medium*Salary etc.
# create dummy variables
df_7$LowSalary <- df_7$Low * df_7$Salary
df_7$MediumSalary <- df_7$Medium * df_7$Salary
df_7$HighSalary <- df_7$High * df_7$Salary

#head(df_7,3)
#tail(df_7,3)
summary(df_7)


#Fit a multiple linear regression model using 'AmountSpent' as the response variable 
# and the indicator variables along with their salary variables as the predictors
# AmountSpent=β0+β1Salary+β2Low+β3Medium+β4High+β5LowSalary+β6MediumSalary+β7HighSalary

lm_3 <- lm(data=df_7, AmountSpent ~Salary + Low + Medium + High + LowSalary + MediumSalary + HighSalary)
summary(lm_3)


#str(lm_3)
#lm_3$coefficients

# for historic type=NONE, 
# means all other historic type coefficients are zero
# means all other interaction-terms historic type coefficients are zero
# add input df for prediction on new data point
df_noneSalary <- data.frame('Salary'=10000, 'Low'=0, 'Medium'=0, 'High'=0,
                           'LowSalary'=0*10000, 'MediumSalary'=0*10000, 'HighSalary'=0*10000) 
print("input, representing customer with none-type salary")
df_noneSalary

# predict for new data point
ans_noneSalary <- predict(lm_3, df_noneSalary, interval = "confidence")
print("response or model_prediction, for customer with none-type salary")
ans_noneSalary

paste0(c(round(ans_noneSalary[1],2), "is the amount spent by a customer of historic type (NONE) given salary is 10,000"),collapse=NULL)


# for historic type=High, (None, Low, Medium, and High)
# means all other historic type coefficients are zero
# means all other interaction-terms historic type coefficients are zero
# add input df for prediction on new data point
df_highSalary <- data.frame('Salary'=10000, 'Low'=0, 'Medium'=0, 'High'=1,
                           'LowSalary'=0*10000, 'MediumSalary'=0*10000, 'HighSalary'=1*10000) 
print("input, representing customer with high-type salary")
df_highSalary

# predict for new data point
ans_highSalary <- predict(lm_3, df_highSalary, interval = "confidence")
print("response or model_prediction, for customer with high-type salary")
ans_highSalary

paste0(c(round(ans_highSalary[1],2), "is the amount spent by a customer of historic type (highSalary) given salary is 10,000"),collapse=NULL)

# for historic type=Medium, (None, Low, Medium, and High)
# means all other historic type coefficients are zero
# means all other interaction-terms historic type coefficients are zero
# add input df for prediction on new data point
df_mediumSalary <- data.frame('Salary'=10000, 'Low'=0, 'Medium'=1, 'High'=0,
                           'LowSalary'=0*10000, 'MediumSalary'=1*10000, 'HighSalary'=0*10000) 
print("input, representing customer with medium-type salary")
df_mediumSalary

# predict for new data point
ans_mediumSalary <- predict(lm_3, df_mediumSalary, interval = "confidence")
print("response or model_prediction, for customer with medium-type salary")
ans_mediumSalary

paste0(c(round(ans_mediumSalary[1],2), "is the amount spent by a customer of historic type (mediumSalary) given salary is 10,000"),collapse=NULL)

#colnames(df_7)
# for historic type=Low, 
# means all other historic type coefficients are zero
# means all other interaction-terms historic type coefficients are zero
# add input df for prediction on new data point
df_lowSalary <- data.frame('Salary'=10000, 'Low'=1, 'Medium'=0, 'High'=0,
                           'LowSalary'=1*10000, 'MediumSalary'=0*10000, 'HighSalary'=0*10000) 
print("input, representing customer with low-type salary")
df_lowSalary

# predict for new data point
ans_lowSalary <- predict(lm_3, df_lowSalary, interval = "confidence")
print("response or model_prediction, for customer with low-type salary")
ans_lowSalary

paste0(c(round(ans_lowSalary[1],2), "is the amount spent by a customer of historic type (lowSalary) given salary is 10,000"),collapse=NULL)


