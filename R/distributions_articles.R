#install.packages("devtools")
#install_github("easyGgplot2", "kassambara")
#install.packages("gridExtra")
library(gridExtra)
library(ggplot2)
library(devtools)
library(easyGgplot2)

article_creds <- read.csv("./Distributions/dist_articles_credibles.csv")
article_rest <- read.csv("./Distributions/dist_articles_non_credibles.csv")

x1 = article_creds$comments_count
x2 = article_creds$keywords_count
x3 = article_creds$nouns_count
x4 = article_creds$numerical_count
x5 = article_creds$publication_date
x6 = article_creds$punctuation_count
x7 = article_creds$uppercase_count
x8 = article_creds$entities_count
x9= article_creds$word_count
x10 = article_creds$sentiment_count

y1 = article_rest$comments_count
y2 = article_rest$keywords_count
y3 = article_rest$nouns_count
y4 = article_rest$numerical_count
y5 = article_rest$publication_date
y6 = article_rest$punctuation_count
y7 = article_rest$uppercase_count
y8 = article_rest$entities_count
y9= article_rest$word_count
y10 = article_rest$sentiment_count

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
  mainTitle="#comments",
  xTickLabelFont=c(9, "plain", "#000000"),
  yTickLabelFont=c(9, "plain", "#000000"),
  xShowTitle=FALSE, yShowTitle=FALSE,
  xShowTickLabel=TRUE, yShowTickLabel=TRUE,
  hideAxisTicks=TRUE,
  showLegend=FALSE,
  breaks=seq(0, 250, by=25)
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
  mainTitle="#keywords",
  xTickLabelFont=c(9, "plain", "#000000"),
  yTickLabelFont=c(9, "plain", "#000000"),
  xShowTitle=FALSE, yShowTitle=FALSE,
  xShowTickLabel=TRUE, yShowTickLabel=TRUE,
  hideAxisTicks=TRUE,
  showLegend=FALSE,
  breaks=seq(0, 30, by=3)
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
  mainTitle="#nouns",
  xTickLabelFont=c(9, "plain", "#000000"),
  yTickLabelFont=c(9, "plain", "#000000"),
  xShowTitle=FALSE, yShowTitle=FALSE,
  xShowTickLabel=TRUE, yShowTickLabel=TRUE,
  hideAxisTicks=TRUE,
  showLegend=FALSE,
  breaks=seq(0, 150, by=15)
)

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
  mainTitle="#numerical entities",
  xTickLabelFont=c(9, "plain", "#000000"),
  yTickLabelFont=c(9, "plain", "#000000"),
  xShowTitle=FALSE, yShowTitle=FALSE,
  xShowTickLabel=TRUE, yShowTickLabel=TRUE,
  hideAxisTicks=TRUE,
  showLegend=FALSE,
  breaks=seq(0, 70, by=7)
)

temp_x5 = as.character(levels(x5))[x5]
x_x5 <- do.call('c',lapply(temp_x5,function(x){as.Date(strptime(x, "%Y-%m-%dT%H:%M:%SZ"))}))
temp_y5 = as.character(levels(y5))[y5]
x_y5 <- do.call('c',lapply(temp_y5,function(x){as.Date(strptime(x, "%Y-%m-%dT%H:%M:%SZ"))}))

credible <- data.frame(group="credible", tweets=x_x5)
rest <- data.frame(group="rest",tweets=x_y5)
DF <- rbind(credible,rest)
g5 <- ggplot2.histogram(
  data=DF, 
  xName='tweets',
  groupName='group', 
  legendPosition="right",
  position = "stack",
  alpha=0.3,
  binwidth=200,
  mainTitle="publication date",
  xShowTitle=FALSE, yShowTitle=FALSE,
  xShowTickLabel=TRUE, yShowTickLabel=TRUE,
  xTickLabelFont=c(9, "plain", "#000000"),
  yTickLabelFont=c(9, "plain", "#000000"),
  hideAxisTicks=TRUE,
  showLegend=FALSE
) + theme(axis.text.x = element_text(angle = 90, hjust = 1))

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
  mainTitle="#symbols",
  xTickLabelFont=c(9, "plain", "#000000"),
  yTickLabelFont=c(9, "plain", "#000000"),
  xShowTitle=FALSE, 
  yShowTitle=FALSE,
  xShowTickLabel=TRUE, 
  yShowTickLabel=TRUE,
  hideAxisTicks=TRUE,
  showLegend=FALSE,
  breaks=seq(0, 260, by=26)
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
  mainTitle="#uppercase characters",
  xTickLabelFont=c(9, "plain", "#000000"),
  yTickLabelFont=c(9, "plain", "#000000"),
  xShowTitle=FALSE, 
  yShowTitle=FALSE,
  xShowTickLabel=TRUE, 
  yShowTickLabel=TRUE,
  hideAxisTicks=TRUE,
  showLegend=FALSE,
  breaks=seq(0, 300, by=30)
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
  mainTitle="#wiki entities",
  xTickLabelFont=c(9, "plain", "#000000"),
  yTickLabelFont=c(9, "plain", "#000000"),
  xShowTitle=FALSE, 
  yShowTitle=FALSE,
  xShowTickLabel=TRUE, 
  yShowTickLabel=TRUE,
  hideAxisTicks=TRUE,
  showLegend=FALSE,
  breaks=seq(0, 400, by=40)
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
  mainTitle="#words",
  xTickLabelFont=c(9, "plain", "#000000"),
  yTickLabelFont=c(9, "plain", "#000000"),
  xShowTitle=FALSE, 
  yShowTitle=FALSE,
  xShowTickLabel=TRUE, 
  yShowTickLabel=TRUE,
  hideAxisTicks=TRUE,
  showLegend=FALSE,
  breaks=seq(0, 1500, by=150)
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
  mainTitle="sentiment score",
  xTickLabelFont=c(9, "plain", "#000000"),
  yTickLabelFont=c(9, "plain", "#000000"),
  xShowTitle=FALSE, 
  yShowTitle=FALSE,
  xShowTickLabel=TRUE, 
  yShowTickLabel=TRUE,
  hideAxisTicks=TRUE,
  showLegend=FALSE,
  breaks=seq(-13, 7, by=2)
)

grid.arrange(g1, g2, g3, ncol=3)
grid.arrange(g4, g5, g6, ncol=3)
grid.arrange(g7, g8, g9, ncol=3)
grid.arrange(g10, ncol=3)

