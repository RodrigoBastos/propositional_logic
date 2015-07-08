__author__ = 'rodrigo'




class Temp():




  @classmethod
  def generateTemp(cls, propositions):
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