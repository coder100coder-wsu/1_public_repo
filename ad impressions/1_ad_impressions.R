library(tidyverse)

data  <- read.csv('KAG.csv',stringsAsFactors = FALSE)

#nrow(data %>% filter(CPC == 0))

data_2 <- data %>% filter(CPC > 0) 

min_CPC <- min(data_2$CPC)

data_2 %>% group_by(CPC) %>% summarise(count=length(ad_id))
# as seen there exists only 1-count "ad_id" for the least CPC value

index_1 <- which(data_2$CPC==min_CPC)[1]

data_2[index_1,]

ad_id_ans <- data_2[index_1,'ad_id']

# a. Among the ads that have the least CPC, 
# which one ad leads to the most impressions? (provide ad_id as the answer)
paste0(c("Among the ads that have the least CPC, the ad_id that leads to the most impressions is:  ",
         ad_id_ans), 
       collapse = "")

######################################
colnames(data)
data <- data %>% mutate(CPM = round(((Spent / Impressions) * 100),4) )
colnames(data)
data %>% group_by(CPM) %>% summarise(count=length(ad_id)) %>% arrange(desc(CPM))

index_2 <- which(data$CPM==max(data$CPM))[1]

data[index_2,]

campgn_id_ans <- data[index_2,'campaign_id']

# What campaign (provide campaign_id as the answer) had spent least efficiently on brand awareness on an average 
# (i.e. most Cost per mille or CPM: use total cost for the campaign / total impressions in thousands)? 
paste0(c(" answer 'campaign_id':  ", campgn_id_ans), 
       collapse = "")
######################################

data_3 <-data %>% filter(Spent > 0) 

data_3 <-data_3 %>% group_by(gender)

data_3 <- data_3 %>% mutate(tot_conv_dollars = round((10 * Total_Conversion),4))

data_3 <- data_3 %>% mutate(apprv_conv_dollars = round((50 * Approved_Conversion),4))

data_3 <- data_3 %>% mutate(revenue = round((tot_conv_dollars + apprv_conv_dollars),4))

data_3 <- data_3 %>% mutate(roas_metric = round((revenue / Spent)*100, 2))


# Make a boxplot of the ROAS grouped by gender for interest_id = 15, 21, 101 in one graph.
# Try to use the function '+ scale_y_log10()' in ggplot to make the visualization look better. 
# The x-axis label should be 'Interest ID' while the
# y-axis label should be ROAS; 
# and each interest_id will have two boxplots (one boxplot for each gender)
colnames(data_3)

data_4 <- data_3 %>% filter(interest ==15 | interest ==21 | interest == 101) 

ggplot(data_4,
         aes(x = interest,y = roas_metric, group=interest)) +
  scale_y_log10() +
  xlab('Interest ID') + 
  ylab('ROAS') + 
  theme(legend.position = "none")+
  ggtitle("ROAS vs Interest ID")+
  geom_boxplot() 

######################################
# Summarize the median and mean of ROAS by genders when campign_id == 1178.
# Hint: Remember to filter the advertisements where there is no advertising spent.
# Hint: Your answer should include all interest_ids
# Hint: ROAS should be rounded to the second decimal.

data_5 <-data_3 %>% filter(campaign_id == 1178) 

#data_3 already grouped by gender.

data_5 %>% summarise(mean_ROAS = round(mean(roas_metric),2), 
                     median_ROAS = round(median(roas_metric),2))


######################################

#Using the Advertising.csv dataset
library(pROC) 
library(caret)
library(dplyr) 
library(ggplot2)
library(e1071)

data <- read.csv("Advertising.csv", header = TRUE, stringsAsFactors = FALSE)
data$Clicked.on.Ad <- as.factor(data$Clicked.on.Ad)
head(data)

# Make a scatter plot for 'Daily.Internet.Usage' against 'Age'. 
# Separate the datapoints by different shapes and/or color based on if the datapoint has
# clicked on the ad or not 
# (Clicked.on.Ad=0 means no, and Clicked.on.Ad=1 means yes). 
# Based off the general trends in the scatter plot you created, 
# consider a new data point where an individual has 
# a 'Daily.Internet.Usage' less than or equal to 150, 
# and an age of 40. 
# Would this new individual be likely to click the ad or not click the ad?

ggplot(data, aes(x = Age, y = Daily.Internet.Usage, size = Clicked.on.Ad, color= Clicked.on.Ad)) +
  geom_point(shape = 21)+
  ggtitle("Scatter Plot, Daily.Internet.Usage vs Age")
  
######################################
# Create a logistic regression model using the variables
# 'Daily.Time.Spent.on.Site', 'Age', and 'Area.Income' to predict the variable
# 'Clicked.on.Ad'. 
# Display the summary output of this logistic regression model.
# Now that we have created our logistic regression model, we must test the
# model. When testing such models, it is always recommended to split the data
# into a training (from which we build the model) and test (on which we test the
# model) set. This is done to avoid bias, as testing the model on the data from
# which it is originally built from is unrepresentative of how the model will
# perform on new data. 
#
# That said, for the case of simplicity, test the model on the full original dataset.
#
# Use type = "response" to insure we get the predicted probabilities of clicking the advert
#
# Append the predicted probabilities to a new column in the original dataset or
# simply to a new data frame. The choice is up to you, but ensure you know how
# to reference this column of probabilities.
#
# Using a threshold of 80% (0.8), create a new column in the original dataset
# that represents if the model predicts a click or not for that person. Note
# this means probabilities greater than or equal to 80% should be treated as a
# click prediction. 

# Now, using the caret package, create a confusion matrix for
# the model predictions and actual clicks. 
# Print and/or plot this output.

log_model <- glm(data, family = "binomial", 
                 formula = Clicked.on.Ad ~ Daily.Time.Spent.on.Site + Age + Area.Income)

summary(log_model)

# predicted values for ENTIRE data
data_prob <- predict(object = log_model, newdata = data, type = "response")

data <- cbind(data, "prob"= data_prob)

data$factor_prob <- ifelse(data$prob>=0.8,1,0)

a <- as.factor(data$factor_prob)
b <- data$Clicked.on.Ad

confusionMatrix(
  data = a,
  reference= b,
  dnn = c("Prediction", "Reference"),
)

# Using the Proc() library, use the roc() function to create and plot a ROC
# curve of our predictions and true labels.
plot(roc(data$Clicked.on.Ad, data$factor_prob))

######################################

df_servers <- data.frame("servers_qty"=seq(7,20,1),
                         "lambda"=c(82,82,82,82,82,82,82,82,82,82,82,82,82,82))

df_servers$mu <- df_servers$servers_qty * 14

df_servers$Avg_time_in_queue_hrs <- df_servers$lambda / (df_servers$mu * (df_servers$mu - df_servers$lambda))

df_servers$Avg_time_in_queue_mins <- round(df_servers$Avg_time_in_queue_hrs * 60,2)


#colnames(df_servers)
df_servers
                      
ggplot(df_servers, aes(x=servers_qty, y=Avg_time_in_queue_mins)) +
  geom_point()+
  ggtitle("Scatter Plot, Avg_time_in_queue_mins vs servers_qty")
  


ggplot(df_servers, aes(x=servers_qty, y=Avg_time_in_queue_mins)) +
    geom_point()+
    stat_smooth(method = "lm", formula = y ~ poly(x, 2), size = 1)+
    guides(color = guide_legend("Model Type"))+
    ggtitle("Scatter Plot, Avg_time_in_queue_mins vs servers_qty")
  

# what value does avg time in quese approach if we add more servers ?
df_servers <- data.frame("servers_qty"=seq(7,50,1))

df_servers$lambda <- rep(82, times = nrow(df_servers))   

df_servers$mu <- df_servers$servers_qty * 14

df_servers$Avg_time_in_queue_hrs <- df_servers$lambda / (df_servers$mu * (df_servers$mu - df_servers$lambda))

df_servers$Avg_time_in_queue_mins <- round(df_servers$Avg_time_in_queue_hrs * 60,2)


#colnames(df_servers)
head(df_servers,5)
tail(df_servers,5)

ggplot(df_servers, aes(x=servers_qty, y=Avg_time_in_queue_mins)) +
  geom_point()+
  ggtitle("Scatter Plot, Avg_time_in_queue_mins vs servers_qty")







