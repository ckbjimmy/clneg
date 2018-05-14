library(stringr)

neg = read.table("../data/Annotations-1-120.txt", sep="\t", fill=T, header=T)
n = neg[neg$Negation=='Negated',]
nn = n
n$Sentence = gsub("(\\.+|[[:punct:]])", " \\1 ", n$Sentence)
n$Sentence = gsub("(?<=[\\s])\\s*|^\\s+|\\s+$", "", n$Sentence, perl=TRUE)
n$Sentence = sapply(n$Sentence, tolower)
n = n[!duplicated(n$Sentence), ]
write.table(n$Sentence, "../data/test_ready.txt", quote=F, row.names=F, col.names=F)
write.table(nn, "../data/for_negex.txt", sep="\t", quote=F, row.names=F, col.names=T)