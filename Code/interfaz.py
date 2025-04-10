import PySimpleGUI as sg
import os
import subprocess
import json
import shutil
from PIL import Image
from io import BytesIO
import kagglehub
import pandas as pd

# ────────────────────────────────
# 📁 Constantes de rutas y archivos
# ────────────────────────────────
NOTEBOOK_PATH = "Notebooks/proyecto_final.ipynb"
CARPETAS_VISUALIZACION = [
    "Visuals/exploracion_inicial",
    "Visuals/preprocesamiento_y_modelado",
    "Visuals/models_ajustados",
    "Visuals/shap"
]
CONFIG_FOLDER = "Configuracion"
LOGO_PATH = "Assets/logo.png"
REPORTS_FOLDER = "Reports"

# ────────────────────────────────
# 🔧 Cargar archivo de configuración
# ────────────────────────────────
def obtener_archivo_config():
    for file in os.listdir(CONFIG_FOLDER):
        if file.endswith(".json"):
            return os.path.join(CONFIG_FOLDER, file)
    return None

CONFIG_PATH = obtener_archivo_config()

# ────────────────────────────────
# 🚀 Ejecutar Notebook
# ────────────────────────────────
def ejecutar_notebook():
    try:
        subprocess.run([
            "jupyter", "nbconvert",
            "--to", "notebook",
            "--execute",
            "--inplace",
            NOTEBOOK_PATH
        ], check=True)
        sg.popup("✅ ¡El notebook ha sido ejecutado correctamente!")
    except subprocess.CalledProcessError as e:
        sg.popup_error(f"❌ Error al ejecutar el notebook:\n{e}")

# ────────────────────────────────
# 🖼️ Mostrar imagen de la carpeta
# ────────────────────────────────
def mostrar_imagen(carpeta, nombre_imagen):
    ruta = os.path.join(carpeta, nombre_imagen)
    if os.path.exists(ruta):
        with Image.open(ruta) as img:
            img.thumbnail((600, 600))
            bio = BytesIO()
            img.save(bio, format="PNG")
        return bio.getvalue()
    else:
        sg.popup_error("❌ No se encontró la imagen.")
        return None

# ────────────────────────────────
# 📁 Cargar nombres de imágenes
# ────────────────────────────────
def cargar_nombres_imagenes(carpeta):
    if not os.path.exists(carpeta):
        return []
    return [f for f in os.listdir(carpeta) if f.lower().endswith((".png", ".jpg", ".jpeg"))]

# ────────────────────────────────
# 📄 Cargar nombres de reportes
# ────────────────────────────────
def cargar_nombres_reportes():
    if not os.path.exists(REPORTS_FOLDER):
        return []
    return [f for f in os.listdir(REPORTS_FOLDER) if f.lower().endswith(".csv")]

# ────────────────────────────────
# ⚙️ Panel para modificar configuración
# ────────────────────────────────
def abrir_panel_configuracion():
    if not CONFIG_PATH:
        sg.popup_error("No se encontró archivo de configuración en 'Configuracion'")
        return

    with open(CONFIG_PATH, "r") as f:
        config_data = json.load(f)

    layout = [
        [sg.Text("Modificar Variable Objetivo y Dataset")],
        [sg.Text("Variable Objetivo:"), sg.InputText(config_data.get("target_variable", ""), key="-TARGET-")],
        [sg.Text("Seleccionar nuevo dataset (CSV):"), sg.Input(key="-DATA_PATH-"), sg.FileBrowse(initial_folder="Data", file_types=(("CSV Files", "*.csv"),))],
        [sg.Button("💾 Guardar Configuración"), sg.Button("❌ Cancelar")]
    ]

    ventana_config = sg.Window("Configuración", layout)

    while True:
        evento, valores = ventana_config.read()
        if evento in (sg.WINDOW_CLOSED, "❌ Cancelar"):
            break
        elif evento == "💾 Guardar Configuración":
            config_data["target_variable"] = valores["-TARGET-"]
            if valores["-DATA_PATH-"]:
                config_data["data_path"] = os.path.relpath(valores["-DATA_PATH-"], start="Code")
            with open(CONFIG_PATH, "w") as f:
                json.dump(config_data, f, indent=4)
            sg.popup("✅ Configuración actualizada")
            break
    ventana_config.close()

# ────────────────────────────────
# ⬇️ Descargar dataset desde Kaggle
# ────────────────────────────────
def descargar_dataset():
    path = kagglehub.dataset_download("blastchar/telco-customer-churn")
    downloaded_files = os.listdir(path)
    csv_file = next((f for f in downloaded_files if f.endswith(".csv")), None)
    if csv_file:
        destino = os.path.join("Data", "telco_customer_churn.csv")
        shutil.copy(os.path.join(path, csv_file), destino)
        if CONFIG_PATH:
            with open(CONFIG_PATH, "r") as f:
                config = json.load(f)
            config["data_path"] = os.path.relpath(destino, start="Code")
            with open(CONFIG_PATH, "w") as f:
                json.dump(config, f, indent=4)
        sg.popup("✅ Dataset descargado y configuración actualizada")
    else:
        sg.popup_error("❌ No se encontró el archivo .csv en el dataset descargado")

# ────────────────────────────────
# 🖼️ Redimensionar el logo
# ────────────────────────────────
def cargar_logo_redimensionado(tamaño=(100, 100)):
    with Image.open(LOGO_PATH) as img:
        img.thumbnail(tamaño)
        bio = BytesIO()
        img.save(bio, format="PNG")
    return bio.getvalue()

# ────────────────────────────────
# 📄 Visualizar reporte con paginado
# ────────────────────────────────
def mostrar_reporte_paginado(nombre_reporte, filas_por_pagina=20):
    ruta = os.path.join(REPORTS_FOLDER, nombre_reporte)
    if not os.path.exists(ruta):
        sg.popup_error("❌ No se encontró el reporte.")
        return

    df = pd.read_csv(ruta)
    total_filas = len(df)
    total_paginas = (total_filas + filas_por_pagina - 1) // filas_por_pagina
    pagina_actual = 0

    def construir_tabla(pagina):
        inicio = pagina * filas_por_pagina
        fin = inicio + filas_por_pagina
        datos = df.iloc[inicio:fin].values.tolist()
        return datos

    layout_tabla = [
        [sg.Text(f"📄 Reporte: {nombre_reporte}", font=("Helvetica", 14))],
        [sg.Table(values=construir_tabla(pagina_actual), headings=list(df.columns),
                  key='-TABLA-', num_rows=filas_por_pagina,
                  auto_size_columns=True, justification='left', enable_events=False)],
        [
            sg.Button("⏮️ Anterior"),
            sg.Text(f"Página {pagina_actual+1} de {total_paginas}", key='-PAGINA-'),
            sg.Button("⏭️ Siguiente"),
            sg.Button("❌ Cerrar")
        ]
    ]

    window_tabla = sg.Window(f"📄 Reporte: {nombre_reporte}", layout_tabla, modal=True)

    while True:
        event, _ = window_tabla.read()
        if event in (sg.WINDOW_CLOSED, "❌ Cerrar"):
            break
        elif event == "⏭️ Siguiente" and pagina_actual < total_paginas - 1:
            pagina_actual += 1
        elif event == "⏮️ Anterior" and pagina_actual > 0:
            pagina_actual -= 1

        window_tabla["-TABLA-"].update(values=construir_tabla(pagina_actual))
        window_tabla["-PAGINA-"].update(f"Página {pagina_actual+1} de {total_paginas}")

    window_tabla.close()

# ────────────────────────────────
# 🧠 Interfaz Gráfica Principal
# ────────────────────────────────
sg.theme("DarkBlue3")

layout = [
    [sg.Text("🧠 Herramienta de Análisis de Datos", font=("Helvetica", 16), justification="center", expand_x=True)],
    [
        sg.Button(image_data=cargar_logo_redimensionado(), key="📊 Analizar Notebook", border_width=0, tooltip="Ejecutar análisis del notebook"),
        sg.Text("Presionar logo para Correr Notebook", font=("Helvetica", 11))
    ],
    [sg.Button("⚙️ Configuración"), sg.Button("🔍 Buscar Dataset Automáticamente")],
    [sg.Text("Seleccionar carpeta:"), sg.Combo(values=CARPETAS_VISUALIZACION, default_value=CARPETAS_VISUALIZACION[0], key="-CARPETA-"), sg.Button("🔄 Refrescar Imágenes")],
    [sg.Text("Seleccionar imagen:"), sg.Combo(values=[], key="-IMAGEN-"), sg.Button("📷 Mostrar Imagen")],
    [sg.Text("Seleccionar reporte (.csv):"), sg.Combo(values=cargar_nombres_reportes(), key="-REPORTE-"), sg.Button("📄 Ver Reporte"), sg.Button("🔁 Refrescar Reportes")],
    [sg.Image(key="-IMG-", size=(600, 600))],
    [sg.Button("❌ Salir")]
]

window = sg.Window("Analizador de Datos Telco", layout, finalize=True, location=(None, None), element_justification='center')

# Inicializar lista de imágenes
carpeta_actual = window["-CARPETA-"].get()
window["-IMAGEN-"].update(values=cargar_nombres_imagenes(carpeta_actual))

# ────────────────────────────────
# 🌀 Loop principal de eventos
# ────────────────────────────────
while True:
    event, values = window.read()
    if event in (sg.WINDOW_CLOSED, "❌ Salir"):
        break
    elif event == "📊 Analizar Notebook":
        ejecutar_notebook()
    elif event == "📷 Mostrar Imagen":
        imagen = values["-IMAGEN-"]
        carpeta = values["-CARPETA-"]
        if imagen and carpeta:
            data = mostrar_imagen(carpeta, imagen)
            if data:
                window["-IMG-"].update(data=data)
    elif event == "🔄 Refrescar Imágenes":
        carpeta_actual = values["-CARPETA-"]
        window["-IMAGEN-"].update(values=cargar_nombres_imagenes(carpeta_actual))
    elif event == "🔁 Refrescar Reportes":
        window["-REPORTE-"].update(values=cargar_nombres_reportes())
    elif event == "⚙️ Configuración":
        abrir_panel_configuracion()
    elif event == "🔍 Buscar Dataset Automáticamente":
        descargar_dataset()
    elif event == "📄 Ver Reporte":
        nombre_reporte = values["-REPORTE-"]
        if nombre_reporte:
            mostrar_reporte_paginado(nombre_reporte)

window.close()
