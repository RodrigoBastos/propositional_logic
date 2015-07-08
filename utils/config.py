# coding=utf-8
__author__ = 'rodrigo'

lp_lang = ['->', '<->', '^', 'v', '(', ')', '~']

bad_alfa_intial = ['->', '<->', '^', 'v' ')']
#rule_imples: tem que ter duas condições.

bad_chars = ['@', '$', '%', '=', '-', '*', "[", "}", "]", "{", "&", "/", "\\"]

neg = ['~']
conectors = ['->', '<->', '^', 'v']
open_parentheses = ['(']
close_parentheses = [')']

tokens = {
  '~':'negative',
  '->':'conector',
  '<->':'conector',
  '^':'conector',
  'v':'conector',
  '(':'open_parentheses',
  ')':'close_parentheses',
  }


op_next_tokens = ['atomo', 'negative']
cp_next_tokens = ['conector', 'close_parentheses']
atomo_next_tokens = ['close_parentheses', 'conector']
conectors_next_tokens = ['atomo', 'negative', 'open_parentheses']
negative_next_tokens = ['atomo', 'open_parentheses', 'negative']


formule_and = {
  'False and False': 'False',
  'False and True': 'False',
  'True and False': 'False',
  'True and True': 'True'
}

formule_or = {
  'False or False': 'False',
  'False or True': 'True',
  'True or False': 'True',
  'True or True': 'True'
}

formule_then = {
  'False then False': 'True',
  'False then True': 'True',
  'True then False': 'False',
  'True then True': 'True'
}

formule_bithen = {
  'False bithen False': 'True',
  'False bithen True': 'False',
  'True bithen False': 'False',
  'True bithen True': 'True'
}

formule_isnot = {
  'not True':'False',
  'not False':'True'
}

lp_to_ln = {
  'v':'or',
  '^': 'and',
  '->': 'then',
  '<->': 'bithen',
  '~': 'not'
}


ptb_to_lp = ['então', 'implica', 'portanto', '' ]

trashed_ptb = ['']