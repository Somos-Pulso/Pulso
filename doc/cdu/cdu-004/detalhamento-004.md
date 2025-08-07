# CDU004. Criar plantão

* **Ator principal**: Gestor
* **Atores secundários**: Médicos
* **Resumo**: O gestor, ao escolher uma data, cria um plantão, informando horário de início e fim, alocando médicos para esse plantão.
* **Pré-condição**:Deve existir uma escala previamente criada e médicos cadastrados no sistema.
* **Pós-condição**: O plantão é criado e inserido corretamente na escala da data escolhida, com os médicos devidamente alocados.

### Fluxo Principal

| Ações do Gestor                                                                           | Ações do Sistema                                                                                                                                                                                                                    |
| ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **1 - Seleciona** o dia específico na escala                                       |                                                                                                                                                                                                                                     |
|                                                                                           | **2 - O sistema exibe** o formulário para criação do plantão, com campos para horário de início, horário de término, seleção do(s) médico(s) e descrição. Campos como data, hospital, setor e gestor já vêm preenchidos automaticamente. |
| **3 - O gestor preenche** os horários de entrada e saída e seleciona o(s) médico(s) desejado(s) caso já definidos |                                                                                                                                                                                                                                     |
|                                                                                           | **4 - O sistema salva** o plantão no calendário da escala.       



## Protótipo
![Criar plantao](https://github.com/user-attachments/assets/1cce7b29-c71e-4f32-8640-1e7fe7ef2afe)

> Obs. as seções a seguir apenas serão utilizadas na segunda unidade do PDSWeb (segundo orientações do gerente do projeto).

## Diagrama de Interação (Sequência ou Comunicação)

<img width="3436" height="1516" alt="etapa 1 - criar plantao" src="https://github.com/user-attachments/assets/507def08-3ee9-44b3-97f5-3273876314d3" />

## Diagrama de Classes de Projeto

<img width="1781" height="1062" alt="classes de projeto" src="https://github.com/user-attachments/assets/9ee016c4-6c16-4399-a387-82f58e116391" />
