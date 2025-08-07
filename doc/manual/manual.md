### Pré-requisitos

Antes de iniciar, certifique-se de ter instalado:

* [Docker](https://docs.docker.com/get-docker/)

---

### Passo a Passo

1. **Suba os containers (com build inicial)**

   ```bash
   docker compose up --build
   ```

   > Isso criará e iniciará os serviços `pulso-web` e `pulso-db`, conforme definidos no `docker-compose.yml`.


2. **Carregue os dados de teste**

   para dados de teste, carregue com:

   ```bash
   docker exec pulso-web python manage.py loaddata db.json
   ```

   > so irá popular o banco de dados com informações iniciais, como usuários fictícios, escalas e plantões, permitindo que você explore e utilize o sistema normalmente, mesmo sem cadastrar nada manualmente.

   #### 👤 Usuários disponíveis para login:

   - **Gestor**
   - Usuário: `Demostenes`
   - Senha: `manager123`
   - **Médicos**
   - Usuários: `Icaro`, `Flavio`, `George`, `Asaph`, `Gustavo`
   - Senha comum: `doctor123`

3. **Acesse o sistema via navegador**

   * [http://localhost:8000](http://localhost:8000)

---

###  Parar e remover os containers

```bash
docker compose down
```

> Isso encerra os containers e mantém os dados do banco (persistentes via volume `pgdata`).
