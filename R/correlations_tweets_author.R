tweet_author_features <- read.csv("./Correlation/tweet_author_features.csv")

y1 = tweet_author_features$credible_count
x1 = tweet_author_features$has_user_avatar
x2 = tweet_author_features$has_user_background
x3 = tweet_author_features$has_user_description
x4 = tweet_author_features$user_created_at
x5 = tweet_author_features$user_favourites_count
x6 = tweet_author_features$user_followers_count
x7 = tweet_author_features$user_friends_count
x8 = tweet_author_features$user_listed_count
x9= tweet_author_features$user_statuses_count
x10 = tweet_author_features$user_verified

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
plot(x1, y1, main='author has avatar', xlab = c('r = ', c1), ylab = '')
plot(x2, y1, main='author has background', xlab = c('r = ', c2), ylab = '')
plot(x3, y1, main='author has description', xlab = c('r = ', c3), ylab = '')
plot(x4, y1, main='author registration date', xlab = c('r = ', c4), ylab = '')
plot(x5, y1, main='author #favourites', xlab = c('r = ', c5), ylab = '')
plot(x6, y1, main='author #followers', xlab = c('r = ', c6), ylab = '')
plot(x7, y1, main='author #friends', xlab = c('r = ', c7), ylab = '')
plot(x8, y1, main='author #friendlists', xlab = c('r = ', c8), ylab = '')
plot(x9, y1, main='author #posts', xlab = c('r = ', c9), ylab = '')
plot(x10, y1, main='author is verified', xlab = c('r = ', c10), ylab = '')

counts = list(
  as.numeric(count(x1 > 0)[2,'freq'][1]),
  as.numeric(count(x2 > 0)[2,'freq'][1]),
  as.numeric(count(x3 > 0)[2,'freq'][1]),
  as.numeric(count(x4 > 0)[2,'freq'][1]),
  as.numeric(count(x5 > 0)[2,'freq'][1]),
  as.numeric(count(x6 > 0)[2,'freq'][1]),
  as.numeric(count(x7 > 0)[2,'freq'][1]),
  as.numeric(count(x8 > 0)[2,'freq'][1]),
  as.numeric(count(x9 > 0)[2,'freq'][1]),
  as.numeric(count(x10 > 0)[2,'freq'][1])
)
