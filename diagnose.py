import sys
import os
import requests
from dotenv import load_dotenv
import google.generativeai as genai

# Force UTF-8 for Windows console
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

# Load environment variables
load_dotenv()

def check_newsapi():
    key = os.getenv('NEWS_API_KEY')
    if not key:
        return "❌ NEWS_API_KEY não encontrada no .env ou variáveis de ambiente."
    
    try:
        url = "https://newsapi.org/v2/top-headlines?country=br&apiKey=" + key
        response = requests.get(url)
        if response.status_code == 200:
            return "✅ NewsAPI conectada com sucesso!"
        else:
            return f"❌ Erro na NewsAPI: {response.status_code} - {response.json().get('message', '')}"
    except Exception as e:
        return f"❌ Exceção ao testar NewsAPI: {str(e)}"

def check_gemini():
    key = os.getenv('GEMINI_API_KEY')
    if not key:
        return "❌ GEMINI_API_KEY não encontrada no .env ou variáveis de ambiente."
    
    try:
        genai.configure(api_key=key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Teste de conexão.")
        if response and response.text:
            return "✅ Gemini API conectada e gerando texto com sucesso!"
        else:
            return "❌ Gemini API conectada, mas não retornou texto."
    except Exception as e:
        return f"❌ Erro no Gemini: {str(e)}"

def check_perplexity():
    key = os.getenv('PERPLEXITY_API_KEY')
    if not key:
        return "⚠️ PERPLEXITY_API_KEY não encontrada (Opcional se tiver Gemini)."
    
    try:
        url = "https://api.perplexity.ai/chat/completions"
        payload = {
            "model": "llama-3.1-sonar-small-128k-online",
            "messages": [{"role": "user", "content": "Teste."}]
        }
        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        }
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return "✅ Perplexity API conectada com sucesso!"
        else:
            return f"❌ Erro na Perplexity: {response.status_code} - {response.text}"
    except Exception as e:
        return f"❌ Exceção ao testar Perplexity: {str(e)}"

def check_slack():
    url = os.getenv('SLACK_WEBHOOK_URL')
    if not url:
        return "❌ SLACK_WEBHOOK_URL não encontrada."
    if "hooks.slack.com" not in url:
        return "❌ SLACK_WEBHOOK_URL parece inválida (não contém hooks.slack.com)."
    return "✅ SLACK_WEBHOOK_URL configurada (Teste de envio real não realizado para evitar spam)."

print("🔍 Iniciando Diagnóstico de APIs...\n")
print(f"Arquivo .env encontrado? {'Sim' if os.path.exists('.env') else 'Não'}")
print("-" * 30)
print(check_newsapi())
print("-" * 30)
print(check_gemini())
print("-" * 30)
print(check_perplexity())
print("-" * 30)
print(check_slack())
print("\n🏁 Diagnóstico concluído.")
