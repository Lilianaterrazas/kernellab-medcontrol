# KernelLab — Simulador de Sistemas Operacionais (MedControl)

## Problema e objetivo
Simular decisões de um sistema operacional com uma CPU, comparando escalonamento, substituição de páginas e acesso concorrente a dispositivos em um cenário de monitoramento de saúde (MedControl). O projeto é didático: não controla dispositivos médicos reais.

## Arquitetura
- `src/main.py`: interface de terminal, leitura do JSON e relatórios.
- `src/schedulers.py`: FCFS, SJF **não preemptivo**, RR (quantum configurável), prioridade **não preemptiva** (menor valor = maior prioridade).
- `src/metrics.py`: espera, retorno, resposta, médias e trocas.
- `src/memory.py`: FIFO, LRU e Optimal; estados dos frames por referência.
- `src/devices.py`: matriz de permissões, fila FIFO e demonstração de mutex com threads.
- `src/plots.py`: gráficos PNG de CPU, memória e Gantt.
- `data/processes.json`: processos e parâmetros editáveis.
- `tests/test_algorithms.py`: testes automatizados.
- `docs/saida_exemplo.txt`: saída integral com tabelas.

## Instalação e execução
Requer Python 3.10 ou superior. A partir da pasta `kernellab`:

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python -m src.main --plots
```

Os gráficos serão salvos em `docs/`. Execução sem gráficos: `python -m src.main`.

## Alterar dados de entrada
Edite `data/processes.json` para ajustar processos, chegada (`arrival`), burst (`burst`), prioridade (`priority`), memória (`memory_mb`), dispositivos (`devices`), `quantum`, `frames` e sequência `pages`. Cada processo deve ter ID único; burst positivo e chegada não negativa. Exemplos:

```bash
python -m src.main --quantum 5 --frames 3
python -m src.main --pages 1,2,1,3,4 --plots
python -m src.main --input data/processes.json
```

## Testes
```bash
python -m unittest discover -s tests -v
```

## Métricas
- Retorno = conclusão - chegada.
- Espera = retorno - burst (não há bloqueios de E/S no modelo de CPU).
- Resposta = primeira execução - chegada.
- Trocas = mudanças de PID entre segmentos executados; transições para/de IDLE não contam, custo de troca considerado zero.
- Taxa de page faults = faults / referências.

## Resultados de referência (dados originais)

| Escalonador | Espera média | Retorno médio | Resposta média | Trocas |
|---|---:|---:|---:|---:|
| FCFS | 13,67 | 20,50 | 13,67 | 5 |
| SJF | 10,67 | 17,50 | 10,67 | 5 |
| RR q=3 | 18,00 | 24,83 | 5,33 | 13 |
| Prioridade | 10,67 | 17,50 | 10,67 | 5 |

| Memória | Hits | Faults | Taxa |
|---|---:|---:|---:|
| FIFO | 5 | 12 | 70,59% |
| LRU | 7 | 10 | 58,82% |
| Optimal | 10 | 7 | 41,18% |

## Interpretação e recomendação
SJF e prioridade empataram na média de espera **neste conjunto**, mas seguem ordens distintas. O alarme P4 espera 5 unidades sob prioridade não preemptiva e SJF, 6 no RR e 18 no FCFS. RR oferece resposta média melhor e rodízio mais justo, porém com mais trocas. A política recomendada para uma futura evolução é **prioridade preemptiva para alarmes críticos, com envelhecimento (aging) e fatias de tempo para os demais processos**. Essa política híbrida **não foi implementada** nos quatro escalonadores solicitados; deve ser avaliada antes de qualquer aplicação real.

## Controle de dispositivos e segurança
A ACL é uma **política didática** baseada nos dispositivos associados a cada processo; todos podem acessar logs e nenhum recebe permissão de executar em dispositivos. O acesso exclusivo é autorizado a operações de disco e áudio. A fila FIFO serializa requisições de disco; a demonstração com `threading.Lock` impede que duas threads ocupem a seção crítica simultaneamente. A ACL é exibida e não constitui controle de acesso do sistema operacional real.

## Limitações e melhorias
Escalonamento não preemptivo em SJF/prioridade; tempo de CPU discreto; sem overhead de troca, interrupções, prazos, I/O blocking, concorrência de CPU e memória por processo; frames abstratos, sem paginação real; nenhuma garantia de tempo real; sem autenticação real de dispositivos. Melhorias: prioridade preemptiva, EDF, aging, métricas de deadline, simulação de eventos de E/S, custos de troca e testes de carga.

## Referências para aprofundamento
- TANENBAUM, Andrew S.; BOS, Herbert. *Sistemas Operacionais Modernos*.
- Material da disciplina de Sistemas Operacionais no AVA (consultar unidades e videoaulas).
- UNIVASF. *Sistemas multiprogramados*. https://www.docentes.univasf.edu.br/max.santana/material/OAC-II/sistemas_multiprogramados.pdf
- PUC-Rio. *INF 1316: Sistemas Operacionais*. https://www-di.inf.puc-rio.br/~endler/courses/inf1019/transp/aulas-teoricas/cap-1.pdf
- Tecnoblog. *O que é um sistema operacional?* https://tecnoblog.net/responde/o-que-e-um-sistema-operacional/

## Publicação no GitHub
Crie um repositório público chamado `kernellab` no GitHub e envie **o conteúdo desta pasta**. O ZIP entregue não publica o repositório automaticamente.
