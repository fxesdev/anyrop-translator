#!/usr/bin/python3
#this is terminal based, I might add a gui later, not now, its too complicated.

import os
import sys
ropa = open(sys.argv[1])
disasa = open(sys.argv[2])
disasb = open(sys.argv[3])
searchl = sys.argv[5]
for line in disasa:
  if 'pop pc' in line:
    os.system('echo ' + line + '>disasap')
disasap = open('disasap')
for lline in disasb:
  if 'pop pc' in lline:
    os.system('echo ' + lline + '>disasbp')
disasbp = open('disasbp')
for llline in ropa:
  if llline in disasa:
    if llline in disasbp:
      os.system('printf ' + "'" +  disasbp.split()[0] + disasbp.split()[1] + disasbp.split()[2] + disasbp.split()[3] + disasbp.split()[4] + "'")
    
