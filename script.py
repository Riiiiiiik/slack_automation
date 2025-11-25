import os
from dotenv import load_dotenv
load_dotenv()

import requests
import json
import random
from datetime import datetime
import pytz
import sqlite3
import feedparser
from newspaper import Article
import google.generativeai as genai

# Weekly Themed Feeds Schedule
WEEKLY_FEEDS = {
    0: {  # Segunda-feira - Filosofia
        "theme": "🧠 Filosofia",
        "emoji": "🧠",
        "keywords": "(philosophy OR ethics OR epistemology OR metaphysics) AND (theory OR analysis OR debate) -celebrity -gossip",
        "feeds": [
            "https://dailynous.com/feed/",
            "https://aeon.co/feed.rss",
            "https://plato.stanford.edu/rss/sep.xml",
            "https://philosophynow.org/rss"
        ]
    },
    1: {  # Terça-feira - Finanças & Hedge Funds
        "theme": "💰 Finanças & Hedge Funds",
        "emoji": "💰",
        "keywords": "(\"hedge fund\" OR \"investment strategy\" OR \"portfolio management\" OR \"financial markets\" OR \"asset management\") AND (analysis OR strategy OR performance) -crypto -bitcoin",
        "feeds": [
            "https://www.ft.com/rss/home",
            "https://www.hedgeweek.com/feed/",
            "https://seekingalpha.com/feed.xml"
        ]
    },
    2: {  # Quarta-feira - Ciências Sociais
        "theme": "👥 Ciências Sociais",
        "emoji": "👥",
        "keywords": "(sociology OR anthropology OR \"social psychology\" OR \"behavioral science\") AND (research OR study OR theory) -celebrity -entertainment",
        "feeds": [
            "https://theconversation.com/global/topics/sociology-76/articles.atom",
            "https://www.sciencedaily.com/rss/mind_brain/psychology.xml"
        ]
    },
    3: {  # Quinta-feira - Alta Gastronomia & Culinária
        "theme": "🍽️ Alta Gastronomia & Culinária",
        "emoji": "🍽️",
        "keywords": "(\"fine dining\" OR gastronomy OR \"culinary arts\" OR \"michelin star\" OR \"haute cuisine\" OR chef) AND (restaurant OR technique OR innovation) -recipe -home",
        "feeds": [
            "https://www.seriouseats.com/feed",
            "https://www.eater.com/rss/index.xml"
        ]
    },
    4: {  # Sexta-feira - Ciência em Geral
        "theme": "🔬 Ciência em Geral",
        "emoji": "🔬",
        "keywords": "(\"scientific research\" OR \"breakthrough\" OR discovery OR physics OR biology OR \"space exploration\" OR astronomy) AND (study OR experiment OR findings) -horoscope -astrology",
        "feeds": [
            "https://www.nature.com/nature.rss",
            "https://www.sciencedaily.com/rss/all.xml",
            "https://phys.org/rss-feed/"
        ]
    },
    5: {  # Sábado - Diversos
        "theme": "🌍 Tópicos Diversos",
        "emoji": "🌍",
        "keywords": "(technology OR innovation OR \"artificial intelligence\" OR geopolitics OR \"global affairs\") AND (analysis OR impact OR development) -celebrity -sports",
        "feeds": [
            "https://www.theguardian.com/world/rss",
            "https://www.wired.com/feed/rss",
            "https://aeon.co/feed.rss"
        ]
    },
    6: {  # Domingo - Arte & Cultura
        "theme": "🎨 Arte, Cultura & Diversos",
        "emoji": "🎨",
        "keywords": "(\"contemporary art\" OR literature OR \"cultural criticism\" OR exhibition OR museum OR \"art history\") AND (review OR analysis OR critique) -celebrity -gossip",
        "feeds": [
            "https://hyperallergic.com/feed/",
            "https://lithub.com/feed/"
        ]
    }
}

class DailyReporter:
    def __init__(self, webhook_url, gemini_api_key=None, perplexity_api_key=None, news_api_key=None):
        import sys
        if sys.platform == 'win32':
            try:
                sys.stdout.reconfigure(encoding='utf-8')
            except:
                pass
        
        self.webhook_url = webhook_url
        self.tz_BR = pytz.timezone('America/Sao_Paulo')
        
        # MELHORIA 5: SQLite para histórico
        self.conn = sqlite3.connect('history.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS sent_articles (link TEXT PRIMARY KEY, date TEXT)')
        self.conn.commit()
        
        self.news_api_key = news_api_key
        if self.news_api_key:
            print("✅ NewsAPI configurada!")
        else:
            print("⚠️ NewsAPI key não fornecida.")

        self.perplexity_api_key = perplexity_api_key
        if self.perplexity_api_key:
            print("✅ Perplexity API configurada!")
        else:
            print("⚠️ Perplexity API key não fornecida.")
        
        self.gemini_api_key = gemini_api_key
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            print("✅ Gemini API configurada!")
        else:
            print("⚠️ Gemini API key não fornecida.")

    def url_already_sent(self, url):
        """MELHORIA 5: Verifica se URL já foi enviada usando SQLite"""
        self.cursor.execute('SELECT 1 FROM sent_articles WHERE link = ?', (url,))
        return self.cursor.fetchone() is not None

    def mark_as_sent(self, url):
        """MELHORIA 5: Marca URL como enviada no SQLite"""
        self.cursor.execute('INSERT OR IGNORE INTO sent_articles VALUES (?, ?)', (url, datetime.now().isoformat()))
        self.conn.commit()

    def get_current_time(self):
        return datetime.now(self.tz_BR).strftime('%d/%m/%Y %H:%M:%S')

    def fetch_article_data(self, url):
        """MELHORIA 2: Usa newspaper3k para extrair texto limpo e imagem"""
        try:
            article = Article(url)
            article.download()
            article.parse()
            return {
                "text": article.text[:3000],
                "image": article.top_image
            }
        except Exception as e:
            print(f"   ⚠️ Erro ao ler {url}: {e}")
            return None

    def generate_summary_perplexity(self, article, content):
        """MELHORIA 1: Modelo correto llama-3.1-sonar-small-128k-online"""
        if not self.perplexity_api_key:
            return None, "API Key não configurada"
        
        prompt = f"""Você é um especialista. Gere um resumo em Português Brasileiro com EXATAMENTE 500 caracteres.

Título: {article['title']}
Fonte: {article['source']}

Texto: {content}

Resumo (500 caracteres):"""

        try:
            print(f"   🔮 Tentando Perplexity...")
            url = "https://api.perplexity.ai/chat/completions"
            
            payload = {
                "model": "llama-3.1-sonar-small-128k-online",  # MELHORIA 1: Modelo correto
                "messages": [
                    {"role": "system", "content": "Gere resumos com exatamente 500 caracteres em Português."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 200,
                "temperature": 0.3
            }
            
            headers = {
                "Authorization": f"Bearer {self.perplexity_api_key}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            result = response.json()
            
            if 'choices' in result and len(result['choices']) > 0:
                summary = result['choices'][0]['message']['content']
                print(f"   ✅ Perplexity OK!")
                return summary[:500], None
            return None, "Resposta vazia"
        except Exception as e:
            return None, str(e)

    def generate_summary_gemini(self, article, content):
        """MELHORIA 1: Modelo correto gemini-1.5-flash"""
        if not self.gemini_api_key:
            return None, "API Key não configurada"
        
        model_name = 'gemini-1.5-flash'  # MELHORIA 1: Modelo de produção estável
        
        prompt = f"""Você é um especialista. Gere um resumo em Português Brasileiro com EXATAMENTE 500 caracteres.

Título: {article['title']}
Fonte: {article['source']}

Texto: {content}

Resumo (500 caracteres):"""

        try:
            print(f"   🤖 Tentando Gemini ({model_name})...")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            
            if response and response.text:
                print(f"   ✅ Gemini OK!")
                return response.text[:500], None
            return None, "Resposta vazia"
        except Exception as e:
            return None, str(e)

    def generate_summary(self, article, content):
        """Gera resumo com IA (Perplexity ou Gemini)"""
        if not content or len(content) < 50:
            return (article.get('summary', 'Sem resumo disponível'))[:500]

        # Tenta Perplexity
        summary, _ = self.generate_summary_perplexity(article, content)
        if summary:
            return summary[:500]

        # Tenta Gemini
        summary, _ = self.generate_summary_gemini(article, content)
        if summary:
            return summary[:500]

        return (article.get('summary', 'Sem resumo disponível'))[:500]

    def fetch_from_newsapi(self, keywords):
        """Busca artigos na NewsAPI"""
        if not self.news_api_key:
            return []

        print(f"   📡 NewsAPI: {keywords[:50]}...")
        url = "https://newsapi.org/v2/everything"
        
        params = {
            'q': keywords,
            'language': 'en',
            'sortBy': 'popularity',
            'pageSize': 20,
            'apiKey': self.news_api_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            return [
                {
                    "title": item['title'],
                    "link": item['url'],
                    "source": item['source']['name'],
                    "summary": item['description'] or ""
                }
                for item in data.get('articles', [])
                if item['title'] != '[Removed]'
            ]
        except Exception as e:
            print(f"   ⚠️ Erro NewsAPI: {e}")
            return []

    def fetch_from_rss(self, feeds_list):
        """MELHORIA 3: Busca em feeds RSS como fallback"""
        print(f"   📡 Buscando em feeds RSS...")
        articles = []
        for feed_url in feeds_list:
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries[:2]:  # 2 mais recentes de cada
                    articles.append({
                        "title": entry.title,
                        "link": entry.link,
                        "source": feed.feed.get('title', 'RSS'),
                        "summary": getattr(entry, 'summary', '')
                    })
            except:
                continue
        return articles

    def collect_data(self):
        """MELHORIA 3: Lógica híbrida NewsAPI + RSS"""
        today = datetime.now(self.tz_BR).weekday()
        cfg = WEEKLY_FEEDS[today]
        
        print(f"📅 Tema: {cfg['theme']}")
        
        # 1. Tenta NewsAPI
        articles = self.fetch_from_newsapi(cfg["keywords"])
        
        # 2. Se tiver menos de 5, completa com RSS
        if len(articles) < 5:
            print(f"   ⚠️ Poucos artigos da NewsAPI ({len(articles)}), complementando com RSS...")
            rss_articles = self.fetch_from_rss(cfg["feeds"])
            articles.extend(rss_articles)
        
        # Filtra já enviados usando SQLite
        new = [a for a in articles if not self.url_already_sent(a["link"])]
        
        print(f"📊 Total: {len(articles)} | Novos: {len(new)}")
        
        if not new:
            return None, cfg
        
        return random.sample(new, min(2, len(new))), cfg

    def format_message(self, articles, cfg):
        """MELHORIA 4: Adiciona imagens no Slack"""
        now = self.get_current_time()
        
        blocks = [
            {
                "type": "header",
                "text": {"type": "plain_text", "text": f"{cfg['emoji']} Curadoria Diária: {cfg['theme']}"}
            },
            {
                "type": "context",
                "elements": [{"type": "mrkdwn", "text": f"📅 *{now}*"}]
            },
            {"type": "divider"}
        ]
        
        for article in articles:
            # MELHORIA 2: Usa newspaper3k
            data = self.fetch_article_data(article["link"])
            content = data["text"] if data else article.get("summary", "")
            image_url = data["image"] if data else None
            
            # Gera resumo com IA
            summary = self.generate_summary(article, content)
            
            # MELHORIA 4: Cria bloco com imagem
            section = {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*<{article['link']}|{article['title']}>*\n\n_{article['source']}_\n\n{summary}"
                }
            }
            
            # Se tiver imagem, adiciona miniatura
            if image_url and image_url.startswith("http"):
                section["accessory"] = {
                    "type": "image",
                    "image_url": image_url,
                    "alt_text": "Imagem da notícia"
                }
            
            blocks.append(section)
            blocks.append({"type": "divider"})
        
        return {"blocks": blocks}

    def send(self):
        print("🔄 Coletando dados...")
        result = self.collect_data()
        
        if not result or not result[0]:
            print("📭 Nenhum artigo novo.")
            return
        
        articles, cfg = result
        
        print("📝 Formatando...")
        message = self.format_message(articles, cfg)
        
        if not self.webhook_url:
            print("⚠️ SLACK_WEBHOOK_URL não definido.")
            print(json.dumps(message, indent=2, ensure_ascii=False))
            return
        
        print("🚀 Enviando...")
        try:
            r = requests.post(
                self.webhook_url,
                data=json.dumps(message),
                headers={"Content-Type": "application/json"}
            )
            if r.status_code == 200:
                print("✅ Enviado!")
                for a in articles:
                    self.mark_as_sent(a["link"])  # MELHORIA 5: SQLite
            else:
                print(f"❌ Erro: {r.status_code}: {r.text}")
        except Exception as e:
            print(f"❌ Exceção: {e}")

if __name__ == "__main__":
    webhook_url = os.environ.get("SLACK_WEBHOOK_URL")
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    perplexity_api_key = os.environ.get("PERPLEXITY_API_KEY")
    news_api_key = os.environ.get("NEWS_API_KEY")
    
    reporter = DailyReporter(webhook_url, gemini_api_key, perplexity_api_key, news_api_key)
    reporter.send()
