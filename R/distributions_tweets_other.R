#install.packages("devtools")
#install_github("easyGgplot2", "kassambara")
#install.packages("gridExtra")

library(ggplot2)
library(devtools)
library(easyGgplot2)
library(gridExtra)

tweet_other_creds <- read.csv("./Distributions/dist_tweet_other_credibles.csv")
tweet_other_rest <- read.csv("./Distributions/dist_tweet_other_non_credibles.csv")

x1 = tweet_other_creds$sentiment140_score
x2 = tweet_other_creds$sentiwordnet_score
x3 = tweet_other_creds$created_at
x4 = tweet_other_creds$favorite_count
x5 = tweet_other_creds$hashtag_count
x6 = tweet_other_creds$nouns_count
x7 = tweet_other_creds$numerical_count
x8 = tweet_other_creds$punctuation_count
x9 = tweet_other_creds$retweets_count
x10 = tweet_other_creds$uppercase_count
x11 = tweet_other_creds$url_count
x12 = tweet_other_creds$user_mentions_count
x13 = tweet_other_creds$wiki_entities_count
x14 = tweet_other_creds$word_count
x15 = tweet_other_creds$url_in_newser
x16 = tweet_other_creds$url_in_newser100

y1 = tweet_other_rest$sentiment140_score
y2 = tweet_other_rest$sentiwordnet_score
y3 = tweet_other_rest$created_at
y4 = tweet_other_rest$favorite_count
y5 = tweet_other_rest$hashtag_count
y6 = tweet_other_rest$nouns_count
y7 = tweet_other_rest$numerical_count
y8 = tweet_other_rest$punctuation_count
y9 = tweet_other_rest$retweets_count
y10 = tweet_other_rest$uppercase_count
y11 = tweet_other_rest$url_count
y12 = tweet_other_rest$user_mentions_count
y13 = tweet_other_rest$wiki_entities_count
y14 = tweet_other_rest$word_count
y15 = tweet_other_rest$url_in_newser
y16 = tweet_other_rest$url_in_newser100


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
  mainTitle="sentiment140 score",
  xTickLabelFont=c(9, "plain", "#000000"),
  yTickLabelFont=c(9, "plain", "#000000"),
  xShowTitle=FALSE, yShowTitle=FALSE,
  xShowTickLabel=TRUE, yShowTickLabel=TRUE,
  hideAxisTicks=TRUE,
  showLegend=FALSE,
  breaks=seq(-1, 5, by=2)
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
  mainTitle="sentiwordnet score",
  xTickLabelFont=c(9, "plain", "#000000"),
  yTickLabelFont=c(9, "plain", "#000000"),
  xShowTitle=FALSE, yShowTitle=FALSE,
  xShowTickLabel=TRUE, yShowTickLabel=TRUE,
  hideAxisTicks=TRUE,
  showLegend=FALSE,
  breaks=seq(-1, 1, by=0.2)
)

temp_x3 = as.character(levels(x3))[x3]
x_x3 <- do.call('c',lapply(temp_x3,function(x){as.Date(strptime(x, "%a %b %d %H:%M:%S %z %Y", tz = "GMT"), tz = "GMT")}))
temp_y3 = as.character(levels(y3))[y3]
x_y3 <- do.call('c',lapply(temp_y3,function(x){as.Date(strptime(x, "%a %b %d %H:%M:%S %z %Y", tz = "GMT"), tz = "GMT")}))

credible <- data.frame(group="credible", tweets=x_x3)
rest <- data.frame(group="rest",tweets=x_y3)
DF <- rbind(credible,rest)
g3 <- ggplot2.histogram(
  data=DF, 
  xName='tweets',
  groupName='group', 
  legendPosition="right",
  position = "stack",
  alpha=0.3,
  binwidth=15,
  mainTitle="created date",
  xShowTitle=FALSE, yShowTitle=FALSE,
  xShowTickLabel=TRUE, yShowTickLabel=TRUE,
  xTickLabelFont=c(9, "plain", "#000000"),
  yTickLabelFont=c(9, "plain", "#000000"),
  hideAxisTicks=TRUE,
  showLegend=FALSE
) + theme(axis.text.x = element_text(angle = 90, hjust = 1))

credible <- data.frame(group="credible", tweets=x4)
rest <- data.frame(group="rest",tweets=y4)
DF <- rbind(credible,rest)
g4 <- ggplot2.histogram(
  data=DF, 
  xName='tweets',
  groupName='group', 
  legendPosition="right",
  position = "stack",
  alpha=0.3,
  binwidth=1,
  mainTitle="#favourites",
  xTickLabelFont=c(9, "plain", "#000000"),
  yTickLabelFont=c(9, "plain", "#000000"),
  xShowTitle=FALSE, yShowTitle=FALSE,
  xShowTickLabel=TRUE, yShowTickLabel=TRUE,
  hideAxisTicks=TRUE,
  showLegend=FALSE,
  breaks=seq(0, 20, by=2)
)

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
  mainTitle="#hashtags",
  xTickLabelFont=c(9, "plain", "#000000"),
  yTickLabelFont=c(9, "plain", "#000000"),
  xShowTitle=FALSE, 
  yShowTitle=FALSE,
  xShowTickLabel=TRUE, 
  yShowTickLabel=TRUE,
  hideAxisTicks=TRUE,
  showLegend=FALSE,
  breaks=seq(0, 10, by=1)
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
  mainTitle="#nouns",
  xTickLabelFont=c(9, "plain", "#000000"),
  yTickLabelFont=c(9, "plain", "#000000"),
  xShowTitle=FALSE, 
  yShowTitle=FALSE,
  xShowTickLabel=TRUE, 
  yShowTickLabel=TRUE,
  hideAxisTicks=TRUE,
  showLegend=FALSE,
  breaks=seq(0, 10, by=1)
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
  mainTitle="#numerical entities",
  xTickLabelFont=c(9, "plain", "#000000"),
  yTickLabelFont=c(9, "plain", "#000000"),
  xShowTitle=FALSE, 
  yShowTitle=FALSE,
  xShowTickLabel=TRUE, 
  yShowTickLabel=TRUE,
  hideAxisTicks=TRUE,
  showLegend=FALSE,
  breaks=seq(0, 10, by=1)
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
  mainTitle="#symbols",
  xTickLabelFont=c(9, "plain", "#000000"),
  yTickLabelFont=c(9, "plain", "#000000"),
  xShowTitle=FALSE, 
  yShowTitle=FALSE,
  xShowTickLabel=TRUE, 
  yShowTickLabel=TRUE,
  hideAxisTicks=TRUE,
  showLegend=FALSE,
  breaks=seq(0, 10, by=1)
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
  mainTitle="#retweets",
  xTickLabelFont=c(9, "plain", "#000000"),
  yTickLabelFont=c(9, "plain", "#000000"),
  xShowTitle=FALSE, 
  yShowTitle=FALSE,
  xShowTickLabel=TRUE, 
  yShowTickLabel=TRUE,
  hideAxisTicks=TRUE,
  showLegend=FALSE,
  breaks=seq(0, 30, by=3)
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
  mainTitle="#uppercase characters",
  xTickLabelFont=c(9, "plain", "#000000"),
  yTickLabelFont=c(9, "plain", "#000000"),
  xShowTitle=FALSE, 
  yShowTitle=FALSE,
  xShowTickLabel=TRUE, 
  yShowTickLabel=TRUE,
  hideAxisTicks=TRUE,
  showLegend=FALSE,
  breaks=seq(0, 50, by=5)
)

credible <- data.frame(group="credible", tweets=x11)
rest <- data.frame(group="rest",tweets=y11)
DF <- rbind(credible,rest)
g11 <- ggplot2.histogram(
  data=DF, 
  xName='tweets',
  groupName='group', 
  #legendPosition="bottom",
  position = "stack",
  alpha=0.3,
  binwidth=1,
  mainTitle="#urls",
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

credible <- data.frame(group="credible", tweets=x12)
rest <- data.frame(group="rest",tweets=y12)
DF <- rbind(credible,rest)
g12 <- ggplot2.histogram(
  data=DF, 
  xName='tweets',
  groupName='group', 
  #legendPosition="bottom",
  position = "stack",
  alpha=0.3,
  binwidth=1,
  mainTitle="#user mentions",
  xTickLabelFont=c(9, "plain", "#000000"),
  yTickLabelFont=c(9, "plain", "#000000"),
  xShowTitle=FALSE, 
  yShowTitle=FALSE,
  xShowTickLabel=TRUE, 
  yShowTickLabel=TRUE,
  hideAxisTicks=TRUE,
  showLegend=FALSE,
  breaks=seq(0, 7, by=1)
)

credible <- data.frame(group="credible", tweets=x13)
rest <- data.frame(group="rest",tweets=y13)
DF <- rbind(credible,rest)
g13 <- ggplot2.histogram(
  data=DF, 
  xName='tweets',
  groupName='group', 
  #legendPosition="bottom",
  position = "stack",
  alpha=0.3,
  binwidth=1,
  mainTitle="#wiki entities",
  xTickLabelFont=c(9, "plain", "#000000"),
  yTickLabelFont=c(9, "plain", "#000000"),
  xShowTitle=FALSE, 
  yShowTitle=FALSE,
  xShowTickLabel=TRUE, 
  yShowTickLabel=TRUE,
  hideAxisTicks=TRUE,
  showLegend=FALSE,
  breaks=seq(0, 10, by=1)
)

credible <- data.frame(group="credible", tweets=x14)
rest <- data.frame(group="rest",tweets=y14)
DF <- rbind(credible,rest)
g14 <- ggplot2.histogram(
  data=DF, 
  xName='tweets',
  groupName='group', 
  #legendPosition="bottom",
  position = "stack",
  alpha=0.3,
  binwidth=1,
  mainTitle="#words",
  xTickLabelFont=c(9, "plain", "#000000"),
  yTickLabelFont=c(9, "plain", "#000000"),
  xShowTitle=FALSE, 
  yShowTitle=FALSE,
  xShowTickLabel=TRUE, 
  yShowTickLabel=TRUE,
  hideAxisTicks=TRUE,
  showLegend=FALSE,
  breaks=seq(0, 30, by=3)
)

credible <- data.frame(group="credible", tweets=x15)
rest <- data.frame(group="rest",tweets=y15)
DF <- rbind(credible,rest)
g15 <- ggplot2.histogram(
  data=DF, 
  xName='tweets',
  groupName='group', 
  #legendPosition="bottom",
  position = "stack",
  alpha=0.3,
  binwidth=1,
  mainTitle="#url in newser",
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

credible <- data.frame(group="credible", tweets=x16)
rest <- data.frame(group="rest",tweets=y16)
DF <- rbind(credible,rest)
g16 <- ggplot2.histogram(
  data=DF, 
  xName='tweets',
  groupName='group', 
  #legendPosition="bottom",
  position = "stack",
  alpha=0.3,
  binwidth=1,
  mainTitle="#url in newser top 100",
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
grid.arrange(g10, g11, g12, ncol=3)
grid.arrange(g13, g14, g15, ncol=3)
grid.arrange(g16, ncol=3)

summary(x2)
summary(y2)
summary(x2)
summary(y2)

