# ##########################################################################
rm(list = ls())
options(digits = 5)
# if (!is.null(dev.list())){dev.off()}
# #########################################################################

# Clustering is a form of UNsupervised learning.
# k-means clustering
library(factoextra)
library(cluster)
library(dplyr) 

# import (iris) dataset as data-frame
df <- as.data.frame(iris)
head(df)
#plot(df)

#The na.omit R function removes all incomplete cases of a data object
df <- na.omit(df)

#scale/normalize/standardize
#scale(function)
#cast as data frame
#drop 5th column because non-numeric, cannot scale non-numeric
df_scaled <- as.data.frame(scale(df[,1:4]))

set.seed(123)
#kmeans(data, centers, nstart)

#start of run
centers_value = 2
run_cluster <- kmeans(df_scaled[,1:2], centers = centers_value, nstart = 5)
a_2_12 <- run_cluster$tot.withinss

run_cluster<- kmeans(df_scaled[,1:3], centers = centers_value, nstart = 5)
a_2_13 <- run_cluster$tot.withinss

run_cluster <- kmeans(df_scaled[,1:4], centers = centers_value, nstart = 5)
a_2_14 <- run_cluster$tot.withinss

run_cluster <- kmeans(df_scaled[,2:3], centers = centers_value, nstart = 5)
a_2_23 <- run_cluster$tot.withinss

run_cluster <- kmeans(df_scaled[,2:4], centers = centers_value, nstart = 5)
a_2_24 <- run_cluster$tot.withinss

run_cluster <- kmeans(df_scaled[,3:4], centers = centers_value, nstart = 5)
a_2_34 <- run_cluster$tot.withinss

center_results <- c(a_2_34, a_2_24, a_2_23, a_2_14, a_2_13, a_2_12)

center_labels <- c("a_2_34", "a_2_24", "a_2_23", "a_2_14", "a_2_13", "a_2_12")
center_2_df <- data.frame(center_labels, center_results)
center_2_df

#compare to original response
table(run_cluster$cluster, iris$Species)
#end of run

#start of run
centers_value = 3
run_cluster <- kmeans(df_scaled[,1:2], centers = centers_value, nstart = 5)
a_3_12 <- run_cluster$tot.withinss
# tot.withinss = Total within-cluster sum of squares, i.e.sum(withinss).

run_cluster<- kmeans(df_scaled[,1:3], centers = centers_value, nstart = 5)
a_3_13 <- run_cluster$tot.withinss

run_cluster <- kmeans(df_scaled[,1:4], centers = centers_value, nstart = 5)
a_3_14 <- run_cluster$tot.withinss

run_cluster <- kmeans(df_scaled[,2:3], centers = centers_value, nstart = 5)
a_3_23 <- run_cluster$tot.withinss

run_cluster <- kmeans(df_scaled[,2:4], centers = centers_value, nstart = 5)
a_3_24 <- run_cluster$tot.withinss

run_cluster <- kmeans(df_scaled[,3:4], centers = centers_value, nstart = 5)
a_3_34 <- run_cluster$tot.withinss

center_results <- c(a_3_34, a_3_24, a_3_23, a_3_14, a_3_13, a_3_12)

center_labels <- c("a_3_34", "a_3_24", "a_3_23", "a_3_14", "a_3_13", "a_3_12")

center_3_df <- data.frame(center_labels, center_results)

#compare to original response
table(run_cluster$cluster, iris$Species)
#end of run

#start of run
centers_value = 4
run_cluster <- kmeans(df_scaled[,1:2], centers = centers_value, nstart = 5)
a_4_12 <- run_cluster$tot.withinss

run_cluster<- kmeans(df_scaled[,1:3], centers = centers_value, nstart = 5)
a_4_13 <- run_cluster$tot.withinss

run_cluster <- kmeans(df_scaled[,1:4], centers = centers_value, nstart = 5)
a_4_14 <- run_cluster$tot.withinss

run_cluster <- kmeans(df_scaled[,2:3], centers = centers_value, nstart = 5)
a_4_23 <- run_cluster$tot.withinss

run_cluster <- kmeans(df_scaled[,2:4], centers = centers_value, nstart = 5)
a_4_24 <- run_cluster$tot.withinss

run_cluster <- kmeans(df_scaled[,3:4], centers = centers_value, nstart = 5)
a_4_34 <- run_cluster$tot.withinss

center_results <- c(a_4_34, a_4_24, a_4_23, a_4_14, a_4_13, a_4_12)

center_labels <- c("a_4_34", "a_4_24", "a_4_23", "a_4_14", "a_4_13", "a_4_12")

center_4_df <- data.frame(center_labels, center_results)

#end of run

#start of run
centers_value = 5
run_cluster <- kmeans(df_scaled[,1:2], centers = centers_value, nstart = 5)
a_5_12 <- run_cluster$tot.withinss

run_cluster<- kmeans(df_scaled[,1:3], centers = centers_value, nstart = 5)
a_5_13 <- run_cluster$tot.withinss

run_cluster <- kmeans(df_scaled[,1:4], centers = centers_value, nstart = 5)
a_5_14 <- run_cluster$tot.withinss

run_cluster <- kmeans(df_scaled[,2:3], centers = centers_value, nstart = 5)
a_5_23 <- run_cluster$tot.withinss

run_cluster <- kmeans(df_scaled[,2:4], centers = centers_value, nstart = 5)
a_5_24 <- run_cluster$tot.withinss

run_cluster <- kmeans(df_scaled[,3:4], centers = centers_value, nstart = 5)
a_5_34 <- run_cluster$tot.withinss

center_results <- c(a_5_34, a_5_24, a_5_23, a_5_14, a_5_13, a_5_12)

center_labels <- c("a_5_34", "a_5_24", "a_5_23", "a_5_14", "a_5_13", "a_5_12")

center_5_df <- data.frame(center_labels, center_results)

#compare to original response
table(run_cluster$cluster, iris$Species)
#end of run

all_results <- rbind2(center_5_df, center_4_df)
all_results <- rbind2(all_results, center_3_df)
all_results <- rbind2(all_results, center_3_df)
all_results <- rbind2(all_results, center_2_df)
all_results

all_results_total_withinss <- all_results[order(all_results$center_results),][1,]
all_results_total_withinss

#based on results above, select run a_5_34
a_5_34 

# rerun the clustering so that selected configuration is now active in "run_cluster" variable
run_cluster <- kmeans(df_scaled[,3:4], centers = centers_value, nstart = 5)
a_5_34 <- run_cluster$tot.withinss

#compare to original response
table(run_cluster$cluster, iris$Species)

all_results <- arrange(all_results, center_results)

ggplot(
        all_results, aes(y = center_labels, x = center_results)) + 
        geom_point() + 
        theme(axis.text.x = element_text(angle = 90, vjust = 0.5)
      )

all_results <- arrange(all_results, center_labels)

ggplot(
  all_results, aes(x = center_labels, y = center_results)) + 
  geom_point() + 
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5)
  )
