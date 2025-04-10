# 📊 Predicción de Churn en una Empresa de Telecomunicaciones

Este proyecto tiene como objetivo predecir la probabilidad de que un cliente cancele los servicios de una empresa de telecomunicaciones (churn) usando técnicas avanzadas de Machine Learning. Además, se ha desarrollado una interfaz gráfica interactiva que permite ejecutar automáticamente el pipeline de análisis, visualizar los resultados y gestionar configuraciones.

---
## Acerca del Dataset

Al Ejecutar el proyecto asegurese que esta en el entorno virtual si asi lo configuró, si es el caso, usted solo debe correr interfaz.py

---
## 📂 Acerca del Dataset

Este proyecto utiliza el dataset Telco Customer Churn, creado por IBM para fines educativos y de demostración.
Está disponible públicamente en Kaggle.

Cada fila representa a un cliente de una empresa de telecomunicaciones, incluyendo información demográfica, servicios contratados, datos de facturación y si el cliente canceló el servicio (Churn).
El objetivo es predecir la probabilidad de churn con base en estas variables.

---

## 🎯 Objetivo

Desarrollar un modelo de clasificación binaria capaz de identificar clientes con alta probabilidad de hacer churn (cancelar servicios), con el fin de permitir acciones preventivas de retención.

---

## 🧠 Tecnologías y Librerías Usadas

- Python 3
- Pandas, NumPy
- Matplotlib, Seaborn
- Scikit-learn
- XGBoost, LightGBM
- SHAP (SHapley Additive Explanations)
- Jupyter y JupyterLab

---

## 📁 Estructura del Proyecto

proyecto_churn/

│

├── data/             → Dataset original y limpio

├── notebooks/        → Jupyter Notebooks de análisis, modelado y pruebas

├── src/              → Scripts reutilizables y funciones auxiliares

├── visuals/          → Gráficos generados para análisis y reportes

├── reports/           → Reportes técnicos y presentaciones

├── Informe/          → Informes pdf

├── Code/             → Reportes técnicos y presentaciones

├── Configuracion/    → Configuracion Json

├── Models/           → Modelos Entrenados

├── requirements.txt  → Librerías necesarias para ejecutar el proyecto

├── .gitignore        → Archivos excluidos del control de versiones

└── README.md         → Este documento


## 🚀 ¿Cómo Ejecutar el Proyecto?

- Clona este repositorio:

git clone https://github.com/tuusuario/proyecto_churn.git
cd proyecto_churn

- Crea y activa un entorno virtual:

En Windows:
python -m venv venv
venv\Scripts\activate

En Mac/Linux:
python -m venv venv
source venv/bin/activate

- Instalar las dependencias:

pip install -r requirements.txt

- Abre el notebook notebooks/proyecto_final.ipynb con VS Code o Jupyter.

Asegúrate de seleccionar el kernel del entorno virtual (venv

---

## 📦 Requisitos del Proyecto

Este proyecto utiliza un conjunto reducido de librerías esenciales para asegurar compatibilidad y facilidad de instalación. El archivo `requirements.txt` incluye únicamente las dependencias necesarias para:

- Análisis y visualización de datos
- Modelos de machine learning clásicos y avanzados
- Interpretabilidad de modelos
- Ejecución en notebooks de Jupyter

Si prefieres usar todas las librerías instaladas durante el desarrollo (incluyendo el ecosistema completo de JupyterLab), puedes utilizar el archivo alternativo `requirements_full.txt`.

Para instalar el entorno mínimo:
bash
pip install -r requirements.txt

Para instalar el entorno completo (opcional):
pip install -r requirements_full.txt


## Resultados Esperados

Exploración y limpieza de datos.

Entrenamiento de múltiples modelos de clasificación.

Evaluación mediante métricas como F1-score, precisión, AUC-ROC.

Interpretación del modelo con SHAP.

Recomendaciones estratégicas de retención.

## 👨‍💻 Autor

Erik González Molina
Curso: Transformación Digital a través de la Inteligencia Artificial
Universidad Central – 2025

## 📜 Licencia

Este proyecto es de uso educativo y académico.
No está destinado a uso comercial sin autorización del autor.