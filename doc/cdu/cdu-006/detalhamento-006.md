# CDU006. Ver notificação

- **Ator principal**: Médico
- **Atores secundários**: Sistema
- **Resumo**: Apresenta ao médico de forma detalhada uma notificação interna, inclui publicação de escala, atualização de plantãoe exclusão de plantão.
- **Pré-condição**: O médico clica em uma notificação, ou acessa detalhes de uma notificação direto da lista de notificações.
- **Pós-condição**: A página de detalhes apresenta os detalhes da notificação em questão como data, hora, setor, gestor responsável e descrição.

## Fluxo Principal
| Ações do ator | Ações do sistema |
| :-----------: | :--------------: |
| 1 - Clica em uma notificação da lista de notificações | ... |
| ... | 2 - Apresenta detalhes da nolicitação em questão |

## Fluxo Alternativo I - [Notificação de entidade]
| Ações do ator | Ações do sistema |
| :-----------: | :--------------: |
| 1 - Clica em uma notificação da lista de notificações | ... |
| ... | 2 - Redirecionamento para detalhes da entidade em questão, podendo ser plantão ou escala |

## Fluxo Exceção I - [Erro ao carregar]
| Ações do ator | Ações do sistema |
| :-----------: | :--------------: |
| 1 - Clica em uma notificação da lista de notificações | ... |
| ... | 2 - Exibe mensagem: “Erro ao carregar detalhes da notificação" |

## Protótipo
![Detalhes da Solicitações](https://github.com/user-attachments/assets/38c57b87-e3e6-481f-9785-025504c54b08)

> Obs. as seções a seguir apenas serão utilizadas na segunda unidade do PDSWeb (segundo orientações do gerente do projeto).

## Diagrama de Interação (Sequência ou Comunicação)

<img width="1700" height="692" alt="etapa 1 - ver notificacao" src="https://github.com/user-attachments/assets/699aad87-29fc-4dc7-acee-7060589c166d" />

## Diagrama de Classes de Projeto

<img width="1408" height="1069" alt="classes de projeto" src="https://github.com/user-attachments/assets/f47e95d9-a9b5-4ff5-8410-9fd799696349" />
