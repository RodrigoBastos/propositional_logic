# coding=utf-8
import Queue
import math
from nltk import data
from resolutions.tabela_verdade import binaryStringCalc
from utils.config import formule_and, formule_or, formule_then, formule_bithen, lp_to_ln, formule_isnot, lp_lang
from utils.validation import tokenizador

__author__ = 'rodrigo'


class TrueTable():

  @classmethod
  def generate_truetable(cls, promises, derivation, propositions, conclusion):
    #Encontrar todos os componentes
    propositions.append("".join(conclusion))
    promises.append(derivation)
    components = get_components(promises)

    #Gerando possibilidades
    possibilities = soma_binaria(len(components))

    truetable = []

    #Informações da Tabela
    str_components = " | ".join(components)
    str_propositions = " | ".join(propositions)

    #First Row
    if len(promises) - 1  == 1:
      singlePromise = True
      truetable.append(str_components+" | "+str_propositions+' | -> ')
    else:
      singlePromise = False
      truetable.append(str_components+" | "+str_propositions+' | ^ | -> ')
    #Quantidade de promises
    promises_size = len(promises)
    #Auxiliar
    conclusion_result = ''

    check_value = True
    #Analisando todas as possibilidades
    for possibility in possibilities:
      check_conclusion = True
      #Dados da Tabela
      str_possibility = " | ".join(str(b) for b in possibility)
      line = str_possibility
      count = 1
      #Varrendo atomicos
      for promise in promises:
        #Calculando problema de acordo com as possibilidades
        # result = calculateProblem(promise, possibility, components)
        result = broke_formule(promise, possibility, components)
        if count == promises_size:
          conclusion_result = result
        #Adicioandno resultados na linha da Tabela
        line +=  " | "+str(result)
        if result == 'False' and count < promises_size:
          check_conclusion = False
        count += 1


      if not singlePromise:
        if not check_conclusion:
          line +=  " | "+'False'
        else:
          line +=  " | "+'True'

      value = formule_then.get(str(check_conclusion)+" then "+conclusion_result)

      if value == 'False':
        check_value = False

      line +=  " | "+value
      #Nova linha
      truetable.append(line)

    # for tt in truetable:
    #   print tt

    first = truetable[0].split('|')
    row_format ="{:>11}" * (len(first) + 1)
    for tt in truetable:
      print row_format.format("", *tt.split('|'))

    if check_value:
      print "TAUTOLOGIA"
    else:
      print "Fórmula Não válida"


def bin_to_bool(result):
  list_bool = []
  list_bin = map(str.strip, result)
  for bin in list_bin:
    if bin == '0':
      list_bool.append(False)
    else:
      list_bool.append(True)
  return list_bool


def soma_binaria(components_size):
  total = int(math.pow(2,components_size))
  a = 0
  aux = 0
  results = []
  for i in range(0, total):
    somatorio = str(a)+" + "+str(aux)

    result  = binaryStringCalc(somatorio)
    a = result
    qtd = components_size - len(result)
    if qtd > 0:
      for q in range(0, qtd):
        result = '0'+result
    aux = 1
    results.append(bin_to_bool(result))
  return results

def get_components(promises):
  components = []
  for promisse in promises:
    for alfa in promisse:
      if alfa not in lp_lang:
        if alfa not in  components:
          components.append(alfa)
  return components

def broke_formule(promise, possibility, components):
  values = {}
  count = 0
  result = None
  for component in components:
    values[str(component)] = possibility[count]
    count += 1

  need_queue = Queue.LifoQueue()
  #Formule Final
  final_formule = []
  internal_formule = []
  partial_formule= []
  state_parantheses = False
  new_list = False
  end_formule = False
  list_conectors = []
  list_components = []
  isFormuleInternal = False


  for p in promise:

    token = tokenizador(p)
    state_parentheses = False
    if token == 'open_parentheses':
      state_parantheses = True
      #Verifica se é uma formula interna interna
      if isFormuleInternal:
        for p in partial_formule:
          internal_formule.append(p)

        # internal_formule.append(partial_formule)
        partial_formule = []
        #Salvar a lista parcial
        #Gerar nova lista

        #Já é uma formula interna
        isFormuleInternal = True
        #Adicionando pendencia na pilha
        need_queue.put(")")

    elif token == 'close_parentheses':
      state_parantheses = True
      need_queue.get(")")

      if need_queue.empty() and len(internal_formule) > 0:
        partial_formule = internal_formule
        internal_formule = []

      count = len(internal_formule)
      result = resolverFormule(partial_formule, values,list_components, list_conectors)

      if count == 0:

        final_formule.append(result)

      else:

        internal_formule.append(result)

      if need_queue.empty():
        partial_formule = []
        isFormuleInternal = False

    if token == 'conector' and p not in list_conectors :
      list_conectors.append(p)

    if token =="atomo" and p not in list_components:

      list_components.append(p)


    #Condições de leituras:
    if not isFormuleInternal and not state_parantheses:
      #Adicionar na Final
      final_formule.append(p)
    else:
      if not state_parantheses:
        #Adicionar na Parcial
        partial_formule.append(p)

  if final_formule[0] == 'True' or final_formule[0] == 'False' and len(final_formule) == 1:
    return final_formule[0]

  result = resolverFormule(final_formule, values,list_components, list_conectors)

  return result


def resolverFormule(formule, values, atomicos, conectores):
  back = ''
  bools = ['True', 'False']
  new_formule = []

  for f in formule:
    if f in atomicos or f in bools:

      if back == '~':

        if f in bools:
          component = formule_isnot.get('not '+str(f))
        else:
          component = formule_isnot.get('not '+str(values.get(f)))
        new_formule.append(component)
      else:
        if f in bools:
          component = str(f)
        else:
          component = values.get(str(f))
        new_formule.append(component)
    if f in conectores:
      new_formule.append(lp_to_ln.get(f))


    back = f
  result_problem = []
  #Ordem de precedência ~  ^  v   ->   <->
  if 'and' in new_formule:
    new_formule = solution(new_formule, 'and', formule_and)
  if 'or' in new_formule:
    new_formule = solution(new_formule, 'or', formule_or)
  if 'then' in new_formule:
    new_formule = solution(new_formule, 'then', formule_then)
  if 'bithen' in new_formule:
    new_formule = solution(new_formule, 'bithen', formule_bithen)


  return str(new_formule[0])


def solution(new_formule, op, rule):
  eq = ''
  resolved = False
  result_queue = Queue.LifoQueue()
  result_problem = []
  aux = new_formule
  for nf in aux:
    if resolved:
      x = rule.get(str(result_queue.get())+' '+str(op)+' '+str(nf))
      result_queue.put(x)
      size = len(result_problem) - 1

      result_problem = result_problem[0:size]
      result_problem.append(x)
      resolved = False
    else:
      if nf == op:
        resolved = True
      else:
        result_queue.put(nf)
        result_problem.append(nf)

  return result_problem
