## 🌿 Fluxo de Contribuição

> ⚠️ **Importante:** Nunca faça alterações diretamente na branch `main`. 
> Sempre crie uma branch separada para suas contribuições.

1. Faça um fork do repositório no GitHub clicando em **Fork** no canto superior direito

2. Clone o seu fork
```bash
git clone https://github.com/SEU-USUARIO/descarte-certo.git
cd descarte-certo
```

3. Adicione o repositório original como remote
```bash
git remote add upstream https://github.com/Joseefreitas/descarte-certo.git
```

4. Crie uma branch para sua feature
```bash
git checkout -b feat/nome-da-feature
```

5. Faça suas alterações e commit
```bash
git add .
git commit -m "feat: descrição da sua alteração"
```

6. Atualize com o repositório original antes de subir
```bash
git pull upstream main --no-rebase
git push origin feat/nome-da-feature
```

7. Abra um **Pull Request** no GitHub apontando para a branch `main` do repositório original

8. Aguarde a revisão do time antes do merge