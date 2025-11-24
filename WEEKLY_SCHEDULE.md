# 📅 Calendário Temático Semanal

## 🎯 Visão Geral

O bot agora funciona com um **calendário temático semanal**, enviando conteúdo diferente para cada dia da semana!

---

## 📆 Programação Semanal

### 🧠 Segunda-feira - Filosofia
**Fontes:**
- Daily Nous
- Aeon
- Stanford Encyclopedia of Philosophy
- Philosophy Now
- Leiter Reports
- Philosophy Bites
- The Conversation - Philosophy

**Temas típicos:**
- Epistemologia
- Ética e Moral
- Filosofia Política
- Metafísica
- Lógica e Filosofia da Ciência

---

### 💰 Terça-feira - Finanças & Hedge Funds
**Fontes:**
- Financial Times
- Bloomberg
- Hedge Week
- Institutional Investor
- Investopedia
- Seeking Alpha
- MarketWatch

**Temas típicos:**
- Estratégias de investimento
- Análise de mercado
- Hedge funds e private equity
- Economia global
- Criptomoedas e fintech

---

### 👥 Quarta-feira - Ciências Sociais
**Fontes:**
- The Conversation - Sociology
- Science Daily - Psychology
- Taylor & Francis - Social Sciences
- SAGE Journals
- Anthropology News
- LSE Blogs

**Temas típicos:**
- Sociologia
- Psicologia
- Antropologia
- Estudos culturais
- Comportamento humano

---

### 🍽️ Quinta-feira - Alta Gastronomia & Culinária
**Fontes:**
- Serious Eats
- Bon Appétit
- Saveur
- Food & Wine
- The World's 50 Best
- Eater
- Fine Dining Lovers

**Temas típicos:**
- Técnicas culinárias
- Restaurantes estrelados
- Tendências gastronômicas
- Ingredientes e produtos
- Chefs e suas histórias

---

### 🔬 Sexta-feira - Ciência em Geral
**Fontes:**
- Nature
- Science Magazine
- Science Daily
- New Scientist
- Scientific American
- Phys.org
- Space.com

**Temas típicos:**
- Descobertas científicas
- Física e astronomia
- Biologia e medicina
- Tecnologia e inovação
- Meio ambiente

---

### 🌍 Sábado - Tópicos Diversos
**Fontes:**
- The Guardian
- BBC News
- The Atlantic
- The New Yorker
- Wired
- Aeon
- Vox

**Temas típicos:**
- Atualidades globais
- Política internacional
- Tecnologia e sociedade
- Reportagens investigativas
- Ensaios longos

---

### 🎨 Domingo - Arte, Cultura & Diversos
**Fontes:**
- Artforum
- Hyperallergic
- The Paris Review
- Literary Hub
- Smithsonian Magazine
- NPR Arts
- TED Talks

**Temas típicos:**
- Artes visuais
- Literatura
- Cultura pop
- História da arte
- Crítica cultural

---

## 🔧 Personalização

### Como adicionar novos feeds

Edite o arquivo `script.py` e localize o dicionário `WEEKLY_FEEDS`. Exemplo:

```python
WEEKLY_FEEDS = {
    0: {  # Segunda-feira
        "theme": "🧠 Filosofia",
        "emoji": "🧠",
        "feeds": [
            "https://seu-novo-feed.com/rss",
            # ... outros feeds
        ]
    },
    # ... outros dias
}
```

### Como mudar o tema de um dia

Basta editar o `theme` e `emoji` do dia desejado:

```python
1: {  # Terça-feira
    "theme": "💼 Negócios & Empreendedorismo",  # Novo tema
    "emoji": "💼",  # Novo emoji
    "feeds": [
        # Seus feeds aqui
    ]
}
```

### Como mudar a quantidade de artigos

No método `collect_data()`, linha ~237:

```python
# Atualmente: 2 artigos
selected = random.sample(new_entries, min(2, len(new_entries)))

# Para 5 artigos:
selected = random.sample(new_entries, min(5, len(new_entries)))
```

---

## 📊 Estatísticas

Com a configuração atual:
- **7 temas diferentes** por semana
- **~7 fontes** por tema
- **2 artigos** selecionados por dia
- **14 artigos** por semana
- **~60 artigos** por mês

---

## 🎨 Exemplo de Mensagem

```
🧠 Curadoria Diária: Filosofia
📅 23/11/2025 22:50:00 | Resumos gerados por IA 🤖
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📖 O Pragmatismo Filosófico Americano
Philosophy Bites

🤖 Resumo gerado por IA:

O pragmatismo é uma corrente filosófica americana que surgiu 
no final do século XIX, tendo como principais representantes 
Charles Sanders Peirce, William James e John Dewey...

[Conceitos principais]
[Relevância do tema]
```

---

## 🔄 Testando Diferentes Dias

Para testar como ficaria em um dia específico, você pode modificar temporariamente o código:

```python
# No método collect_data(), substitua:
today = datetime.now(self.tz_BR).weekday()

# Por (exemplo para testar quinta-feira):
today = 3  # 0=Seg, 1=Ter, 2=Qua, 3=Qui, etc.
```

---

## 💡 Dicas

1. **Variedade**: Mantenha pelo menos 5-7 fontes por tema para garantir conteúdo diversificado
2. **Qualidade**: Priorize fontes confiáveis e bem estabelecidas
3. **Atualização**: Alguns feeds podem ficar inativos - revise periodicamente
4. **Idioma**: O Gemini traduzirá automaticamente para PT-BR, mas fontes em português são sempre bem-vindas!

---

## 🆘 Problemas Comuns

### "Nenhum artigo novo encontrado"
- Alguns feeds podem não ter atualizações diárias
- O histórico pode já conter todos os artigos recentes
- Solução: Adicione mais fontes ou limpe o `history.json`

### Feeds que não funcionam
- Alguns sites bloqueiam scrapers
- Feeds podem mudar de URL
- Solução: Teste os feeds manualmente e substitua os que não funcionam

### Temas repetitivos
- Adicione mais variedade de fontes
- Aumente o número de artigos selecionados
- Considere adicionar filtros por palavras-chave

---

**Aproveite sua curadoria temática semanal!** 🎉
