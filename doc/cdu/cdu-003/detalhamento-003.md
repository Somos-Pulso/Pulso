# CDU003. Ver Escala

* **Ator principal**: Gestor  
* **Atores secundários**: Sistema  
* **Resumo**: Permite que o gestor acesse uma escala previamente registrada e visualize informações detalhadas, como nome, setor, período, status e plantões atribuídos. A apresentação é feita em um calendário com modo de exibição ajustável.  
* **Pré-condição**: A escala deve ter sido criada anteriormente.  
* **Pós-condição**: A escala selecionada é apresentada com todos os seus dados e plantões.

---

## Fluxo Principal – Visualização da Escala

| Ações do Gestor                                       | Ações do Sistema                                         |
|-------------------------------------------------------|----------------------------------------------------------|
| 0 - Seleciona uma escala no menu de "Ver Escalas"     |                                                          |
|                                                       | 1 - Exibe a tela de visualização da escala selecionada   |
| 2 - Visualiza as informações gerais e os plantões     |                                                          |


## Fluxo Alternativo I – Visualização após Criação

| Ações do Gestor                                      | Ações do Sistema                                                   |
|------------------------------------------------------|--------------------------------------------------------------------|
| 0.1 - Seleciona "Próximo" após concluir a criação de uma escala |                                                              |
|                                                      | 0.2 - Exibe a tela da nova escala com status definido como "rascunho" |


## Fluxo Alternativo II – Edição da Escala

| Ações do Gestor                        | Ações do Sistema                                        |
|----------------------------------------|---------------------------------------------------------|
| 2.1 - Seleciona a opção de editar escala |                                                         |
|                                        | 2.2 - Apresenta a tela de edição da escala selecionada  |
| 2.3 - Altera as informações da escala   |                                                         |

## Fluxo Alternativo III – Publicação da Escala

| Ações do Gestor                          | Ações do Sistema                                                                            |
|------------------------------------------|---------------------------------------------------------------------------------------------|
| 2.a - Seleciona a opção de publicar escala |                                                                                             |
|                                          | 2.b - Atualiza o status da escala para "publicada" e notifica os médicos vinculados         |


## Fluxo de Exceção I – Publicação sem Plantões

| Ações do Gestor                                  | Ações do Sistema                                                                                 |
|--------------------------------------------------|--------------------------------------------------------------------------------------------------|
| 2.a.1 - Tenta publicar uma escala sem plantões   |                                                                                                  |
|                                                  | 2.a.2 - Impede a publicação e informa que a escala deve conter pelo menos um plantão registrado |

## Protótipo
![Ver escala](https://github.com/user-attachments/assets/7453dc22-e48b-4aa8-a0ab-90ccf219ac44)

> Obs. as seções a seguir apenas serão utilizadas na segunda unidade do PDSWeb (segundo orientações do gerente do projeto).

## Diagrama de Interação (Sequência ou Comunicação)

### Sequência - Etapa 1 - Ver Escala

<img width="3164" height="1380" alt="etapa 1 - ver escala" src="https://github.com/user-attachments/assets/746d6b5e-2981-4d19-b93e-e5400f718cbe" />

### Sequência - Etapa 2 - Publicar Escala

<img width="4445" height="1816" alt="etapa 2 - publicar escala" src="https://github.com/user-attachments/assets/c8980320-aa5c-4cca-b3a7-4cdd83f472ba" />

## Diagrama de Classes de Projeto

<img width="3212" height="1541" alt="classes de projeto" src="https://github.com/user-attachments/assets/c26697b3-9db3-4d9d-891b-d19b111dc532" />
