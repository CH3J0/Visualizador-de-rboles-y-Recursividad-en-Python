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

    def preorden(self, nodo, resultado=None):
        if resultado is None: resultado = []
        if nodo:
            resultado.append(nodo.valor)
            self.preorden(nodo.izquierdo, resultado)
            self.preorden(nodo.derecho, resultado)
        return resultado

    def inorden(self, nodo, resultado=None):
        if resultado is None: resultado = []
        if nodo:
            self.inorden(nodo.izquierdo, resultado)
            resultado.append(nodo.valor)
            self.inorden(nodo.derecho, resultado)
        return resultado

    def postorden(self, nodo, resultado=None):
        if resultado is None: resultado = []
        if nodo:
            self.postorden(nodo.izquierdo, resultado)
            self.postorden(nodo.derecho, resultado)
            resultado.append(nodo.valor)
        return resultado
