tweet_other_features <- read.csv("D:/Dropbox/School/Thesis/Final/results/Correlation/tweet_other_features.csv")

y1 = tweet_other_features$credible_count

x1 = tweet_other_features$sentiment140_score
x2 = tweet_other_features$sentiwordnet_score
x3 = tweet_other_features$created_at
x4 = tweet_other_features$favorite_count
x5 = tweet_other_features$hashtag_count
x6 = tweet_other_features$nouns_count
x7 = tweet_other_features$numerical_count
x8 = tweet_other_features$punctuation_count
x9= tweet_other_features$retweets_count
x10 = tweet_other_features$uppercase_count
x11 = tweet_other_features$url_count
x12 = tweet_other_features$user_mentions_count
x13 = tweet_other_features$wiki_entities_count
x14 = tweet_other_features$word_count
x15 = tweet_other_features$url_in_newser
x16 = tweet_other_features$url_in_newser100

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
c11 = cor(x11,y1, use="all.obs", method="pearson") 
c12 = cor(x12,y1, use="all.obs", method="pearson") 
c13 = cor(x13,y1, use="all.obs", method="pearson") 
c14 = cor(x14,y1, use="all.obs", method="pearson") 
c15 = cor(x15,y1, use="all.obs", method="pearson") 
c16 = cor(x16,y1, use="all.obs", method="pearson") 

par(mfrow=c(1, 3))
plot(x1, y1, main='sentiment140 score', xlab = c('r = ', c1), ylab = '')
plot(x2, y1, main='sentiwordnet score', xlab = c('r = ', c2), ylab = '')
plot(x3, y1, main='created date', xlab = c('r = ', c3), ylab = '')
plot(x4, y1, main='#favourites', xlab = c('r = ', c4), ylab = '')
plot(x5, y1, main='#hashtags', xlab = c('r = ', c5), ylab = '')
plot(x6, y1, main='#nouns', xlab = c('r = ', c6), ylab = '')
plot(x7, y1, main='#numerical entities', xlab = c('r = ', c7), ylab = '')
plot(x8, y1, main='#symbols', xlab = c('r = ', c8), ylab = '')
plot(x9, y1, main='#retweets', xlab = c('r = ', c9), ylab = '')
plot(x10, y1, main='#uppercase characters', xlab = c('r = ', c10), ylab = '')
plot(x11, y1, main='#urls', xlab = c('r = ', c11), ylab = '')
plot(x12, y1, main='#user mentions', xlab = c('r = ', c12), ylab = '')
plot(x13, y1, main='#wiki entities', xlab = c('r = ', c13), ylab = '')
plot(x14, y1, main='#words', xlab = c('r = ', c14), ylab = '')
plot(x15, y1, main='#url in newser', xlab = c('r = ', c15), ylab = '')
plot(x16, y1, main='#url in newser top 100', xlab = c('r = ', c16), ylab = '')

