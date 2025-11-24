# Como Configurar o Webhook do Slack

Para que o script possa enviar mensagens para o seu Slack, você precisa criar um "Incoming Webhook". Siga os passos abaixo:

1. **Acesse seus Apps do Slack**:
   - Vá para [api.slack.com/apps](https://api.slack.com/apps).
   - Clique em **"Create New App"**.
   - Escolha **"From scratch"**.
   - Dê um nome ao App (ex: "Notificações Diárias") e selecione o Workspace onde você quer receber as mensagens.

2. **Ative os Webhooks**:
   - No menu lateral esquerdo, clique em **"Incoming Webhooks"**.
   - Mude a chave "Activate Incoming Webhooks" para **"On"**.

3. **Crie o Webhook**:
   - Role a página até o final e clique no botão **"Add New Webhook to Workspace"**.
   - O Slack vai pedir permissão para acessar o seu Workspace. Escolha o **canal** (channel) onde você quer que as mensagens sejam postadas (ex: `#geral` ou um canal privado para você).
   - Clique em **"Allow"**.

4. **Copie a URL**:
   - Você será redirecionado de volta para a página de configurações.
   - Procure pela tabela "Webhook URLs for Your Workspace".
   - Copie a URL que começa com `https://hooks.slack.com/services/...`. **Essa é a sua chave secreta!**

5. **Adicione ao GitHub**:
   - Vá para o seu repositório no GitHub.
   - Clique em **Settings** (Configurações) > **Secrets and variables** > **Actions**.
   - Clique em **"New repository secret"**.
   - **Name**: `SLACK_WEBHOOK_URL`
   - **Secret**: Cole a URL que você copiou do Slack.
   - Clique em **"Add secret"**.

Pronto! Agora o GitHub Actions terá permissão para enviar mensagens para o seu Slack.
