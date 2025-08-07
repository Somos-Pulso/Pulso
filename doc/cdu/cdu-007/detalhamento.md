# CDU007. Listar plantões

- **Ator principal**: Médico
- **Atores secundários**: Sistema
- **Resumo**: Permite a visualização a lista de plantões gerados, incluindo informações como data, médico, gestor escalado, etc.
- **Pré-condição**: O usuário estar autenticado e clicou na opção "Plantões".
- **Pós-condição**: A lista de plantões é apresentada com os dados relevantes e pronta para interações adicionais.

## Fluxo Principal
| Ações do ator | Ações do sistema |
| :-----------: | :--------------: |
| 0 - Seleciona a opção plantões | ... |
| ... | 1 - O sistema carrega a lista de plantões cadastrados|

## Fluxo Alternativo I - [Filtragem de plantão]
| Ações do ator | Ações do sistema |
| :-----------: | :--------------: |
| 1.1 - Aplica filtros ou busca um plantão específico | ... |
| ... | 1.2 - Atualiza a lista de plantão com base nos critérios informados |

## Fluxo Exceção I - [Lista de plantão vazio]
| Ações do ator | Ações do sistema |
| :-----------: | :--------------: |
| 0.1 - Acessa a tela de escalas | ... |
| ... | 0.2 - Exibe mensagem: “Nenhuma plantão criado até o momento.” |

## Fluxo Exceção II - [Falha no carregamento dos plantões]
| Ações do ator | Ações do sistema |
| :-----------: | :--------------: |
| 0.a - Acessa a tela de escalas | ... |
| ... | 0.b - Exibe mensagem de erro: “Ocorreu um erro ao carregar os plantões. Tente novamente mais tarde.” |

## Protótipo
![Meus plantões](https://github.com/user-attachments/assets/093928e7-1851-4d74-9f7d-247b8463c784)

> Obs. as seções a seguir apenas serão utilizadas na segunda unidade do PDSWeb (segundo orientações do gerente do projeto).

## Diagrama de Interação (Sequência)

<img width="1936" height="636" alt="etapa 1 - listar plantoes" src="https://github.com/user-attachments/assets/c69db4c2-e82e-408f-9fd2-da5843e8b756" />

## Diagrama de Classes de Projeto

<img width="1402" height="1080" alt="classes de projeto" src="https://github.com/user-attachments/assets/2e8a44a7-2545-401e-890b-536a8a2f5cb0" />
