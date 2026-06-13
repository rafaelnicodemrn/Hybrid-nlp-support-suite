import os
import json
import asyncio
import logging
from transformers import pipeline
from google import genai
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    logger.error("ALERTA: A variável GOOGLE_API_KEY não foi localizada no arquivo .env!")

logger.info("Carregando pipeline de análise de sentimentos local (RoBERTuito)...")
sentiment_pipeline = pipeline("text-classification", model="pysentimiento/robertuito-sentiment-analysis")
genai_client = genai.Client(api_key=GOOGLE_API_KEY) if GOOGLE_API_KEY else None

class MLService:
    def analyze_local(self, text: str):
        try:
            res_local = sentiment_pipeline(text)[0]
            return res_local['label'], float(res_local['score'])
        except Exception as e:
            logger.error(f"Erro no processamento do modelo local: {e}")
            raise e

    async def get_llm_insight(self, text: str, sentiment: str):
        if not genai_client:
            logger.warning("Variável de chave inválida. Ativando Degradação Graciosa Básica.")
            priority_level = "ALTA" if sentiment == "NEG" else "NORMAL"
            insight = "Sentimos muito pelo inconveniente. Nossa equipe humana já foi notificada."
            return priority_level, insight

        prompt = (
            "Você é um especialista em triagem de suporte técnico corporativo. Analise o ticket abaixo e retorne APENAS um objeto JSON válido, sem formatações adicionais, contendo exatamente as chaves:\n"
            "1. 'prioridade': Classifique a urgência estritamente como 'ALTA' (sistemas fora do ar, bugs críticos, bloqueio de operação ou perdas financeiras), 'NORMAL' (dúvidas operacionais) ou 'BAIXA' (elogios, solicitações simples de TI como pedidos de teclados ou mouses sem fio).\n"
            "2. 'insight': Escreva uma sugestão de resposta curta e empática direcionada ao cliente em exatamente uma frase.\n\n"
            f"Ticket: '{text}'"
        )
        try:
            response = await asyncio.to_thread(
                genai_client.models.generate_content,
                model="gemini-3.5-flash",
                contents=prompt
            )
            # Limpa formatação de código caso a IA coloque blocos de markdown
            texto_limpo = response.text.replace('```json', '').replace('```', '').strip()
            dados_ia = json.loads(texto_limpo)
            
            priority_level = dados_ia.get("prioridade", "NORMAL").upper()
            insight = dados_ia.get("insight", "Análise processada pela contingência externa.")
            
            if priority_level not in ["ALTA", "NORMAL", "BAIXA"]:
                priority_level = "NORMAL"
                
            return priority_level, insight
        except Exception as e:
            logger.warning(f"Degradação Graciosa Ativada por erro na LLM externa: {e}")
            priority_level = "ALTA" if sentiment == "NEG" else "NORMAL"
            insight = "Sentimos muito pelo inconveniente. Nossa equipe humana já foi notificada."
            return priority_level, insight

# Instância única para ser importada pelo main.py
ml_service = MLService()