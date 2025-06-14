# 🧵 Sistema de Monitoramento de Enfesto em Indústrias Têxteis

## 📌 Grupo: 44

### 👨‍💻 Integrantes:

* Thiago Scutari - RM562831 | thiago.scutari@outlook.com
* Hnrique Ribiro Siqueira - RM565044 | henrique.ribeiro1201@gmail.com
* Mariana Cavalante Oliveira - RM561678 | mari.kvalcant@gmail.com

### 👩‍🏫 Professores:

* Leonardo Ruiz Orabona
* Andre Godoi Chiovato

---

## 📜 Descrição

Este projeto tem como objetivo desenvolver uma solução prática para **monitoramento do processo de Enfesto** em indústrias têxteis, visando otimizar a produtividade e qualidade no corte de tecidos. O sistema utilizará sensores a laser para medir a **distância percorrida**, **velocidade média**, **data e hora** dos processos de enfesto, integrando esses dados a um módulo de cadastro de tecidos que inclui **código**, **nome** e **gramatura**.

A aplicação contempla:

* Cálculo do tempo e velocidade média por enfesto (produtividade);
* Análise do impacto da gramatura nas médias de produtividade;
* Identificação de períodos de ociosidade e alta demanda;
* Marcação de manutenção com correlação entre tempo de uso e esforço aplicado;
* Registro e armazenamento dos dados para análises futuras.

---

## 🛠️ Definição Técnica e Metodologia

### 🔍 Justificativa do Problema

No processo de enfesto em indústrias têxteis, a precisão e eficiência são essenciais para garantir a qualidade do corte dos tecidos e minimizar desperdícios. Problemas como torções, bolhas e amassados podem comprometer a qualidade das peças e aumentar os custos operacionais. Além disso, o monitoramento em tempo real da produtividade e manutenção dos equipamentos pode melhorar significativamente a eficiência do processo.

### 📐 Arquitetura da Solução

A solução proposta inclui:

* **Sensores a laser** para medição de distância e velocidade.
* **Microcontroladores (ESP32)** para coleta e transmissão dos dados.
* **Banco de Dados (SQLite)** para armazenamento local e persistência dos dados.
* **Visualização e Análise de Dados** com integração a dashboards futuros.

### 🌐 Pipeline de Dados

📝 1. **Coleta de Dados:**

   * Sensores a laser medem a distância, velocidade e tempo de operação.
   * Dados são capturados em tempo real e enviados para o microcontrolador.
  
   * Descrição Detalhada:
   * A etapa inicial do processo é a coleta de dados diretamente na mesa de corte. Sensores a laser medem a distância percorrida, velocidade média e tempo total de operação do enfesto. Esses dados são fundamentais para calcular a produtividade e identificar possíveis falhas, como paradas inesperadas ou baixa eficiência em função da gramatura do tecido.
     
   * Recursos utilizados:
   * Sensores a Laser: Medem a distância com alta precisão.
   * Microcontrolador (ESP32): Processa os dados dos sensores e os envia para armazenamento.
   * Conexão Wi-Fi/Bluetooth: Para transmissão dos dados.

🗄️ 2. **Armazenamento:**

   * Dados são armazenados localmente em um banco de dados SQLite.
     
   * Descrição detalhada:
   * Os dados coletados precisam ser armazenados para garantir persistência e facilitar análises futuras. Para isso, é utilizado um banco de dados local SQLite, que registra todas as medições, incluindo informações como código do tecido, nome, gramatura, data/hora e tempo de operação. Este armazenamento local é ideal para protótipos e testes, mas pode ser expandido para um sistema em nuvem em fases futuras.
     
   * Recursos utilizado:
   * Banco de Dados SQLite: Armazena as medições localmente.
   * Módulo de Comunicação (UART/Wi-Fi): Integra o ESP32 ao banco de dados.

🖥️ 3. **Processamento e Análise:**

   * Cálculo da produtividade e análise do impacto da gramatura nos resultados.
  
   * Descrição detalhada:
   * Nesta etapa, os dados armazenados são analisados para gerar insights e calcular métricas como produtividade, impacto da gramatura e períodos de ociosidade. Aqui, os algoritmos calculam a velocidade média, o tempo total de operação e identificam padrões de eficiência, auxiliando na manutenção preditiva e otimização do processo.
     
   * Recursos utilizados:
   * Python: Para scripts de análise de dados e cálculos de produtividade.
   * Bibliotecas como Pandas e Numpy: Para manipulação e análise dos dados.

📊 4. **Visualização:**

   * Integração futura com dashboards para visualização em tempo real.

   * Descrição detalhada:
   * Para facilitar a interpretação dos dados, é essencial que as informações sejam apresentadas de forma clara e acessível. Dashboards futuros podem incluir gráficos de produtividade, histórico de manutenção, alertas de eficiência e análise de impacto da gramatura. Esses dashboards permitirão o acompanhamento em tempo real, auxiliando na tomada de decisões rápidas.

   * Recursos utilizados:
   * Streamlit, Grafana ou Power BI: Ferramentas para criação de dashboards interativos.
   * API para Integração com Banco de Dados: Para atualização em tempo real.

### 📝 Estratégia de Coleta de Dados

* **Simulação:** Para testes iniciais, os dados podem ser simulados para validar a arquitetura.
* **Planejamento:** Em uma segunda fase, integração com sensores físicos como **ESP32** e módulos de medição a laser para dados reais.

### 🗂️ Plano de Desenvolvimento

* **Fase 1:** Definição da arquitetura e escolha dos componentes.
* **Fase 2:** Desenvolvimento do código de coleta e armazenamento de dados.
* **Fase 3:** Testes com dados simulados e ajustes no código.
* **Fase 4:** Integração com sensores físicos e dashboards.

### 👥 Divisão de Responsabilidades

* **Coleta de Dados:** Marcos Fernandes
* **Armazenamento e Banco de Dados: Thiago Scutari
* **Processamento e Análise: Henrique Siqueira
* **Integração com Dashboards: Mariana Oliveira

---

## 📁 Estrutura de Pastas

```
monitoramento_enfesto/
├── src/
│   ├── main.py
│   └── banco.py
├── relatorios/
│   ├── relatorio_enfesto_1.csv
│   └── relatorio_enfesto_1.json
├── dados/
│   ├── tecidos.csv
│   └── historico_enfestos.csv
├── documentacao/
│   └── manual_de_uso.docx
├── simulacoes.db
├── requirements.txt
└── README.md
```

---

## 🔧 Como executar o projeto

### ✔️ Requisitos:

* Python 3.10+
* Biblioteca padrão do Python (`sqlite3`, `csv`, `json`, `datetime`)
* Sistema operacional: Windows/Linux/Mac

### ▶️ Passo a passo:

1. **Clone o repositório:**

```bash
git clone '***.\monitoramento_enfesto'
cd monitoramento_enfesto
```

2. **Instale as dependências:**

```bash
pip install -r requirements.txt
```

3. **Execute o programa:**

```bash
python main.py
```

---

## 🗃 Histórico de Lançamentos

***

---
