# CDU002. Criar Escala

- **Ator principal**: Gestor
- **Atores secundários**: Médico	 
- **Resumo**: O gestor após clicar em um botão, pode criar uma escala.
- **Pré-condição**: O usuário deve ter uma conta do tipo gestor e ser autenticado.
- **Pós-Condição**: Feedback de ação bem sucedida ou erro após cada interação.

## Fluxo Principal
| Ações do ator | Ações do sistema |
| :-----------------: | :-----------------: | 
| 1 - O gestor acessa a interface de criação de escala. | |  
| | 2 - O sistema mostra a interface da cricação de escala, sendo possível informar o nome, o setor e o periodo da escala. |
| 3 - Preenche os dados obrigatórios (nome, setor, período inicial e príodo final). | |  
| | 4 - O sistema valida os dados e cria a nova escala e então o caso de uso é finalizado | 
| | 5 - O gestor é redirecionado para a tela de criação de plantões associados.| 

## Fluxo de Exceção - [Escala duplicada]
| Ações do ator | Ações do sistema |
| :-----------------: | :-----------------: | 
| 2.1 - O gestor tenta criar uma escala para um setor e período que já possuem uma escala ativa.| |  
| | 2.2 -  O sistema impede a criação e exibe uma mensagem: “Já existe uma escala para este setor e período.” |  

## Protótipo
![image](https://github.com/user-attachments/assets/8f646c0e-80ac-4a3a-8ad4-4ead8127dc4f)

> Obs. as seções a seguir apenas serão utilizadas na segunda unidade do PDSWeb (segundo orientações do gerente do projeto).

## Diagrama de Interação (Sequência ou Comunicação)

### Sequência - Etapa 1

<img width="2296" height="686" alt="etapa 1 - ver criar escala" src="https://github.com/user-attachments/assets/dc58262a-4b3f-415a-842d-8d7ddd736d32" />

### Sequência - Etapa 2

<img width="2649" height="789" alt="etapa 2 - criar nova escala" src="https://github.com/user-attachments/assets/94eeb394-e674-4b90-abe5-29eb1912a838" />

## Diagrama de Classes de Projeto

<img width="1201" height="885" alt="classes de projeto" src="https://github.com/user-attachments/assets/4c5449d9-dc80-4292-aa5a-23de3f0e7558" />
