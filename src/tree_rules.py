# tree rules

trts = {}
# no "jvd|murmurs|deficits" not work, pleural -> vbz?
# trts['NP'] = ('NP=target << DT=neg <<, /no|without/ !> NP >> TOP=t >> S=s', \
#               'excise s target,delete neg')

# if np with top node=S???
# trts['NP'] = ('NP=target << DT=neg <<, /no|without/ !> NP >> TOP=t >> S=s', \
#               'excise s target,delete neg')
trts['NP'] = ('NP=target << DT=neg <<, /no|without/ !> NP >> TOP=t', \
              'delete neg')
# if np with top node=NP
trts['NP-nS'] = ('NP=target <<, /DT|NN|RB/=neg <<, /no|without/ !> NP >> TOP=t', \
              'delete neg')


# denies -> mis pos to nns
trts['NP-denies'] = ('NP=target <<, /denies|deny|denied/=neg >> TOP=t', \
              'delete neg')

# vp only
trts['VP-A'] = ('VP=target << /VB*/=neg <<, /denies|deny|denied/ >> TOP=t', \
              'delete neg')
# vp only, 'resolved', add that neg1 part to prevent jvd -> VP, rashes -> VP error pos tagging
trts['VP-P'] = ('NP=target <<, DT=neg1 <<, /no|negative|not/ $ VP=neg2 >> TOP=t >> S=s', \
              'delete neg1')
# this is post, ... is negative
trts['ADJP-P'] = ('VP=vp < ADJP <<- /negative/=neg $ NP=target >> TOP=t >> S=s', \
                'delete vp,excise s target')
# this is ant, negative for ...
trts['ADJP-A'] = ('PP=head $ JJ=neg < NP=target >> TOP=t > ADJP=s', \
                'delete neg')
# not
trts['ADVP-P'] = ('VP=target <<, /VB*|MD/ $ RB=neg >> TOP=t >> S=s', \
                'excise s target')

trts['ADVP-A'] = ('VP=target <<, /VB*|MD/ $ RB=neg >> TOP=t >> S=s', \
                'excise s target')
# remove sbar
trts['ADVP-sbar'] = ('PP=head <<, /of|without/=neg > NP $ NP < NP=target >> TOP=t >> NP=st << SBAR=sbar', \
                'excise st target,delete sbar')
# remove RB
trts['ADVP-RB'] = ('TOP=target <<, RB=neg', \
                'delete neg')

# sob become this, so need to be after np and vp
trts['PP'] = ('PP=head <<, /of|without/=neg > NP $ NP < NP=target >> TOP=t >> NP=s', \
              'excise s target')
trts['PP-2'] = ('PP=head << IN=neg <<, /of|without/ >> TOP=t', \
                'delete neg')

trts['NP-CC'] = ('S=s < NP =head<< PP=target << DT=neg <<, /no|without/ < CC=but << but < S=rm < /\.|\,/=punct << SBAR=sbar !> NP > TOP=t', 
                 'delete neg,delete sbar,delete punct,delete but,delete rm')
trts['NP-although'] = ('S=s < NP =head<< PP=target << DT=neg <<, /no|without/ << /although|but/ < /\.|\,/=punct << SBAR=sbar !> NP > TOP=t', 
                       'delete neg,delete sbar,delete punct')