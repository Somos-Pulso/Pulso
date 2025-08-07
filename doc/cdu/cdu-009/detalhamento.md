# CDU009. Listar Notificações

- **Ator principal**: Médico e Gestor
- **Atores secundários**: Sistema
- **Resumo**: Apresenta uma lista de notificações de todas as ações que envolvam o agente em questão dentro do sistema.
- **Pré-condição**: O Ator acessa a lista de notificações a partir da sidebar ou através do ícone de notificação do header e em seguida em "ver todas".
- **Pós-condição**: A página de notificações apresenta a lista das notificações destinadas ao agente logado.

## Fluxo Principal
| Ações do ator | Ações do sistema |
| :-----------: | :--------------: |
| 0 - Seleciona a opção de listagem de notificações | ... |
| ... | 1 - O sistema carrega a lista de notificações|

## Fluxo Alternativo I - [Filtragem ou busca de notificações]
| Ações do ator | Ações do sistema |
| :-----------: | :--------------: |
| 1.1 - Aplica filtros ou busca uma notificação específica | ... |
| ... | 1.2 - Atualiza a lista de notificações com base nos critérios informados |

## Fluxo Exceção I - [Lista de notificações vazia]
| Ações do ator | Ações do sistema |
| :-----------: | :--------------: |
| 0.1 - Acessa a tela de notificações | ... |
| ... | 0.2 - Exibe mensagem: “Nenhuma notificação.” |

## Fluxo Exceção II - [Falha no carregamento das notificações]
| Ações do ator | Ações do sistema |
| :-----------: | :--------------: |
| 0.a - Acessa a tela de notificações | ... |
| ... | 0.b - Exibe mensagem de erro: “Ocorreu um erro ao carregar as suas notificações. Tente novamente mais tarde.” |


## Protótipo
![Detalhes de Listar Notificações](https://github.com/user-attachments/assets/f91c296b-f744-44fe-8173-99e96af3bfe8)


> Obs. as seções a seguir apenas serão utilizadas na segunda unidade do PDSWeb (segundo orientações do gerente do projeto).

## Diagrama de Interação (Sequência ou Comunicação)

<img width="1600" height="686" alt="etapa 1 - listar notificacoes" src="https://github.com/user-attachments/assets/dbe5a786-3f79-4212-9f01-dc7309187788" />

## Diagrama de Classes de Projeto

<img width="1232" height="928" alt="classes de projeto" src="https://github.com/user-attachments/assets/1c9cc656-93b6-46f7-b913-7daebbb0f47b" />
