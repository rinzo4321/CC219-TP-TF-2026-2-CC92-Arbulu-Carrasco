import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, f1_score
import json

# Rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
OUTPUT_DIR = os.path.join(BASE_DIR, 'figures')

print("Cargando dataset procesado...")
df = pd.read_csv(os.path.join(DATA_DIR, 'incels_processed_dataset.csv'))

print(f"Total registros: {len(df)}")

# ==============================================================
# EXPERIMENTO 1: Clasificacion de Nivel de Riesgo (Pregunta 1)
# ==============================================================
print("\n--- EXPERIMENTO 1: Clasificación de Nivel de Riesgo ---")
X = df['clean_text'].astype(str)
y = df['risk_level']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# Vectorizacion TF-IDF (1-gramas y 2-gramas)
vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2), stop_words='english')
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

models = {
    'Multinomial Naive Bayes': MultinomialNB(),
    'Logistic Regression (Balanced)': LogisticRegression(max_iter=1000, class_weight='balanced'),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42)
}

results = {}
for name, model in models.items():
    model.fit(X_train_vec, y_train)
    y_pred = model.predict(X_test_vec)
    acc = accuracy_score(y_test, y_pred)
    f1_macro = f1_score(y_test, y_pred, average='macro')
    f1_weighted = f1_score(y_test, y_pred, average='weighted')
    
    results[name] = {
        'Accuracy': round(acc, 4),
        'F1_Macro': round(f1_macro, 4),
        'F1_Weighted': round(f1_weighted, 4),
        'Report': classification_report(y_test, y_pred, output_dict=True)
    }
    print(f"Modelo: {name} -> Acc: {acc:.4f}, F1-Macro: {f1_macro:.4f}, F1-Weighted: {f1_weighted:.4f}")

# Guardar resultados en un resumen JSON
with open(os.path.join(OUTPUT_DIR, 'baseline_results.json'), 'w') as f:
    json.dump(results, f, indent=4)

print("\nModelos baseline evaluados con exito.")
