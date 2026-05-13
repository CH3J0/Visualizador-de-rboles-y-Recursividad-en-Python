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

    """ Recorridos """
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
    
""" Árbol Binario de Búsqueda (BST) """
class BST(ArbolBinario):
    def insertar(self, valor):
        self.raiz = self._insertar_recursivo(self.raiz, valor)

    """ Recursivos """
    def _insertar_recursivo(self, nodo, valor):
        if nodo is None:
            return Nodo(valor)
        if valor < nodo.valor:
            nodo.izquierdo = self._insertar_recursivo(nodo.izquierdo, valor)
        elif valor > nodo.valor:
            nodo.derecho = self._insertar_recursivo(nodo.derecho, valor)
        return nodo

    def buscar(self, nodo, valor):
        if nodo is None or nodo.valor == valor:
            return nodo
        if valor < nodo.valor:
            return self.buscar(nodo.izquierdo, valor)
        return self.buscar(nodo.derecho, valor)

    def eliminar(self, valor):
        self.raiz = self._eliminar_recursivo(self.raiz, valor)

    def _eliminar_recursivo(self, nodo, valor):
        if nodo is None: return nodo

        if valor < nodo.valor:
            nodo.izquierdo = self._eliminar_recursivo(nodo.izquierdo, valor)
        elif valor > nodo.valor:
            nodo.derecho = self._eliminar_recursivo(nodo.derecho, valor)
        else:
            # Caso 1 y 2: Nodo con un hijo o sin hijos
            if nodo.izquierdo is None: return nodo.derecho
            elif nodo.derecho is None: return nodo.izquierdo
            
            # Caso 3: Nodo con dos hijos
            temp = self._min_valor_nodo(nodo.derecho)
            nodo.valor = temp.valor
            nodo.derecho = self._eliminar_recursivo(nodo.derecho, temp.valor)
        return nodo

    def _min_valor_nodo(self, nodo):
        actual = nodo
        while actual.izquierdo is not None:
            actual = actual.izquierdo
        return actual
