# coding=utf-8
__author__ = 'rodrigo'
from utils.fnc import rules_then, rules_bithen, rules_negative_parentheses, rules_negative_double, rules_or, simplify, rules_negative
from utils.validation import isPredicate, tokenizador


class EquivalenceRule ():

  @classmethod
  def run(cls, propositions, conclusion):

    formules = []
    noSimplify = []
    print 'Formula Normal Conjuntiva'
    for proposition in propositions:
      #Função responsável por aplicar as regras de equivalência no conector implica

      formule = proposition
      if '->' in proposition:
        formule = rules_then(proposition)
        formule = filter(None, formule)

      #Eliminando o bi-implica
      if '<->' in formule:
        formule = rules_bithen(formule)
        formule = filter(None, formule)
      #
      # # #Equivalencia negação em parenteses


      formule = rules_negative(formule, '^')
      formule = rules_negative(formule, 'v')

      #Equivalencia negações duplas
      formule = rules_negative_double(formule)

      formule = rules_or(formule)
      noSimplify.append(formule)
      formules.append(simplify(formule))

    x, dict = calculate(formules)
    strconclusion = "".join(conclusion[0])

    print '*****************************'

    print 'Resultado da Equivalencia: '+x
    print 'Valor da conclusão: '+str(dict.get(strconclusion))
    print 'Conclusão: '+strconclusion
    print 'RESULTADO FINAL: '


    if x == strconclusion:
      print 'VERDADEIRO'
    else:
      print 'FALSO'


def calculate(formules):

  #Encontrar verdades
  new_formule = []
  resp = []
  dict = {}
  oposto = {}
  count = 0
  size = len(formules) - 1
  tic = 0
  while count < size :

    for formule in formules:
      ispredicate, value = isPredicate(formule)

      if ispredicate:
        x = dict.get(formule)
        if x is None:
          if value:
            count +=1
            dict[formule] = value
            dict['~'+formule] = not value
          else:
            res = formule.replace('~ ', '~')
            dict[res] = not value
            dict[res.replace('~', '').strip()] = value

    for formule in formules:
      aux = []
      strformule = formule.replace('~ ', '~')
      for component in strformule.split(' '):
        token = tokenizador(component)

        if token == 'atomo':

          value = dict.get(component)

          if value is not None:
            aux.append(str(value))
          else:
            aux.append(str(component))
        else:
          aux.append(component)

      array = " ".join(aux).split(' v ')

      if len(array) > 1:

        if array[0] == 'True' or array[1] == 'True':
          count +=1
          aux = ['True']

        elif array[0] == 'False':
          aux = [array[1]]

        elif array[1] == 'False':
          aux = [array[0]]


      new_formule.append(" ".join(aux))

    formules = new_formule
    resp = new_formule
    new_formule = []

  result = ''
  for r in resp:
    if not result:
      result = r
    else:
      if r == 'False':
        result = 'False'
      elif r != 'True':
        result = r

  return result, dict



