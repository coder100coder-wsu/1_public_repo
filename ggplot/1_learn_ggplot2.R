# # ##########################################################################
# rm(list = ls())
# if (!is.null(dev.list()))
#   dev.off()
# options(digits = 5)
# dev.off()
# #########################################################################
library(tidyverse)
# #####################
mpg

#creates blank graph. need to add layers
ggplot(data = mpg)

#add layer with geom_point
ggplot(data = mpg) + 
  geom_point(mapping = aes(x = displ, y = hwy))

#get summary
summary(mpg)

#get structure
str(mpg)

#get dimensions
dim(mpg)

#new plot hwy vs cyl
ggplot(data = mpg) + 
  geom_point(mapping = aes(x = cyl, y = hwy))

#new plot, class vs drv
ggplot(data = mpg) + 
  geom_point(mapping = aes(x = drv, y = class))
#drv, the type of drive train, where f = front-wheel drive, r = rear wheel drive, 4 = 4wd
#class, "type" of car
#this plot is not useful (to determine any fuel efficiency)

#add aestheic, color
ggplot(data = mpg) + 
  geom_point(mapping = aes(x = displ, y = hwy, color = class))

ggplot(data = mpg) + 
  geom_point(mapping = aes(x = displ, y = hwy, color = displ))

ggplot(data = mpg) + 
  geom_point(mapping = aes(x = displ, y = hwy, color = cyl))

ggplot(data = mpg) + 
  geom_point(mapping = aes(x = displ, y = hwy, color = cty))

ggplot(data = mpg) + 
  geom_point(mapping = aes(x = displ, y = hwy, color = manufacturer))

#add aestheic, size
ggplot(data = mpg) + 
  geom_point(mapping = aes(x= displ, y= hwy, color= class, size= class))

#add aestheic, alpha (or transperency)
ggplot(data = mpg) + 
  geom_point(mapping = aes(x= displ, y= hwy, color= class, size= class, alpha= class))

#facets
ggplot(data = mpg) + 
  geom_point(mapping = aes(x = displ, y = hwy)) + 
  facet_wrap(~ class, nrow = 2)

#facets, non-continous/categorical facet variable
ggplot(data = mpg) + 
  geom_point(mapping = aes(x = displ, y = hwy)) + 
  facet_wrap(~ cyl, nrow = 2)

#facets, continous/NON-categorical facet variable
ggplot(data = mpg) + 
  geom_point(mapping = aes(x = displ, y = hwy)) + 
  facet_wrap(~ cty, nrow = 2)

#facet grid, 2-additional predictor variables
ggplot(data = mpg) + 
  geom_point(mapping = aes(x = displ, y = hwy)) + 
  facet_grid(cyl ~ drv)

#facet-grid, 2-additional predictor variables
ggplot(data = mpg) + 
  geom_point(mapping = aes(x = displ, y = hwy)) + 
  facet_grid(cyl ~ cty)

#facet-grid, 1-additional predictor variable
ggplot(data = mpg) + 
  geom_point(mapping = aes(x = displ, y = hwy)) + 
  facet_grid(. ~ cyl) #facet variable axis, opposite to x-axis

#facet-grid, 1-additional predictor variable
ggplot(data = mpg) + 
  geom_point(mapping = aes(x = displ, y = hwy)) + 
  facet_grid(cyl~ .) #facet variable axis, opposite to y-axis

# scatter-plot
ggplot(data = mpg) + 
  geom_point(mapping = aes(x = displ, y = hwy))

# smoothed line plot, method selected automatically
# refer to R-output
ggplot(data = mpg) + 
  geom_smooth(mapping = aes(x = displ, y = hwy))

# smoothed line plot, explicit method specified
ggplot(data = mpg) + 
  geom_smooth(mapping = aes(x = displ, y = hwy), 
              method = "loess", formula= y~x)

# smoothed line plot
ggplot(data = mpg) + 
  geom_smooth(mapping = aes(x = displ, y = hwy), 
              method = "gam", formula= y~x)

# smoothed line plot
ggplot(data = mpg) + 
  geom_smooth(mapping = aes(x = displ, y = hwy), 
              method = "glm", formula= y~x)

# smoothed line plot
ggplot(data = mpg) + 
  geom_smooth(mapping = aes(x = displ, y = hwy), 
              method = "lm", formula= y~x)

# add aesthetic linetype, categorical-only/non-continous
ggplot(data = mpg) + 
  geom_smooth(mapping = aes(x = displ, y = hwy, linetype = drv))

# add aesthetic linetype, categorical-only/non-continous
#ggplot(data = mpg) + 
  #geom_smooth(mapping = aes(x = displ, y = hwy, linetype = cyl))
# Error: A continuous variable can not be mapped to linetype
# cyl is continuous-variable

# add aesthetic linetype, categorical-only/non-continous
ggplot(data = mpg) + 
  geom_smooth(mapping = aes(x = displ, y = hwy, linetype = class))

# add aesthetic linetype, categorical-only/non-continous
ggplot(data = mpg) + 
  geom_smooth(mapping = aes(x = displ, y = hwy, linetype = class), 
              method = "lm", formula= y~x, se= TRUE)

# add scatter-plot as another layer 
ggplot(data = mpg) + 
  geom_point(mapping = aes(x = displ, y = hwy, color= class)) +
  geom_smooth(mapping = aes(x = displ, y = hwy, linetype = class, color= class), 
              method = "lm", formula= y~x, se= FALSE)

# add scatter-plot as another layer 
ggplot(data = mpg) + 
  geom_point(mapping = aes(x = displ, y = hwy, color= drv)) +
  geom_smooth(mapping = aes(x = displ, y = hwy, linetype = drv, color= drv), 
              method = "lm", formula= y~x, se= FALSE)


ggplot(data = mpg) +
  geom_smooth(mapping = aes(x = displ, y = hwy), 
              method = "lm", formula= y~x, show.legend = TRUE)

ggplot(data = mpg) +
  geom_smooth(mapping = aes(x = displ, y = hwy, group = drv), 
              method = "lm", formula= y~x, show.legend = TRUE)

ggplot(data = mpg) +
  geom_smooth(mapping = aes(x = displ, y = hwy, color = drv),
              show.legend = TRUE, method = "lm", formula= y~x)







