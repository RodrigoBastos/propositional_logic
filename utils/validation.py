# coding=utf-8
__author__ = 'rodrigo'
import Queue



from rules import rules_atomo, rules_cp
from pilha import Pilha
from config import bad_alfa_intial, bad_chars, lp_lang, tokens, op_next_tokens, cp_next_tokens, atomo_next_tokens, negative_next_tokens, conectors_next_tokens

#Ordem de precedência ~  ^  v   ->   <->

def preprocess(text):
  list_text = map(str.strip, text)
  filter_text = filter(None, list_text)
  text = "".join(filter_text)
  #Replaces
  text = text.replace('(', '( ').replace(")", ' )').replace('^', ' ^ ').replace('v', ' v ').replace('<->', ' <-> ').replace('->', ' -> ').replace('~', ' ~ ')

  return text

def rules_geral(first_char):
  #Verificar se o primeiro caracter é valido
  if first_char in bad_alfa_intial or first_char in bad_chars:
    return False
  return True


def pertence_lang(char):
  if char in lp_lang:
    return True
  return False


def is_bad_chars(char):
  if char in bad_chars:
    return False
  return True

def tokenizador(alfa):
  token = tokens.get(alfa)
  if token:
    return token
  else:
    return 'atomo'

def generate_next_tokens(token, promise_queue):
  if token == 'close_parentheses':
    return rules_cp(promise_queue)
  elif token == 'conector':
    return conectors_next_tokens
  elif token == 'negative':
    return negative_next_tokens
  elif token == 'open_parentheses':
    return  op_next_tokens
  else:
    return rules_atomo(promise_queue)

def validation_propositions(propositions):
  promises = []
  for proposition in propositions:

    proposition = preprocess(proposition)

    proposition =  proposition.split(' ')
    proposition = filter(None, proposition)

    if validation_premisse(proposition):
      promises.append(proposition)
    else:
      print 'Premissa inválida'
      return None

  return promises

def validation_premisse(alfas):
  #Criando duas pilhas, uma para ler os componentes
  read_queue = Queue.LifoQueue()
  promise_queue = Queue.LifoQueue()
  # read_queue = Pilha()
  # promise_queue = Pilha()
  alfas = filter(None, alfas)
  next_tokens = []
  alfas_size = len(alfas)
  count = 1
  for alfa in alfas:
    #Pertence a linguagem e nao pertence a bad_chars
    if pertence_lang(alfa) or is_bad_chars(alfa):

      #Identificando o TOKEN
      token = tokenizador(alfa)
      #Validando Token
      if token in next_tokens or len(next_tokens) == 0:

        read_queue.put(token)

        #Gerenciamento da pilha
        if token == 'close_parentheses':

          if promise_queue.empty():

            return False
          else:
            promise_queue.get()

        if token == 'open_parentheses':
          promise_queue.put('close_parentheses')

        if token == 'conector' and alfas_size == count :
          return False

        next_tokens = generate_next_tokens(token, promise_queue)

      else:
        return False
    else:
      return False
    count += 1

  if promise_queue.empty():
    return True
  return False


def isPredicate(formule):
  str = " ".join(formule)


  if 'v' not in formule and '^' not in formule and '->' not in formule:
    if '~' in formule:
      return True, False
    return True, True
  # else:
  #   str = str.replace('~', '').strip()
  #   print 'STR'
  #   print str
  #   if tokenizador(str) == 'atomo':
  #     return True, False

  return False, None

