import json
import os
from datetime import datetime


class GestorArchivos:
    """Maneja la persistencia de árboles en archivos JSON."""

    DIRECTORIO = "arboles_guardados"

    def __init__(self):
        os.makedirs(self.DIRECTORIO, exist_ok=True)

    # ------------------------------------------------------------------ #
    #  GUARDAR                                                             #
    # ------------------------------------------------------------------ #

    def guardar(self, arbol, nombre: str) -> str:
        """Guarda el árbol en un archivo JSON. Retorna la ruta del archivo."""
        if not nombre.strip():
            nombre = f"arbol_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        nombre = nombre.strip().replace(" ", "_")
        if not nombre.endswith(".json"):
            nombre += ".json"

        datos = arbol.a_dict()
        datos["fecha_guardado"] = datetime.now().isoformat()

        ruta = os.path.join(self.DIRECTORIO, nombre)
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
        return ruta

    # ------------------------------------------------------------------ #
    #  CARGAR                                                              #
    # ------------------------------------------------------------------ #

    def cargar(self, nombre: str):
        """
        Carga un árbol desde archivo JSON.
        Retorna (tipo_str, datos_dict) o lanza FileNotFoundError.
        """
        if not nombre.endswith(".json"):
            nombre += ".json"
        ruta = os.path.join(self.DIRECTORIO, nombre)
        if not os.path.exists(ruta):
            raise FileNotFoundError(f"No se encontró el archivo: {ruta}")
        with open(ruta, "r", encoding="utf-8") as f:
            datos = json.load(f)
        return datos

    # ------------------------------------------------------------------ #
    #  LISTAR ARCHIVOS                                                     #
    # ------------------------------------------------------------------ #

    def listar_archivos(self):
        """Retorna lista de archivos .json guardados."""
        archivos = []
        for nombre in os.listdir(self.DIRECTORIO):
            if nombre.endswith(".json"):
                ruta = os.path.join(self.DIRECTORIO, nombre)
                size = os.path.getsize(ruta)
                mtime = os.path.getmtime(ruta)
                fecha = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")
                archivos.append({
                    "nombre": nombre,
                    "tamano": size,
                    "fecha": fecha
                })
        return archivos

    # ------------------------------------------------------------------ #
    #  ELIMINAR ARCHIVO                                                    #
    # ------------------------------------------------------------------ #

    def eliminar_archivo(self, nombre: str) -> bool:
        if not nombre.endswith(".json"):
            nombre += ".json"
        ruta = os.path.join(self.DIRECTORIO, nombre)
        if os.path.exists(ruta):
            os.remove(ruta)
            return True
        return False
