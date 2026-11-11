AP <- AirPassengers; lx <- log(AP)
s0 <- stl(lx, s.window="periodic")
cat("win:", s0$win, " jump:", s0$jump, " inner/outer:", s0$inner, s0$outer, "\n")
ts0 <- s0$time.series
cat("Jul55 T S R:", ts0[79,"trend"], ts0[79,"seasonal"], ts0[79,"remainder"], " exp:", exp(ts0[79,2]), exp(ts0[79,1]), exp(ts0[79,3]), "\n")
cat("Dec60 trend:", ts0[144,"trend"], " Sep S:", ts0[9,"seasonal"], exp(ts0[9,"seasonal"]), "\n")
cat("range Jul seasonal periodic:", diff(range(ts0[cycle(AP)==7,"seasonal"])), "\n")
s11 <- stl(lx, s.window=11); cat("s.window=11 -> t.window:", s11$win, "\n")
j <- s11$time.series[cycle(AP)==7,"seasonal"]; cat("Jul seasonal s11: 1949", exp(j[1])-1, " 1960", exp(j[12])-1, " range log:", diff(range(j)), " first-last:", j[12]-j[1], "\n")
# trend window jump effect
s0j <- stl(lx, s.window="periodic", t.jump=1)
cat("max |trend tjump2 - tjump1|:", max(abs(s0j$time.series[,2]-ts0[,2])), "\n")
# radius convention test: inner=1, outer=0, t.jump=1
s1 <- stl(lx, s.window="periodic", inner=1, outer=0, t.jump=1)
des <- as.numeric(lx - s1$time.series[,"seasonal"])
loc <- function(y, foco, q, deg=1, plus=0) {
  n <- length(y); k <- (q-1)%/%2; ini <- foco-k; fin <- foco+k
  if (ini<1) {fin <- min(n, fin-ini+1); ini <- 1}
  if (fin>n) {ini <- max(1, ini-(fin-n)); fin <- n}
  i <- ini:fin; x <- i-foco; h <- max(abs(x)) + plus
  u <- abs(x)/h; w <- ifelse(u<1,(1-u^3)^3,0)
  if (deg==0) return(sum(w*y[i])/sum(w))
  coef(lm(y[i] ~ x, weights=w))[1]
}
tr1 <- as.numeric(s1$time.series[,"trend"])
fA <- sapply(1:144, function(t) loc(des,t,19,1,0))
fB <- sapply(1:144, function(t) loc(des,t,19,1,1))
cat("radius = max dist (edge weight 0): max|diff| =", max(abs(fA-tr1)), "\n")
cat("radius = max dist + 1 (chapter):  max|diff| =", max(abs(fB-tr1)), "\n")
cat("tricube weights u=0.3,0.6,0.9:", (1-0.3^3)^3, (1-0.6^3)^3, (1-0.9^3)^3, " stl-convention dist 3,6 of 9:", (1-(3/9)^3)^3, (1-(6/9)^3)^3, "\n")
# simulator numbers (chapter convention, using default stl output des = T+R)
desD <- as.numeric(ts0[,"trend"]+ts0[,"remainder"])
cat("Dec60 deg1:", loc(desD,144,19,1,1), " deg0:", loc(desD,144,19,0,1), " diff:", loc(desD,144,19,1,1)-loc(desD,144,19,0,1), "\n")
cat("Dec54 deg1:", loc(desD,72,19,1,1), " deg0:", loc(desD,72,19,0,1), " MA19:", mean(desD[63:81]), "\n")
# robust
ap_out <- AP; ap_out[79] <- ap_out[79]*1.5
sn <- stl(log(ap_out), s.window="periodic"); R <- sn$time.series[,"remainder"]
thr <- 6*median(abs(R)); u <- abs(R)/thr; w <- ifelse(u<1,(1-u^2)^2,0)
cat("|R79|:", abs(R[79]), " thr:", thr, " u:", u[79], " zeros:", which(w==0), " median others:", median(w[-79]), "\n")
s1o <- stl(log(ap_out), s.window="periodic", robust=TRUE, inner=2, outer=1)
cat("stl weights after 1 outer (inner=2) zeros:", which(s1o$weights==0), " median:", median(s1o$weights[-79]), " w79:", s1o$weights[79],"\n")
sr <- stl(log(ap_out), s.window="periodic", robust=TRUE)
cat("final robust (default) zeros:", which(sr$weights < 1e-12), " n<0.5:", sum(sr$weights<0.5), " w79:", sr$weights[79], "\n")
src <- stl(lx, s.window="periodic", robust=TRUE)
cat("clean robust zeros:", which(src$weights < 1e-12), " n<0.5:", sum(src$weights<0.5), " min:", min(src$weights), "\n")
cat("idx stl jul: clean rob", exp(src$time.series[7,1]), " cont rob", exp(sr$time.series[7,1]), " clean nonrob", exp(ts0[7,1]), " cont nonrob", exp(sn$time.series[7,1]), "\n")
cat("classical jul clean/cont:", decompose(AP,"multiplicative")$figure[7], decompose(ap_out,"multiplicative")$figure[7], "\n")
# strengths
fz <- function(x, lg=FALSE){ z <- if (lg) log(x) else x; st <- stl(z, s.window="periodic")$time.series
  R<-st[,3];T_<-st[,2];S<-st[,1]; c(FT=max(0,1-var(R)/var(T_+R)), FS=max(0,1-var(R)/var(S+R)), vR=var(R), vTR=var(T_+R))}
print(round(fz(co2),4)); print(round(fz(USAccDeaths),4)); print(round(fz(AP,TRUE),5))
