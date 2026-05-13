""" Clase Principal """
class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None
        self.altura = 1  # Fundamental para el balanceo del AVL

""" Clase Arbol Binario """
class ArbolBinario:
    def __init__(self):
        self.raiz = None
