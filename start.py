# coding=utf-8
__author__ = 'rodrigo'

from truetable.truetable import TrueTable
from utils.validation import validation_propositions
from rules.InferenceRule import InferenceRule
from rules.EquivalenceRule import EquivalenceRule

from pln.pln import Pln

#Teste
def start():

  #Por PLN
  # ln_premissa = ['Sérgio mora em Fortaleza então Sérgio mora no Brasil', 'Sérgio não mora no Brasil então Sérgio mora na Espanha', 'Sérgio mora no Brasil']
  # ln_conclusion = ['Sérgio não mora na Espanha']
  ln_premissa = ['João mora em Maceio então João mora em Alagoas', 'João mora em Alagoas então João mora no Brasil', 'João mora em Arapiraca ou João mora em Maceio', 'João não mora em Arapiraca']
  ln_conclusion = ['João mora no Brasil']
  input, conclusion, dict = Pln.toPL(ln_premissa+ln_conclusion)
  print 'Resuldado do PLN'
  print input
  print conclusion
  print dict

  print "*****************************************************************"
  print " "

  #Por LP

  #Validação da entrada
  premissas = validation_propositions(input)
  derivation = validation_propositions([conclusion])
  print 'Resuldado da Validaçao'
  print premissas
  print derivation

  print "*****************************************************************"
  print " "

  if premissas and derivation:
    #Por tabela Verdade
    print 'Resolvendo por Tabela Verdade'
    TrueTable.generate_truetable(premissas, derivation[0], input, conclusion)

    print "*****************************************************************"
    #Por equivalencia
    print 'Resolvendo por Equivalência'
    EquivalenceRule.run(premissas, derivation)


    print "*****************************************************************"

    # Por regras de inferencia
    print 'Resovlendo por Regras de Inferencia'
    InferenceRule.run(premissas, derivation)

start()