articles_features <- read.csv("D:/Dropbox/School/Thesis/Final/results/Correlation/articles_features.csv")

y1 = articles_features$credible_count

x1 = articles_features$comments_count
x2 = articles_features$keywords_count
x3 = articles_features$nouns_count
x4 = articles_features$numerical_count
x5 = articles_features$publication_date
x6 = articles_features$punctuation_count
x7 = articles_features$uppercase_count
x8 = articles_features$entities_count
x9= articles_features$word_count
x10 = articles_features$sentiment_count

c1 = cor(x1,y1, use="all.obs", method="pearson") 
c2 = cor(x2,y1, use="all.obs", method="pearson") 
c3 = cor(x3,y1, use="all.obs", method="pearson") 
c4 = cor(x4,y1, use="all.obs", method="pearson") 
c5 = cor(x5,y1, use="all.obs", method="pearson") 
c6 = cor(x6,y1, use="all.obs", method="pearson") 
c7 = cor(x7,y1, use="all.obs", method="pearson") 
c8 = cor(x8,y1, use="all.obs", method="pearson") 
c9 = cor(x9,y1, use="all.obs", method="pearson") 
c10 = cor(x10,y1, use="all.obs", method="pearson") 

par(mfrow=c(1, 3))
plot(x1, y1, main='#comments', xlab = c('r = ', c1), ylab = '')
plot(x2, y1, main='#keywords', xlab = c('r = ', c2), ylab = '')
plot(x3, y1, main='#nouns', xlab = c('r = ', c3), ylab = '')
plot(x4, y1, main='#numerical entities', xlab = c('r = ', c4), ylab = '')
plot(x5, y1, main='publication date', xlab = c('r = ', c5), ylab = '')
plot(x6, y1, main='#symbols', xlab = c('r = ', c6), ylab = '')
plot(x7, y1, main='#uppercase characters', xlab = c('r = ', c7), ylab = '')
plot(x8, y1, main='#wiki entities', xlab = c('r = ', c8), ylab = '')
plot(x9, y1, main='#words', xlab = c('r = ', c9), ylab = '')
plot(x10, y1, main='sentiment score', xlab = c('r = ', c10), ylab = '')
