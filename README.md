# 🧠 Curadoria Temática Semanal com IA 🤖

Este projeto é uma automação que roda todos os dias às **07:30 (Horário de Brasília)**, busca artigos sobre **temas diferentes para cada dia da semana**, **usa IA (Perplexity ou Google Gemini) para gerar resumos em português**, e envia 2 destaques para o seu Slack.

## 📅 Calendário Semanal

Cada dia da semana tem um tema diferente:
- 🧠 **Segunda**: Filosofia
- 💰 **Terça**: Finanças & Hedge Funds
- 👥 **Quarta**: Ciências Sociais
- 🍽️ **Quinta**: Alta Gastronomia & Culinária
- 🔬 **Sexta**: Ciência em Geral
- 🌍 **Sábado**: Tópicos Diversos
- 🎨 **Domingo**: Arte, Cultura & Diversos

📖 **[Ver programação completa e fontes](WEEKLY_SCHEDULE.md)**

## ✨ Recursos Principais

### 🤖 Resumos Gerados por IA
O bot não envia apenas snippets dos feeds RSS. Ele:
- 📖 Lê o artigo completo
- 🔮 Usa **Perplexity AI** (preferencial) ou **Google Gemini** (fallback) para gerar resumos inteligentes
- 🇧🇷 Traduz e adapta para Português Brasileiro
- 💡 Destaca os conceitos principais de cada tema
- 🔄 Sistema de fallback automático entre APIs para máxima confiabilidade

## 🚀 Como colocar no ar

### Passo 1: Configurar o Slack
Você precisa gerar um link de Webhook para o seu Slack.
📄 **[Clique aqui para ver o guia passo-a-passo](slack_setup_guide.md)**.

Ao final, você terá uma URL parecida com: `https://hooks.slack.com/services/T00000/B00000/XXXXX`.

### Passo 2: Criar o Repositório no GitHub
1. Acesse [github.com/new](https://github.com/new).
2. Dê um nome para o repositório (ex: `daily-philosophy`).
3. Pode ser **Público** ou **Privado**.
4. **Não** marque a opção de adicionar README ou .gitignore (já criamos aqui).
5. Clique em **Create repository**.

### Passo 3: Enviar o código
Abra o terminal na pasta deste projeto e rode os comandos que o GitHub vai te mostrar (na seção "...or push an existing repository from the command line"):

```bash
git remote add origin https://github.com/SEU_USUARIO/daily-philosophy.git
git branch -M main
git push -u origin main
```

*(Substitua `SEU_USUARIO` pelo seu nome de usuário do GitHub)*

### Passo 4: Configurar os Segredos (Secrets)
Para que o GitHub Actions consiga enviar mensagens e gerar resumos com IA, você precisa configurar os seguintes secrets:

#### 4.1 - SLACK_WEBHOOK_URL (Obrigatório)
1. No seu repositório no GitHub, vá em **Settings** (aba superior).
2. No menu lateral esquerdo, clique em **Secrets and variables** > **Actions**.
3. Clique no botão verde **New repository secret**.
4. **Name**: `SLACK_WEBHOOK_URL`
5. **Secret**: Cole a URL do Webhook do Slack (aquela do Passo 1).
6. Clique em **Add secret**.

#### 4.2 - PERPLEXITY_API_KEY (Opcional - Recomendado)
A Perplexity AI é usada preferencialmente para gerar resumos de alta qualidade:
1. Acesse: https://www.perplexity.ai/settings/api
2. Faça login e crie uma API key
3. Copie a chave gerada
4. No GitHub, clique em **New repository secret**
5. **Name**: `PERPLEXITY_API_KEY`
6. **Secret**: Cole a API key da Perplexity
7. Clique em **Add secret**

#### 4.3 - GEMINI_API_KEY (Opcional - Fallback)
O Gemini é usado como fallback caso a Perplexity não esteja configurada ou falhe:
1. Acesse: https://aistudio.google.com/app/apikey
2. Faça login com sua conta Google
3. Clique em **"Create API Key"** e copie a chave
4. Volte para o GitHub, clique em **New repository secret** novamente
5. **Name**: `GEMINI_API_KEY`
6. **Secret**: Cole a API key do Gemini
7. Clique em **Add secret**

> **💡 Dica**: Configure pelo menos uma das APIs de IA (Perplexity ou Gemini) para obter resumos inteligentes. Se nenhuma estiver configurada, o bot enviará apenas os resumos originais do RSS.

📖 **[Guia completo de configuração da Perplexity](PERPLEXITY_SETUP.md)**  
📖 **[Guia completo de configuração do Gemini](GEMINI_SETUP.md)**

### ✅ Pronto!
A automação já está configurada.
- Ela vai rodar automaticamente todo dia às 07:30 BRT.
- Se quiser testar agora, vá na aba **Actions**, selecione **Daily Slack Notification** e clique em **Run workflow**.

## 📂 Estrutura do Projeto
- `.github/workflows/daily_slack.yml`: O agendamento da automação.
- `script.py`: O código Python que busca as notícias e envia.
- `history.json`: Arquivo que guarda o histórico para não repetir notícias (atualizado automaticamente).
- `slack_setup_guide.md`: Guia para criar o Webhook.
