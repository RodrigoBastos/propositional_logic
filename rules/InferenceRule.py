# coding=utf-8
import Queue
from utils.validation import tokenizador

__author__ = 'rodrigo'

class InferenceRule():

  @classmethod
  def run(cls, propositions, conclusion):
    temp_num = 1
    premissas = []
    prop_to_temp = {}
    temp_to_prop = {}
    temps = []

    for proposition in propositions:

      isFormuleInternal = False
      queue = Queue.LifoQueue()
      internal = []
      partial = []
      final = []

      for component in proposition:
        state_parentheses = False
        token = tokenizador(component)
        #Verificando o componente é uma abertura
        if token == 'open_parentheses':
          #Estado de abertura
          state_parentheses = True

          #Verifica se é uma formula interna interna
          if isFormuleInternal:
            for p in partial:
              internal.append(p)
            partial = []


          #Já é uma formula interna
          isFormuleInternal = True
          #Adicionando pendencia na pilha
          queue.put(")")

        elif token == 'close_parentheses':
          #Estado de Fechamento
          state_parentheses = True
          #Removendo pendencia na pilha
          queue.get(")")

          if queue.empty() and len(internal) > 0:
            partial = internal
            internal = []

          formule = " ".join(partial)

          #Verificando se já existe temporia com essa formula
          temp = prop_to_temp.get(formule)

          #Se não existe temporario, vamos criar um novo
          if not temp:
            temp = 'temp'+str(temp_num)
            temp_num += 1
            prop_to_temp[formule] = temp
            temp_to_prop[temp] = formule
            temps.append(temp)

          size = len(internal)
          if size > 0:
            internal.append(temp)

          else:
            final.append(temp)

          #verificando se a pilha ta vazia
          if queue.empty():
            partial = []
            isFormuleInternal = False

        if not isFormuleInternal and not state_parentheses:
          final.append(component)
        else:

          if not state_parentheses:
            partial.append(component)

      premissas.append(final)


    i = 0
    j = 0
    stop = premissas

    #Aplicando regras de inferencias
    size = len(premissas)
    case = 1
    while len(stop) > 0 :
      if j != i:
        result, rule = inference_machine(premissas[i], premissas[j], temps)
        if result:
          p1 = premissas[i]
          p2 = premissas[j]
          #Tenho resultado
          print '*******************************************************'
          print 'CASO '+str(case)+' :'+rule
          print 'Propositions: '+" ".join(p1)+' ---- '+" ".join(p2)
          print 'Resultado: '+result
          print '*******************************************************'

          case += 1
          if result in temps:
            result = temp_to_prop.get(result)
          stop.remove(p1)
          stop.remove(p2)
          premissas.append(result.split(' '))
          size = len(premissas)
          print premissas
          print ' '

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

    if " ".join(conclusion[0]) == text:
      print "Verdade"
    else:
      print "Falsa"


def inference_machine(prop1, prop2, temps):
  #verificar modus ponens
  rule = 'Modus Ponens'
  result = modus_ponens(prop1, prop2, temps)
  if not result:
    result = modus_ponens(prop2, prop1, temps)
    if result:
      return  result, rule
  else:
    return result, rule

  result = modus_tollens(prop1, prop2)
  if result:
    return result, rule
  else:
    result = modus_tollens(prop2, prop1)
    if result:
      return result, rule

  rule = 'Silogismo Hipotético'
  result = silogismo_hipotetico(prop1,prop2)
  if result:
    return  result, rule

  rule ='Silogismo Disjuntivo'
  result = silogismo_disjuntivo(prop1, prop2)
  if result:
    return result, rule
  else:

    result = silogismo_disjuntivo(prop2, prop1)
    if result:
      return result, rule

  return  result, rule

#MODUS PONES
def modus_ponens(x, y, temps):
  result = None
  if ' -> ' in ' '.join(x):
    array = ' '.join(x).split(' -> ')
    x1 = array[0]
    x2 = array[1]
    if len(y) <= 2:
      y1 = y[0]
      if x1 == y1:
        result = x2

  return result


def silogismo_disjuntivo(x, y):
  result = None
  if  'v' in " ".join(x):
    if '~' in ' '.join(y):
      if len(x) == 3:
        components = " ".join(x).split(' v ')
        if components[0] == y[1]:
          result = components[1]
  return result

def modus_tollens(x, y):
  result = None
  if '~' in " ".join(x):
    component = x[1]
    if tokenizador(component) == 'atomo':
      if '->' in ' '.join(y):
        # array = prop2.remove('->')
        if component == y[2]:
          result = '~ '+y[0]
  return result

def silogismo_hipotetico(x, y):
  result = None
  if ' -> ' in ' '.join(x):
    if ' -> ' in ' '.join(y):
      array = ' '.join(x).split(' -> ')
      x1 = array[0]
      x2 = array[1]

      array = ' '.join(y).split(' -> ')
      y1 = array[0]
      y2 = array[1]

      if x2 == y1:
        result = x1+' -> '+y2

  return result