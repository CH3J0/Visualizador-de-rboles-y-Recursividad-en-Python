"""
    CLASE PRINCIPAL DEL SISTEMA
"""

class Nodo:
    """Representa un nodo de árbol binario."""

    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None
        self.altura = 1  # Usado por AVL

    def __repr__(self):
        return f"Nodo({self.valor})"
    
"""
    CLASES SECUDNARIAS Y USOS
"""

class ArbolBST:
    """Árbol Binario de Búsqueda. Cada operación usa recursividad."""

    def __init__(self):
        self.raiz = None

    # ------------------------------------------------------------------ #
    #  INSERCIÓN RECURSIVA                                                 #
    # ------------------------------------------------------------------ #

    def insertar(self, valor):
        """Inserta un valor respetando la propiedad BST."""
        camino = []
        self.raiz = self._insertar_rec(self.raiz, valor, camino)
        return camino

    def _insertar_rec(self, nodo, valor, camino):
        if nodo is None:
            return Nodo(valor)
        camino.append(nodo.valor)
        if valor < nodo.valor:
            nodo.izquierdo = self._insertar_rec(nodo.izquierdo, valor, camino)
        elif valor > nodo.valor:
            nodo.derecho = self._insertar_rec(nodo.derecho, valor, camino)
        # Si valor == nodo.valor, no se insertan duplicados
        return nodo

    # ------------------------------------------------------------------ #
    #  BÚSQUEDA RECURSIVA                                                  #
    # ------------------------------------------------------------------ #

    def buscar(self, valor):
        """Busca un valor. Retorna (encontrado, camino_recorrido)."""
        camino = []
        encontrado = self._buscar_rec(self.raiz, valor, camino)
        return encontrado, camino

    def _buscar_rec(self, nodo, valor, camino):
        if nodo is None:
            return False
        camino.append(nodo.valor)
        if valor == nodo.valor:
            return True
        elif valor < nodo.valor:
            return self._buscar_rec(nodo.izquierdo, valor, camino)
        else:
            return self._buscar_rec(nodo.derecho, valor, camino)

    # ------------------------------------------------------------------ #
    #  ELIMINACIÓN RECURSIVA (3 casos)                                    #
    # ------------------------------------------------------------------ #

    def eliminar(self, valor):
        """Elimina un nodo considerando los 3 casos clásicos."""
        encontrado = [False]
        self.raiz = self._eliminar_rec(self.raiz, valor, encontrado)
        return encontrado[0]

    def _eliminar_rec(self, nodo, valor, encontrado):
        if nodo is None:
            return None

        if valor < nodo.valor:
            nodo.izquierdo = self._eliminar_rec(nodo.izquierdo, valor, encontrado)
        elif valor > nodo.valor:
            nodo.derecho = self._eliminar_rec(nodo.derecho, valor, encontrado)
        else:
            encontrado[0] = True
            # Caso 1: Nodo hoja
            if nodo.izquierdo is None and nodo.derecho is None:
                return None
            # Caso 2: Un solo hijo
            if nodo.izquierdo is None:
                return nodo.derecho
            if nodo.derecho is None:
                return nodo.izquierdo
            # Caso 3: Dos hijos → reemplazar con sucesor inorden (mínimo del subárbol derecho)
            sucesor = self._minimo(nodo.derecho)
            nodo.valor = sucesor.valor
            nodo.derecho = self._eliminar_rec(nodo.derecho, sucesor.valor, [True])
        return nodo

    def _minimo(self, nodo):
        while nodo.izquierdo:
            nodo = nodo.izquierdo
        return nodo

    # ------------------------------------------------------------------ #
    #  RECORRIDOS RECURSIVOS                                               #
    # ------------------------------------------------------------------ #

    def preorden(self):
        resultado = []
        self._preorden_rec(self.raiz, resultado)
        return resultado

    def _preorden_rec(self, nodo, resultado):
        if nodo is None:
            return
        resultado.append(nodo.valor)
        self._preorden_rec(nodo.izquierdo, resultado)
        self._preorden_rec(nodo.derecho, resultado)

    def inorden(self):
        resultado = []
        self._inorden_rec(self.raiz, resultado)
        return resultado

    def _inorden_rec(self, nodo, resultado):
        if nodo is None:
            return
        self._inorden_rec(nodo.izquierdo, resultado)
        resultado.append(nodo.valor)
        self._inorden_rec(nodo.derecho, resultado)

    def postorden(self):
        resultado = []
        self._postorden_rec(self.raiz, resultado)
        return resultado

    def _postorden_rec(self, nodo, resultado):
        if nodo is None:
            return
        self._postorden_rec(nodo.izquierdo, resultado)
        self._postorden_rec(nodo.derecho, resultado)
        resultado.append(nodo.valor)

    # ------------------------------------------------------------------ #
    #  INFORMACIÓN GENERAL                                                 #
    # ------------------------------------------------------------------ #

    def altura(self):
        return self._altura_rec(self.raiz)

    def _altura_rec(self, nodo):
        if nodo is None:
            return 0
        return 1 + max(self._altura_rec(nodo.izquierdo),
                       self._altura_rec(nodo.derecho))

    def contar_nodos(self):
        return self._contar_rec(self.raiz)

    def _contar_rec(self, nodo):
        if nodo is None:
            return 0
        return 1 + self._contar_rec(nodo.izquierdo) + self._contar_rec(nodo.derecho)

    def raiz_valor(self):
        return self.raiz.valor if self.raiz else None

    # ------------------------------------------------------------------ #
    #  SERIALIZACIÓN                                                       #
    # ------------------------------------------------------------------ #

    def a_dict(self):
        return {"tipo": "bst", "nodos": self._serializar(self.raiz)}

    def _serializar(self, nodo):
        if nodo is None:
            return None
        return {
            "valor": nodo.valor,
            "izquierdo": self._serializar(nodo.izquierdo),
            "derecho": self._serializar(nodo.derecho)
        }

    def desde_dict(self, datos):
        self.raiz = self._deserializar(datos.get("nodos"))

    def _deserializar(self, datos):
        if datos is None:
            return None
        nodo = Nodo(datos["valor"])
        nodo.izquierdo = self._deserializar(datos.get("izquierdo"))
        nodo.derecho = self._deserializar(datos.get("derecho"))
        return nodo
    

class ArbolBinario:
    """
    Árbol Binario simple.
    La inserción coloca los valores de izquierda a derecha nivel por nivel.
    """

    def __init__(self):
        self.raiz = None

    # ------------------------------------------------------------------ #
    #  INSERCIÓN                                                           #
    # ------------------------------------------------------------------ #

    def insertar(self, valor):
        """Inserta un valor usando BFS para mantener el árbol completo."""
        nuevo = Nodo(valor)
        if self.raiz is None:
            self.raiz = nuevo
            return
        cola = [self.raiz]
        while cola:
            actual = cola.pop(0)
            if actual.izquierdo is None:
                actual.izquierdo = nuevo
                return
            else:
                cola.append(actual.izquierdo)
            if actual.derecho is None:
                actual.derecho = nuevo
                return
            else:
                cola.append(actual.derecho)

    # ------------------------------------------------------------------ #
    #  BÚSQUEDA RECURSIVA                                                  #
    # ------------------------------------------------------------------ #

    def buscar(self, valor):
        """Busca un valor y retorna el camino recorrido."""
        camino = []
        encontrado = self._buscar_rec(self.raiz, valor, camino)
        return encontrado, camino

    def _buscar_rec(self, nodo, valor, camino):
        if nodo is None:
            return False
        camino.append(nodo.valor)
        if nodo.valor == valor:
            return True
        return (self._buscar_rec(nodo.izquierdo, valor, camino) or
                self._buscar_rec(nodo.derecho, valor, camino))

    # ------------------------------------------------------------------ #
    #  ELIMINACIÓN                                                         #
    # ------------------------------------------------------------------ #

    def eliminar(self, valor):
        """
        Elimina un nodo del árbol binario simple.
        Reemplaza con el nodo más profundo/derecho.
        """
        if self.raiz is None:
            return False
        # Caso especial: solo la raíz
        if (self.raiz.izquierdo is None and
                self.raiz.derecho is None):
            if self.raiz.valor == valor:
                self.raiz = None
                return True
            return False

        nodo_objetivo = None
        ultimo_nodo = None
        ultimo_padre = None
        es_hijo_izq = False

        cola = [self.raiz]
        while cola:
            actual = cola.pop(0)
            if actual.valor == valor:
                nodo_objetivo = actual
            if actual.izquierdo:
                ultimo_padre = actual
                es_hijo_izq = True
                ultimo_nodo = actual.izquierdo
                cola.append(actual.izquierdo)
            if actual.derecho:
                ultimo_padre = actual
                es_hijo_izq = False
                ultimo_nodo = actual.derecho
                cola.append(actual.derecho)

        if nodo_objetivo is None:
            return False

        nodo_objetivo.valor = ultimo_nodo.valor
        if es_hijo_izq:
            ultimo_padre.izquierdo = None
        else:
            ultimo_padre.derecho = None
        return True

    # ------------------------------------------------------------------ #
    #  RECORRIDOS RECURSIVOS                                               #
    # ------------------------------------------------------------------ #

    def preorden(self):
        resultado = []
        self._preorden_rec(self.raiz, resultado)
        return resultado

    def _preorden_rec(self, nodo, resultado):
        if nodo is None:
            return
        resultado.append(nodo.valor)
        self._preorden_rec(nodo.izquierdo, resultado)
        self._preorden_rec(nodo.derecho, resultado)

    def inorden(self):
        resultado = []
        self._inorden_rec(self.raiz, resultado)
        return resultado

    def _inorden_rec(self, nodo, resultado):
        if nodo is None:
            return
        self._inorden_rec(nodo.izquierdo, resultado)
        resultado.append(nodo.valor)
        self._inorden_rec(nodo.derecho, resultado)

    def postorden(self):
        resultado = []
        self._postorden_rec(self.raiz, resultado)
        return resultado

    def _postorden_rec(self, nodo, resultado):
        if nodo is None:
            return
        self._postorden_rec(nodo.izquierdo, resultado)
        self._postorden_rec(nodo.derecho, resultado)
        resultado.append(nodo.valor)

    # ------------------------------------------------------------------ #
    #  INFORMACIÓN GENERAL                                                 #
    # ------------------------------------------------------------------ #

    def altura(self):
        return self._altura_rec(self.raiz)

    def _altura_rec(self, nodo):
        if nodo is None:
            return 0
        return 1 + max(self._altura_rec(nodo.izquierdo),
                       self._altura_rec(nodo.derecho))

    def contar_nodos(self):
        return self._contar_rec(self.raiz)

    def _contar_rec(self, nodo):
        if nodo is None:
            return 0
        return 1 + self._contar_rec(nodo.izquierdo) + self._contar_rec(nodo.derecho)

    def raiz_valor(self):
        return self.raiz.valor if self.raiz else None

    # ------------------------------------------------------------------ #
    #  SERIALIZACIÓN                                                       #
    # ------------------------------------------------------------------ #

    def a_dict(self):
        return {"tipo": "binario", "nodos": self._serializar(self.raiz)}

    def _serializar(self, nodo):
        if nodo is None:
            return None
        return {
            "valor": nodo.valor,
            "izquierdo": self._serializar(nodo.izquierdo),
            "derecho": self._serializar(nodo.derecho)
        }

    def desde_dict(self, datos):
        self.raiz = self._deserializar(datos.get("nodos"))

    def _deserializar(self, datos):
        if datos is None:
            return None
        nodo = Nodo(datos["valor"])
        nodo.izquierdo = self._deserializar(datos.get("izquierdo"))
        nodo.derecho = self._deserializar(datos.get("derecho"))
        return nodo


class ArbolAVL:
    """
    Árbol AVL que mantiene el balance automáticamente.
    Factor de balance = altura(izq) - altura(der)
    """

    def __init__(self):
        self.raiz = None
        self.ultimo_camino_insercion = []  # Para visualización

    # ------------------------------------------------------------------ #
    #  ALTURA Y FACTOR DE BALANCE                                          #
    # ------------------------------------------------------------------ #

    def _altura_nodo(self, nodo):
        return nodo.altura if nodo else 0

    def _actualizar_altura(self, nodo):
        nodo.altura = 1 + max(self._altura_nodo(nodo.izquierdo),
                              self._altura_nodo(nodo.derecho))

    def _factor_balance(self, nodo):
        if nodo is None:
            return 0
        return self._altura_nodo(nodo.izquierdo) - self._altura_nodo(nodo.derecho)

    # ------------------------------------------------------------------ #
    #  ROTACIONES                                                          #
    # ------------------------------------------------------------------ #

    def _rotar_derecha(self, y):
        """Rotación simple a la derecha (caso izquierda-izquierda)."""
        x = y.izquierdo
        t2 = x.derecho
        x.derecho = y
        y.izquierdo = t2
        self._actualizar_altura(y)
        self._actualizar_altura(x)
        return x

    def _rotar_izquierda(self, x):
        """Rotación simple a la izquierda (caso derecha-derecha)."""
        y = x.derecho
        t2 = y.izquierdo
        y.izquierdo = x
        x.derecho = t2
        self._actualizar_altura(x)
        self._actualizar_altura(y)
        return y

    def _balancear(self, nodo):
        """Aplica la rotación necesaria según el factor de balance."""
        self._actualizar_altura(nodo)
        fb = self._factor_balance(nodo)

        # Caso Izquierda-Izquierda (rotación simple derecha)
        if fb > 1 and self._factor_balance(nodo.izquierdo) >= 0:
            return self._rotar_derecha(nodo)

        # Caso Izquierda-Derecha (rotación doble: izq-der)
        if fb > 1 and self._factor_balance(nodo.izquierdo) < 0:
            nodo.izquierdo = self._rotar_izquierda(nodo.izquierdo)
            return self._rotar_derecha(nodo)

        # Caso Derecha-Derecha (rotación simple izquierda)
        if fb < -1 and self._factor_balance(nodo.derecho) <= 0:
            return self._rotar_izquierda(nodo)

        # Caso Derecha-Izquierda (rotación doble: der-izq)
        if fb < -1 and self._factor_balance(nodo.derecho) > 0:
            nodo.derecho = self._rotar_derecha(nodo.derecho)
            return self._rotar_izquierda(nodo)

        return nodo

    # ------------------------------------------------------------------ #
    #  INSERCIÓN RECURSIVA                                                 #
    # ------------------------------------------------------------------ #

    def insertar(self, valor):
        camino = []
        self.raiz = self._insertar_rec(self.raiz, valor, camino)
        self.ultimo_camino_insercion = camino
        return camino

    def _insertar_rec(self, nodo, valor, camino):
        if nodo is None:
            return Nodo(valor)
        camino.append(nodo.valor)
        if valor < nodo.valor:
            nodo.izquierdo = self._insertar_rec(nodo.izquierdo, valor, camino)
        elif valor > nodo.valor:
            nodo.derecho = self._insertar_rec(nodo.derecho, valor, camino)
        else:
            return nodo  # No duplicados
        return self._balancear(nodo)

    # ------------------------------------------------------------------ #
    #  BÚSQUEDA RECURSIVA                                                  #
    # ------------------------------------------------------------------ #

    def buscar(self, valor):
        camino = []
        encontrado = self._buscar_rec(self.raiz, valor, camino)
        return encontrado, camino

    def _buscar_rec(self, nodo, valor, camino):
        if nodo is None:
            return False
        camino.append(nodo.valor)
        if valor == nodo.valor:
            return True
        elif valor < nodo.valor:
            return self._buscar_rec(nodo.izquierdo, valor, camino)
        else:
            return self._buscar_rec(nodo.derecho, valor, camino)

    # ------------------------------------------------------------------ #
    #  ELIMINACIÓN RECURSIVA                                               #
    # ------------------------------------------------------------------ #

    def eliminar(self, valor):
        encontrado = [False]
        self.raiz = self._eliminar_rec(self.raiz, valor, encontrado)
        return encontrado[0]

    def _eliminar_rec(self, nodo, valor, encontrado):
        if nodo is None:
            return None
        if valor < nodo.valor:
            nodo.izquierdo = self._eliminar_rec(nodo.izquierdo, valor, encontrado)
        elif valor > nodo.valor:
            nodo.derecho = self._eliminar_rec(nodo.derecho, valor, encontrado)
        else:
            encontrado[0] = True
            # Caso 1: Nodo hoja
            if nodo.izquierdo is None and nodo.derecho is None:
                return None
            # Caso 2: Un solo hijo
            if nodo.izquierdo is None:
                return nodo.derecho
            if nodo.derecho is None:
                return nodo.izquierdo
            # Caso 3: Dos hijos
            sucesor = self._minimo(nodo.derecho)
            nodo.valor = sucesor.valor
            nodo.derecho = self._eliminar_rec(nodo.derecho, sucesor.valor, [True])

        return self._balancear(nodo)

    def _minimo(self, nodo):
        while nodo.izquierdo:
            nodo = nodo.izquierdo
        return nodo

    # ------------------------------------------------------------------ #
    #  RECORRIDOS RECURSIVOS                                               #
    # ------------------------------------------------------------------ #

    def preorden(self):
        resultado = []
        self._preorden_rec(self.raiz, resultado)
        return resultado

    def _preorden_rec(self, nodo, resultado):
        if nodo is None:
            return
        resultado.append(nodo.valor)
        self._preorden_rec(nodo.izquierdo, resultado)
        self._preorden_rec(nodo.derecho, resultado)

    def inorden(self):
        resultado = []
        self._inorden_rec(self.raiz, resultado)
        return resultado

    def _inorden_rec(self, nodo, resultado):
        if nodo is None:
            return
        self._inorden_rec(nodo.izquierdo, resultado)
        resultado.append(nodo.valor)
        self._inorden_rec(nodo.derecho, resultado)

    def postorden(self):
        resultado = []
        self._postorden_rec(self.raiz, resultado)
        return resultado

    def _postorden_rec(self, nodo, resultado):
        if nodo is None:
            return
        self._postorden_rec(nodo.izquierdo, resultado)
        self._postorden_rec(nodo.derecho, resultado)
        resultado.append(nodo.valor)

    # ------------------------------------------------------------------ #
    #  INFORMACIÓN GENERAL                                                 #
    # ------------------------------------------------------------------ #

    def altura(self):
        return self._altura_nodo(self.raiz)

    def contar_nodos(self):
        return self._contar_rec(self.raiz)

    def _contar_rec(self, nodo):
        if nodo is None:
            return 0
        return 1 + self._contar_rec(nodo.izquierdo) + self._contar_rec(nodo.derecho)

    def raiz_valor(self):
        return self.raiz.valor if self.raiz else None

    def obtener_factores_balance(self):
        """Retorna dict {valor: factor_balance} para todos los nodos."""
        factores = {}
        self._factores_rec(self.raiz, factores)
        return factores

    def _factores_rec(self, nodo, factores):
        if nodo is None:
            return
        factores[nodo.valor] = self._factor_balance(nodo)
        self._factores_rec(nodo.izquierdo, factores)
        self._factores_rec(nodo.derecho, factores)

    # ------------------------------------------------------------------ #
    #  SERIALIZACIÓN                                                       #
    # ------------------------------------------------------------------ #

    def a_dict(self):
        return {"tipo": "avl", "nodos": self._serializar(self.raiz)}

    def _serializar(self, nodo):
        if nodo is None:
            return None
        return {
            "valor": nodo.valor,
            "altura": nodo.altura,
            "izquierdo": self._serializar(nodo.izquierdo),
            "derecho": self._serializar(nodo.derecho)
        }

    def desde_dict(self, datos):
        self.raiz = self._deserializar(datos.get("nodos"))

    def _deserializar(self, datos):
        if datos is None:
            return None
        nodo = Nodo(datos["valor"])
        nodo.altura = datos.get("altura", 1)
        nodo.izquierdo = self._deserializar(datos.get("izquierdo"))
        nodo.derecho = self._deserializar(datos.get("derecho"))
        return nodo

