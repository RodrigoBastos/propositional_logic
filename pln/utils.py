# coding=utf-8
__author__ = 'rodrigo'
from corpus import ligation, implies, conjuntion, disjuntion, negative


def tokenize(word):
  #verificando se a palavra é um auxiliar de ligação
  if word in ligation:
    return 'ligation'
  elif word in implies:
    return 'implies'
  elif word in conjuntion:
    return 'conjuntion'
  elif word in disjuntion:
    return 'disjuntion'
  elif word in negative:
    return 'negative'
  else:
    return 'subject'

class Word():
  text = ''
  token = ''

  def __init__(self, text, token):
    self.token = token
    self.text = text