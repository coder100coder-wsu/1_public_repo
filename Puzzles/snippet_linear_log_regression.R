 # script snippet for linear / log regression

# linear_linear model
lm_linear_linear<- lm(data=df_sub_1, formula= Survived ~ .)
summary(lm_linear_linear)

# linear_log model
lm_linear_log<- lm(data=df_sub_1, formula= Qty ~ Survived ~ .)
summary(lm_linear_log)

# log_linear model
lm_log_linear<- lm(data=df_sub_1, formula= log(Qty) ~ Survived ~ .)
summary(lm_log_linear)

# log_log model
lm_log_log<- lm(data=df_sub_1, formula= log(Qty) ~ Survived ~ .)
summary(lm_log_log)