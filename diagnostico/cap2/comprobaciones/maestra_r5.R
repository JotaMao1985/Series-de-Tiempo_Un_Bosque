suppressMessages({library(forecast); library(tseries)})
# Guerrero propio, sin copiar la funcion del HTML: CV de s_h / mean_h^(1-l) en bloques anuales
g <- function(y,l){m<-frequency(y);n<-m*(length(y)%/%m);M<-matrix(y[1:n],nrow=m);q<-apply(M,2,sd)/colMeans(M)^(1-l);sd(q)/mean(q)}
cat("AP", round(sapply(c(1,0,-0.2947),function(l)g(AirPassengers,l)),3),"\n")
lj<-BoxCox.lambda(JohnsonJohnson,"guerrero"); cv<-sapply(c(1,.5,0,lj),function(l)g(JohnsonJohnson,l))
cat("JJ lambda",round(lj,4),"cv",round(cv,3),"pct",round(100*(cv[1]-cv[3])/(cv[1]-cv[4]),1),"max/min",round(max(JohnsonJohnson)/min(JohnsonJohnson),1),"\n")
cat("exp", round(exp(2.75),2), round(exp(2.75+c(-.4,.4)),2), "media teorica", round(exp(2.75+.02),2),"\n")
lu<-BoxCox.lambda(UKgas,"guerrero"); cu<-sapply(c(1,0,lu),function(l)g(UKgas,l)); cat("UKgas",round(cu,3),round((cu[1]-cu[2])/(cu[1]-cu[3]),2),"\n")
cat("P2", (1.96/.15)^2, ceiling((1.96/.15)^2), "\n")
r<-diff(log(EuStockMarkets[,"DAX"])); b<-1.96/sqrt(length(r))
f<-function(x) which(abs(acf(x,24,plot=FALSE)$acf[-1])>b); cat("DAX", f(r), "|", f(r^2),"\n")
a<-suppressWarnings(adf.test(UKDriverDeaths)); a12<-adf.test(UKDriverDeaths,k=12); cat("UKDD", round(a$statistic,3),a$p.value, round(a12$statistic,3), round(a12$p.value,3),"\n")
set.seed(2026); cam<-replicate(500,cumsum(rnorm(144))); rj<-function(x) suppressWarnings(adf.test(x)$p.value)<.05
cat("E2", 100*mean(apply(cam,2,rj)), 100*mean(apply(cam+4*sin(2*pi*(1:144)/12),2,rj)), round(100*sqrt(.05*.95/500),2),"\n")
x<-window(discoveries,1927,1936); cat("disc",x," r1r2(T)",round(acf(x,2,plot=FALSE)$acf[2:3],3),"band",round(1.96/sqrt(10),3),"\n")
# --- segunda tanda: cifras de las correcciones tras la verificación
e<-exp(2.75+c(-.4,0,.4)); print(round(c(e[2]-e[1], e[3]-e[2]),4))
set.seed(8); w<-rnorm(1e5,2.75,.2); print(c(mean(exp(w))-median(exp(w)), mean(exp(w))-exp(2.75)))
print(c(ndiffs(nhtemp), ndiffs(nhtemp,type="trend")))
trm<-ts(read.csv("Htmls_Series/datos/trm_mensual_2015-01_2026-06.csv")$trm,start=c(2015,1),frequency=12); print(nsdiffs(trm))
print(abs(170.8-171)<=0.2); print(abs(171.2-171)<=0.2)
