# Deploy Instructions

## Via GitHub (Recomendado)

1. Upload arquivos para GitHub:
   - Criar repositório `3dcal-web`
   - Fazer upload de todos os arquivos

2. Deploy no Vercel:
   - Acessar vercel.com
   - Login com GitHub
   - New Project → Importar `3dcal-web`
   - Deploy automático

3. Configurar domínio:
   - Settings → Domains
   - Adicionar `calcular3d.com`

## Via CLI (Após reiniciar terminal)

```bash
# Navegar para pasta
cd "c:\Users\jpbri\OneDrive\Área de Trabalho\projetos_python\3dcal-web"

# Iniciar Git
git init
git add .
git commit -m "Initial commit"

# Login no Vercel
vercel login

# Deploy
vercel --prod

# Configurar domínio
vercel domains add calcular3d.com
```

## Arquivos Criados

- app.py (Flask backend)
- index.py (Handler Vercel)
- templates/index.html (Frontend)
- requirements.txt (Dependências)
- vercel.json (Config Vercel)
- README.md (Documentação)
