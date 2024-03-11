class Restaurante:
    restaurantes = []

#__str__ = ele e um metoto especial que pega um objeto em formato de texto e mostra esta informação, a gente pode escolher o nome categoria o ativo podemos pode escolher e definir.
#__init__ = um método construtor sempre onde que criarmos uma instância de um objeto esse método é chamado
    
    def __init__(self, nome, categoria):#Para nao confundir sempre passamos como primeiro parametro "self" para entender que se trata do objeto que nos referenciamos naquele momento
        self.nome = nome
        self.categoria = categoria 
        self.ativo= False
        Restaurante.restaurantes.append(self)

    def __str__(self):
        return f'{self.nome} | {self.categoria}'
    
    def listar_restaurantes():
        for restaurante in Restaurante.restaurantes:
            print(f'{restaurante.nome} | {restaurante.categoria} | {restaurante.ativo}')

        

#Podemos criar uma variável e armazenar em classe.
restaurante_cao_novo = Restaurante('Cão Novo', 'Hamburgueria')
restaurante_cantina = Restaurante('Cantina', 'Buffet')


Restaurante.listar_restaurantes()

#vars função onde acessamos o dicionário dos atributos e metodos
#print(restaurante_cantina)#função dir trás para nós os atributos guardados dentro do objeto.
#print(restaurante_cao_novo)
