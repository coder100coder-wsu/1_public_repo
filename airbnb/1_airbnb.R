
#open filehandle. good practice to close file handle after use.
fh <- "airbnb_data.csv"

#read data into a dataframe.
df_1 <- read.table(fh, header=TRUE, sep = ",")
head(df_1,5)
summary(df_1)

# Remove ‘id’columns (‘room_id’, ‘survey_id’, ‘host_id’) and ‘city’ from your dataset,
df <- subset (df_1, select = -c(room_id, survey_id, host_id, city))

# check if required columns are deleted. and necessary columns are retained.
colnames(df)

# fit a multiple linear regression model using price as the response variable and all others as predictor variables
# Note: Do not fit a model using id columns and city as predictors
lm_1 <- lm(data=df, price ~room_type + reviews + overall_satisfaction + accommodates + bedrooms)
summary(lm_1)

# Which variables are statistically significant at a 95% confidence interval.

# 'room_typePrivate room' p-value 0.94(2-decimals), larger than 0 & many other p-values, NOT statistically significant

# 'room_typeShared room' p-value 0.20(2-decimals), larger than 0 & many other p-values, NOT statistically significant

# 'reviews' p-value 0.91(2-decimals), larger than 0 & many other p-values, NOT statistically significant

# 'overall_satisfaction' p-value 0.002, closer to 0 & smaller than many other p-values, YES-statistically significant

# 'accommodates' p-value 1.27e-05, closer to 0 & smaller than many other p-values, YES-statistically significant

# 'bedrooms' p-value 1.95e-13, closer to 0 & smallest of p-values, YES-statistically significant


# b) Interpret the coefficients for predictors: 'room_type', 'bedrooms'. (4 points)

# interpretation below using "ceteris paribus" meaning 'all else is the same or held constant' (ref:from lectures)

# for 'bedrooms', keeping all other predictors constant, 
# with every 1-unit increase in 'bedrooms', the response variable 'price' increases by estimated 85.645-units.

# for 'room_typePrivate room', keeping all other predictors constant, 
# with every 1-unit increase in 'room_typePrivate room', the response variable 'price' decreases by estimated 0.93-units.
# In above explanation, 'price' (rounded to 2 decimals)

# for 'room_typeShared room', keeping all other predictors constant, 
# with every 1-unit increase in 'room_typeShared room', the response variable 'price' decreases by estimated 76.67-units.
# In above explanation, 'price' (rounded to 2 decimals)


# Add new data point. Use new df. 
# alternate method could be using rbind to earlier df, and using only the "new row"
df_2 <- data.frame(bedrooms=1, accommodates=2, reviews=70, overall_satisfaction=4, room_type='Private room') 
#check input data is correct per given problem
df_2
# predict using established model; 
y_hat <- predict(lm_1, df_2, interval = "confidence")
#display prediction for mean value of response (price) and 95% confidence interval values
y_hat


# Identify outliers using Cook's distance approach. 

# plot model to attempt to visually identify outliers using cook's distance.
plot(lm_1)



# find Cook's distances
cooks_d <- cooks.distance(lm_1)
# add cooks1 column to df_2
df_3 <- cbind(df, cooks_d)
print("summary of df_3")
summary(df_3)

# Remove points having Cook's distance > 1. 
# drop rows where cooks_d >1 
df_4 <-subset(df_3, cooks_d<=1)
print("summary of df_4; contains new data without outliers")
summary(df_4)
# by visual observation of the summary for column cooks_d, 
# we can clearly see the maximum has decreased

# check IF dropping rows has worked correctly. use max(cook_d) as indicator. Expected TRUE.
print("check IF dropping rows has worked correctly. use max(cook_d) as indicator. Expected TRUE.")
max(df_4$cooks_d)<=1

# identify which rows were dropped due to cooks_d >1 
# this fulfills the requirement for "Identify outliers using Cook's distance approach."
df_5 <- subset(df_3, cooks_d>1)
print("summary of df_5; only contains removed rows, because outliers")
df_5


# Rerun the model after the removal of these points and print the summary.
lm_2 <- lm(data=df_4, price ~room_type + reviews + overall_satisfaction + accommodates + bedrooms)
summary(lm_2)


# AFTER removing outliers
# Which variables are statistically significant at a 95% confidence interval.

# CHANGED: 'room_typePrivate room' p-value 2.92e-09, closer to 0, YES-statistically significant

# CHANGED: 'room_typeShared room' p-value 0.000171, closer to 0, YES-statistically significant

# NO CHANGE: reviews' p-value 0.144202, much smaller than previous p-values, but still NOT statistically significant

# NO CHANGE:'overall_satisfaction' p-value 1.78e-06, closer to 0 & smaller than many other p-values, YES-statistically significant

# NO CHANGE:'accommodates' p-value 3.68e-08, closer to 0 & smaller than many other p-values, YES-statistically significant

# NO CHANGE:'bedrooms' p-value 4.25e-13, closer to 0 & smallest of p-values, YES-statistically significant

# seems dropping outliers made predictor room_type (factor data type) YES-statistically significant from previously NOT.

# conlcusion is outliers can significantly affect outcome of model

# AFTER removing outliers
# predict using established model; 
y_hat_2 <- predict(lm_2, df_2, interval = "confidence")
#display prediction for mean value of response (price) and 95% confidence interval values
print("prediction by first model WITH outliers")
y_hat
print("prediction by second model withOUT outliers")
y_hat_2

print(c("lm_1 adj.r.squared",summary(lm_1)$adj.r.squared))
print(c("lm_2 adj.r.squared",summary(lm_2)$adj.r.squared))
print(c("adj.r.squared for lm_2 > lm_1", summary(lm_2)$adj.r.squared > summary(lm_1)$adj.r.squared))
# better adj.r.squared for lm_2 AFTER dropping outliers.


df_8 <- read.table(fh, header=TRUE, sep = ",")
print("original data")
head(df_8,5)
summary(df_8)

# use new dataframe to store only the reponse and 1-qty predictor as required by question
df_9 <- subset (df_8, select = c(price,overall_satisfaction))
print("subset of data per question")
head(df_9,5)
summary(df_9)
# SOLUTION ENDS HERE

# SOLUTION BEGINS HERE
# linear_linear model, no transformation
lm_4_linear_linear <- lm(data=df_9, price ~ overall_satisfaction)
summary(lm_4_linear_linear)


plot(lm_4_linear_linear)


#create column, log(overall_satisfaction) denoted as log_X
df_9$log_X <- log(df_9$overall_satisfaction)
print("Check df_9$log_X column minimum")
min(df_9$log_X)
# notice df_9$log_X column minimum is -Inf. 

# Because overall_satisfaction contains ‘0’ values, 
# need to use log(x+1) transformations instead of log(x) transformations
print("AFTER log(X+1) transformation")
df_9$log_Xplus1 <- log(df_9$overall_satisfaction+1)
summary(df_9)

#create column, log(price) denoted as log_Y
df_9$log_Y <- log(df_9$price)


# linear_log model, transformation for X predictor, use Y response as is
lm_5_linear_log <- lm(data=df_9, price ~ log_Xplus1)
summary(lm_5_linear_log)

plot(lm_5_linear_log)

# log_linear model, NO transformation for X predictor, log transformation for Y response
lm_6_log_linear <- lm(data=df_9,  log_Y~ overall_satisfaction)
summary(lm_6_log_linear)


plot(lm_6_log_linear)

# log_log model, log transformation for X predictor, log transformation for Y response
lm_6_log_log <- lm(data=df_9,  log_Y~ log_Xplus1)
summary(lm_6_log_log)

plot(lm_6_log_log)

#Fit all four models i.e., linear-linear, linear-log, log-linear and log-log regression models 
#using price as the response variable and overall_satisfaction as the predictor.
# asnwer- all four models per question, have been fitted above, relevant results extracted below

# adj.r.squared, extract from previously run models
a<- summary(lm_6_log_log)$adj.r.squared
b<-summary(lm_6_log_linear)$adj.r.squared
c<-summary(lm_5_linear_log)$adj.r.squared
d<-summary(lm_4_linear_linear)$adj.r.squared

# create new df for storing and reporting results
df_r_sq <- data.frame('adj.r.squared'=c(a,b,c,d))

# create column with model names
df_r_sq$model_names <- c('lm_6_log_log', 'lm_6_log_linear', 'lm_5_linear_log', 'lm_4_linear_linear')

# r.squared, extract from previously run models
e<- summary(lm_6_log_log)$r.squared
f<-summary(lm_6_log_linear)$r.squared
g<-summary(lm_5_linear_log)$r.squared
h<-summary(lm_4_linear_linear)$r.squared

# add r_sqrd values to results df
df_r_sq$r_sqrd <- c(e,f,g,h)

#print compiled results df
df_r_sq

# answer question, 
# Which of the four models has the best R2R2? 
print("best r_sqrd")
df_r_sq[which.max(df_r_sq$r_sqrd),]

print("best adj_r_sqrd")
df_r_sq[which.max(df_r_sq$adj.r.squared),]



# Do you have any comments on the choice of the independent variables?
#summary(df_8)
head(df_8,5)
tail(df_8,5)
# comments:
# using only 1-qty predictor (overall_satisfaction) results in rather poor fit, based on low R-sqr
# adj_r_sqr can be referred to in case of multiple linear regression

# potential solution is using (overall_satisfaction), reviews, 
# and interaction terms (overall_satisfaction*reviews) and (overall_satisfaction / reviews)
# we could potentially drop rows that result in error due to division by zero.

# alternatively run linear_linear model using (city, reviews, overall_satisfaction, accommodates, bedrooms, price)
# check significance values
# shortlist most significant predictors
# re-run linear_linear model using most significant predictors

# alternatively scale and center predictors
# use PCA-Principal Component Analysis to shortlist most significant PCs(say cumulative captured variance>95%)
# run linear_linear model using selected PC
# back-transform PC to original variables