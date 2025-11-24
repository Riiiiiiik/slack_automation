# 🤖 Configuração da Integração com Google Gemini

## 📋 Visão Geral

O script agora usa a **API do Google Gemini** para:
- ✅ Extrair o conteúdo completo dos artigos
- ✅ Gerar resumos inteligentes em **Português Brasileiro**
- ✅ Identificar conceitos filosóficos principais
- ✅ Explicar a relevância do tema

## 🔑 Como Obter sua API Key do Gemini

### Passo 1: Acesse o Google AI Studio
1. Vá para: https://aistudio.google.com/app/apikey
2. Faça login com sua conta Google
3. Clique em **"Create API Key"**
4. Copie a chave gerada

### Passo 2: Adicionar a API Key no GitHub

1. Acesse: https://github.com/Riiiiiiik/slack_automation/settings/secrets/actions
2. Clique em **"New repository secret"**
3. Nome: `GEMINI_API_KEY`
4. Value: Cole a API key que você copiou
5. Clique em **"Add secret"**

## 🧪 Testar Localmente

Para testar o script localmente com o Gemini:

### Windows (PowerShell):
```powershell
# Instalar dependências
pip install beautifulsoup4 google-generativeai

# Configurar variáveis de ambiente
$env:GEMINI_API_KEY="sua-api-key-aqui"
$env:SLACK_WEBHOOK_URL="seu-webhook-url-aqui"

# Executar o script
python script.py
```

### Linux/Mac:
```bash
# Instalar dependências
pip install beautifulsoup4 google-generativeai

# Configurar variáveis de ambiente
export GEMINI_API_KEY="sua-api-key-aqui"
export SLACK_WEBHOOK_URL="seu-webhook-url-aqui"

# Executar o script
python script.py
```

## 📊 O que mudou?

### Antes:
- Enviava apenas o snippet do RSS feed (200 caracteres)
- Conteúdo em inglês
- Informação superficial

### Agora:
- 🤖 **Resumo completo gerado por IA**
- 🇧🇷 **Traduzido para Português Brasileiro**
- 📚 **Conceitos filosóficos explicados**
- 💡 **Relevância do tema destacada**

## 🎯 Exemplo de Resumo Gerado

**Antes:**
```
In this episode of the Philosophy Bites podcast Robert B. Talisse in discussion with Nigel Warburton explains what the philosphical movement of Pragmatism was, and some of the differences between t...
```

**Agora:**
```
🤖 Resumo gerado por IA:

O pragmatismo é uma corrente filosófica americana que surgiu no final do século XIX, 
tendo como principais representantes Charles Sanders Peirce, William James e John Dewey. 
Esta filosofia propõe que o significado de uma ideia está nas suas consequências práticas 
e na sua utilidade para resolver problemas concretos.

Principais conceitos:
- Verdade pragmática: uma ideia é verdadeira se funciona na prática
- Método científico aplicado à filosofia
- Foco na experiência e na ação

Relevância: O pragmatismo continua influente hoje, especialmente em debates sobre 
democracia, educação e ética aplicada.
```

## ⚙️ Configurações Avançadas

### Ajustar o modelo do Gemini
No arquivo `script.py`, linha 33:
```python
self.model = genai.GenerativeModel('gemini-1.5-flash')  # Rápido e eficiente
# ou
self.model = genai.GenerativeModel('gemini-1.5-pro')    # Mais poderoso
```

### Ajustar o tamanho do conteúdo extraído
No arquivo `script.py`, linha 79:
```python
return text[:3000]  # Aumentar para mais contexto (cuidado com limites de tokens)
```

## 💰 Custos

A API do Google Gemini tem um **tier gratuito generoso**:
- **Gemini 1.5 Flash**: 15 requisições por minuto (grátis)
- **Gemini 1.5 Pro**: 2 requisições por minuto (grátis)

Para 2 artigos por dia, você ficará **bem dentro do limite gratuito**! 🎉

## 🔒 Segurança

- ✅ A API key é armazenada como **Secret** no GitHub
- ✅ Nunca é exposta nos logs
- ✅ Não é commitada no código

## 🆘 Troubleshooting

### "Gemini API key não fornecida"
- Verifique se adicionou o secret `GEMINI_API_KEY` no GitHub
- Ou configure a variável de ambiente localmente

### "Erro ao gerar resumo com Gemini"
- Verifique se sua API key é válida
- Verifique se não excedeu o limite de requisições
- Verifique sua conexão com a internet

### "Erro ao buscar conteúdo"
- Alguns sites bloqueiam web scraping
- O script continuará funcionando com o resumo básico do RSS

## 📚 Recursos

- [Google AI Studio](https://aistudio.google.com/)
- [Documentação Gemini API](https://ai.google.dev/docs)
- [Limites e Quotas](https://ai.google.dev/pricing)
