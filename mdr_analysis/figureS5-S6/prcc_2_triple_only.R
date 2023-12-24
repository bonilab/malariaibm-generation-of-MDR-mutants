# read data ---------------------------------------------------------------
result = read.csv(sprintf('task4_auc_triple_only.csv'), header = TRUE)

# prcc --------------------------------------------------------------------

library(epiR)
r1 = result

# r1 = result[ result$mda_coverage > 0.8, ]

# r1 = r1[-7]

# plot(r1$mda_coverage, r1$V6)


prcc_res = epi.prcc(r1, sided.test = 2, conf.level = 0.95)
c_names = c ("Mutation Rate", "Treatment Coverage", "Mosquito Biting Rate", "Cost of Resistance", "Cycling Period" )
prcc_res = cbind(prcc_res, varname = c_names)
prcc_res = prcc_res[order(-abs(prcc_res$est)),]

# plot --------------------------------------------------------------------
# Increase margin size
# par(mar=c(10,10,0,0))
# par(mar = c(0, 0, 0, 0))
par(mar = c(6.5, 10.5, 4.5, 4.5), mgp = c(5, 1, 0))

x<-barplot(prcc_res$est,
           horiz=TRUE,
           names.arg=prcc_res$varname,
           # axes = FALSE,  
           # space = 0,         
           # col = c("darkgreen", "red"),
           xlim = c(-1, 1),
           ylim = c(5.5, 0),
           axes=FALSE, 
           las = 1,
           xlab = expression('Partial Rank Correlation Coefficient with AUC')
)

tx_offset = 0.09
prcc_res$x_pos = with(prcc_res, ifelse(est < 0, est - tx_offset, est - tx_offset))
text(prcc_res$x_pos, x , sprintf("%.3f",prcc_res$est) ,cex=1)
axis(3)

#-----
write.csv(prcc_res, "prcc_results_triple_only.csv", row.names=FALSE)
