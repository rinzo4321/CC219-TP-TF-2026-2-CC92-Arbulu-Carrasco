# Detección de Trayectorias de Radicalización en Línea y Evaluación Predictiva de Riesgo en Comunidades Incel

**Curso:** CC219 - Aplicaciones de Data Science (2026-02)  
**Sección:** CC92  
**Repositorio:** `CC219-TP-TF-2026-2-CC92`

---

## 1. Objetivo del Trabajo
El objetivo general de este proyecto es diseñar, implementar y evaluar un pipeline de Ciencia de Datos basado en Minería de Textos y Procesamiento de Lenguaje Natural (NLP longitudinal) para analizar la propagación del discurso de odio, cuantificar la presencia de neologismos y jerga propia de la subcultura incel, y predecir trayectorias de radicalización extrema (*"spiraling"*) orientadas a la evaluación temprana de riesgos de violencia dirigida.

### Preguntas Analíticas de Clasificación y Predicción:
1. **Pregunta 1 (Clasificación de Nivel de Riesgo Ideológico):** ¿Es posible clasificar publicaciones en tres niveles de riesgo (Nivel 0: Bajo/Cotidiano, Nivel 1: Moderado/Ideológico, Nivel 2: Alto Riesgo/Violencia Extrema) mediante representaciones textuales y análisis léxico-semántico?
2. **Pregunta 2 (Predicción Longitudinal de Escalamiento / "Spiraling"):** ¿Se puede predecir mediante el historial temporal de mensajes de un usuario si este escalará hacia un discurso de alta toxicidad o violencia en sus siguientes intervenciones?
3. **Pregunta 3 (Identificación y Clasificación de Neologismos y Marcadores de Fijación):** ¿Es posible identificar y aislar automáticamente los términos criptolécticos (*blackpill, looksmaxxing, foid, going ER*) frente al vocabulario estándar?

---

## 2. Alumnos Participantes
* Integrante 1: Carrasco Betancourt, Chris - U202314934 
* Integrante 2: Arbulú Dávila, Renzo Fabián - U202323115

---

## 3. Estructura del Repositorio
```text
CC219-TP-TF-2026-2-CC92/
├── data/
│   ├── samples/                     # Muestra original de hilos y foros
│   ├── samples.zip                  # Archivo comprimido del corpus base
│   └── incels_processed_dataset.csv # Dataset final limpio y normalizado con variables analíticas
├── code/
│   ├── 01_eda_preprocessing.py      # Pipeline de carga, limpieza, EDA y generación de gráficos
│   ├── 02_model_baseline_proposal.py# Evaluación empírica de baselines para propuesta de modelización
│   ├── 03_colab_large_scale_pipeline.ipynb # Pipeline escalable para Google Colab (100k+ posts con GPU)
│   └── generate_report_docx.py      # Generador automatizado del informe oficial en .docx
├── figures/                         # Gráficos generados para el informe
│   ├── 01_distribucion_niveles_riesgo.png
│   ├── 02_top_neologismos_incel.png
│   ├── 03_distribucion_sentimiento.png
│   ├── 04_espiral_radicalizacion_longitudinal.png
│   └── baseline_results.json
└── README.md
```

---

## 4. Descripción del Dataset
* **Origen:** Corpus académico derivado de la investigación *"The Evolution of the Manosphere Across the Web"* (Ribeiro et al., ICWSM 2021, AAAI), alojado formalmente en Zenodo (DOI: [10.5281/zenodo.4007913](https://doi.org/10.5281/zenodo.4007913)).
* **Volumen:** 4,407 publicaciones válidas analizadas tras filtrado de calidad y normalización, provenientes de 1,166 usuarios únicos en comunidades representativas (*incels.co*, *love-shy*, *red_pill_talk*).
* **Campos clave:** `author`, `date_post`, `text_post`, `thread`, `forum`, `clean_text`, `sentiment_compound`, `slang_count`, `risk_level`.

---

## 5. Conclusiones Preliminares (Hito 1 - Trabajo Parcial)
1. **Endogamia y Neologismos:** El análisis exploratorio revela una fuerte presencia de términos especializados propios de la comunidad (*chad, foids, cope, blackpill, looksmaxxing*), los cuales concentran la carga semántica de deshumanización y suelen eludir filtros de moderación convencionales.
2. **Trayectoria Longitudinal ("Spiraling"):** El seguimiento secuencial de usuarios activos (con más de 10 mensajes) evidencia un patrón dinámico de radicalización donde la adopción de jerga ideológica precede a picos de sentimiento altamente negativo y lenguaje fatalista.
3. **Viabilidad de Modelado:** Los experimentos baseline arrojaron un rendimiento sólido con **Logistic Regression Balanceada (78.22% Accuracy, 78.11% F1-Weighted)** y **Random Forest (78.04% Accuracy)** utilizando representaciones TF-IDF, estableciendo una base rigurosa para la incorporación de modelos Transformers preentrenados (HateBERT) en el Trabajo Final.

---

## 6. Licencia
Este proyecto se distribuye bajo la licencia **MIT License** para el código fuente desarrollado y **Creative Commons Attribution 4.0 International (CC-BY-4.0)** para los datos derivados con fines estrictamente académicos y de investigación.
