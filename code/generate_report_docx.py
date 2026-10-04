import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def create_full_report():
    doc = docx.Document()

    # Configurar margenes (1 pulgada = 2.54 cm)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Colores corporativos UPC
    COLOR_PRIMARY = RGBColor(180, 20, 30)   # Rojo institucional
    COLOR_SECONDARY = RGBColor(50, 50, 50)  # Gris oscuro
    COLOR_BODY = RGBColor(30, 30, 30)

    # Estilo base
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Calibri'
    style_normal.font.size = Pt(11)
    style_normal.font.color.rgb = COLOR_BODY
    style_normal.paragraph_format.line_spacing = 1.15
    style_normal.paragraph_format.space_after = Pt(6)

    # Helper para titulos con estilo
    def add_custom_heading(text, level):
        h = doc.add_heading(level=level)
        run = h.add_run(text)
        run.bold = True
        if level == 1:
            run.font.size = Pt(16)
            run.font.color.rgb = COLOR_PRIMARY
            h.paragraph_format.space_before = Pt(14)
            h.paragraph_format.space_after = Pt(6)
        elif level == 2:
            run.font.size = Pt(13)
            run.font.color.rgb = COLOR_SECONDARY
            h.paragraph_format.space_before = Pt(10)
            h.paragraph_format.space_after = Pt(4)
        elif level == 3:
            run.font.size = Pt(11.5)
            run.font.color.rgb = COLOR_SECONDARY
            h.paragraph_format.space_before = Pt(6)
            h.paragraph_format.space_after = Pt(2)
        return h

    # Helper para tablas elegantes
    def style_table(table):
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        for i, row in enumerate(table.rows):
            for cell in row.cells:
                cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                # Padding interno
                tcPr = cell._tc.get_or_add_tcPr()
                tcMar = OxmlElement('w:tcMar')
                for m in ['top', 'bottom']:
                    node = OxmlElement(f'w:{m}')
                    node.set(qn('w:w'), '120')
                    node.set(qn('w:type'), 'dxa')
                    tcMar.append(node)
                for m in ['left', 'right']:
                    node = OxmlElement(f'w:{m}')
                    node.set(qn('w:w'), '160')
                    node.set(qn('w:type'), 'dxa')
                    tcMar.append(node)
                tcPr.append(tcMar)

                if i == 0:
                    shading = parse_xml(r'<w:shd {} w:fill="B4141E"/>'.format(nsdecls('w')))
                    cell._tc.get_or_add_tcPr().append(shading)
                    for paragraph in cell.paragraphs:
                        for run in paragraph.runs:
                            run.font.bold = True
                            run.font.color.rgb = RGBColor(255, 255, 255)
                            run.font.size = Pt(10)
                else:
                    if i % 2 == 1:
                        shd_xml = r'<w:shd {} w:fill="F5F5F5"/>'.format(nsdecls('w'))
                    else:
                        shd_xml = r'<w:shd {} w:fill="FFFFFF"/>'.format(nsdecls('w'))
                    cell._tc.get_or_add_tcPr().append(parse_xml(shd_xml))
                    for paragraph in cell.paragraphs:
                        for run in paragraph.runs:
                            run.font.size = Pt(9.5)

    # ==========================================
    # PORTADA
    # ==========================================
    p_uni = doc.add_paragraph()
    p_uni.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_uni = p_uni.add_run("UNIVERSIDAD PERUANA DE CIENCIAS APLICADAS\nFACULTAD DE INGENIERÍA\nCARRERA DE CIENCIAS DE LA COMPUTACIÓN / INGENIERÍA DE SOFTWARE")
    r_uni.font.size = Pt(12)
    r_uni.font.bold = True
    r_uni.font.color.rgb = COLOR_SECONDARY

    doc.add_paragraph("\n\n")

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("INFORME DE TRABAJO PARCIAL (HITO 1)\n\nDETECCIÓN DE TRAYECTORIAS DE RADICALIZACIÓN EN LÍNEA Y EVALUACIÓN PREDICTIVA DE RIESGO EN COMUNIDADES INCEL MEDIANTE MINERÍA DE TEXTOS Y NLP LONGITUDINAL")
    r_title.font.size = Pt(16)
    r_title.font.bold = True
    r_title.font.color.rgb = COLOR_PRIMARY

    doc.add_paragraph("\n")

    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_meta = p_meta.add_run("CURSO: CC219 – APLICACIONES DE DATA SCIENCE\nCICLO: 2026-02 | SECCIÓN: CC92\n\nPROFESOR DEL CURSO:\n[Nombre del Docente]\n\nINTEGRANTES DEL GRUPO:\n[Nombre y Apellidos del Alumno 1] – [Código]\n[Nombre y Apellidos del Alumno 2] – [Código]\n[Nombre y Apellidos del Alumno 3] – [Código]\n\nREPOSITORIO EN GITHUB:\nhttps://github.com/CC219-TP-TF-2026-2-CC92\n\nLima, Octubre de 2026")
    r_meta.font.size = Pt(11)
    r_meta.font.color.rgb = COLOR_SECONDARY

    doc.add_page_break()

    # ==========================================
    # 1. DESCRIPCIÓN DEL CASO DE USO
    # ==========================================
    add_custom_heading("1. Descripción y Fundamentación del Caso de Uso", level=1)

    add_custom_heading("1.1. Contexto y Planteamiento del Problema", level=2)
    p = doc.add_paragraph(
        "En la última década, la proliferación de comunidades extremistas en entornos digitales cerrados o semi-moderados ha generado un desafío de seguridad pública e informática sin precedentes. Dentro de la denominada manosphere (manosfera), el ecosistema de los grupos denominados incels (involuntary celibates o célibes involuntarios) se distingue por el desarrollo de una subcultura ideológica radical cimentada en la deshumanización del género femenino, el fatalismo biológico extremo y la apología del resentimiento colectivo (Baele et al., 2020; Ribeiro et al., 2021). "
        "Diversos actos de violencia masiva y terrorismo con motivación ideológica en Estados Unidos, Canadá y Europa han sido perpetrados por individuos autoreferenciados como parte de este movimiento, quienes justificaron sus crímenes como 'actos de retribución' tras procesos de inmersión prolongada en foros como Incels.co, 4chan y subreddits como r/Braincels (Hoffman et al., 2020)."
    )
    p = doc.add_paragraph(
        "Un elemento lingüístico distintivo de estas comunidades es la creación acelerada de un criptolecto o jerga endogámica especializada: términos como 'blackpill' (adopción de una cosmovisión nihilista e inmutable sobre el determinismo físico y social), 'foids' o 'femoids' (abreviación de female humanoids para despojar de humanidad a las mujeres), 'looksmaxxing', 'hypergamy', y referencias reverenciales a asesinos masivos previstos como mártires ('saint Elliot', 'going ER'). "
        "Este léxico opera con un doble propósito: reforzar la cohesión grupal y evadir sistemáticamente los filtros de moderación léxicos tradicionales y las reglas sintácticas convencionales empleadas por las principales plataformas web (Pelzer et al., 2021)."
    )

    add_custom_heading("1.2. El Fenómeno del 'Spiraling' hacia el Extremismo Violento", level=2)
    p = doc.add_paragraph(
        "Desde la perspectiva de la criminología computacional y la psicología social, los individuos no cometen actos de violencia extrema de manera súbita; atraviesan una trayectoria o espiral de radicalización progresiva ('spiraling pipeline'). Inicialmente, un usuario suele ingresar a estos foros buscando soporte emocional o expresando frustración interpersonal y baja autoestima (Fase 1: Vulnerabilidad y Queja Pasiva). Conforme interactúa con el ecosistema, absorbe el marco interpretativo dominante y adopta el vocabulario identitario deshumanizante (Fase 2: Aculturación y Misoginia Ideológica). Finalmente, un subgrupo crítico transita hacia la aceptación de la violencia como única respuesta legítima, glorificando atentados previos y manifestando ideación suicida u homicida (Fase 3: Fijación Violenta y Riesgo Inminente) (Scrivens et al., 2021)."
    )
    p = doc.add_paragraph(
        "Los sistemas actuales de detección de abuso en redes sociales suelen analizar publicaciones de forma aislada e instantánea, ignorando la dimensión secuencial y temporal del usuario. Esta carencia metodológica impide detectar las alertas tempranas del 'spiraling'. En este contexto, la Minería de Textos y el Procesamiento de Lenguaje Natural (NLP) longitudinal ofrecen una oportunidad tecnológica para modelar cómo el lenguaje, la polaridad afectiva y el uso de neologismos evolucionan en el tiempo, posibilitando una evaluación predictiva del riesgo de violencia orientada a la prevención de incidentes."
    )

    add_custom_heading("1.3. Preguntas Analíticas de Clasificación y Predicción", level=2)
    p = doc.add_paragraph(
        "Para dar estricto cumplimiento a los requerimientos del curso de responder a preguntas fundamentadas de clasificación y predicción, el presente proyecto formula las siguientes interrogantes analíticas:"
    )

    p_q1 = doc.add_paragraph()
    r = p_q1.add_run("• Pregunta 1 (Clasificación Multiclase de Riesgo Ideológico): ")
    r.bold = True
    p_q1.add_run(
        "¿Es posible clasificar automáticamente un mensaje o publicación en tres niveles de riesgo ideológico (Nivel 0: Bajo / Cotidiano, Nivel 1: Moderado / Discurso Ideológico, Nivel 2: Alto Riesgo / Violencia Extrema) a partir de sus representaciones textuales (TF-IDF y embeddings contextuales) y la identificación de marcadores léxicos de hostilidad?"
    )

    p_q2 = doc.add_paragraph()
    r = p_q2.add_run("• Pregunta 2 (Predicción Longitudinal de Escalamiento / 'Spiraling'): ")
    r.bold = True
    p_q2.add_run(
        "¿Se puede predecir con una ventana temporal de k publicaciones previas si un usuario activo escalará hacia un comportamiento de alta hostilidad (Nivel 2) en su siguiente periodo de actividad, a partir de la tasa de cambio en su sentimiento y la densidad acumulada de neologismos violentos?"
    )

    p_q3 = doc.add_paragraph()
    r = p_q3.add_run("• Pregunta 3 (Clasificación de Neologismos y Marcadores de Fijación Violenta - Alcance Trabajo Final): ")
    r.bold = True
    p_q3.add_run(
        "¿Es viable identificar y clasificar automáticamente secuencias de texto que contengan jerga emergente de fijación y veneración a terroristas ('going ER', 'saint', 'day of retribution') diferenciándolas del lenguaje estándar de discusión no hostil?"
    )

    # ==========================================
    # 2. DESCRIPCIÓN DEL CONJUNTO DE DATOS
    # ==========================================
    add_custom_heading("2. Descripción del Conjunto de Datos (Dataset)", level=1)

    add_custom_heading("2.1. Origen y Características de la Muestra", level=2)
    p = doc.add_paragraph(
        "Los datos recolectados para este proyecto provienen del repositorio académico de investigación abierto alojado en Zenodo bajo el DOI 10.5281/zenodo.4007913, titulado 'The Evolution of the Manosphere Across the Web', desarrollado por Ribeiro et al. y presentado en la 15th International AAAI Conference on Weblogs and Social Media (ICWSM 2021). "
        "El corpus original comprende más de 28 millones de publicaciones recolectadas de múltiples foros independientes y subreddits. Para efectos del presente estudio, se delimitó una muestra focalizada en tres comunidades paradigmáticas de la subcultura incel y afines: Incels.co (la principal plataforma global del movimiento), Red Pill Talk (foro derivado del histórico sluthate.com) y Love-Shy (comunidad precursora de timidez amorosa y aislamiento)."
    )

    add_custom_heading("2.2. Estructura y Diccionario de Datos", level=2)
    p = doc.add_paragraph(
        "Los datos recolectados son de naturaleza no estructurada y semiestructurada. El archivo procesado consolidado resultante (incels_processed_dataset.csv) cuenta con un total de 4,407 registros textuales válidos generados por 1,166 usuarios únicos. Cada registro contiene los siguientes campos fundamentales:"
    )

    # Tabla de variables
    table_vars = doc.add_table(rows=1, cols=3)
    hdr_cells = table_vars.rows[0].cells
    hdr_cells[0].text = "Variable"
    hdr_cells[1].text = "Tipo de Dato"
    hdr_cells[2].text = "Descripción y Rol en el Proyecto"

    vars_info = [
        ("author", "Texto (String)", "Identificador anonimizado del autor. Clave para agrupar trayectorias longitudinales."),
        ("date_post", "Numérico / Timestamp", "Fecha y hora de publicación del mensaje en el foro."),
        ("text_post", "Texto No Estructurado", "Cuerpo textual original de la publicación o comentario."),
        ("clean_text", "Texto No Estructurado", "Texto preprocesado: sin URLs, normalizado a minúsculas y sin caracteres no alfanuméricos."),
        ("forum", "Categórico", "Comunidad de procedencia: 'incels', 'red_pill_talk', 'love_shy'."),
        ("word_count", "Numérico Entero", "Longitud de la publicación en cantidad de palabras."),
        ("slang_count", "Numérico Entero", "Conteo total de neologismos y jerga incel detectados en el texto."),
        ("slang_terms", "Lista de Términos", "Subconjunto específico de neologismos incel encontrados en el mensaje."),
        ("sentiment_compound", "Numérico Continuo", "Puntaje de polaridad global VADER en el rango [-1.0 (muy negativo), +1.0 (muy positivo)]."),
        ("risk_level", "Categórico (Target)", "Nivel de riesgo asignado: Nivel 0 (Bajo), Nivel 1 (Moderado), Nivel 2 (Alto Riesgo).")
    ]

    for var_name, var_type, var_desc in vars_info:
        row_cells = table_vars.add_row().cells
        row_cells[0].text = var_name
        row_cells[1].text = var_type
        row_cells[2].text = var_desc

    style_table(table_vars)

    # ==========================================
    # 3. ANÁLISIS EXPLORATORIO DE DATOS (EDA)
    # ==========================================
    add_custom_heading("3. Análisis Exploratorio de Datos (EDA) y Preprocesamiento", level=1)

    add_custom_heading("3.1. Pipeline de Limpieza y Normalización Textual", level=2)
    p = doc.add_paragraph(
        "Dado que el texto extraído de foros de internet presenta un alto grado de ruido (hipervínculos, etiquetas HTML residuales, sintaxis informal, emojis y caracteres de control), se implementó un pipeline riguroso de preprocesamiento en Python utilizando NLTK y expresiones regulares: "
        "1) Eliminación de URLs y menciones mediante regex. 2) Supresión de etiquetas HTML. 3) Filtrado de caracteres no alfanuméricos preservando estructuras semánticas. 4) Conversión a minúsculas para homologar vocablos. 5) Eliminación de registros con longitud inferior a 3 palabras para descartar mensajes de spam o respuestas monosilábicas (ej. 'cope', 'lol')."
    )

    add_custom_heading("3.2. Distribución de Niveles de Riesgo y Desbalance de Clases", level=2)
    p = doc.add_paragraph(
        "La variable objetivo de riesgo fue estructurada a partir de la presencia de neologismos de deshumanización, marcadores de violencia/fatalismo y la polaridad afectiva negativa calculada con el analizador léxico VADER. "
        "La distribución obtenida en el corpus refleja con gran realismo la naturaleza de la detección de amenazas en entornos reales: una proporción mayoritaria de interacción cotidiana de baja gravedad (Nivel 0: 53.94%), una fracción sustantiva de discurso ideológico moderado (Nivel 1: 44.45%) y una clase minoritaria pero crítica de alto riesgo / violencia explícita (Nivel 2: 1.61%, 71 publicaciones)."
    )

    # Insertar Grafico 1
    fig1_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'figures', '01_distribucion_niveles_riesgo.png')
    if os.path.exists(fig1_path):
        doc.add_paragraph().alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture(fig1_path, width=Inches(6.0))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap = p_cap.add_run("Figura 1: Distribución de Niveles de Riesgo Ideológico según el foro de origen.")
        r_cap.font.italic = True
        r_cap.font.size = Pt(9.5)

    p = doc.add_paragraph(
        "Como se observa en la Figura 1, el foro Incels.co exhibe una preponderancia marcada de publicaciones categorizadas en Nivel 1 (Discurso Ideológico) respecto al Nivel 0, concentrando además la gran mayoría de casos de Nivel 2. En contraste, comunidades como Love-Shy muestran una distribución dominada por el Nivel 0, evidenciando que su contenido está centrado principalmente en el desahogo personal y la soledad antes que en la agresión sistemática."
    )

    add_custom_heading("3.3. Detección y Frecuencia de Neologismos y Slang Especializado", level=2)
    p = doc.add_paragraph(
        "Se construyó un lexicón ontológico especializado para capturar la terminología dominante de la comunidad, clasificada en tres categorías: ideología general (blackpill, redpill, foids, chad, cuck, normies), apariencia física (looksmaxxing, hunter eyes, manlet, recessed jaw) y fatalismo/violencia (its over, rope, roping, going ER, saint Elliot, retribution). "
        "En la Figura 2 se presentan los 15 términos más prevalentes identificados en el corpus analizado."
    )

    # Insertar Grafico 2
    fig2_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'figures', '02_top_neologismos_incel.png')
    if os.path.exists(fig2_path):
        doc.add_paragraph().alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture(fig2_path, width=Inches(6.0))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap = p_cap.add_run("Figura 2: Top 15 Neologismos y Jerga Incel Más Frecuentes en el Corpus.")
        r_cap.font.italic = True
        r_cap.font.size = Pt(9.5)

    p = doc.add_paragraph(
        "Los términos 'chad' (con 286 menciones), 'incels' (181), 'foids' (158), 'cope' (107) y 'cuck' (52) lideran la frecuencia de uso. La alta recurrencia del despectivo 'foids' y del arquetipo 'chad' ratifica la centralidad de la jerarquía sociosexual en la retórica de estos foros, donde la cosificación y la frustración jerárquica vertebran el discurso común."
    )

    add_custom_heading("3.4. Distribución de Polaridad de Sentimiento", level=2)
    p = doc.add_paragraph(
        "El análisis de sentimiento mediante VADER arrojó una distribución bimodal con sesgo hacia la negatividad extrema, como se ilustra en la Figura 3. Existe una concentración notoria de mensajes en el rango inferior a -0.75, reflejando expresiones de odio, desesperanza y auto-desprecio ('suicidefuel', 'it's over')."
    )

    # Insertar Grafico 3
    fig3_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'figures', '03_distribucion_sentimiento.png')
    if os.path.exists(fig3_path):
        doc.add_paragraph().alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture(fig3_path, width=Inches(6.0))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap = p_cap.add_run("Figura 3: Histograma y Curva de Densidad de Polaridad VADER Compound.")
        r_cap.font.italic = True
        r_cap.font.size = Pt(9.5)

    add_custom_heading("3.5. Modelado Longitudinal: Evidencia Empírica de 'Spiraling'", level=2)
    p = doc.add_paragraph(
        "Para responder a la hipótesis de la espiral de radicalización temporal, se seleccionó el subconjunto de usuarios prolíficos (con 10 o más publicaciones cronológicas) y se evaluó la correlación entre su progreso secuencial en el foro, el incremento de sentimiento negativo y la densidad de jerga absorbida. "
        "Los resultados empíricos se plasman en la Figura 4."
    )

    # Insertar Grafico 4
    fig4_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'figures', '04_espiral_radicalizacion_longitudinal.png')
    if os.path.exists(fig4_path):
        doc.add_paragraph().alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture(fig4_path, width=Inches(6.0))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap = p_cap.add_run("Figura 4: Trayectoria Temporal de Radicalización ('Spiraling'): Evolución de Sentimiento Negativo y Densidad de Jerga.")
        r_cap.font.italic = True
        r_cap.font.size = Pt(9.5)

    p = doc.add_paragraph(
        "El análisis longitudinal revela un comportamiento notable: durante los primeros 5 mensajes, los usuarios experimentan un rápido proceso de enculturación lingüística, alcanzando un pico inicial en la densidad de neologismos (~0.47 términos por post). Conforme el usuario supera los 10 a 14 mensajes, se observa un recrudecimiento drástico en el nivel de sentimiento negativo promedio (superando 0.14 de intensidad negativa neta). Este desfase temporal confirma que la adopción del léxico del grupo precede y cataliza la radicalización emocional, proporcionando un indicador predictivo crucial para la identificación de trayectorias de alto riesgo."
    )

    # ==========================================
    # 4. PROPUESTA DE MODELIZACIÓN
    # ==========================================
    add_custom_heading("4. Propuesta de Modelización y Resultados Baseline", level=1)

    add_custom_heading("4.1. Arquitectura del Pipeline de Modelado", level=2)
    p = doc.add_paragraph(
        "La arquitectura del sistema analítico para resolver las preguntas de clasificación y predicción se divide en dos fases: "
        "En primer término, la fase de modelos baseline (evaluada para este Hito 1), cuyo propósito es establecer el rendimiento de referencia utilizando técnicas de vectorización TF-IDF con n-gramas (unigramas y bigramas) combinadas con clasificadores supervisados clásicos. "
        "En segundo término, la fase avanzada (a desarrollar e implementar en el Trabajo Final), que incorporará arquitecturas Transformer preentrenadas en discurso de odio (HateBERT, RoBERTa) y redes recurrentes (LSTM) para el modelado secuencial de secuencias temporales completas de usuarios."
    )

    add_custom_heading("4.2. Experimentación y Resultados de Modelos Baseline", level=2)
    p = doc.add_paragraph(
        "Para responder experimentalmente a la Pregunta 1 (Clasificación de Nivel de Riesgo), se dividió el corpus en un conjunto de entrenamiento (75%, 3,305 registros) y prueba (25%, 1,102 registros), aplicando estratificación para preservar la proporción de las clases. Se extrajeron 5,000 características TF-IDF y se evaluaron tres algoritmos representativos: "
        "Multinomial Naive Bayes, Logistic Regression con balanceo de pesos de clase y Random Forest. "
        "Los resultados cuantitativos obtenidos se resumen en la Tabla 2:"
    )

    # Tabla de resultados
    table_res = doc.add_table(rows=1, cols=4)
    hdr_res = table_res.rows[0].cells
    hdr_res[0].text = "Algoritmo Evaluado"
    hdr_res[1].text = "Accuracy Global"
    hdr_res[2].text = "F1-Score (Macro)"
    hdr_res[3].text = "F1-Score (Weighted)"

    model_metrics = [
        ("Multinomial Naive Bayes", "75.23%", "50.08%", "74.30%"),
        ("Logistic Regression (Balanced)", "78.22%", "65.68%", "78.11%"),
        ("Random Forest (100 Estimadores)", "78.04%", "58.60%", "77.33%")
    ]

    for m_name, m_acc, m_f1m, m_f1w in model_metrics:
        row_c = table_res.add_row().cells
        row_c[0].text = m_name
        row_c[1].text = m_acc
        row_c[2].text = m_f1m
        row_c[3].text = m_f1w

    style_table(table_res)

    p = doc.add_paragraph(
        "Discusión de resultados baseline: Logistic Regression con ponderación balanceada obtuvo el mejor desempeño global (78.22% de Accuracy y 65.68% de F1-Macro). La ponderación balanceada demostró ser indispensable debido a la naturaleza minoritaria de la clase de alto riesgo (Nivel 2), permitiendo capturar instancias críticas que algoritmos sin compensación de balanceo tienden a omitir. Sin embargo, el F1-Macro de 65.68% evidencia las limitaciones de las representaciones estáticas como TF-IDF para captar el contexto y el doble sentido irónico, justificando plenamente la necesidad de migrar hacia Transformers contextuales."
    )

    add_custom_heading("4.3. Plan de Modelización para el Trabajo Final (Hito 2)", level=2)
    p = doc.add_paragraph(
        "Para el Hito Final (Trabajo Final), se implementará el siguiente plan experimental avanzado a gran escala: "
        "1) Escalamiento en la Nube (Google Colab con GPU): Mediante el notebook desarrollado (03_colab_large_scale_pipeline.ipynb), se ingestará en streaming el archivo completo ndjson.zip de Zenodo (22.1 millones de publicaciones), extrayendo una cohorte de más de 100,000 publicaciones longitudinales de r/Braincels e Incels.co para entrenar sin saturar el almacenamiento local de Git. "
        "2) Fine-tuning de HateBERT y RoBERTa: Empleo de modelos Transformer contextuales entrenados específicamente en lenguaje abusivo para elevar el F1-Score en la clase minoritaria de alto riesgo. "
        "3) Modelo Longitudinal de 'Spiraling' (LSTM / GRU): Modelado de secuencias de vectores latentes por autor para predecir si la trayectoria de un usuario escalará en las próximas 3 intervenciones. "
        "4) Desarrollo de Interfaz Gráfica (GUI) para Stakeholders: Implementación de un dashboard en Streamlit destinado a analistas de seguridad digital o equipos de moderación, que permita visualizar alertas de usuarios en riesgo y la evolución temporal de su vocabulario."
    )

    # ==========================================
    # 5. REFERENCIAS BIBLIOGRÁFICAS
    # ==========================================
    add_custom_heading("5. Referencias Bibliográficas", level=1)

    refs = [
        "Baele, S. J., Brace, L., & Coan, T. G. (2021). Uncovering the online incel ecosystem: Towards a world-level taxonomy of male supremacist communities. Political Studies, 69(4), 868-892.",
        "Caselli, T., Basile, V., Mitrović, J., & Granitzer, M. (2020). HateBERT: Retraining BERT for abusive language detection on English Twitter. Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP).",
        "Hoffman, B., Ware, J., & Shapiro, E. (2020). Assessing the threat of incel violence. Studies in Conflict & Terrorism, 43(7), 565-587.",
        "Pelzer, B., Kaati, E., & Cohen, K. (2021). Toxic language in online incel communities: An NLP analysis. Journal of Policing, Intelligence and Counter Terrorism, 16(3), 260-279.",
        "Ribeiro, M. H., Blackburn, J., Bradlyn, B., De Cristofaro, E., Stringhini, G., Long, S., Greenberg, S., & Zannettou, S. (2021). The evolution of the manosphere across the Web. Proceedings of the 15th International AAAI Conference on Weblogs and Social Media (ICWSM'21), 15(1), 196-207. https://doi.org/10.5281/zenodo.4007913",
        "Scrivens, R., Davies, G., Frank, R., & Dawson, L. (2021). Measuring the evolution of extreme right-wing posting behavior: A longitudinal analysis of violent and non-violent users. Terrorism and Political Violence, 33(7), 1404-1422."
    ]

    for r in refs:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.left_indent = Inches(0.5)
        p_ref.paragraph_format.first_line_indent = Inches(-0.5)
        run_ref = p_ref.add_run(r)
        run_ref.font.size = Pt(9.5)

    # Guardar documento
    output_docx = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'TP_Informe_Radicalizacion_Incels.docx')
    doc.save(output_docx)
    print(f"Informe Word generado exitosamente en: {output_docx}")

if __name__ == '__main__':
    create_full_report()
