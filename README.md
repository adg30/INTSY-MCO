# DnD 5e Monster Challenge Rating Predictor

**By:** Aaron Go, John Alonzo, Sean Olores, and Sean Cardeño  
**Dataset:** [DnD 5e Bestiary](https://5e.tools/bestiary.html) 
**Course:** STINTSY Major Project

---

## Motivation

In Dungeons & Dragons 5th Edition, *Challenge Rating* (CR) is a numerical estimate of a monster's combat difficulty. It determines whether an encounter is trivially easy or potentially lethal for a given party level. Calculating it correctly involves cross-referencing offensive output, defensive resilience, and special abilities using a multi-step formula from the Dungeon Master's Guide. This is a process that is tedious and error-prone for custom *homebrew* content.

This project trains machine learning models to predict CR directly from a monster's raw statistics. A reliable predictor lets Game Masters instantly validate homebrew balance without doing the math by hand.

## Goal

By the end of this project, our goal is to train and evaluate at least three supervised machine learning models (two classical models and one neural network) that can accurately predict the Challenge Rating of a D&D 5e monster given its raw stat block.

---

## Setup

> This project uses [uv](https://docs.astral.sh/uv/getting-started/installation/) as its package manager. All other dependencies are declared in [`pyproject.toml`](./pyproject.toml) and handled automatically.

1. Clone the repository
2. Run `uv sync` to install all dependencies
3. Open notebooks in VSCode or PyCharm directly (Run it as a kernel), or launch a browser interface with:
```bash
   uv run --with jupyter jupyter lab
```

---

## Notebooks

Run the notebooks in order. Each builds on the output of the previous one.

| # | Notebook | Description | Output |
|---|----------|-------------|--------|
| 01 | `01_introduction.ipynb` | Project overview, dataset description, and feature reference | — |
| 02 | `02_new_data_preparation.ipynb` | Data cleaning, deduplication by source priority, type/HP/AC extraction | `prepared_bestiary.csv` |
| 03 | `03_new_eda.ipynb` | Univariate, bivariate, and categorical analysis with visualizations | — |
| 04 | `04_new_feature_engineering.ipynb` | Ordinal encoding, one-hot encoding, binary flags, complexity scores | `engineered_bestiary.csv` |
| 05 | `05_new_preprocessing.ipynb` | Log transform, Z-score standardization, Min-Max scaling, pruning | `preprocessed_bestiary.csv` |
| 06 | `06_data_splitting.ipynb` | Stratified 80/20 and 70/15/15 train/val/test splits | `X_train.csv`, `X_test.csv`, etc. |
| 07 | `07_classical_models.ipynb` | [model 1] and [model 2] training and evaluation | — |
| 08 | `08_neural_network.ipynb` | MLP training and evaluation | — |
| 09 | `09_evaluation_and_conclusion.ipynb` | Model evaluation and conclusions | — |

---

## Data

The raw dataset (`raw_bestiary.csv`) contains 4,454 monsters from [5eTools](https://5e.tools/index.html), a community-maintained online reference that aggregates Dungeons & Dragons 5th Edition rules content into a structured, searchable database. After cleaning and deduplication, the working dataset is **3,119 unique monsters** with **28 engineered features**.


---

## Models

*(TODO: Fill in once finalized)* This section will describe the three models trained, their justifications, and a summary of their performance.

---

## AI Use Declaration

This project used AI tools for **concept understanding, exploration, and brainstorming only**, in accordance with the course AI use policy. No AI-generated code or text was directly used in the submission.

Specifically:
- **Tool used:** 
- **How it was used:** 

All AI responses were validated through the team's own understanding and independent research.
