# coding=utf-8
__author__ = 'rodrigo'


def start_true_table(atomos, promisses):
  """
  Utilizar números binários para popular tabela verdade
  FFF - 000
  FFV - 001
  FVF - 010
  FVV - 011
  VFF - 100
  VFV - 101
  VVF - 110
  VVV - 111
  """


def binaryStringCalc(strValue):
  result = 0
  for v in strValue.split(' + '):
    result += int(v,2)
  return str(bin(result)).split('0b')[1]
