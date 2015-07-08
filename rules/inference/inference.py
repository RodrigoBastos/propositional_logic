# coding=utf-8
import Queue
from Proposition import Propostion
from utils.validation import tokenizador, validation_premisse

__author__ = 'rodrigo'

import re


def components_valid(components):
  isValidAllComponent = True
  for component  in components:
    if not component.isValid:
      isValidAllComponent = False

  return  isValidAllComponent


def isConectorComponent(components):
  index = None
  i = 0
  for component in components:
    if tokenizador(component) == 'conector':
      index = i
      break
    i += 1

  return index

def generateproposition(array):
  text = " ".join(array)
  print text
  text = text.replace(' (', '(').replace('( ', '(').replace(' ) ', '(').replace(' )', '(')
  formulas = text.split('(')
  formulas = filter(None, formulas)

  components = []
  print formulas
  ok = False
  for formula in formulas:
    if validation_premisse(formula.split(" ")):
      ok = True
    else:
      ok = False

    components.append(Component(formula, ok))


  #Verificar se todos os components são validos.
  premissa = []
  propositions = []
  if components_valid(components):
    if '->' in components[0].text:
      premissa = components[0].text.split(' -> ')
      propositions.append(Propostion(premissa[0], '->', premissa[1], components[0].text))
      print premissa
    elif 'v' in components[0].text:
      premissa = components[0].text.split(' v ')
      propositions.append(Propostion(premissa[0], 'v', premissa[1], components[0].text))
      print premissa
    elif '^' in components[0].text:
      premissa = components[0].text.split(' ^ ')
      propositions.append(Propostion(premissa[0], '^', premissa[1], components[0].text))
      print premissa

  else:
    i = 0
    print 'oi'
    #verificar se existe um conector sozinho
    index = isConectorComponent(components)
    if index:
      print index



class Component():
  text = None
  isValid = False

  def __init__(self, text, isValid):
    self.text = text
    self.isValid = isValid




# print validation_premisse('p ^ r')

def run_inference_rules(propositions, conclusion):
  temp_num = 1
  premissas = []
  prop_to_temp = {}
  temp_to_prop = {}
  temps = []

  for proposition in propositions:

    isFormuleInternal = False
    state_parentheses = False
    queue = Queue.LifoQueue()
    internal = []
    partial = []
    final = []

    print proposition
    for component in proposition:
      state_parentheses = False
      print 'INCIANDO'
      print component
      token = tokenizador(component)
      #Verificando o componente é uma abertura
      if token == 'open_parentheses':
        print 'Iniciando formula interna'
        #Estado de abertura
        state_parentheses = True

        #Verifica se é uma formula interna interna
        if isFormuleInternal:
          print '+Interna'
          for p in partial:
            internal.append(p)
          partial = []


        #Já é uma formula interna
        isFormuleInternal = True
        #Adicionando pendencia na pilha
        queue.put(")")

      elif token == 'close_parentheses':
        print 'Fim de formula interna - Criar Temporario'
        #Estado de Fechamento
        state_parentheses = True
        #Removendo pendencia na pilha
        queue.get(")")

        if queue.empty() and len(internal) > 0:
          partial = internal
          internal = []

        formule = " ".join(partial)

        print 'String formule: '+formule
        #Verificando se já existe temporia com essa formula
        temp = prop_to_temp.get(formule)
        print 'TEMPORARIO'
        print temp
        #Se não existe temporario, vamos criar um novo
        if not temp:
          print 'Novo Temporario'
          temp = 'temp'+str(temp_num)
          temp_num += 1
          prop_to_temp[formule] = temp
          temp_to_prop[temp] = formule
          temps.append(temp)
          print prop_to_temp

        size = len(internal)
        if size > 0:
          print 'Adicionando na formula interna'
          internal.append(temp)

        else:
          print 'Lista interna vazia. Adicionar na lista Final'
          final.append(temp)

        #verificando se a pilha ta vazia
        if queue.empty():
          print 'Pilha vazia. Fim de formula interna'
          partial = []
          isFormuleInternal = False

      if not isFormuleInternal and not state_parentheses:
        print 'Adicionar na final'
        final.append(component)
      else:

        if not state_parentheses:
          print "Adicionar na parcial"
          partial.append(component)

    print 'FIM DE PROPOSIçÂO'
    print final
    premissas.append(final)

  print premissas
  print prop_to_temp
  print temps
  i = 0
  j = 0
  stop = premissas
  print 'STOP'
  print stop


  #Aplicando regras de inferencias
  size = len(premissas)
  while len(stop) > 0 :
    print 'PREMISSAS: '+str(len(stop))
    print premissas
    # if i == size:
    #   break
    if j != i:
      print j
      print i
      result, rule = inference_machine(premissas[i], premissas[j], temps)
      if result:
        p1 = premissas[i]
        p2 = premissas[j]
        #Tenho resultado
        print 'CASO 1 :'+rule
        print 'Propositions: '+" ".join(p1)+' ---- '+" ".join(p2)
        print 'Resultado: '+result
        if result in temps:
          result = temp_to_prop.get(result)
        stop.remove(p1)
        stop.remove(p2)
        premissas.append(result.split(' '))
        size = len(premissas)

        print 'PREMISSAS'
        print premissas
        i = 0
        j = 0
      else:
        if j  >= size - 1:
          i += 1
          j = 0

        else:
          j +=1
    else:
      if j < size -1:
        j +=1
      else:
        break
  text =''
  for premissa in premissas:
    text += " ".join(premissa)
  print text
  print ' '.join(conclusion)

  if " ".join(conclusion) == text:
    print "VERDADE"
  else:
    print "FALSO"


def modus_ponens(x, y, temps):
  result = None
  print 'MODUS PONES'
  if ' -> ' in ' '.join(x):
    array = ' '.join(x).split(' -> ')
    x1 = array[0]
    x2 = array[1]
    y1 = y[0]
    if x1 == y1:
      result = x2

  return result
  # result = None
  # print 'MODUS PONES'
  # if tokenizador(" ".join(x)) == 'atomo' or " ".join(x) in temps:
  #   if '->' in ' '.join(y):
  #     # array = prop2.remove('->')
  #     if ' '.join(x) == y[0]:
  #       print 'São iguais'
  #       result = y[2]
  # return  result

def modus_tollens(x, y):
  print 'MODUS TOLLENS'

  result = None
  if '~' in " ".join(x):
    component = x[1]
    if tokenizador(component) == 'atomo':
      if '->' in ' '.join(y):
      # array = prop2.remove('->')
        if component == y[2]:
          print 'São iguais'
          result = '~ '+y[0]
  return result

def silogismo_hipotetico(x, y):
  print 'silogismo_hipotetico'
  result = None
  if '->' in ' '.join(x):
    if '->' in ' '.join(y):
      if x[2] == y[0]:
        result = x[0]+' -> '+y[2]

  return result

def silogismo_disjuntivo(x, y):
  result = None
  if  'v' in " ".join(x):
    print 'OR'
    if '~' in ' '.join(y):
      print 'NEG'
      if len(x) == 3:
        print '3'
        components = " ".join(x).split(' v ')
        print components

        if components[0] == y[1]:
          print'iguais'
          result = components[1]
  return result

def inference_machine(prop1, prop2, temps):
  #verificar modus ponens
  print 'INFERECE'
  print " ".join(prop1)
  print ' '.join(prop2)
  rule = 'Modus Ponens'
  result = modus_ponens(prop1, prop2, temps)
  if not result:
    print 'Sem resultado'
    print " ".join(prop1)
    print ' '.join(prop2)
    result = modus_ponens(prop2, prop1, temps)
    if result:
      return  result, rule
  else:
    return result, rule

  rule = 'Modus Tollens'
  print " ".join(prop1)
  print ' '.join(prop2)
  result = modus_tollens(prop1, prop2)
  if result:
    return result, rule
  else:
    print 'Sem resultado'
    print " ".join(prop1)
    print ' '.join(prop2)
    result = modus_tollens(prop2, prop1)
    if result:
      return result, rule
    print 'Sem resultado'


  print " ".join(prop1)
  print ' '.join(prop2)
  rule = 'Silogismo Hipotético'
  result = silogismo_hipotetico(prop1,prop2)
  if result:
    return  result, rule

  rule ='Silogismo'
  result = silogismo_disjuntivo(prop1, prop2)
  if result:
    return result, rule
  else:
    print 'sem resultado'
    result = silogismo_disjuntivo(prop2, prop1)
    if result:
      return result, rule
    print 'sem resultado'

  return  result, rule


# generateproposition(['p', '->', '(', 'q', '^', 'r', ')'])
# generateproposition(['p', '^', 'q', '^', 'r'])
# run_inference_rules([['p', '->', '(', 'q', '^', 'r', ')'], ['(', 'q', '^', 'r', ')', '->', 's'], ['s', '->', '(', 't', 'v', '(', '~', 't', '->', 'u', ')', ')'], ['p'], ['~', 't']], ['~', 't', '->', 'u'])
run_inference_rules([['p', '->', 'q'],['q', '->', 'r'], ['s', 'v', 'p'], ['~', 's']], ['r'])




