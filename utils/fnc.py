# coding=utf-8
import Queue
import re

__author__ = 'rodrigo'

from utils.validation import validation_premisse, tokenizador


######################
######AUXILIARES######
######################

def syncFormule(formule, keys):
  """
  :argument - Função responsável por atualizar a formula utilizando as chaves temporárias.
  :param    - Recebe a formula em array e o respectivo array de chaves temporárias.
  :return   - Retorna a formula em string com as chaves atualizadas.
  """
  aux = " ".join(formule).split(" ")
  count = len(aux)
  for a in aux:
    if a in keys:
      value = " ".join(keys.get(a))
      value = "( "+value+" )"
      aux[count - 1] = value
  count +=1

  return " ".join(aux).split(" ")


def simplify(formule):
  #PARENTHES ATOMO PARANTHES
  string = " ".join(formule)

  myre = re.compile(r'([\w])')
  atalho = re.findall(myre, string)
  for a in atalho:
    aux = "( "+a+" )"
    aux2 = "( ~ "+a+" )"

    if aux in string:
      string = string.replace(str(aux), str(a))

    if aux2 in string:
      string = string.replace(str(aux2), "~ "+str(a))

  myre = re.compile(r'([)+])')
  cps = re.findall(myre, string)
  cps_size = len(cps)

  myre = re.compile(r'([(+])')
  ops = re.findall(myre, string)
  ops_size = len(ops)

  atalho = list(set(atalho))

  if ops_size > cps_size:
    dif = ops_size - cps_size
    string = string.replace('( ', '', dif)

  elif ops_size < cps_size:
    dif = cps_size - ops_size
    reverse = string[::-1]
    reverse = reverse.replace(' )', '', dif)
    string = reverse[::-1]

  for a in atalho:
    aux = "( "+a+" v "+a+" )"
    if aux in string:
      string = string.replace(str(aux), str(a))

  array = string.split(' ')

  if array[0] == '(':
    string = string.replace('( ', '').replace(' )', '')

  string = string.replace('~ ~ ', '')

  return string


#######################
######ELIMINAÇÕES######
#######################

#THEN
def elimination_then(prop1, prop2):

  formule = ['(','~', '(']
  for p in prop1:
    formule.append(p)
  formule.append(')')
  formule.append('v')
  for p in prop2:
    formule.append(p)
  formule.append(')')
  return formule

#BITHEN
def elimination_bithen(prop1, prop2):
  #((~ p v q ) ^ (p ^ q))
  formule = ['(', '(', '~']

  for p in prop1:
    formule.append(p)
  formule.append('v')
  for p in prop2:
    formule.append(p)
  formule.append(')')

  formule.append('^')

  formule.append('(')
  for p in prop1:
    formule.append(p)
  formule.append('v')
  for p in prop2:
    formule.append(p)

  formule.append(')')

  formule.append(')')

  return formule

def elimination_negative_parentheses(propositions, op):

  dict = {
    '^': 'v',
    'v': '^'
  }
  formule = ['(']
  count = 1

  predicates = " ".join(propositions).split(op)
  pred1 = predicates[0]
  pred2 = predicates[1]
  formule.append('~')
  formule.append(pred1)
  formule.append(dict.get(op))
  formule.append('~')
  formule.append(pred2)
  # size = len(propositions)
  # for proposition in propositions:
  #   formule.append('~')
  #   for component in proposition:
  #     formule.append(component)
  #   if count < size:
  #     formule.append(dict.get(op))
  #   count += 1
  formule.append(')')
  #
  return formule

def elimination_or(propositions, atomico):
  formule = []
  count = 1
  size = len(propositions)
  for proposition in propositions:
    formule.append('(')
    formule.append(atomico)
    formule.append('v')
    formule.append('(')
    for p in proposition:
      formule.append(p)
    formule.append(')')
    formule.append(')')
    if count < size:
      formule.append('^')
    count += 1

  return formule


##################
######REGRAS######
##################

def rules_then (input):
  """
  :argument - Função responsável por encontrar casos de implica e aplicar a FNC
  :param    - Recebe um array da proposição
  :return   - Retorna a proposição em string
  """

  #Proposição em string
  str_proposition = " ".join(input)

  #Dicionário com o valor referente a cada chave instancia
  dict = {}
  #Variaveis auxilares para criação dos nomes da chaves
  key_name = 'key'
  key_num = 1
  #Array de chaves criadas
  keys = []

  #Processo para encontrar a formula mais interna
  str_proposition = str_proposition.replace(' ) ', ' ( ').replace(' )', '  ( ')
  propositions = str_proposition.split(' ( ')
  propositions = filter(None, propositions)


  #Eliminando todos os implicas
  while ' ->' in " ".join(propositions):
    #Variavel auxilar utiliza na varredura do array de proposições
    count = 1

    #Removendo espaços em branco do array
    propositions = filter(None, propositions)

    #Inciando varredura do array
    for proposition in propositions:
      #Transformando a string em array separado por espaço em branco e removendo vazios do array
      array = proposition.split(' ')
      array = filter(None, array)

      #Verificando se a proposição interna é valida
      if validation_premisse(array):

        #Verificando se a formule tem implica
        if '->' in array:
          #Separando as proposições em componentes
          components = proposition.split(' -> ')
          #Quantidade de componentes
          size = len(components)
          #Verificando se a operação implica possui mais de 2 componentes
          if size > 2:
            components = [components[0], components[size -1]]

          #Verficando se os componentes são chaves do dicionário
          if components[0] in key_name:
            #Recuperando componente/formula
            p1 = dict.get(components[0])
          else:
            #Seperando o primeiro componente em um array
            p1 = components[0].split(' ')

          if components[1] in keys:
            #Recuperando componente/formula
            p2 = dict.get(components[1])
          else:
            #Seperando o segundo componente em um array
            p2 = components[1].split(' ')

          #Eliminando implica por sua equivalência
          formule = elimination_then(p1, p2)

          #Verificando se é a primeira formula das proposições
          if count > 1:
            #Apos a resolução atualizamos a formula anterior com a formula sem implica

            key_name ='key'+ str(key_num) #Criando uma nova chave
            keys.append(key_name)
            dict[key_name] = formule #Adicionando chave e formula (Valor) no dicionário

            #Variavel auxilar para armazenar o valor da formula anterior
            aux = propositions[count -2]
            #Atualizando o valor da formula anterior acrescentando o valor da formula sem implica
            propositions[count - 2] = aux +' '+ key_name
            #Removendo formula solucionada
            propositions.remove(proposition)
            #Atualizando variavel para criação de chaves
            key_num += 1
          else:
            #Caso seja a primeira formula do array, apenas atualizamos o seu valor
            propositions = formule

      else:
        print 'invalida'
      #Contador para saber a posição do array
      count += 1

  #Após aplicar as regras de equivalência referente ao implicar vamos sincronizar com a formula final.
  propositions = syncFormule(propositions, dict)
  return propositions


#CASE BITHEN FOR FNC
def rules_bithen(input):
  """
  :argument - Função responsável por encontrar casos de bimplica e aplicar a FNC
  :param    - Recebe um array da proposição
  :return   - Retorna a proposição em string
  """

  #Transformando entrada em String
  str_proposition = " ".join(input)

  #Dicionario que irá salvar as chaves criadas e as formulas tratadas, sem bimplica.
  dict = {}
  keys = []

  #Nomes das chaves
  key_name = 'key'
  key_num = 1

  #Encontrando formulas mais internas
  str_proposition = str_proposition.replace(' ) ', ' ( ').replace(' )', '  ( ')
  propositions = str_proposition.split(' ( ')
  propositions = filter(None, propositions)

  loop = 0
  bimplica = 0

  #Loop para eliminar por equivalência o conector bimplica
  while '<->' in " ".join(propositions):

    #Variavel auxilar para acompanhamento da varredura do array de proposições
    count = 1

    for proposition in propositions:

      array = proposition.split(' ')
      array = filter(None, array)
      if validation_premisse(array):

        #Verificando se a formule tem bimplica
        if '<->' in proposition:
          bimplica += 1
          #Seperando em componentes a proposition a partir do bimplica
          components = proposition.split(' <-> ')
          components = filter(None, components)
          #Quantidade de componentes
          size = len(components)
          if size > 2:
            components = [components[0], components[size -1]]

          if components[0] in key_name:
            p1 = dict.get(components[0])
          else:
            p1 = components[0].split(' ')

          if components[1] in keys:
            p2 = dict.get(components[1])
          else:
            p2 = components[1].split(' ')

          formule = elimination_bithen(p1, p2)


          if count > 1:
            key_name ='key_name'+ str(key_num)
            keys.append(key_name)
            dict[key_name] = formule

            aux = propositions[count -2]
            propositions[count - 2] = aux +' '+ key_name
            propositions.remove(proposition)
            key_num += 1
          else:
            propositions = formule
        else:
          if count > 1:
            key_name ='key'+ str(key_num)
            keys.append(key_name)

            dict[key_name] = array

            aux = propositions[count -2]
            propositions[count - 2] = aux +' '+ key_name
            propositions.remove(proposition)
            key_num += 1

      else:
        print 'invalida'
      count += 1
    loop += 1
    propositions = filter(None, propositions)

  propositions = syncFormule(propositions, dict)
  return propositions


def rules_negative(components, op):
  old_token = ''
  possible = False
  queue = Queue.LifoQueue()
  partial = []
  formule = []

  #Varrendo componentes
  for component in components:
    #TOKEN
    token = tokenizador(component)
    #Caso encontrado
    if possible:
      #Encontrando formula interna.
      if token == 'close_parentheses':
        queue.get(')')

        #Fim de formula interna
        if queue.empty():
          #Verificar se em parcial tem op
          if op in " ".join(partial):
            result = elimination_negative_parentheses(partial, op)
            formule = formule + result

          else:
            formule.append('~')
            formule.append('(')
            formule = formule + partial
            formule.append(')')

          partial = []
          possible = False


      else:
        partial.append(component)



    elif token == 'open_parentheses' and old_token == 'negative':
      possible = True
      queue.put(')')

    else:
      if token != 'negative' and not possible:
        if old_token == 'negative':
          formule.append('~')
        formule.append(component)


    old_token = token


  return formule

def rules_negative_parentheses(components, op):
  older_token = ''
  possible = False
  formule = []
  partial = []
  queue = Queue.LifoQueue()
  resolved = False
  internal = False
  point = False
  count = 0
  update = False

  for component in components:
    token = tokenizador(component)
    if possible:
      if token == 'close_parentheses':
        queue.get(')')

        if queue.empty():

            formule.append(partial)
            partial = []
            internal = False
            update = True
            resolved = True
            # if op in partial:
            formule = elimination_negative_parentheses(formule, op)
            aux = components[:point]
            formule = aux + formule
            possible = False


      if token == 'open_parentheses':
        queue.put(')')
        internal = True

      if token == 'conector':
        if component != op and not internal:

          possible = False

        if component == op and not internal:
          formule.append(partial)
          partial = []

      if not resolved:
        if component == op and not internal:
          print 'ok'
        else:
          partial.append(component)

    else:
      if token == 'open_parentheses':
        if older_token == 'negative':
          queue.put(')')
          possible = True
          formule = []
          point = count - 1
      older_token = token
    count += 1
  if update:
    return formule

  else:
    return components


def rules_negative_double(components):
  older_token = ''
  count = 1
  for component in components:
    token = tokenizador(component)
    if token == 'negative':
      if older_token == 'negative':
        components[count - 1] = ''
        components[count - 2] = ''
    older_token = token
    count += 1

  return filter(None, components)

def rules_or(components):
  older_token = ''
  possible = False
  formule = []
  partial = []
  queue = Queue.LifoQueue()
  resolved = False
  internal = False
  point = False
  count = 0
  update = False
  last_token = ''

  for component in components:
    token = tokenizador(component)
    if possible:
      if token == 'close_parentheses':

        queue.get(')')

        if queue.empty():
          formule.append(partial)
          partial = []
          internal = False
          update = True
          resolved = True
          formule = elimination_or(formule, last_p)
          aux = components[:point]
          formule = aux + formule
          possible = False


      if token == 'open_parentheses':
        queue.put(')')
        internal = True

      if token == 'conector':
        if component != '^' and not internal:

          possible = False

        if component == '^' and not internal:
          formule.append(partial)
          partial = []

      if not resolved:
        if component == '^' and not internal:
          print 'ok'
        else:
          partial.append(component)

    else:

      if token == 'open_parentheses':
        if older_token == 'v':
          if last_token != '^':
            queue.put(')')
            possible = True
            formule = []
            point = count - 2

      if token == 'conector':
        last_token = older_token
        older_token = component
      if token == 'atomo':
        last_p = component

    count += 1
  if update:
    return formule

  else:
    return components