import os
import requests
import json
import feedparser
import random
from datetime import datetime
import pytz
from bs4 import BeautifulSoup
import google.generativeai as genai

# List of Philosophy RSS Feeds
FEEDS = [
    "https://dailynous.com/feed/",
    "https://aeon.co/feed.rss",
    "https://plato.stanford.edu/rss/sep.xml",
    "https://philosophynow.org/rss",
    "https://leiterreports.typepad.com/blog/atom.xml",
    "http://feeds.feedburner.com/PhilosophyBites",
    "https://theconversation.com/global/topics/philosophy-24/articles.atom"
]

HISTORY_FILE = "history.json"

class DailyReporter:
    def __init__(self, webhook_url, gemini_api_key=None):
        self.webhook_url = webhook_url
        self.tz_BR = pytz.timezone('America/Sao_Paulo')
        self.history = self.load_history()
        
        # Initialize Gemini API
        self.gemini_api_key = gemini_api_key
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            print("✅ Gemini API configurada com sucesso!")
        else:
            self.model = None
            print("⚠️ Gemini API key não fornecida. Resumos não serão gerados.")

    def load_history(self):
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []

    def save_history(self):
        with open(HISTORY_FILE, 'w') as f:
            json.dump(self.history, f, indent=2)

    def get_current_time(self):
        return datetime.now(self.tz_BR).strftime('%d/%m/%Y %H:%M:%S')
    
    def fetch_article_content(self, url):
        """Fetch the full article content from URL"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text content
            text = soup.get_text()
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            # Limit to first 3000 characters to avoid token limits
            return text[:3000]
        except Exception as e:
            print(f"   ⚠️ Erro ao buscar conteúdo de {url}: {e}")
            return None
    
    def generate_summary(self, article):
        """Generate a Portuguese summary using Gemini AI"""
        if not self.model:
            return article.get('summary', 'Sem resumo disponível')
        
        try:
            # Fetch full article content
            content = self.fetch_article_content(article['link'])
            
            if not content:
                return article.get('summary', 'Sem resumo disponível')
            
            # Create prompt for Gemini
            prompt = f"""Você é um especialista em filosofia. Analise o seguinte artigo e forneça:

1. Um resumo conciso em português (máximo 3 parágrafos)
2. Os principais conceitos filosóficos abordados
3. A relevância do tema

Título: {article['title']}
Fonte: {article['source']}

Conteúdo:
{content}

Forneça o resumo em português brasileiro, de forma clara e acessível."""

            print(f"   🤖 Gerando resumo com Gemini para: {article['title'][:50]}...")
            response = self.model.generate_content(prompt)
            
            return response.text
            
        except Exception as e:
            print(f"   ⚠️ Erro ao gerar resumo com Gemini: {e}")
            return article.get('summary', 'Sem resumo disponível')

    def collect_data(self):
        print("📡 Buscando feeds RSS...")
        all_entries = []
        
        for feed_url in FEEDS:
            try:
                print(f"   - Lendo: {feed_url}")
                feed = feedparser.parse(feed_url)
                for entry in feed.entries:
                    # Basic normalization
                    all_entries.append({
                        "title": entry.title,
                        "link": entry.link,
                        "source": feed.feed.get('title', 'Unknown Source'),
                        "summary": entry.get('summary', 'No summary available')[:200] + "..."
                    })
            except Exception as e:
                print(f"   ⚠️ Erro ao ler {feed_url}: {e}")

        # Filter out already sent articles
        new_entries = [e for e in all_entries if e['link'] not in self.history]
        
        print(f"📊 Total de artigos encontrados: {len(all_entries)}")
        print(f"🆕 Artigos novos (não enviados): {len(new_entries)}")

        if not new_entries:
            return None

        # Select 2 random articles
        selected = random.sample(new_entries, min(2, len(new_entries)))
        
        return selected

    def format_message(self, articles):
        current_time = self.get_current_time()
        
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "🧠 Dose Diária de Filosofia",
                    "emoji": True
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": f"📅 *{current_time}* | Resumos gerados por IA 🤖"
                    }
                ]
            },
            {"type": "divider"}
        ]

        for article in articles:
            # Generate AI summary
            summary = self.generate_summary(article)
            
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*<{article['link']}|{article['title']}>*\n_{article['source']}_\n\n{summary}"
                }
            })
            blocks.append({"type": "divider"})

        return {"blocks": blocks}

    def send(self):
        # Force UTF-8 for Windows console
        import sys
        if sys.platform == 'win32':
            sys.stdout.reconfigure(encoding='utf-8')

        print("🔄 Coletando dados...")
        data = self.collect_data()
        
        if not data:
            print("📭 Nenhum artigo novo encontrado hoje.")
            return

        print("📝 Formatando mensagem...")
        message_payload = self.format_message(data)

        if not self.webhook_url:
            print("⚠️ Error: SLACK_WEBHOOK_URL not set. Skipping send (Dry Run).")
            print("--- PREVIEW ---")
            print(json.dumps(message_payload, indent=2, ensure_ascii=False))
            return

        print("🚀 Enviando para o Slack...")
        try:
            response = requests.post(
                self.webhook_url, 
                data=json.dumps(message_payload),
                headers={'Content-Type': 'application/json'}
            )

            if response.status_code != 200:
                print(f"❌ Erro ao enviar: {response.status_code}\n{response.text}")
                exit(1)
            else:
                print("✅ Mensagem enviada com sucesso!")
                # Update history only on success
                for article in data:
                    self.history.append(article['link'])
                self.save_history()
                
        except Exception as e:
            print(f"❌ Exceção: {e}")
            exit(1)

if __name__ == "__main__":
    webhook_url = os.environ.get('SLACK_WEBHOOK_URL')
    gemini_api_key = os.environ.get('GEMINI_API_KEY')
    reporter = DailyReporter(webhook_url, gemini_api_key)
    reporter.send()
