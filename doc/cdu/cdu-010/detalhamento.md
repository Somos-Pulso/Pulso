# CDU010. Modificar Escala

- **Ator principal**: Gestor
- **Atores secundários**: Sistema
- **Resumo**: Permite ao gestor realizar a exclusão da escala.
- **Pré-condição**: Gestor devidamente logado, escala devidamente criada e sem estar publicada.
- **Pós-condição**: A página apresenta a página de listagem de escalas, agora sem a escala que foi excluida.

## Fluxo Principal
| Ações do ator | Ações do sistema |
| :-----------: | :--------------: |
| 0 - Seleciona a escala | ... |
| ... | 1 - O sistema carrega as informações da escala |
| 2 - Seleciona a opção de excluir escala | ... |
| ... | 3 - O sitema pergunta se o gestor realmente quer excluir a escala |
| 4 - Confirma a exclusão | ... |
| ... | 5 - O sistema exclui a escala em questão |
| ... | 6 - O sistema mostra a lista de escalas agora sem a escala |

## Protótipo

<img width="1440" height="1100" alt="Editar escala" src="https://github.com/user-attachments/assets/c6c6d126-f82b-42ae-a6a2-8affd334fc67" />

## Diagrama de Interação (Sequência ou Comunicação)

<img width="2734" height="784" alt="etapa 1 - excluir escala" src="https://github.com/user-attachments/assets/b1058c4d-4a54-4e3c-bfa9-866bc0268998" />

## Diagrama de Classes de Projeto

<img width="1333" height="1036" alt="classes de projeto" src="https://github.com/user-attachments/assets/17c3a29a-c5bf-4e48-9c36-adffba6e2149" />
