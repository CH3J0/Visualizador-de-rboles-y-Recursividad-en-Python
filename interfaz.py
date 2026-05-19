import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from Base import ArbolBinario, ArbolBST, ArbolAVL
from gestor_archivos import GestorArchivos


# ────────────────────────────────────────────────────────────────────────────
# Paleta de colores (interfaz)
# ────────────────────────────────────────────────────────────────────────────
FONDO_OSCURO  = "#1E1E2E"
FONDO_PANEL   = "#2A2A3E"
FONDO_WIDGET  = "#313147"
ACENTO        = "#7C6AF7"
ACENTO2       = "#4A90D9"
TEXTO_CLARO   = "#E0E0EE"
TEXTO_APAGADO = "#8888AA"
VERDE         = "#27AE60"
ROJO          = "#E74C3C"
AMARILLO      = "#E8A838"

# ────────────────────────────────────────────────────────────────────────────
# Constantes del canvas visualizador
# ────────────────────────────────────────────────────────────────────────────
COLOR_NODO_NORMAL    = "#4A90D9"
COLOR_NODO_RESALTADO = "#E8A838"
COLOR_NODO_ENCONTRADO = "#27AE60"
COLOR_NODO_ELIMINADO = "#E74C3C"
COLOR_TEXTO          = "white"
COLOR_LINEA          = "#BDC3C7"
COLOR_FONDO          = "#1E1E2E"

RADIO_NODO   = 22
SEPARACION_H = 48
SEPARACION_V = 65


# ════════════════════════════════════════════════════════════════════════════
# VISUALIZADOR 
# ════════════════════════════════════════════════════════════════════════════

class VisualizadorArbol(tk.Canvas):
    """Canvas especializado para dibujar árboles binarios."""

    def __init__(self, master, **kwargs):
        kwargs.setdefault("bg", COLOR_FONDO)
        kwargs.setdefault("highlightthickness", 0)
        super().__init__(master, **kwargs)
        self.nodos_resaltados = set()
        self.nodo_encontrado  = None
        self._items = []

    # ------------------------------------------------------------------ #
    #  API PÚBLICA                                                         #
    # ------------------------------------------------------------------ #

    def dibujar(self, raiz, resaltados=None, encontrado=None):
        """Redibuja el árbol completo."""
        self.nodos_resaltados = set(resaltados) if resaltados else set()
        self.nodo_encontrado  = encontrado
        self._limpiar()
        if raiz is None:
            self._texto_vacio()
            return
        posiciones = {}
        self._calcular_posiciones(raiz, posiciones)
        self._dibujar_lineas(raiz, posiciones)
        self._dibujar_nodos(raiz, posiciones)
        self._ajustar_scroll(posiciones)

    def resaltar_paso_a_paso(self, raiz, camino, encontrado=None, delay_ms=600):
        """Anima el recorrido del camino nodo a nodo."""
        def paso(i):
            if i <= len(camino):
                actuales = camino[:i]
                enc = encontrado if (i == len(camino) and encontrado is not None) else None
                self.dibujar(raiz, resaltados=actuales, encontrado=enc)
                self.after(delay_ms, lambda: paso(i + 1))
        paso(1)

    def animar_recorrido(self, raiz, lista_valores, delay_ms=500):
        """Anima un recorrido resaltando nodo a nodo."""
        def paso(i):
            if i <= len(lista_valores):
                self.dibujar(raiz,
                             resaltados=lista_valores[:i],
                             encontrado=lista_valores[i - 1] if i > 0 else None)
                self.after(delay_ms, lambda: paso(i + 1))
        paso(1)

    # ------------------------------------------------------------------ #
    #  CÁLCULO DE POSICIONES                                               #
    # ------------------------------------------------------------------ #

    def _calcular_posiciones(self, raiz, posiciones):
        nodos_inorden = []
        self._inorden_lista(raiz, nodos_inorden)
        ancho    = max(self.winfo_width(), 800)
        inicio_x = 60
        espaciado = max(SEPARACION_H,
                        (ancho - 120) // max(len(nodos_inorden), 1))
        indices = {id(nodo): i for i, nodo in enumerate(nodos_inorden)}

        def asignar(nodo, nivel):
            if nodo is None:
                return
            x = inicio_x + indices[id(nodo)] * espaciado
            y = 50 + nivel * SEPARACION_V
            posiciones[id(nodo)] = (x, y, nodo)
            asignar(nodo.izquierdo, nivel + 1)
            asignar(nodo.derecho,   nivel + 1)

        asignar(raiz, 0)

    def _inorden_lista(self, nodo, lista):
        if nodo is None:
            return
        self._inorden_lista(nodo.izquierdo, lista)
        lista.append(nodo)
        self._inorden_lista(nodo.derecho, lista)

    # ------------------------------------------------------------------ #
    #  DIBUJO                                                              #
    # ------------------------------------------------------------------ #

    def _dibujar_lineas(self, raiz, posiciones):
        def recorrer(nodo):
            if nodo is None:
                return
            x1, y1, _ = posiciones[id(nodo)]
            for hijo in (nodo.izquierdo, nodo.derecho):
                if hijo:
                    x2, y2, _ = posiciones[id(hijo)]
                    self._items.append(
                        self.create_line(x1, y1, x2, y2,
                                         fill=COLOR_LINEA, width=2))
            recorrer(nodo.izquierdo)
            recorrer(nodo.derecho)
        recorrer(raiz)

    def _dibujar_nodos(self, raiz, posiciones):
        def recorrer(nodo):
            if nodo is None:
                return
            x, y, _ = posiciones[id(nodo)]
            color = self._color_nodo(nodo.valor)
            # Sombra
            self._items.append(
                self.create_oval(x - RADIO_NODO + 3, y - RADIO_NODO + 3,
                                 x + RADIO_NODO + 3, y + RADIO_NODO + 3,
                                 fill="#111122", outline=""))
            # Círculo
            self._items.append(
                self.create_oval(x - RADIO_NODO, y - RADIO_NODO,
                                 x + RADIO_NODO, y + RADIO_NODO,
                                 fill=color, outline="white", width=2))
            # Texto valor
            self._items.append(
                self.create_text(x, y, text=str(nodo.valor),
                                 fill=COLOR_TEXTO,
                                 font=("Consolas", 11, "bold")))
            # Factor de balance para nodos con altura (BST y AVL)
            if hasattr(nodo, "altura"):
                fb = self._factor_balance(nodo)
                self._items.append(
                    self.create_text(x + RADIO_NODO + 12, y - RADIO_NODO,
                                     text=f"fb:{fb:+d}",
                                     fill="#AABBCC",
                                     font=("Consolas", 8)))
            recorrer(nodo.izquierdo)
            recorrer(nodo.derecho)
        recorrer(raiz)

    def _factor_balance(self, nodo):
        def h(n): return n.altura if n else 0
        return h(nodo.izquierdo) - h(nodo.derecho)

    def _color_nodo(self, valor):
        if valor == self.nodo_encontrado:
            return COLOR_NODO_ENCONTRADO
        if valor in self.nodos_resaltados:
            return COLOR_NODO_RESALTADO
        return COLOR_NODO_NORMAL

    def _texto_vacio(self):
        w = self.winfo_width() // 2 or 400
        self._items.append(
            self.create_text(w, 120,
                             text="El árbol está vacío.\nInserta un valor para comenzar.",
                             fill="#555577",
                             font=("Consolas", 13),
                             justify="center"))

    def _limpiar(self):
        for item in self._items:
            self.delete(item)
        self._items.clear()

    def _ajustar_scroll(self, posiciones):
        if not posiciones:
            return
        xs = [v[0] for v in posiciones.values()]
        ys = [v[1] for v in posiciones.values()]
        margen = 60
        self.configure(scrollregion=(
            min(xs) - margen, min(ys) - margen,
            max(xs) + margen, max(ys) + margen
        ))


# ════════════════════════════════════════════════════════════════════════════
# APLICACIÓN PRINCIPAL
# ════════════════════════════════════════════════════════════════════════════

class AplicacionArboles(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🌳 Visualizador de Árboles Binarios")
        self.geometry("1280x750")
        self.configure(bg=FONDO_OSCURO)
        self.resizable(True, True)

        self.gestor    = GestorArchivos()
        self.tipo_arbol = tk.StringVar(value="BST")
        self.arbol     = ArbolBST()

        self._estilos()
        self._construir_ui()
        self._actualizar_info()

    # ------------------------------------------------------------------ #
    #  ESTILOS TTK                                                         #
    # ------------------------------------------------------------------ #

    def _estilos(self):
        s = ttk.Style(self)
        s.theme_use("clam")
        s.configure("TFrame",      background=FONDO_PANEL)
        s.configure("TLabel",      background=FONDO_PANEL, foreground=TEXTO_CLARO,
                    font=("Segoe UI", 10))
        s.configure("Titulo.TLabel", background=FONDO_PANEL, foreground=ACENTO,
                    font=("Segoe UI", 12, "bold"))
        s.configure("Info.TLabel", background=FONDO_PANEL, foreground=TEXTO_APAGADO,
                    font=("Consolas", 9))
        s.configure("TButton",     background=ACENTO, foreground="white",
                    font=("Segoe UI", 9, "bold"), relief="flat", padding=6)
        s.map("TButton",
              background=[("active", ACENTO2), ("disabled", "#555566")])
        s.configure("Peligro.TButton", background=ROJO, foreground="white",
                    font=("Segoe UI", 9, "bold"), padding=6)
        s.map("Peligro.TButton", background=[("active", "#C0392B")])
        s.configure("Verde.TButton", background=VERDE, foreground="white",
                    font=("Segoe UI", 9, "bold"), padding=6)
        s.map("Verde.TButton",   background=[("active", "#1E8449")])
        s.configure("TEntry",    fieldbackground=FONDO_WIDGET, foreground=TEXTO_CLARO,
                    insertcolor=TEXTO_CLARO, font=("Consolas", 11))
        s.configure("TRadiobutton", background=FONDO_PANEL, foreground=TEXTO_CLARO,
                    font=("Segoe UI", 10))

    # ------------------------------------------------------------------ #
    #  CONSTRUCCIÓN DE UI                                                  #
    # ------------------------------------------------------------------ #

    def _construir_ui(self):
        self._barra_superior()
        contenedor = ttk.Frame(self)
        contenedor.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        self._panel_izquierdo(contenedor)
        self._panel_canvas(contenedor)
        self._panel_derecho(contenedor)

    # ---------- BARRA SUPERIOR ----------

    def _barra_superior(self):
        barra = tk.Frame(self, bg=FONDO_PANEL, pady=8)
        barra.pack(fill="x")

        tk.Label(barra, text="🌳  Visualizador de Árboles Binarios",
                 bg=FONDO_PANEL, fg=ACENTO,
                 font=("Segoe UI", 15, "bold")).pack(side="left", padx=16)

        tk.Label(barra, text="Tipo de árbol:", bg=FONDO_PANEL,
                 fg=TEXTO_APAGADO, font=("Segoe UI", 10)).pack(side="left", padx=(20, 4))

        for tipo in ("Binario", "BST", "AVL"):
            tk.Radiobutton(barra, text=tipo, variable=self.tipo_arbol,
                           value=tipo, bg=FONDO_PANEL, fg=TEXTO_CLARO,
                           selectcolor=FONDO_WIDGET, activebackground=FONDO_PANEL,
                           activeforeground=ACENTO,
                           font=("Segoe UI", 10, "bold"),
                           command=self._cambiar_tipo).pack(side="left", padx=4)

        ttk.Button(barra, text="💾 Guardar", command=self._guardar,
                   style="Verde.TButton").pack(side="right", padx=6)
        ttk.Button(barra, text="📂 Cargar",  command=self._cargar
                   ).pack(side="right", padx=6)

    # ---------- PANEL IZQUIERDO ----------

    def _panel_izquierdo(self, parent):
        panel = ttk.Frame(parent, width=230)
        panel.pack(side="left", fill="y", padx=(0, 6), pady=4)
        panel.pack_propagate(False)

        # Inserción
        ttk.Label(panel, text="INSERTAR VALOR",
                  style="Titulo.TLabel").pack(anchor="w", padx=10, pady=(12, 4))
        fi = ttk.Frame(panel)
        fi.pack(fill="x", padx=10)
        self.entry_valor = ttk.Entry(fi, width=10)
        self.entry_valor.pack(side="left")
        self.entry_valor.bind("<Return>", lambda e: self._insertar())
        ttk.Button(fi, text="Insertar", command=self._insertar).pack(side="left", padx=4)

        # Búsqueda
        ttk.Label(panel, text="BUSCAR VALOR",
                  style="Titulo.TLabel").pack(anchor="w", padx=10, pady=(16, 4))
        fb = ttk.Frame(panel)
        fb.pack(fill="x", padx=10)
        self.entry_buscar = ttk.Entry(fb, width=10)
        self.entry_buscar.pack(side="left")
        self.entry_buscar.bind("<Return>", lambda e: self._buscar())
        ttk.Button(fb, text="Buscar", command=self._buscar).pack(side="left", padx=4)

        # Eliminación
        ttk.Label(panel, text="ELIMINAR VALOR",
                  style="Titulo.TLabel").pack(anchor="w", padx=10, pady=(16, 4))
        fe = ttk.Frame(panel)
        fe.pack(fill="x", padx=10)
        self.entry_eliminar = ttk.Entry(fe, width=10)
        self.entry_eliminar.pack(side="left")
        self.entry_eliminar.bind("<Return>", lambda e: self._eliminar())
        ttk.Button(fe, text="Eliminar", style="Peligro.TButton",
                   command=self._eliminar).pack(side="left", padx=4)

        # Recorridos
        ttk.Label(panel, text="RECORRIDOS",
                  style="Titulo.TLabel").pack(anchor="w", padx=10, pady=(16, 4))
        for label, cmd in [("▶ Preorden",  self._preorden),
                           ("▶ Inorden",   self._inorden),
                           ("▶ Postorden", self._postorden)]:
            ttk.Button(panel, text=label, command=cmd).pack(fill="x", padx=10, pady=2)

        # Delay animación
        ttk.Label(panel, text="ANIMACIÓN",
                  style="Titulo.TLabel").pack(anchor="w", padx=10, pady=(16, 4))
        fa = ttk.Frame(panel)
        fa.pack(fill="x", padx=10)
        ttk.Label(fa, text="Delay (ms):").pack(side="left")
        self.spin_delay = tk.Spinbox(fa, from_=100, to=2000, increment=100,
                                     width=6, bg=FONDO_WIDGET, fg=TEXTO_CLARO,
                                     buttonbackground=FONDO_PANEL)
        self.spin_delay.delete(0, "end")
        self.spin_delay.insert(0, "600")
        self.spin_delay.pack(side="left", padx=4)

        # Limpiar
        ttk.Button(panel, text="🗑 Limpiar árbol", style="Peligro.TButton",
                   command=self._limpiar_arbol).pack(fill="x", padx=10, pady=(24, 4))

        # Info del árbol
        ttk.Label(panel, text="INFORMACIÓN",
                  style="Titulo.TLabel").pack(anchor="w", padx=10, pady=(16, 4))
        self.lbl_altura = ttk.Label(panel, text="Altura:  —", style="Info.TLabel")
        self.lbl_altura.pack(anchor="w", padx=14)
        self.lbl_nodos  = ttk.Label(panel, text="Nodos:   —", style="Info.TLabel")
        self.lbl_nodos.pack(anchor="w", padx=14)
        self.lbl_raiz   = ttk.Label(panel, text="Raíz:    —", style="Info.TLabel")
        self.lbl_raiz.pack(anchor="w", padx=14)
        self.lbl_tipo   = ttk.Label(panel, text="Tipo:    BST", style="Info.TLabel")
        self.lbl_tipo.pack(anchor="w", padx=14)

    # ---------- PANEL CANVAS ----------

    def _panel_canvas(self, parent):
        marco = tk.Frame(parent, bg=FONDO_OSCURO, bd=2, relief="flat")
        marco.pack(side="left", fill="both", expand=True)

        self.canvas = VisualizadorArbol(marco, bg="#1A1A2A")
        scroll_y = tk.Scrollbar(marco, orient="vertical",
                                command=self.canvas.yview, bg=FONDO_PANEL)
        scroll_x = tk.Scrollbar(marco, orient="horizontal",
                                command=self.canvas.xview, bg=FONDO_PANEL)
        self.canvas.configure(yscrollcommand=scroll_y.set,
                              xscrollcommand=scroll_x.set)
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", lambda e: self._redibujar())

    # ---------- PANEL DERECHO (LOG) ----------

    def _panel_derecho(self, parent):
        panel = ttk.Frame(parent, width=260)
        panel.pack(side="right", fill="y", padx=(6, 0), pady=4)
        panel.pack_propagate(False)

        ttk.Label(panel, text="REGISTRO DE OPERACIONES",
                  style="Titulo.TLabel").pack(anchor="w", padx=10, pady=(12, 4))

        self.text_log = tk.Text(panel, bg=FONDO_WIDGET, fg=TEXTO_CLARO,
                                font=("Consolas", 9), state="disabled",
                                relief="flat", wrap="word", padx=6, pady=4)
        scroll = tk.Scrollbar(panel, command=self.text_log.yview, bg=FONDO_PANEL)
        self.text_log.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        self.text_log.pack(fill="both", expand=True, padx=(10, 0))

        self.text_log.tag_configure("ok",    foreground="#27AE60")
        self.text_log.tag_configure("error", foreground="#E74C3C")
        self.text_log.tag_configure("info",  foreground="#7C6AF7")
        self.text_log.tag_configure("warn",  foreground="#E8A838")

        ttk.Button(panel, text="Limpiar registro",
                   command=self._limpiar_log).pack(fill="x", padx=10, pady=6)

    # ------------------------------------------------------------------ #
    #  LÓGICA DE OPERACIONES                                               #
    # ------------------------------------------------------------------ #

    def _insertar(self):
        valor = self._leer_entry(self.entry_valor)
        if valor is None:
            return
        if self.tipo_arbol.get() in ("BST", "AVL"):
            camino = self.arbol.insertar(valor)
            self._log(f"Insertar {valor}  →  camino: {camino}", "ok")
            delay = int(self.spin_delay.get())
            self.canvas.resaltar_paso_a_paso(self.arbol.raiz, camino,
                                             encontrado=None, delay_ms=delay)
            self.after(delay * (len(camino) + 2), self._redibujar)
        else:
            self.arbol.insertar(valor)
            self._log(f"Insertar {valor} en árbol binario.", "ok")
            self._redibujar()
        self._actualizar_info()
        self.entry_valor.delete(0, "end")

    def _buscar(self):
        valor = self._leer_entry(self.entry_buscar)
        if valor is None:
            return
        encontrado, camino = self.arbol.buscar(valor)
        if encontrado:
            self._log(f"Buscar {valor}  →  ENCONTRADO  camino: {camino}", "ok")
        else:
            self._log(f"Buscar {valor}  →  NO encontrado  camino: {camino}", "error")
        delay = int(self.spin_delay.get())
        enc = valor if encontrado else None
        self.canvas.resaltar_paso_a_paso(self.arbol.raiz, camino,
                                         encontrado=enc, delay_ms=delay)
        self.after(delay * (len(camino) + 2), self._redibujar)

    def _eliminar(self):
        valor = self._leer_entry(self.entry_eliminar)
        if valor is None:
            return
        ok = self.arbol.eliminar(valor)
        if ok:
            self._log(f"Eliminar {valor}  →  eliminado correctamente.", "warn")
        else:
            self._log(f"Eliminar {valor}  →  valor NO encontrado.", "error")
        self._redibujar()
        self._actualizar_info()
        self.entry_eliminar.delete(0, "end")

    def _preorden(self):
        resultado = self.arbol.preorden()
        self._log(f"Preorden: {resultado}", "info")
        self.canvas.animar_recorrido(self.arbol.raiz, resultado,
                                     delay_ms=int(self.spin_delay.get()))

    def _inorden(self):
        resultado = self.arbol.inorden()
        self._log(f"Inorden: {resultado}", "info")
        self.canvas.animar_recorrido(self.arbol.raiz, resultado,
                                     delay_ms=int(self.spin_delay.get()))

    def _postorden(self):
        resultado = self.arbol.postorden()
        self._log(f"Postorden: {resultado}", "info")
        self.canvas.animar_recorrido(self.arbol.raiz, resultado,
                                     delay_ms=int(self.spin_delay.get()))

    def _limpiar_arbol(self):
        if messagebox.askyesno("Confirmar", "¿Limpiar el árbol completo?"):
            self._cambiar_tipo()
            self._log("Árbol limpiado.", "warn")

    # ------------------------------------------------------------------ #
    #  GUARDAR / CARGAR                                                    #
    # ------------------------------------------------------------------ #

    def _guardar(self):
        nombre = simpledialog.askstring("Guardar árbol",
                                        "Nombre del archivo (sin extensión):",
                                        parent=self)
        if nombre is None:
            return
        try:
            ruta = self.gestor.guardar(self.arbol, nombre)
            self._log(f"Árbol guardado: {ruta}", "ok")
            messagebox.showinfo("Guardado", f"Árbol guardado en:\n{ruta}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _cargar(self):
        archivos = self.gestor.listar_archivos()
        if not archivos:
            messagebox.showinfo("Sin archivos", "No hay árboles guardados.")
            return

        ventana = tk.Toplevel(self)
        ventana.title("Cargar árbol")
        ventana.configure(bg=FONDO_OSCURO)
        ventana.geometry("360x320")

        ttk.Label(ventana, text="Selecciona un archivo:").pack(pady=10)
        lista = tk.Listbox(ventana, bg=FONDO_WIDGET, fg=TEXTO_CLARO,
                           font=("Consolas", 10), selectbackground=ACENTO)
        for arch in archivos:
            lista.insert("end", f"{arch['nombre']}  ({arch['fecha']})")
        lista.pack(fill="both", expand=True, padx=16)

        def confirmar():
            sel = lista.curselection()
            if not sel:
                messagebox.showwarning("Atención", "Selecciona un archivo.",
                                       parent=ventana)
                return
            nombre = archivos[sel[0]]["nombre"]
            try:
                datos = self.gestor.cargar(nombre)
                tipo  = datos.get("tipo", "bst")
                if tipo == "binario":
                    self.tipo_arbol.set("Binario")
                    self.arbol = ArbolBinario()
                elif tipo == "avl":
                    self.tipo_arbol.set("AVL")
                    self.arbol = ArbolAVL()
                else:
                    self.tipo_arbol.set("BST")
                    self.arbol = ArbolBST()
                self.arbol.desde_dict(datos)
                self._redibujar()
                self._actualizar_info()
                self._log(f"Árbol cargado: {nombre}", "ok")
                ventana.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=ventana)

        ttk.Button(ventana, text="Cargar", command=confirmar).pack(pady=8)

    # ------------------------------------------------------------------ #
    #  AUXILIARES                                                          #
    # ------------------------------------------------------------------ #

    def _cambiar_tipo(self):
        tipo = self.tipo_arbol.get()
        if tipo == "Binario":
            self.arbol = ArbolBinario()
        elif tipo == "AVL":
            self.arbol = ArbolAVL()
        else:
            self.arbol = ArbolBST()
        self._redibujar()
        self._actualizar_info()
        self._log(f"Tipo de árbol cambiado a: {tipo}", "info")

    def _redibujar(self):
        self.canvas.dibujar(self.arbol.raiz)

    def _actualizar_info(self):
        self.lbl_altura.config(text=f"Altura:  {self.arbol.altura()}")
        self.lbl_nodos.config( text=f"Nodos:   {self.arbol.contar_nodos()}")
        rv = self.arbol.raiz_valor()
        self.lbl_raiz.config(  text=f"Raíz:    {rv if rv is not None else '—'}")
        self.lbl_tipo.config(  text=f"Tipo:    {self.tipo_arbol.get()}")

    def _leer_entry(self, entry):
        txt = entry.get().strip()
        if not txt:
            messagebox.showwarning("Campo vacío", "Por favor ingresa un valor.")
            return None
        try:
            return int(txt)
        except ValueError:
            messagebox.showerror("Valor inválido", "Solo se permiten números enteros.")
            return None

    def _log(self, mensaje, tag="info"):
        self.text_log.configure(state="normal")
        self.text_log.insert("end", f"• {mensaje}\n", tag)
        self.text_log.see("end")
        self.text_log.configure(state="disabled")

    def _limpiar_log(self):
        self.text_log.configure(state="normal")
        self.text_log.delete("1.0", "end")
        self.text_log.configure(state="disabled")


# ────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = AplicacionArboles()
    app.mainloop()
