# Formal Concept Analysis Applied to Mortality Prediction in Heart Failure Patients

Projeto de Iniciação Científica (PUC Minas) que aplica **Análise Formal de Conceitos (FCA — Formal Concept Analysis)** à predição de mortalidade em pacientes com insuficiência cardíaca, a partir da discretização de um dataset clínico público.

## 📋 Sobre o projeto

O objetivo é investigar, por meio de FCA, quais combinações de características clínicas e demográficas estão associadas ao óbito ou à sobrevivência de pacientes com insuficiência cardíaca durante o período de acompanhamento. Para isso, os dados clínicos (originalmente contínuos) são discretizados em atributos binários com base em critérios clínicos consolidados na literatura, e então organizados em dois **contextos formais** — um para pacientes que foram a óbito e outro para sobreviventes — analisados com a ferramenta [Lattice Miner](https://sourceforge.net/projects/lattice-miner/).

Este trabalho é desenvolvido em coautoria com Julio Neves, Luis Zárate e Mark Song (PUC Minas), com submissão planejada para a conferência **HEALTHINF (SciTePress)**.

## 🗂️ Base de dados

- **Fonte:** [Heart Failure Clinical Records Dataset](https://archive.ics.uci.edu/dataset/519/heart+failure+clinical+records) (UCI Machine Learning Repository / Kaggle)
- **Origem:** 299 pacientes atendidos em 2015 no Instituto de Cardiologia de Faisalabad e no Allied Hospital (Faisalabad, Paquistão)
- **Variável-alvo:** `DEATH_EVENT` (óbito ou sobrevivência durante o acompanhamento)

## ⚙️ Metodologia

### 1. Discretização (`tabelaDiscretizada.py`)

O script converte as variáveis clínicas contínuas do dataset original em atributos binários, com base em faixas de referência da literatura médica (OMS, American Heart Association, MedlinePlus), e remove a variável `time` (tempo de acompanhamento) para evitar viés temporal na análise. Os principais critérios adotados:

| Atributo derivado | Critério | Fonte |
|---|---|---|
| `elderly` | Idade ≥ 60 anos | OMS |
| `high_cpk` | CPK > 120 mcg/L | MedlinePlus |
| `abnormal_ejection_fraction` | Fora da faixa 55–70% | American Heart Association |
| `abnormal_platelets` | Fora da faixa 150.000–400.000/µL | MedlinePlus |
| `high_serum_creatinine` | > 1,3 mg/dL (homens) / > 0,95 mg/dL (mulheres) | MedlinePlus |
| `low_serum_sodium` | < 135 mEq/L (hiponatremia) | MedlinePlus |
| `anaemia`, `diabetes`, `high_blood_pressure`, `smoking` | Já binárias no dataset original | — |
| `masculine` / `feminine` | Derivadas de `sex` | — |

O resultado é salvo em `heart_failure_fca_ready.csv`, pronto para a etapa de FCA.

### 2. Contextos formais e análise em FCA

A base discretizada é dividida em dois contextos formais (`.cex`), processados no Lattice Miner:

- `contexto_mortos.cex` — pacientes com `DEATH_EVENT = 1`
- `contexto_sobreviventes.cex` — pacientes com `DEATH_EVENT = 0`
- `coracao_contexto.cex` — contexto consolidado

A partir desses contextos são extraídas as **bases de implicação (Stem Base)**, testadas com diferentes parâmetros de suporte (10%, 15% e 20%, com confiança de 100%), gerando os resultados exportados em XML:

- `resultadoMortos10.xml`, `resultadoMortos15.xml`, `resultadoMortos20.xml`
- `resultadoSobreviventes10.xml`, `resultadoSobreviventes15.xml`, `resultadoSobreviventes20.xml`

## 📁 Estrutura do repositório

```
├── Formal_Concept_Analysis_Applied_to_Mortality_Prediction_in_Heart_Failure_Patient/
│                                       # Artigo científico (submissão HEALTHINF)
├── heart_failure_clinical_records_dataset.csv   # Dataset original
├── heart_failure_fca_ready.csv                  # Dataset discretizado, pronto para FCA
├── tabelaDiscretizada.py                        # Script de discretização
├── contexto_mortos.cex                          # Contexto formal — óbitos
├── contexto_sobreviventes.cex                   # Contexto formal — sobreviventes
├── coracao_contexto.cex                         # Contexto formal consolidado
├── resultadoMortos{10,15,20}.xml                # Stem base — óbitos (10/15/20% suporte)
├── resultadoSobreviventes{10,15,20}.xml         # Stem base — sobreviventes (10/15/20% suporte)
└── informacoes sobre a base.txt                 # Notas sobre faixas clínicas e fontes
```

## 🚀 Como executar

Pré-requisito: Python 3 com [pandas](https://pandas.pydata.org/).

```bash
pip install pandas
python tabelaDiscretizada.py
```

Isso gera o arquivo `heart_failure_fca_ready.csv`, que pode ser importado no [Lattice Miner](https://sourceforge.net/projects/lattice-miner/) para construção dos contextos formais e extração da base de implicações.

## 📄 Artigo

**"Formal Concept Analysis Applied to Mortality Prediction in Heart Failure Patients"**
Mateus Soares Gatti Vasconcellos, Julio Neves, Luis Zárate, Mark Song — PUC Minas

