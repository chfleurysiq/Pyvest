from django.shortcuts import render, redirect
from carrinho.models import Investimento
from plot_chart.views import products

# criar um botão para cada investimento com o código e o nome de cada um
# usar a API pra pegar o dado do dia daquele investimento
context = {}
context['acoes'] = []
class Node_Investimentos:
    #construtor
    def __init__(self, symbol, name, price, idAcao):
        # guarda os dados
        self.symbol = symbol
        self.name = name
        self.price = price
        self.idAcao = idAcao
        # guarda a referência (next item)
        self.next = None

class Linked_List_Investimentos:
    #construtor
    def __init__(self):
        self.head = None
        self.tail = None

    def output_list(self):
        current_node = self.head
        
        while current_node is not None:
            print(current_node.symbol)
            
            # jump to the linked node
            current_node = current_node.next
            
        return current_node
    
    def append(self, symbol, name, price, idAcao):
        if self.head:
            pointer = self.head
            while(pointer.next):
                pointer = pointer.next
            pointer.next = Node_Investimentos(symbol, name, price, idAcao)
        else:
            self.head = Node_Investimentos(symbol, name, price, idAcao)
    
    def pop_search(self, name):
        pointer = self.head
        while(pointer.name != name):
            q = pointer
            pointer = pointer.next
        q.next = pointer.next
        pointer.next = None
        
        # 1 2 3
        # |---|

    def load_context(self):
        pointer = self.head
        while(pointer):
            context['acoes'].append({
                    'name' : pointer.name, 
                    'symbol': pointer.symbol,
                    'price': pointer.price,
                    'id': pointer.idAcao
                    })
            pointer = pointer.next

    def __repr__(self):
        r = ""
        pointer = self.head
        while(pointer):
            r = r + str(pointer.name) + "----" + str(pointer.idAcao) + "->"
            pointer = pointer.next
        r = r + "None"
        return r
     
    def __str__(self):
        return self.__repr__()
            

def meus_investimentos(request):
  
    context['acoes'] = []
    lista_investimentos = Linked_List_Investimentos()

    userId = 0
    if request.user.is_authenticated:
        userId = request.user.id
    else:
        print('redicisadmsaks')
        return redirect('/entrar') 
              
    investimentos = Investimento.objects.all().filter(userId= userId)

    for i in investimentos:
        lista_investimentos.append(i.symbol, i.name, i.price, i.id)

    lista_investimentos.load_context()
    
    #print(lista_investimentos)
    
    """ return products(request, "GGBR3") """
    if request.method == 'POST':
        """ lista_investimentos.load_context() """

        x = request.POST.get('symbol')
        y = request.POST.get('id')
        n = request.POST.get('name')
        if x != None:
          print(x)
          return products(request, x, n)
        else:
            investimentos = Investimento.objects.all().filter(id= y).delete()
        
            context['acoes'] = []
            lista_investimentos = Linked_List_Investimentos()
                    
            investimentos = Investimento.objects.all().filter(userId= userId)

            for i in investimentos:
                lista_investimentos.append(i.symbol, i.name, i.price, i.id)

            lista_investimentos.load_context()

            return render(request, 'investimentos_do_usuario.html', context)
    else:
      
            
        return render(request, 'investimentos_do_usuario.html', context)
  
 