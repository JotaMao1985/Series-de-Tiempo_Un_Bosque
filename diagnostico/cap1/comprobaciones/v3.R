suppressPackageStartupMessages({library(tsibble); library(fabletools); library(feasts); library(dplyr)})
p <- as_tsibble(log(AirPassengers))
f <- function(spec) { cm <- components(model(p, stl = spec)); as.data.frame(cm)[79, c("trend","season_year","remainder")] }
cat("feasts STL periodic, no trend window:\n"); a <- f(STL(value ~ season(window="periodic"))); print(a); print(exp(a$season_year))
cat("feasts STL periodic, trend 19:\n"); b <- f(STL(value ~ trend(window=19) + season(window="periodic"))); print(b); print(exp(b$season_year))
cat("feasts STL periodic, trend 21:\n"); c2 <- f(STL(value ~ trend(window=21) + season(window="periodic"))); print(c2); print(exp(c2$season_year))
cat("feasts default STL():\n"); d <- f(STL(value)); print(d)
cat("stats::stl periodic t.window=21 Jul S:", exp(stl(log(AirPassengers), s.window="periodic", t.window=21)$time.series[7,1]), "\n")
cat("feat_stl on log AP (FPP3 way):\n"); print(features(p, value, feat_stl)[,1:2])
cat("feat_stl with periodic:\n"); print(features(p, value, list(~feat_stl(., .period=12, s.window="periodic")))[,1:2])
# check how feasts picks trend window: inspect STL internals
print(tryCatch(body(feasts:::train_stl), error=function(e) e))
