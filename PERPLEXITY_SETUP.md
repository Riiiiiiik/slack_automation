# 🔮 Configuração da API Perplexity

A Perplexity AI é uma plataforma de IA avançada que combina modelos de linguagem com busca em tempo real, oferecendo resumos contextualizados e de alta qualidade.

## Por que usar a Perplexity?

- 🌐 **Acesso à web em tempo real**: Pode buscar informações atualizadas durante a geração
- 🎯 **Resumos contextualizados**: Excelente para sintetizar artigos complexos
- 💡 **Alta qualidade**: Usa modelos Llama 3.1 otimizados para tarefas de pesquisa
- 🔄 **Fallback automático**: Se falhar, o sistema usa o Gemini automaticamente

## Como obter sua API Key

### Passo 1: Criar uma conta
1. Acesse: https://www.perplexity.ai/
2. Clique em **Sign Up** no canto superior direito
3. Crie sua conta usando email, Google ou GitHub

### Passo 2: Acessar configurações de API
1. Faça login na sua conta
2. Acesse: https://www.perplexity.ai/settings/api
3. Você verá a seção **API Keys**

### Passo 3: Gerar uma API Key
1. Clique em **Generate API Key** ou **Create New Key**
2. Dê um nome descritivo para sua chave (ex: "Slack Bot")
3. Copie a chave gerada imediatamente
   - ⚠️ **IMPORTANTE**: A chave só será mostrada uma vez!
   - Se perder, você precisará gerar uma nova

### Passo 4: Configurar no GitHub
1. Vá para o seu repositório no GitHub
2. Clique em **Settings** > **Secrets and variables** > **Actions**
3. Clique em **New repository secret**
4. **Name**: `PERPLEXITY_API_KEY`
5. **Secret**: Cole a API key que você copiou
6. Clique em **Add secret**

## 💰 Planos e Preços

A Perplexity oferece diferentes planos:

- **Free Tier**: Inclui créditos gratuitos para testes
- **Pay-as-you-go**: Pague apenas pelo que usar
- **Pro**: Planos mensais com uso ilimitado

Para este bot que roda uma vez por dia com 2 artigos, o uso é muito baixo e pode funcionar perfeitamente no plano gratuito ou com custo mínimo no pay-as-you-go.

### Estimativa de custo
- **Modelo usado**: `llama-3.1-sonar-small-128k-online`
- **Uso diário**: ~2 requisições
- **Custo aproximado**: < $0.01 por dia

## 🔧 Modelos Disponíveis

O bot usa por padrão o modelo `llama-3.1-sonar-small-128k-online`, que oferece:
- ✅ Ótima relação custo-benefício
- ✅ Acesso à web em tempo real
- ✅ Contexto de até 128k tokens
- ✅ Respostas rápidas e precisas

Outros modelos disponíveis:
- `llama-3.1-sonar-large-128k-online` - Mais poderoso, mais caro
- `llama-3.1-sonar-huge-128k-online` - Máxima qualidade, maior custo

## 🆚 Perplexity vs Gemini

| Característica | Perplexity | Gemini |
|----------------|------------|--------|
| Acesso à web | ✅ Sim, em tempo real | ❌ Não |
| Custo | $ Pay-as-you-go | 🆓 Grátis (com limites) |
| Qualidade | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Velocidade | Rápido | Muito rápido |
| Contexto | Até 128k tokens | Até 1M tokens |

## 🔐 Segurança

- ✅ Nunca compartilhe sua API key publicamente
- ✅ Use GitHub Secrets para armazenar a chave
- ✅ Monitore o uso através do dashboard da Perplexity
- ✅ Revogue e recrie chaves se suspeitar de comprometimento

## 📚 Recursos Adicionais

- 📖 [Documentação oficial da API](https://docs.perplexity.ai/)
- 💬 [Discord da Perplexity](https://discord.gg/perplexity)
- 📊 [Dashboard de uso](https://www.perplexity.ai/settings/api)

## ❓ Problemas Comuns

### "Invalid API Key"
- Verifique se copiou a chave completa
- Confirme que a chave está ativa no dashboard
- Recrie a chave se necessário

### "Rate limit exceeded"
- Você excedeu o limite de requisições
- Aguarde alguns minutos ou upgrade seu plano
- O bot tem fallback automático para Gemini

### "Insufficient credits"
- Adicione créditos na sua conta
- Configure um método de pagamento
- O bot usará Gemini como fallback

## 🎯 Conclusão

A Perplexity é opcional mas **altamente recomendada** para obter os melhores resumos possíveis. O sistema foi projetado com fallback automático, então mesmo se a Perplexity falhar, o bot continuará funcionando com o Gemini.
