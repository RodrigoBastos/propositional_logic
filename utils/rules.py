__author__ = 'rodrigo'


def rules_atomo(promise_queue):

  if promise_queue.empty():
    return ['conector']
  else:
    return ['conector', 'close_parentheses']

def rules_cp(promise_queue):
  if promise_queue.empty():
    return ['conector']
  else:
    return ['conector',  'close_parentheses']