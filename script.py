import os
from dotenv import load_dotenv

load_dotenv()

import requests
import json

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
        "keywords": "philosophy OR ethics OR metaphysics",
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
        "keywords": "hedge funds OR financial markets OR investment strategy",
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
        "keywords": "sociology OR anthropology OR social psychology",
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
        "keywords": "fine dining OR gastronomy OR culinary arts OR michelin star",
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
        "keywords": "scientific research OR physics OR biology OR space exploration",
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
        "keywords": "world news OR technology OR culture OR innovation",
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
        "keywords": "contemporary art OR literature OR cultural criticism",
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
    def __init__(self, webhook_url, gemini_api_key=None, perplexity_api_key=None, news_api_key=None):
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
        
        # Initialize NewsAPI
        self.news_api_key = news_api_key
        if self.news_api_key:
            print("✅ NewsAPI configurada com sucesso!")
        else:
            print("⚠️ NewsAPI key não fornecida. O script não funcionará corretamente sem ela.")

        # Initialize Perplexity API
        self.perplexity_api_key = perplexity_api_key
        if self.perplexity_api_key:
            print("✅ Perplexity API configurada com sucesso!")
        else:
            print("⚠️ Perplexity API key não fornecida.")
        
        # Initialize Gemini API
        self.gemini_api_key = gemini_api_key
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            print("✅ Gemini API configurada com sucesso!")
        else:
            print("⚠️ Gemini API key não fornecida.")

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
    
    def generate_summary_perplexity(self, article, content):
        """Generate a Portuguese summary using Perplexity AI with retry logic"""
        if not self.perplexity_api_key:
            return None, "API Key não configurada"
        
        # Create prompt
        prompt = f"""Você é um especialista em filosofia e cultura. 
Analise o texto abaixo e faça o seguinte:
1. Gere um resumo explicativo em Português Brasileiro com EXATAMENTE 500 caracteres ou menos.
2. Mantenha o tom sofisticado mas acessível.
3. Seja conciso e direto.

Título: {article['title']}
Fonte: {article['source']}

Texto base:
{content}

Resumo em Português (máximo 500 caracteres):"""
        
        # Retry logic with exponential backoff
        max_retries = 3
        retry_delay = 1  # seconds
        
        for attempt in range(max_retries):
            try:
                print(f"   🔮 Tentando gerar resumo com Perplexity - Tentativa {attempt + 1}/{max_retries}...")
                
                # Perplexity API endpoint
                url = "https://api.perplexity.ai/chat/completions"
                
                payload = {
                    "model": "llama-3.1-sonar-small-128k-online",
                    "messages": [
                        {
                            "role": "system",
                            "content": "Você é um assistente especializado em criar resumos sofisticados e concisos em Português Brasileiro. Sempre respeite o limite de caracteres solicitado."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "max_tokens": 200,  # Reduced to ensure we stay within 500 chars
                    "temperature": 0.3,  # Lower temperature for more focused output
                    "top_p": 0.9,
                    "return_citations": False,
                    "search_domain_filter": [],
                    "return_images": False,
                    "return_related_questions": False,
                    "search_recency_filter": "month",
                    "top_k": 0,
                    "stream": False,
                    "presence_penalty": 0,
                    "frequency_penalty": 1
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
                    print(f"   ✅ Resumo gerado com sucesso pela Perplexity!")
                    return summary, None
                else:
                    error_msg = "Resposta vazia da API"
                    print(f"   ⚠️ {error_msg}")
                    if attempt < max_retries - 1:
                        import time
                        time.sleep(retry_delay * (attempt + 1))
                        continue
                    return None, error_msg
                
            except requests.exceptions.HTTPError as e:
                error_msg = f"HTTP {e.response.status_code}: {e.response.text[:200]}"
                print(f"   ⚠️ Falha na tentativa {attempt + 1}: {error_msg}")
                
                if attempt < max_retries - 1:
                    import time
                    time.sleep(retry_delay * (attempt + 1))
                    continue
                else:
                    return None, f"Todas as tentativas falharam. Último erro: {error_msg}"
                    
            except Exception as e:
                error_msg = str(e)
                print(f"   ⚠️ Falha na tentativa {attempt + 1}: {error_msg}")
                
                if attempt < max_retries - 1:
                    import time
                    time.sleep(retry_delay * (attempt + 1))
                    continue
                else:
                    return None, f"Todas as tentativas falharam. Último erro: {error_msg}"
        
        return None, "Número máximo de tentativas excedido"
    
    def generate_summary_gemini(self, article, content):
        """Generate a Portuguese summary using Gemini AI with retry logic"""
        if not self.gemini_api_key:
            return None, "API Key não configurada"
        
        # Use only the most stable model
        model_name = 'gemini-pro'
        
        # Create prompt
        prompt = f"""Você é um especialista em filosofia e cultura. 
Analise o texto abaixo e faça o seguinte:
1. Gere um resumo explicativo em Português Brasileiro com EXATAMENTE 500 caracteres ou menos.
2. Mantenha o tom sofisticado mas acessível.
3. Seja conciso e direto.

Título: {article['title']}
Fonte: {article['source']}

Texto base:
{content}

Resumo em Português (máximo 500 caracteres):"""

        # Retry logic with exponential backoff
        max_retries = 3
        retry_delay = 1  # seconds
        
        for attempt in range(max_retries):
            try:
                print(f"   🤖 Tentando gerar resumo com Gemini ({model_name}) - Tentativa {attempt + 1}/{max_retries}...")
                
                model = genai.GenerativeModel(model_name)
                
                # Configure generation with safety settings
                generation_config = {
                    'temperature': 0.7,
                    'top_p': 0.8,
                    'top_k': 40,
                    'max_output_tokens': 600,
                }
                
                response = model.generate_content(
                    prompt,
                    generation_config=generation_config
                )
                
                if response and response.text:
                    print(f"   ✅ Resumo gerado com sucesso!")
                    return response.text, None
                else:
                    error_msg = "Resposta vazia do modelo"
                    print(f"   ⚠️ {error_msg}")
                    if attempt < max_retries - 1:
                        import time
                        time.sleep(retry_delay * (attempt + 1))
                        continue
                    return None, error_msg
                    
            except Exception as e:
                error_msg = str(e)
                print(f"   ⚠️ Falha na tentativa {attempt + 1}: {error_msg}")
                
                if attempt < max_retries - 1:
                    import time
                    time.sleep(retry_delay * (attempt + 1))
                    continue
                else:
                    return None, f"Todas as tentativas falharam. Último erro: {error_msg}"
        
        return None, "Número máximo de tentativas excedido"
    
    def generate_summary(self, article):
        """Generate a Portuguese summary using AI (Perplexity or Gemini) with fallback"""
        # Try to fetch full article content
        content = self.fetch_article_content(article['link'])
        
        # If fetch fails, use the RSS summary as context
        if not content:
            print(f"   ⚠️ Falha ao ler artigo completo. Usando resumo do RSS para gerar IA.")
            content = article.get('summary', '')

        if not content:
            return "Conteúdo não disponível para resumo."
        
        # Try Perplexity first
        summary, perp_error = self.generate_summary_perplexity(article, content)
        if summary:
            # Enforce 500 character limit
            if len(summary) > 500:
                summary = summary[:497] + "..."
            return summary
        
        # Try Gemini as fallback
        summary, gemini_error = self.generate_summary_gemini(article, content)
        if summary:
            # Enforce 500 character limit
            if len(summary) > 500:
                summary = summary[:497] + "..."
            return summary
        
        # If all AI methods fail, return the original summary from NewsAPI/RSS
        # This is a "graceful degradation" - better to have a simple summary than an error message
        original_summary = article.get('summary', 'Sem resumo disponível')
        
        # Enforce 500 character limit on original summary too
        if len(original_summary) > 500:
            original_summary = original_summary[:497] + "..."
        
        # Add a small footer indicating AI failed, but keep it clean
        footer = "\n\n_(Resumo original da fonte - IA indisponível)_"
        
        # Log the detailed errors for debugging, but don't show them to the end user in the main text
        print(f"   ⚠️ Falha na geração de IA para '{article['title']}':")
        if perp_error:
            print(f"      - Perplexity: {perp_error}")
        if gemini_error:
            print(f"      - Gemini: {gemini_error}")
            
        return f"{original_summary}{footer}"

    def fetch_from_newsapi(self, keywords):
        """Fetch articles using NewsAPI"""
        if not self.news_api_key:
            return []
            
        print(f"   📡 Buscando na NewsAPI por: {keywords}")
        url = "https://newsapi.org/v2/everything"
        
        params = {
            'q': keywords,
            'language': 'en', # Most high quality sources are in English
            'sortBy': 'popularity',
            'pageSize': 20,
            'apiKey': self.news_api_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            articles = []
            for item in data.get('articles', []):
                # Skip removed articles
                if item['title'] == '[Removed]':
                    continue
                    
                articles.append({
                    "title": item['title'],
                    "link": item['url'],
                    "source": item['source']['name'],
                    "summary": item['description'] or "No description"
                })
            
            return articles
        except Exception as e:
            print(f"   ⚠️ Erro na NewsAPI: {e}")
            return []

    def collect_data(self):
        # Get current day of week (0=Monday, 6=Sunday)
        today = datetime.now(self.tz_BR).weekday()
        day_config = WEEKLY_FEEDS[today]
        
        print(f"📅 Tema de hoje: {day_config['theme']}")
        all_entries = []
        
        # NewsAPI is now mandatory/primary
        if self.news_api_key and 'keywords' in day_config:
            print("📡 Usando NewsAPI para busca...")
            api_entries = self.fetch_from_newsapi(day_config['keywords'])
            all_entries.extend(api_entries)
        else:
            print("⚠️ NewsAPI Key não configurada ou keywords ausentes. Configure a NEWS_API_KEY para buscar artigos.")

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
    perplexity_api_key = os.environ.get('PERPLEXITY_API_KEY')
    news_api_key = os.environ.get('NEWS_API_KEY')
    reporter = DailyReporter(webhook_url, gemini_api_key, perplexity_api_key, news_api_key)
    reporter.send()
