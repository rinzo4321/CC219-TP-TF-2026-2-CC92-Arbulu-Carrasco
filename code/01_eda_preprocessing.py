import os
import glob
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Descargar recursos de NLTK necesarios
nltk.download('vader_lexicon', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)

# 1. Definicion de rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
SAMPLES_DIR = os.path.join(DATA_DIR, 'samples')
OUTPUT_DIR = os.path.join(BASE_DIR, 'figures')
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("Directorio base:", BASE_DIR)
print("Directorio de datos:", DATA_DIR)

# 2. Carga robusta de archivos CSV
def load_forum_data(forum_name, max_files=100):
    folder = os.path.join(SAMPLES_DIR, forum_name)
    csv_files = glob.glob(os.path.join(folder, '*.csv'))[:max_files]
    records = []
    
    for f in csv_files:
        try:
            # Lectura con engine python y manejo de errores de encoding/formato
            temp_df = pd.read_csv(f, engine='python', on_bad_lines='skip', encoding='utf-8')
            temp_df['forum'] = forum_name
            records.append(temp_df)
        except Exception as e:
            try:
                temp_df = pd.read_csv(f, engine='python', on_bad_lines='skip', encoding='latin1')
                temp_df['forum'] = forum_name
                records.append(temp_df)
            except Exception as e2:
                continue
                
    if records:
        df = pd.concat(records, ignore_index=True)
        return df
    return pd.DataFrame()

print("Cargando datos de foros...")
df_incels = load_forum_data('incels')
df_redpill = load_forum_data('red_pill_talk')
df_loveshy = load_forum_data('love_shy')

print(f"Posts cargados - Incels: {len(df_incels)}, RedPill: {len(df_redpill)}, LoveShy: {len(df_loveshy)}")

# Consolidar DataFrame principal centrado en Incels
df_all = pd.concat([df_incels, df_redpill, df_loveshy], ignore_index=True)
print(f"Total de registros consolidados: {len(df_all)}")

# Filtrar columnas clave
cols_to_keep = ['author', 'date_post', 'text_post', 'thread', 'forum', 'messages_author', 'id_post']
existing_cols = [c for c in cols_to_keep if c in df_all.columns]
df = df_all[existing_cols].copy()

# Eliminar nulos en texto
df = df.dropna(subset=['text_post'])
df['text_post'] = df['text_post'].astype(str)

print(f"Registros validos tras filtrar nulos: {len(df)}")
print(f"Usuarios unicos: {df['author'].nunique()}")

# 3. Limpieza y Normalizacion de Texto
def clean_text(text):
    # Remover tags html y urls
    text = re.sub(r'http\S+|www\.\S+', '', text)
    text = re.sub(r'<.*?>', '', text)
    # Remover caracteres especiales dejando palabras y espacios
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    # Convertir a minusculas y colapsar espacios
    text = text.lower().strip()
    text = re.sub(r'\s+', ' ', text)
    return text

print("Limpiando y normalizando textos...")
df['clean_text'] = df['text_post'].apply(clean_text)
df['word_count'] = df['clean_text'].apply(lambda x: len(x.split()))
df['char_count'] = df['clean_text'].apply(len)

# Filtrar mensajes muy cortos (ej. 'cope', 'lol', vacios) que no aporten contenido
df = df[df['word_count'] >= 3].copy()
print(f"Registros tras filtrar textos >= 3 palabras: {len(df)}")

# 4. Diccionario de Neologismos / Incel Slang y Marcadores de Radicalizacion
INCEL_LEXICON = {
    'ideology_general': [
        'blackpill', 'redpill', 'bluepill', 'pill', 'hypergamy', '80/20', 'subhuman',
        'sub-human', 'inceldom', 'incels', 'femoid', 'foid', 'foids', 'roastie', 'roasties',
        'becky', 'stacy', 'chad', 'chads', 'normie', 'normies', 'betabuxx', 'cuck'
    ],
    'appearance_looks': [
        'looksmaxxing', 'looksmax', 'psl', 'canthal', 'hunter eyes', 'jawline', 
        'recessed jaw', 'manlet', 'gymcell', 'facecel', 'heightcel', 'wristcel'
    ],
    'fatalism_violence': [
        'it\'s over', 'its over', 'it is over', 'rope', 'roping', 'go er', 'going er',
        'elliot rodger', 'saint elliot', 'retribution', 'involuntary celibate', 'cope',
        'coping', 'ldar', 'lie down and rot', 'suicidefuel', 'ragefuel', 'lifefuel'
    ]
}

# Aplanar lista de terminos
all_slang = set()
for category, terms in INCEL_LEXICON.items():
    for t in terms:
        all_slang.add(t.lower())

def count_slang_terms(text):
    words = text.split()
    count = 0
    found = []
    # Conteo de unigramas
    for w in words:
        if w in all_slang:
            count += 1
            found.append(w)
    # Conteo de n-gramas especificos (ej. 'its over', 'lie down and rot', 'saint elliot')
    for phrase in ['its over', 'it is over', 'going er', 'go er', 'elliot rodger', 'saint elliot', 'lie down and rot']:
        if phrase in text:
            count += 1
            found.append(phrase)
    return count, found

print("Analizando presencia de neologismos y jerga...")
slang_results = df['clean_text'].apply(count_slang_terms)
df['slang_count'] = [r[0] for r in slang_results]
df['slang_terms'] = [r[1] for r in slang_results]
df['has_slang'] = df['slang_count'] > 0

# 5. Analisis de Sentimiento (VADER)
print("Calculando polaridad de sentimiento con VADER...")
sia = SentimentIntensityAnalyzer()

def get_vader_scores(text):
    score = sia.polarity_scores(text)
    return score['compound'], score['pos'], score['neg'], score['neu']

vader_res = df['clean_text'].apply(get_vader_scores)
df['sentiment_compound'] = [r[0] for r in vader_res]
df['sentiment_pos'] = [r[1] for r in vader_res]
df['sentiment_neg'] = [r[2] for r in vader_res]
df['sentiment_neu'] = [r[3] for r in vader_res]

# Clasificar sentimiento general
def classify_sentiment(compound):
    if compound >= 0.05:
        return 'Positivo'
    elif compound <= -0.05:
        return 'Negativo'
    else:
        return 'Neutral'

df['sentiment_label'] = df['sentiment_compound'].apply(classify_sentiment)

# 6. Definicion de Nivel de Riesgo / Radicalizacion (Pregunta 1 de Clasificacion)
# Nivel 0 (Bajo/Neutral): Sentimiento >= -0.1 y 0 slang violento
# Nivel 1 (Moderado/Ideologico): Slang de ideologia/apariencia y sentimiento negativo
# Nivel 2 (Alto/Violencia/Fatalismo): Slang de fatalismo/violencia ('rope', 'going er', 'retribution', 'suicidefuel') o alta negatividad con jerga extrema
def assign_risk_level(row):
    text = row['clean_text']
    slang_list = row['slang_terms']
    neg = row['sentiment_neg']
    compound = row['sentiment_compound']
    
    # Comprobar si hay marcadores de violencia o fatalismo extremo
    violent_markers = ['going er', 'go er', 'elliot rodger', 'saint elliot', 'rope', 'roping', 'retribution', 'suicidefuel', 'subhuman', 'roastie']
    has_violent = any(m in slang_list or m in text for m in violent_markers)
    
    if has_violent and (compound < -0.3 or neg > 0.15):
        return 'Nivel 2: Alto Riesgo / Violencia'
    elif row['slang_count'] >= 1 or compound < -0.2:
        return 'Nivel 1: Moderado / Discurso Ideologico'
    else:
        return 'Nivel 0: Bajo / Cotidiano'

df['risk_level'] = df.apply(assign_risk_level, axis=1)

print("Distribucion de niveles de riesgo:")
print(df['risk_level'].value_counts(normalize=True))

# 7. Analisis Longitudinal por Usuario (Pregunta 2: Spiraling / Trayectoria)
# Agrupar por autor y ordenar por orden de post o messages_author
author_counts = df['author'].value_counts()
prolific_authors = author_counts[author_counts >= 5].index.tolist()
print(f"Usuarios con al menos 5 posts para analisis longitudinal: {len(prolific_authors)}")

# Guardar dataset procesado final
output_csv = os.path.join(DATA_DIR, 'incels_processed_dataset.csv')
df.to_csv(output_csv, index=False, encoding='utf-8')
print(f"Dataset limpio y procesado guardado en: {output_csv}")

# 8. Generacion de Graficos para el Informe
sns.set_theme(style="whitegrid", palette="muted")

# Grafico 1: Distribucion de Niveles de Riesgo por Foro
plt.figure(figsize=(9, 5))
risk_order = ['Nivel 0: Bajo / Cotidiano', 'Nivel 1: Moderado / Discurso Ideologico', 'Nivel 2: Alto Riesgo / Violencia']
ax = sns.countplot(data=df, x='risk_level', order=risk_order, hue='forum')
plt.title('Distribución de Niveles de Riesgo Ideológico por Foro', fontsize=13, weight='bold')
plt.xlabel('Nivel de Riesgo Asignado', fontsize=11)
plt.ylabel('Cantidad de Mensajes', fontsize=11)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '01_distribucion_niveles_riesgo.png'), dpi=300)
plt.close()

# Grafico 2: Top 15 Neologismos y Slang Incel mas Frecuentes
all_found_slang = [item for sublist in df['slang_terms'] for item in sublist]
slang_series = pd.Series(all_found_slang).value_counts().head(15)

plt.figure(figsize=(10, 5))
sns.barplot(x=slang_series.values, y=slang_series.index, palette='viridis')
plt.title('Top 15 Neologismos y Jerga Incel Más Frecuentes en el Corpus', fontsize=13, weight='bold')
plt.xlabel('Frecuencia de Aparición', fontsize=11)
plt.ylabel('Término / Neologismo', fontsize=11)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '02_top_neologismos_incel.png'), dpi=300)
plt.close()

# Grafico 3: Distribucion de Polaridad de Sentimiento (Compound VADER)
plt.figure(figsize=(9, 5))
sns.histplot(df['sentiment_compound'], bins=30, kde=True, color='darkred')
plt.title('Distribución de Polaridad de Sentimiento (VADER Compound)', fontsize=13, weight='bold')
plt.xlabel('Puntaje de Sentimiento (-1: Muy Negativo, +1: Muy Positivo)', fontsize=11)
plt.ylabel('Frecuencia', fontsize=11)
plt.axvline(0, color='grey', linestyle='--')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '03_distribucion_sentimiento.png'), dpi=300)
plt.close()

# Grafico 4: Analisis de 'Spiraling' Longitudinal (Evolucion de Toxicidad vs Actividad)
# Tomar usuarios con al menos 10 posts para ver la trayectoria
authors_10 = author_counts[author_counts >= 10].index.tolist()
df_longitudinal = df[df['author'].isin(authors_10)].copy()

# Ordenar por autor y numero de post si existe, o index
if 'number_post' in df_longitudinal.columns:
    df_longitudinal['post_seq'] = df_longitudinal.groupby('author')['number_post'].rank(method='first')
else:
    df_longitudinal['post_seq'] = df_longitudinal.groupby('author').cumcount() + 1

# Filtrar primeros 15 posts de trayectoria
df_traj = df_longitudinal[df_longitudinal['post_seq'] <= 15]
traj_stats = df_traj.groupby('post_seq').agg({
    'sentiment_neg': 'mean',
    'slang_count': 'mean',
    'sentiment_compound': 'mean'
}).reset_index()

fig, ax1 = plt.subplots(figsize=(10, 5))
color = 'tab:red'
ax1.set_xlabel('Secuencia de Mensajes del Usuario (Progresión Temporal)', fontsize=11)
ax1.set_ylabel('Sentimiento Negativo Promedio', color=color, fontsize=11)
ax1.plot(traj_stats['post_seq'], traj_stats['sentiment_neg'], color=color, marker='o', linewidth=2.5, label='Sentimiento Negativo')
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
color = 'tab:blue'
ax2.set_ylabel('Frecuencia Promedio de Neologismos / Slang', color=color, fontsize=11)
ax2.plot(traj_stats['post_seq'], traj_stats['slang_count'], color=color, marker='s', linestyle='--', linewidth=2.5, label='Densidad de Slang')
ax2.tick_params(axis='y', labelcolor=color)

plt.title('Trayectoria de Radicalización ("Spiraling"): Sentimiento Negativo y Adopción de Jerga en el Tiempo', fontsize=12, weight='bold')
fig.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '04_espiral_radicalizacion_longitudinal.png'), dpi=300)
plt.close()

print(f"Graficos generados exitosamente en: {OUTPUT_DIR}")
print("Proceso de EDA y preparacion de datos finalizado con exito.")
