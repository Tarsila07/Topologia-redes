# Simulador de Topologia de Redes (Tree-Tier)

**Projeto de Redes de Computadores 2025.2 — Universidade de Brasília (UnB)**

---

## 📋 Descrição

Este projeto implementa um simulador de topologia de redes hierárquica (Data Center) desenvolvido em **Python**. O sistema permite carregar, visualizar e operar uma rede em topologia de árvore, oferecendo funcionalidades para:

- Simular latência (RTT);
- Verificar conectividade via comando **XProbe** (ping simulado);
- Calcular rotas otimizadas usando o algoritmo de **Dijkstra**;
- Resolver nomes (Hostname ↔ IP).

---

## 🏗️ Arquitetura da Rede

A topologia segue uma estrutura hierárquica de três camadas (Core → Aggregation → Edge) para alta disponibilidade e organização lógica:

                [c1] - Roteador Core
               /              \
          [a1] - Aggregation  [a2] - Aggregation
         /    \              /    \
     [e1]      [e2]      [e3]      [e4] - Roteadores Edge
      |         |         |         |
    Hosts     Hosts     Hosts     Hosts
  (Sub-e1)  (Sub-e2)  (Sub-e3)  (Sub-e4)

### Especificações das Sub-redes (VLSM)

Rede base: **`192.168.10.0/24`**

- **Subrede e1 — `192.168.10.0/28`** → Hosts: h1, h2, ... (até 14 hosts)  
- **Subrede e2 — `192.168.10.16/28`** → Hosts: h3, h4, ... (até 14 hosts)  
- **Subrede e3 — `192.168.10.64/27`** → Hosts: h5, h6, ... (até 30 hosts)  
- **Subrede e4 — `192.168.10.96/27`** → Hosts: h7, h8, ... (até 30 hosts)  
- **Backbone — `/30`** → Enlaces ponto-a-ponto entre roteadores (Core ↔ Agg ↔ Edge)

---

## 🔌 Tipos de Enlaces (Camada Física)

- 🔴 **Fibra Óptica (10 Gbps):** enlaces do Backbone (Core ↔ Aggregation).  
- 🔵 **Par Trançado Cat6a (1 Gbps):** enlaces de distribuição (Aggregation ↔ Edge).  
- ⚫ **Par Trançado Cat6 (1 Gbps):** enlaces de acesso (Edge ↔ Hosts).


---
## 💻 Funcionalidades do Simulador

- O script simulador_rede.py oferece uma CLI interativa com as seguintes ferramentas:

- Configuração Automática: Carrega a topologia e constrói o grafo de conexões na memória.

- XProbe (Ping Estendido): Verifica conectividade e calcula o RTT Médio (Round Trip Time) baseando-se na latência física dos enlaces (Fibra vs Cobre) + Jitter.

- Trace Route Visual: Exibe o caminho lógico percorrido pelo pacote, demonstrando o funcionamento do algoritmo de roteamento (Dijkstra).

- Input Inteligente: Aceita tanto IPs (192.168.10.2) quanto Hostnames (h1) como entrada.

## Exemplos de Uso
### 📡 Trace Route Visual (Dijkstra)

Mostra o caminho percorrido pelo pacote na árvore.

* **Origem:** `h1`
* **Destino:** `h7`
* **Saída:** `[h1] -> [e1] -> [a1] -> [c1] -> [a2] -> [e4] -> [h7]`

### ⏱️ XProbe (Ping Simulado)

Verifica conectividade e latência.

* **Origem:** `192.168.10.2` (ou `h1`)
* **Destino:** `192.168.10.98` (ou `h7`)
* **Saída:** `[XProbe Result] Status: UP | RTT Médio: 29.04 ms`
## 🔧 Funcionalidades Técnicas

**🧠 Algoritmos e Lógica**
- Dijkstra (Shortest Path): Implementado para calcular a rota de menor custo no grafo ponderado, simulando tabelas de roteamento estático.

- Resolvedor de Nomes: Permite input híbrido (IP ou Hostname), mapeando h1 para 192.168.10.2 automaticamente.

- Simulação de Jitter: O cálculo do RTT inclui uma variação aleatória para simular condições reais de rede.

**✅ Validações**
- Verificação de existência de IPs na tabela de roteamento.

- Tratamento de erros para destinos inalcançáveis ou fora da topologia.

## 🚀 Pré-requisitos e Instalação

### Requisitos

- Python **3.6+**  
- Apenas bibliotecas padrão do Python utilizadas (`heapq`, `random`, `time`). **Sem dependências externas**.

### Como clonar e executar

```bash
git clone https://github.com/Tarsila07/Topologia-redes.git
cd Topologia-redes
```
## 📄 Licença
Projeto desenvolvido para fins acadêmicos na Universidade de Brasília (UnB).


