import os
import requests
import json
import feedparser
import random
from datetime import datetime
import pytz
from bs4 import BeautifulSoup
import google.generativeai as genai

# Weekly Themed Feeds Schedule
WEEKLY_FEEDS = {
    0: {  # Segunda-feira - Filosofia
        "theme": "🧠 Filosofia",
        "emoji": "🧠",
        "feeds": [
            "https://dailynous.com/feed/",
            "https://aeon.co/feed.rss",
            "https://plato.stanford.edu/rss/sep.xml",
            "https://philosophynow.org/rss",
            "https://leiterreports.typepad.com/blog/atom.xml",
            "http://feeds.feedburner.com/PhilosophyBites",
            "https://theconversation.com/global/topics/philosophy-24/articles.atom"
        ]
    },
    1: {  # Terça-feira - Finanças & Hedge Funds
        "theme": "💰 Finanças & Hedge Funds",
        "emoji": "💰",
        "feeds": [
            "https://www.ft.com/rss/home",
            "https://www.bloomberg.com/feed/podcast/etf-iq.xml",
            "https://www.hedgeweek.com/feed/",
            "https://www.institutionalinvestor.com/RSS",
            "https://www.investopedia.com/feedbuilder/feed/getfeed?feedName=rss_headline",
            "https://seekingalpha.com/feed.xml",
            "https://www.marketwatch.com/rss/topstories"
        ]
    },
    2: {  # Quarta-feira - Ciências Sociais
        "theme": "👥 Ciências Sociais",
        "emoji": "👥",
        "feeds": [
            "https://theconversation.com/global/topics/sociology-76/articles.atom",
            "https://www.sciencedaily.com/rss/mind_brain/psychology.xml",
            "https://www.tandfonline.com/feed/rss/rsoc20",
            "https://journals.sagepub.com/action/showFeed?ui=0&mi=ehikzz&ai=2b4&jc=ssia&type=etoc&feed=rss",
            "https://www.anthropology-news.org/feed/",
            "https://blogs.lse.ac.uk/feed/"
        ]
    },
    3: {  # Quinta-feira - Alta Gastronomia & Culinária
        "theme": "🍽️ Alta Gastronomia & Culinária",
        "emoji": "🍽️",
        "feeds": [
            "https://www.seriouseats.com/feed",
            "https://www.bonappetit.com/feed/rss",
            "https://www.saveur.com/feed/",
            "https://www.foodandwine.com/rss/news.xml",
            "https://www.theworlds50best.com/feed",
            "https://www.eater.com/rss/index.xml",
            "https://www.finedininglovers.com/rss"
        ]
    },
    4: {  # Sexta-feira - Ciência em Geral
        "theme": "🔬 Ciência em Geral",
        "emoji": "🔬",
        "feeds": [
            "https://www.nature.com/nature.rss",
            "https://www.sciencemag.org/rss/news_current.xml",
            "https://www.sciencedaily.com/rss/all.xml",
            "https://www.newscientist.com/feed/home",
            "https://www.scientificamerican.com/feed/",
            "https://phys.org/rss-feed/",
            "https://www.space.com/feeds/all"
        ]
    },
    5: {  # Sábado - Diversos
        "theme": "🌍 Tópicos Diversos",
        "emoji": "🌍",
        "feeds": [
            "https://www.theguardian.com/world/rss",
            "https://www.bbc.com/news/rss.xml",
            "https://www.theatlantic.com/feed/all/",
            "https://www.newyorker.com/feed/everything",
            "https://www.wired.com/feed/rss",
            "https://aeon.co/feed.rss",
            "https://www.vox.com/rss/index.xml"
        ]
    },
    6: {  # Domingo - Diversos
        "theme": "🎨 Arte, Cultura & Diversos",
        "emoji": "🎨",
        "feeds": [
            "https://www.artforum.com/rss.xml",
            "https://hyperallergic.com/feed/",
            "https://www.theparisreview.org/blog/feed/",
            "https://lithub.com/feed/",
            "https://www.smithsonianmag.com/rss/latest_articles/",
            "https://www.npr.org/rss/rss.php?id=1008",
            "https://www.ted.com/talks/rss"
        ]
    }
}

HISTORY_FILE = "history.json"

class DailyReporter:
    def __init__(self, webhook_url, gemini_api_key=None):
        # Force UTF-8 for Windows console
        import sys
        if sys.platform == 'win32':
            try:
                sys.stdout.reconfigure(encoding='utf-8')
            except:
                pass
        
        self.webhook_url = webhook_url
        self.tz_BR = pytz.timezone('America/Sao_Paulo')
        self.history = self.load_history()
        
        # Initialize Gemini API
        self.gemini_api_key = gemini_api_key
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            # Usando gemini-pro que é mais estável universalmente
            self.model = genai.GenerativeModel('gemini-pro')
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
            # Try to fetch full article content
            content = self.fetch_article_content(article['link'])
            
            # If fetch fails, use the RSS summary as context
            if not content:
                print(f"   ⚠️ Falha ao ler artigo completo. Usando resumo do RSS para gerar IA.")
                content = article.get('summary', '')

            if not content:
                return "Conteúdo não disponível para resumo."

            # Create prompt for Gemini
            prompt = f"""Você é um especialista em filosofia e cultura. 
Analise o texto abaixo e faça o seguinte:
1. Gere um resumo explicativo em Português Brasileiro.
2. Mantenha o tom sofisticado mas acessível.

Título: {article['title']}
Fonte: {article['source']}

Texto base:
{content}

Resumo em Português:"""

            print(f"   🤖 Gerando resumo com Gemini para: {article['title'][:50]}...")
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            print(f"   ⚠️ Erro ao gerar resumo com Gemini: {e}")
            # Retorna o erro visível para debug
            return f"{article.get('summary', '')}\n\n⚠️ *Erro IA:* {str(e)}"

    def collect_data(self):
        # Get current day of week (0=Monday, 6=Sunday)
        today = datetime.now(self.tz_BR).weekday()
        day_config = WEEKLY_FEEDS[today]
        
        print(f"📅 Tema de hoje: {day_config['theme']}")
        print("📡 Buscando feeds RSS...")
        all_entries = []
        
        for feed_url in day_config['feeds']:
            try:
                print(f"   - Lendo: {feed_url}")
                feed = feedparser.parse(feed_url)
                for entry in feed.entries:
                    # Clean up RSS summary (remove HTML tags)
                    raw_summary = entry.get('summary', 'No summary available')
                    soup = BeautifulSoup(raw_summary, 'html.parser')
                    clean_summary = soup.get_text().strip()

                    # Basic normalization
                    all_entries.append({
                        "title": entry.title,
                        "link": entry.link,
                        "source": feed.feed.get('title', 'Unknown Source'),
                        "summary": clean_summary[:300] + "..."
                    })
            except Exception as e:
                print(f"   ⚠️ Erro ao ler {feed_url}: {e}")

        # Filter out already sent articles
        new_entries = [e for e in all_entries if e['link'] not in self.history]
        
        print(f"📊 Total de artigos encontrados: {len(all_entries)}")
        print(f"🆕 Artigos novos (não enviados): {len(new_entries)}")

        if not new_entries:
            return None, day_config

        # Select 2 random articles
        selected = random.sample(new_entries, min(2, len(new_entries)))
        
        return selected, day_config

    def format_message(self, articles, day_config):
        current_time = self.get_current_time()
        
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"{day_config['emoji']} Curadoria Diária: {day_config['theme']}",
                    "emoji": True
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": f"📅 *{current_time}* | Resumos"
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
                    "text": f"*<{article['link']}|{article['title']}>*\n\n_{article['source']}_\n\n{summary}"
                }
            })
            blocks.append({"type": "divider"})

        return {"blocks": blocks}

    def send(self):
        # Force UTF-8 for Windows console
        import sys
        if sys.platform == 'win32':
            try:
                sys.stdout.reconfigure(encoding='utf-8')
            except:
                pass
    
        print("🔄 Coletando dados...")
        result = self.collect_data()
        
        if not result[0]:  # No articles found
            print("📭 Nenhum artigo novo encontrado hoje.")
            return
        
        articles, day_config = result

        print("📝 Formatando mensagem...")
        message_payload = self.format_message(articles, day_config)

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
                for article in articles:
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
