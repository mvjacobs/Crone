#install.packages("devtools")
#install_github("easyGgplot2", "kassambara")
#install.packages("gridExtra")
library(gridExtra)
library(ggplot2)
library(devtools)
library(easyGgplot2)

tweet_author_creds <- read.csv("./Distributions/dist_tweet_author_credibles.csv")
tweet_author_rest <- read.csv("./Distributions/dist_tweet_author_non_credibles.csv")

x1 = tweet_author_creds$has_user_avatar
x2 = tweet_author_creds$has_user_background
x3 = tweet_author_creds$has_user_description
x4 = tweet_author_creds$user_created_at
x5 = tweet_author_creds$user_favourites_count
x6 = tweet_author_creds$user_followers_count
x7 = tweet_author_creds$user_friends_count
x8 = tweet_author_creds$user_listed_count
x9= tweet_author_creds$user_statuses_count
x10 = tweet_author_creds$user_verified

y1 = tweet_author_rest$credible_count
y1 = tweet_author_rest$has_user_avatar
y2 = tweet_author_rest$has_user_background
y3 = tweet_author_rest$has_user_description
y4 = tweet_author_rest$user_created_at
y5 = tweet_author_rest$user_favourites_count
y6 = tweet_author_rest$user_followers_count
y7 = tweet_author_rest$user_friends_count
y8 = tweet_author_rest$user_listed_count
y9= tweet_author_rest$user_statuses_count
y10 = tweet_author_rest$user_verified


credible <- data.frame(group="credible", tweets=x1)
rest <- data.frame(group="rest",tweets=y1)
DF <- rbind(credible,rest)
g1 <- ggplot2.histogram(
  data=DF, 
  xName='tweets',
  groupName='group', 
  legendPosition="right",
  position = "stack",
  alpha=0.3,
  binwidth=1,
  mainTitle="author has avatar",
  xTickLabelFont=c(9, "plain", "#000000"),
  yTickLabelFont=c(9, "plain", "#000000"),
  xShowTitle=FALSE, yShowTitle=FALSE,
  xShowTickLabel=TRUE, yShowTickLabel=TRUE,
  hideAxisTicks=TRUE,
  showLegend=FALSE,
  breaks=seq(-1, 3, by=1)
)

credible <- data.frame(group="credible", tweets=x2)
rest <- data.frame(group="rest",tweets=y2)
DF <- rbind(credible,rest)
g2 <- ggplot2.histogram(
  data=DF, 
  xName='tweets',
  groupName='group', 
  legendPosition="right",
  position = "stack",
  alpha=0.3,
  binwidth=1,
  mainTitle="author has background",
  xTickLabelFont=c(9, "plain", "#000000"),
  yTickLabelFont=c(9, "plain", "#000000"),
  xShowTitle=FALSE, yShowTitle=FALSE,
  xShowTickLabel=TRUE, yShowTickLabel=TRUE,
  hideAxisTicks=TRUE,
  showLegend=FALSE,
  breaks=seq(-1, 3, by=1)
)

credible <- data.frame(group="credible", tweets=x3)
rest <- data.frame(group="rest",tweets=y3)
DF <- rbind(credible,rest)
g3 <- ggplot2.histogram(
  data=DF, 
  xName='tweets',
  groupName='group', 
  legendPosition="right",
  position = "stack",
  alpha=0.3,
  binwidth=1,
  mainTitle="author has description",
  xTickLabelFont=c(9, "plain", "#000000"),
  yTickLabelFont=c(9, "plain", "#000000"),
  xShowTitle=FALSE, yShowTitle=FALSE,
  xShowTickLabel=TRUE, yShowTickLabel=TRUE,
  hideAxisTicks=TRUE,
  showLegend=FALSE,
  breaks=seq(-1, 3, by=1)
)

temp_x4 = as.character(levels(x4))[x4]
x_x4 <- do.call('c',lapply(temp_x4,function(x){as.Date(strptime(x, "%a %b %d %H:%M:%S %z %Y", tz = "GMT"), tz = "GMT")}))
temp_y4 = as.character(levels(y4))[y4]
x_y4 <- do.call('c',lapply(temp_y4,function(x){as.Date(strptime(x, "%a %b %d %H:%M:%S %z %Y", tz = "GMT"), tz = "GMT")}))

credible <- data.frame(group="credible", tweets=x_x4)
rest <- data.frame(group="rest",tweets=x_y4)
DF <- rbind(credible,rest)
g4 <- ggplot2.histogram(
  data=DF, 
  xName='tweets',
  groupName='group', 
  legendPosition="right",
  position = "stack",
  alpha=0.3,
  binwidth=365,
  mainTitle="author registration date",
  xShowTitle=FALSE, yShowTitle=FALSE,
  xShowTickLabel=TRUE, yShowTickLabel=TRUE,
  xTickLabelFont=c(9, "plain", "#000000"),
  yTickLabelFont=c(9, "plain", "#000000"),
  hideAxisTicks=TRUE,
  showLegend=FALSE
) + theme(axis.text.x = element_text(angle = 90, hjust = 1))

credible <- data.frame(group="credible", tweets=x5)
rest <- data.frame(group="rest",tweets=y5)
DF <- rbind(credible,rest)
g5 <- ggplot2.histogram(
  data=DF, 
  xName='tweets',
  groupName='group', 
  #legendPosition="bottom",
  position = "stack",
  alpha=0.3,
  binwidth=1,
  mainTitle="author #favourites",
  xTickLabelFont=c(9, "plain", "#000000"),
  yTickLabelFont=c(9, "plain", "#000000"),
  xShowTitle=FALSE, 
  yShowTitle=FALSE,
  xShowTickLabel=TRUE, 
  yShowTickLabel=TRUE,
  hideAxisTicks=TRUE,
  showLegend=FALSE,
  breaks=seq(0, boxplot.stats(y5)$stats[5], by=450)
)

credible <- data.frame(group="credible", tweets=x6)
rest <- data.frame(group="rest",tweets=y6)
DF <- rbind(credible,rest)
g6 <- ggplot2.histogram(
  data=DF, 
  xName='tweets',
  groupName='group', 
  #legendPosition="bottom",
  position = "stack",
  alpha=0.3,
  binwidth=1,
  mainTitle="author #followers",
  xTickLabelFont=c(9, "plain", "#000000"),
  yTickLabelFont=c(9, "plain", "#000000"),
  xShowTitle=FALSE, 
  yShowTitle=FALSE,
  xShowTickLabel=TRUE, 
  yShowTickLabel=TRUE,
  hideAxisTicks=TRUE,
  showLegend=FALSE,
  breaks=seq(0, boxplot.stats(y6)$stats[5], by=225)
)

credible <- data.frame(group="credible", tweets=x7)
rest <- data.frame(group="rest",tweets=y7)
DF <- rbind(credible,rest)
g7 <- ggplot2.histogram(
  data=DF, 
  xName='tweets',
  groupName='group', 
  #legendPosition="bottom",
  position = "stack",
  alpha=0.3,
  binwidth=1,
  mainTitle="author #friends",
  xTickLabelFont=c(9, "plain", "#000000"),
  yTickLabelFont=c(9, "plain", "#000000"),
  xShowTitle=FALSE, 
  yShowTitle=FALSE,
  xShowTickLabel=TRUE, 
  yShowTickLabel=TRUE,
  hideAxisTicks=TRUE,
  showLegend=FALSE,
  breaks=seq(0, boxplot.stats(y7)$stats[5], by=200)
)

credible <- data.frame(group="credible", tweets=x8)
rest <- data.frame(group="rest",tweets=y8)
DF <- rbind(credible,rest)
g8 <- ggplot2.histogram(
  data=DF, 
  xName='tweets',
  groupName='group', 
  #legendPosition="bottom",
  position = "stack",
  alpha=0.3,
  binwidth=1,
  mainTitle="author #friendlists",
  xTickLabelFont=c(9, "plain", "#000000"),
  yTickLabelFont=c(9, "plain", "#000000"),
  xShowTitle=FALSE, 
  yShowTitle=FALSE,
  xShowTickLabel=TRUE, 
  yShowTickLabel=TRUE,
  hideAxisTicks=TRUE,
  showLegend=FALSE,
  breaks=seq(0, boxplot.stats(y8)$stats[5], by=8)
)


credible <- data.frame(group="credible", tweets=x9)
rest <- data.frame(group="rest",tweets=y9)
DF <- rbind(credible,rest)
g9 <- ggplot2.histogram(
  data=DF, 
  xName='tweets',
  groupName='group', 
  #legendPosition="bottom",
  position = "stack",
  alpha=0.3,
  binwidth=1,
  mainTitle="author #posts",
  xTickLabelFont=c(9, "plain", "#000000"),
  yTickLabelFont=c(9, "plain", "#000000"),
  xShowTitle=FALSE, 
  yShowTitle=FALSE,
  xShowTickLabel=TRUE, 
  yShowTickLabel=TRUE,
  hideAxisTicks=TRUE,
  showLegend=FALSE,
  breaks=seq(0, boxplot.stats(y9)$stats[5], by=7000)
)

credible <- data.frame(group="credible", tweets=x10)
rest <- data.frame(group="rest",tweets=y10)
DF <- rbind(credible,rest)
g10 <- ggplot2.histogram(
  data=DF, 
  xName='tweets',
  groupName='group', 
  #legendPosition="bottom",
  position = "stack",
  alpha=0.3,
  binwidth=1,
  mainTitle="author is verified",
  xTickLabelFont=c(9, "plain", "#000000"),
  yTickLabelFont=c(9, "plain", "#000000"),
  xShowTitle=FALSE, 
  yShowTitle=FALSE,
  xShowTickLabel=TRUE, 
  yShowTickLabel=TRUE,
  hideAxisTicks=TRUE,
  showLegend=FALSE,
  breaks=seq(-1, 3, by=1)
)

grid.arrange(g1, g2, g3, ncol=3)
grid.arrange(g4, g5, g6, ncol=3)
grid.arrange(g7, g8, g9, ncol=3)
grid.arrange(g10, ncol=3)

