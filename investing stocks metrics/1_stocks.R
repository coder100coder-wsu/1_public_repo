library(tidyverse)
library(xts)
library(PerformanceAnalytics)
library(lubridate)


df_1 <- read.csv("Factor_Data.csv")

#original data
colnames(df_1)
colnames(df_1)[colnames(df_1) == "ï..Date"] <- "Date"
colnames(df_1)

# Estimate a one factor model by regressing Berkshire Hathaway's return in excess of the risk free rate 
# on the market excess return.  
df_1$brk_less_rf <- df_1$Brk_ret - df_1$RF
df_1$mkt_less_rf <- df_1$Mkt - df_1$RF

# Run factor models
factor1 <- lm(brk_less_rf ~ mkt_less_rf, data = df_1)
summary(factor1)

# The regression intercept (i.e., Jensen's Alpha) is:
paste0(c("The regression intercept (i.e., Jensen's Alpha) is: ",
         round(coefficients(factor1)['(Intercept)']*100,1),
         "% per month. >0 and statistically significant; Suggesting that BRK manager has significant skill."), 
       collapse = "")


# Estimate a three factor model by regressing Berkshire Hathaway's return in excess of the risk free rate 
# on MKT-rf; SMB; and HML.  
factor3 <- lm(brk_less_rf ~ Mkt_rf+SMB+HML, data = df_1)
summary(factor3)

paste0(c("The coefficient on HML,  ",
         round(coefficients(factor3)['HML']*100,1),
         "% per month; >0, suggests that the portfolio is tilted towards VALUE stocks"), 
       collapse = "")


paste0(c("The coefficient on SMB,  ",
         round(coefficients(factor3)['SMB']*100,1),
         "% per month; <0, suggests that the portfolio is tilted towards LARGE CAP stocks"), 
       collapse = "")

paste0(c("The regression intercept (i.e., Jensen's Alpha) is:  ",
         round(coefficients(factor3)['(Intercept)']*100,1),
         "% per month; >0 and statistically significant; Suggesting that BRK manager has significant skill."), 
       collapse = "")


# Estimate a six factor model by regressing Berkshire Hathaway's return in excess of the risk free rate 
# on MKT-rf; SMB; HML; MOM; BAB; and QMJ.
factor6 <- lm(brk_less_rf ~ Mkt_rf+SMB+HML+Mom+BAB+QMJ, data = df_1)
summary(factor6)

paste0(c("The coefficient on Mom,  ",
         round(coefficients(factor6)['Mom']*100,1),
         "% per month; <0, suggests that the portfolio is tilted towards LOW MOMENTUM stocks"), 
       collapse = "")

a<- round(summary(factor3)$adj.r.squared,2)
b<- round(summary(factor6)$adj.r.squared,2)
df_adj_r_sqd <- data.frame("Factor3_adj_r_sqd"=a, "Factor6_adj_r_sqd"=b)

df_adj_r_sqd








