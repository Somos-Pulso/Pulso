# Modelo de Dados

## Diagrama ER
<img width="1561" height="1201" alt="diagrama-er" src="https://github.com/user-attachments/assets/0da2c1c6-d609-42b6-8d4c-462721ae9873" />

## Diagrama ER Intermediário

<img width="1727" height="1241" alt="diagrama-er-intermediario (1)" src="https://github.com/user-attachments/assets/e4276237-66af-420b-bf80-d8064ecf4088" />


## Modelo Relacional
<img width="1155" height="598" alt="image" src="https://github.com/user-attachments/assets/4ac5195a-40a2-4aef-9926-92df9b5e1c92" />



## Dicionário de Dados

---

### Tabela : Profissional

**Descrição** : Representa indivíduos que atuam como profissionais de saúde cadastrados no sistema, sendo uma entidade genérica.

| Colunas      | Descrição                                  | Tipo de Dado | Tamanho | Null | PK | FK | Unique | Identity | Default | Check    |
| ------------ | ------------------------------------------ | ------------ | ------- | ---- | -- | -- | ------ | -------- | ------- | -------- |
| id           | Identificador único do profissional        | \[int]       |         | ☐    | ☑  | ☐  | ☐      | ☑        |         | Not null |
| cpf          | Cadastro de pessoa física                  | \[char]      | 11      | ☐    | ☐  | ☐  | ☑      | ☐        |         | Not null |
| telefone     | Número do telefone principal               | \[varchar]   | 11      | ☐    | ☐  | ☐  | ☐      | ☐        |         | Not null |
| descrição    | Informação adicional sobre o profissional  | \[text]      |         | ☑    | ☐  | ☐  | ☐      | ☐        |         |          |
| foto\_perfil | URL da Foto de apresentação do profissional| \[varchar]   | 255     | ☑    | ☐  | ☐  | ☐      | ☐        |         |          |

---

### Tabela : Gestor

**Descrição** : Identifica profissionais com função de gestão. Cada gestor é um profissional.

| Colunas          | Descrição                                    | Tipo de Dado | Tamanho | Null | PK | FK | Unique | Identity | Default | Check    |
| ---------------- | -------------------------------------------- | ------------ | ------- | ---- | -- | -- | ------ | -------- | ------- | -------- |
| id               | Identificador único do gestor                | \[int]       |         | ☐    | ☑  | ☐  | ☐      | ☑        |         | Not null |
| id\_profissional | Chave estrangeira referenciando Profissional | \[int]       |         | ☐    | ☐  | ☑  | ☑      | ☐        |         | Not null |

---

### Tabela : Médico

**Descrição** : Representa profissionais com registro de médico.

| Colunas          | Descrição                                            | Tipo de Dado | Tamanho | Null | PK | FK | Unique | Identity | Default | Check    |
| ---------------- | ---------------------------------------------------- | ------------ | ------- | ---- | -- | -- | ------ | -------- | ------- | -------- |
| id               | Identificador único do médico                        | \[int]       |         | ☐    | ☑  | ☐  | ☐      | ☑        |         | Not null |
| CRM              | Registro no conselho regional de medicina            | \[varchar]   | 20      | ☐    | ☐  | ☐  | ☑      | ☐        |         | Not null |
| carga\_horaria   | Carga horária semanal atribuída ao médico (em horas) | \[int]       |         | ☐    | ☐  | ☐  | ☐      | ☐        |         | Not null |
| id\_profissional | Chave estrangeira referenciando Profissional         | \[int]       |         | ☐    | ☐  | ☑  | ☑      | ☐        |         | Not null |

---

### Tabela : Disponibilidade

**Descrição** : Agenda de disponibilidade de cada médico (dia e turno).

| Colunas    | Descrição                                    | Tipo de Dado | Tamanho | Null | PK | FK | Unique | Identity | Default | Check                                                                   |
| ---------- | -------------------------------------------- | ------------ | ------- | ---- | -- | -- | ------ | -------- | ------- | ----------------------------------------------------------------------- |
| id         | Identificador único da disponibilidade       | \[int]       |         | ☐    | ☑  | ☐  | ☐      | ☑        |         | Not null                                                                |
| dia        | Dia específico que o médico está disponível  | \[varchar]   | 10      | ☐    | ☐  | ☐  | ☐      | ☐        |         | dia IN ('segunda','terça','quarta','quinta','sexta','sábado','domingo') |
| turno      | Turno do dia em que o médico está disponível | \[varchar]   | 20      | ☐    | ☐  | ☐  | ☐      | ☐        |         | turno IN ('manhã','tarde','noite')                                      |
| id\_medico | Chave estrangeira referenciando Médico       | \[int]       |         | ☐    | ☐  | ☑  | ☐      | ☐        |         | Not null                                                                |

---

### Tabela : MédicoEspecialidade

**Descrição** : Associação entre médicos e especialidades.

| Colunas           | Descrição                                     | Tipo de Dado | Tamanho | Null | PK | FK | Unique | Identity | Default | Check    |
| ----------------- | --------------------------------------------- | ------------ | ------- | ---- | -- | -- | ------ | -------- | ------- | -------- |
| id                | Identificador único                           | \[int]       |         | ☐    | ☑  | ☐  | ☐      | ☑        |         | Not null |
| id\_medico        | Chave estrangeira referenciando Médico        | \[int]       |         | ☐    | ☐  | ☑  | ☑      | ☐        |         | Not null |
| id\_especialidade | Chave estrangeira referenciando Especialidade | \[int]       |         | ☐    | ☐  | ☑  | ☑      | ☐        |         | Not null |

---

### Tabela : Especialidade

**Descrição** : Armazena as especialidades médicas disponíveis.

| Colunas | Descrição                            | Tipo de Dado | Tamanho | Null | PK | FK | Unique | Identity | Default | Check    |
| ------- | ------------------------------------ | ------------ | ------- | ---- | -- | -- | ------ | -------- | ------- | -------- |
| id      | Identificador único da especialidade | \[int]       |         | ☐    | ☑  | ☐  | ☐      | ☑        |         | Not null |
| nome    | Nome da especialidade médica         | \[varchar]   | 100     | ☐    | ☐  | ☐  | ☑      | ☐        |         | Not null |

---

### Tabela : Setor

**Descrição** : Representa os setores da instituição.

| Colunas    | Descrição                              | Tipo de Dado | Tamanho | Null | PK | FK | Unique | Identity | Default | Check    |
| ---------- | -------------------------------------- | ------------ | ------- | ---- | -- | -- | ------ | -------- | ------- | -------- |
| id         | Identificador único do setor           | \[int]       |         | ☐    | ☑  | ☐  | ☐      | ☑        |         | Not null |
| nome       | Nome do setor                          | \[varchar]   | 100     | ☐    | ☐  | ☐  | ☑      | ☐        |         | Not null |
| ativo      | Indica se o setor está ativo           | \[boolean]   |         | ☐    | ☐  | ☐  | ☐      | ☐        |         | Not null |
| id\_gestor | Chave estrangeira referenciando Gestor | \[int]       |         | ☐    | ☐  | ☑  | ☐      | ☐        |         | Not null |

---

#### Tabela : SetorMedico

**Descrição**: Tabela de associação entre médicos e setores. Define quais médicos atuam em quais setores.

| Colunas    | Descrição                                   | Tipo de Dado  | Tamanho | Null | PK | FK | Unique | Identity | Default | Check    |
| ---------- | ------------------------------------------- | ------------- | ------- | ---- | -- | -- | ------ | -------- | ------- | -------- |
| id         | Identificador único da relação médico-setor | \[int]        |         | ☐    | ☑  | ☐  | ☐      | ☑        | —       | Not null |
| id\_setor  | Referência ao setor                         | \[int]        |         | ☐    | ☐  | ☑  | ☑      | ☐        | —       | Not null |
| id\_medico | Referência ao médico                        | \[int]        |         | ☐    | ☐  | ☑  | ☑      | ☐        | —       | Not null |


---

### Tabela : Escala

**Descrição** : Armazena o conjunto de plantões de um período e setor.

| Colunas      | Descrição                               | Tipo de Dado | Tamanho | Null | PK | FK | Unique | Identity | Default | Check                    |
| ------------ | --------------------------------------- | ------------ | ------- | ---- | -- | -- | ------ | -------- | ------- | ------------------------ |
| id             | Identificador único da escala         | \[int]       |         | ☐    | ☑  | ☐  | ☐      | ☑        |         | Not null                 |
| nome           | Nome da escala                        | \[varchar]   | 100     | ☐    | ☐  | ☐  | ☐      | ☐        |         | Not null                 |
| data\_inicio   | Data de início da escala              | \[date]      |         | ☐    | ☐  | ☐  | ☐      | ☐        |         | Not null                 |
| data\_fim      | Data de término da escala             | \[date]      |         | ☐    | ☐  | ☐  | ☐      | ☐        |         | data\_fim > data\_inicio |
| status         | Status da escala                      | \[varchar]   | 20      | ☐    | ☐  | ☐  | ☐      | ☐        |         | status IN ('Publicado','Em Rascunho','Arquivado') |
| id\_setor      | Chave estrangeira referenciando Setor | \[int]       |         | ☐    | ☐  | ☑  | ☐      | ☐        |         | Not null                 |
| criado\_em     | Data de criação da escala             | \[timestamp] |         | ☐    | ☐  | ☐  | ☐      | ☐        |         | Not null                 |
| atualizado\_em | Data de atualização da escala         | \[timestamp] |         | ☐    | ☐  | ☐  | ☐      | ☐        |         | Not null                 |

---

### Tabela : Plantão

**Descrição** : Armazena informações detalhadas sobre os turnos de trabalho dentro da escala.

| Colunas        | Descrição                              | Tipo de Dado | Tamanho | Null | PK | FK | Unique | Identity | Default | Check    |
| -------------- | -------------------------------------- | ------------ | ------- | ---- | -- | -- | ------ | -------- | ------- | -------- |
| id             | Identificador único do plantão         | \[int]       |         | ☐    | ☑  | ☐  | ☐      | ☑        |         | Not null |
| data           | Data em que o plantão ocorrerá         | \[date]      |         | ☐    | ☐  | ☐  | ☐      | ☐        |         | Not null |
| hora\_inicio   | Horário de início do plantão           | \[time]      |         | ☐    | ☐  | ☐  | ☐      | ☐        |         | Not null |
| hora\_fim      | Horário de término do plantão          | \[time]      |         | ☐    | ☐  | ☐  | ☐      | ☐        |         | Not null |
| descricao      | Descrição adicional do plantão         | \[text]      |         | ☑    | ☐  | ☐  | ☐      | ☐        |         |          |
| id\_escala     | Chave estrangeira referenciando Escala | \[int]       |         | ☐    | ☐  | ☑  | ☐      | ☐        |         | Not null |
| criado\_em     | Data de criação do plantão             | \[timestamp] |         | ☐    | ☐  | ☐  | ☐      | ☐        |         | Not null |
| atualizado\_em | Data de atualização do plantão         | \[timestamp] |         | ☐    | ☐  | ☐  | ☐      | ☐        |         | Not null |
---

### Tabela : Alocação

**Descrição** : Registra a alocação de médicos a plantões.

| Colunas        | Descrição                                            | Tipo de Dado | Tamanho | Null | PK | FK | Unique | Identity | Default | Check    |
| -------------- | ---------------------------------------------------- | ------------ | ------- | ---- | -- | -- | ------ | -------- | ------- | -------- |
| id             | Identificador único da alocação                      | \[int]       |         | ☐    | ☑  | ☐  | ☐      | ☑        |         | Not null |
| tipo           | Tipo da alocação                                     | \[varchar]   | 50      | ☐    | ☐  | ☐  | ☐      | ☐        |         | tipo IN ('Direta','Sugestão')                   |
| data\_retorno  | Data de confirmação ou recusa da alocação (sugestão) | \[date]      |         | ☑    | ☐  | ☐  | ☐      | ☐        |         |          |
| status         | Status da alocação                                   | \[varchar]   | 10      | ☐    | ☐  | ☐  | ☐      | ☐        |         | status IN ('Confirmada','Recusada','Em Aberto') |
| id\_plantao    | Chave estrangeira referenciando Plantão              | \[int]       |         | ☐    | ☐  | ☑  | ☐      | ☐        |         | Not null |
| id\_medico     | Chave estrangeira referenciando Médico               | \[int]       |         | ☐    | ☐  | ☑  | ☐      | ☐        |         | Not null |
| criado\_em     | Data de criação da alocação                          | \[timestamp] |         | ☐    | ☐  | ☐  | ☐      | ☐        |         | Not null |
| atualizado\_em | Data de atualização da alocação                      | \[timestamp] |         | ☐    | ☐  | ☐  | ☐      | ☐        |         | Not null |

---

### Tabela: Notificação

**Descrição**: Armazena mensagens ou avisos relacionados a uma alocação ou outro objeto, por meio de associação polimórfica.

| Colunas        | Descrição                                            | Tipo de Dado | Tamanho | Null | PK | FK | Unique | Identity | Default | Check    |
| -------------- | ---------------------------------------------------- | ------------ | ------- | ---- | -- | -- | ------ | -------- | ------- | -------- |
| id             | Identificador único da notificação                   | \[int]       |         | ☐    | ☑  | ☐  | ☐      | ☑        |         | Not null |
| mensagem       | Conteúdo textual da notificação                      | \[text]      |         | ☑    | ☐  | ☐  | ☐      | ☐        |         |          |
| lida           | Indica se a notificação foi lida                     | \[boolean]   |         | ☐    | ☐  | ☐  | ☐      | ☐        | false   | Not null |
| objeto         | ID do objeto associado                               | \[int]       |         | ☑    | ☐  | ☐  | ☐      | ☐        |         |          |
| url            | URL para acessar o objeto associado                  | \[varchar]   | 200     | ☑    | ☐  | ☐  | ☐      | ☐        |         | Not null |
| tipo\_conteudo | ID do tipo do objeto associado (FK para ContentType) | \[int]       |         | ☑    | ☐  | ☑  | ☐      | ☐        |         |          |
| remetente      | ID do usuário que gerou a notificação                | \[int]       |         | ☑    | ☐  | ☑  | ☐      | ☐        |         |          |
| destinatario   | ID do usuário que recebeu a notificação              | \[int]       |         | ☑    | ☐  | ☑  | ☐      | ☐        |         |          |
| criado\_em     | Data de criação do plantão                           | \[timestamp] |         | ☐    | ☐  | ☐  | ☐      | ☐        |         | Not null |


