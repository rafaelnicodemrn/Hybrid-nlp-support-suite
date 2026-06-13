from transformers import pipeline
import os

print("==================================================")
print("📥 Iniciando download do modelo RoBERTuito para cache...")
print("==================================================")

# Força o Hugging Face a baixar os pesos (500MB) e salvar no contêiner
pipeline("text-classification", model="pysentimiento/robertuito-sentiment-analysis")

print("✅ Download concluído e modelo salvo em cache no Docker!")