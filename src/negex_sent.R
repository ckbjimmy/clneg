library(stringr)

neg = read.table("~/git/negex/negex.python/Annotations-1-120.txt", sep="\t", fill=T, header = T)
n = neg[neg$Negation=='Negated',]
n$Sentence = gsub("(\\.+|[[:punct:]])", " \\1 ", n$Sentence)
n$Sentence = gsub("(?<=[\\s])\\s*|^\\s+|\\s+$", "", n$Sentence, perl=TRUE)
n$Sentence = sapply(n$Sentence, tolower)
n = n[!duplicated(n$Sentence), ]
write.table(n$Sentence, "~/Desktop/nlp_final/negex", quote=F, row.names=F, col.names=F)
