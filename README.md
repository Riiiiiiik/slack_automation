# 🧠 Automação Diária de Filosofia para Slack

Este projeto é uma automação que roda todos os dias às **07:30 (Horário de Brasília)**, busca artigos de filosofia em diversas fontes internacionais, e envia 2 destaques para o seu Slack.

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

### Passo 4: Configurar o Segredo (Secret)
Para que o GitHub Actions consiga enviar mensagens, ele precisa daquela URL do Slack. Por segurança, não colocamos ela no código.

1. No seu repositório no GitHub, vá em **Settings** (aba superior).
2. No menu lateral esquerdo, clique em **Secrets and variables** > **Actions**.
3. Clique no botão verde **New repository secret**.
4. **Name**: `SLACK_WEBHOOK_URL`
5. **Secret**: Cole a URL do Webhook do Slack (aquela do Passo 1).
6. Clique em **Add secret**.

### ✅ Pronto!
A automação já está configurada.
- Ela vai rodar automaticamente todo dia às 07:30 BRT.
- Se quiser testar agora, vá na aba **Actions**, selecione **Daily Slack Notification** e clique em **Run workflow**.

## 📂 Estrutura do Projeto
- `.github/workflows/daily_slack.yml`: O agendamento da automação.
- `script.py`: O código Python que busca as notícias e envia.
- `history.json`: Arquivo que guarda o histórico para não repetir notícias (atualizado automaticamente).
- `slack_setup_guide.md`: Guia para criar o Webhook.
