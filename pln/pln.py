__author__ = 'rodrigo'

from utils import tokenize, Word

class Pln():
  text = None

  @classmethod
  def toPL(cls, lp):
    dict = {}
    atomics = []
    atomic_name = 'P'
    atomic_num = 1
    results = []
    for text in lp:
      array = []
      words = text.split(' ')
      new_array = []
      for word in words:
        token = tokenize(word)
        array.append(Word(word, token))

      array = removeLigations(array)
      array = positionNegative(array)
      array = groupSuject(array)
      array = switchImpilies(array)
      array = switchDisjuntion(array)
      array = switchConjuntion(array)
      array = switchNegative(array)

      for a in array:
        if a.token == 'subject':
          if a.text not in atomics:
            atomic = atomic_name+str(atomic_num)
            dict[a.text] = atomic
            atomic_num += 1
            atomics.append(a.text)
            new_array.append(Word(atomic, 'subject'))
          else:
            atomic = dict.get(a.text)
            new_array.append(Word(atomic, 'subject'))
        else:
          new_array.append(a)
      results.append(" ".join(a.text for a in new_array))

    size = len(results)
    conclusion = results[size -1]
    results = results[0:size-1]
    return results, conclusion, dict

def removeLigations(array):
  new_array = []
  for a in array:
    if a.token != 'ligation':
      new_array.append(a)
  return new_array

def groupSuject (array):
  old_token = ''
  old_word = ''
  lp = []
  word = Word('', 'subject')
  text = ''
  new_array = []
  size = len(array)
  count = 1
  for a in array:
    if a.token == 'subject':
      if a.token == old_token:
        text += "_"+ a.text
      else:
        text = a.text

      if count == size:
        new_array.append(Word(text, 'subject'))
        text = ''
    else:

      if old_token == 'subject':
        new_array.append(Word(text, 'subject'))
        text = ''
      new_array.append(a)

    old_token = a.token
    count += 1

  return new_array

def switchDisjuntion(array):
  new_array=[]
  for a in array:
    if a.token == 'disjuntion':
      new_array.append(Word('v', 'disjuntion'))
    else:
      new_array.append(a)

  return new_array

def switchConjuntion(array):
  new_array=[]
  for a in array:
    if a.token == 'conjuntion':
      new_array.append(Word('^', 'conjuntion'))
    else:
      new_array.append(a)

  return new_array

def switchNegative(array):
  new_array=[]
  for a in array:
    if a.token == 'negative':
      new_array.append(Word('~', 'negative'))
    else:
      new_array.append(a)

  return new_array


def switchImpilies(array):
  new_array=[]
  for a in array:
    if a.token == 'implies':
      new_array.append(Word('->', 'implies'))
    else:
      new_array.append(a)

  return new_array

def positionNegative(array):
  subjects = []
  new_array = []
  old_token = ''
  count = 1
  for a in array:
    if a.token =='negative':
      if old_token == 'subject':

        new_array.append(a)
        for subject in subjects:
          new_array.append(subject)
        subjects = []

    elif a.token == 'subject':
      subjects.append(a)
      if count == len(array):
        for subject in subjects:
          new_array.append(subject)


    else:

      if len(subjects) > 0:
        for subject in subjects:
          new_array.append(subject)
        subjects = []
      new_array.append(a)


    old_token = a.token
    count += 1

  return new_array


