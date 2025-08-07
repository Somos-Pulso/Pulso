# CDU010. Modificar Plantão

- **Ator principal**: Gestor
- **Atores secundários**: Sistema
- **Resumo**: Permite ao gestor realizar modificações em plantões já criados, tanto modificações dos dados como exclusão.
- **Pré-condição**: Gestor devidamente logado, plantão devidamente criado e sem estar no passado.
- **Pós-condição**: A página apresenta a página da escala que abriga o plantão, que agora está com as devidas modificações.

## Fluxo Principal
| Ações do ator | Ações do sistema |
| :-----------: | :--------------: |
| 0 - Seleciona o plantão | ... |
| ... | 1 - O sistema carrega as informações do plantão |
| 2 - Seleciona a opção de atualizar o plantão | ... |
| ... | 3 - O sistema carrega as informações para ter as opções de atualizações de dados, informando os dados já cadastrados |
| 4 - Insere os dados a serem atualizados | ... |
| 5 - Seleciona a opção de salvar | ... |
| ... | 6 - O sistema atualiza o plantão em questão com os novos dados |
| ... | 7 - O sistema mostra a escala com o plantão com o plantão agora atualizado |

## Fluxo Alternativo I - [Exclusão de plantão]
| Ações do ator | Ações do sistema |
| :-----------: | :--------------: |
| 2.1 - Seleciona a opção de excluir plantão | ... |
| ... | 2.2 - O sistema pergunta se o gestor realmente quer excluir o plantão |
| 2.3 - Confirma a exclusão | ... |
| ... | 2.4 - O sistema exclui o plantão em questão |
| ... | 2.5 - O sistema mostra a escala agora sem o plantão |

## Fluxo Exceção I - [Atualizar plantão para horários no passado]
| Ações do ator | Ações do sistema |
| :-----------: | :--------------: |
| 4.1 - Insere os dados a serem atualizados com o horário de início em horário já passado do horário atual | ... |
| ... | 4.2 - O sistema exibe mensagem: “Não foi possível atualizar plantão” e mantém os dados sem atualizar |

## Fluxo Exceção II - [Excluir plantão com horário no passado]
| Ações do ator | Ações do sistema |
| :-----------: | :--------------: |
| 2.1.1 - Seleciona a opção de excluir plantão em um plantão com horário já passado do horário atual | ... |
| ... | 2.1.2 - O sistema exibe mensagem: “Não foi possível excluir plantão” e mantém os dados |

## Protótipo

<img width="904" height="760" alt="criar plantao (1)" src="https://github.com/user-attachments/assets/6b172118-0054-4536-9aac-323b8a0d3fcf" />

## Diagrama de Interação (Sequência ou Comunicação)

### Sequência - Etapa 1 - Atualizar Plantão

<img width="3302" height="1488" alt="etapa 1 - atualizar plantao" src="https://github.com/user-attachments/assets/1fe0db6b-79e3-48f4-9db4-bef59948577d" />

### Sequência - Etapa 2 - Excluir Plantão

<img width="3397" height="1192" alt="etapa 2 - excluir plantao" src="https://github.com/user-attachments/assets/d4dcdea1-70ef-44d2-84f7-33fad4eab9b5" />

## Diagrama de Classes de Projeto

<img width="2961" height="1314" alt="classes de projeto" src="https://github.com/user-attachments/assets/91066c67-0f91-46cc-9c75-c9e762415a31" />
