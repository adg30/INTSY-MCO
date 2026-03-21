# DnD 5e Monster Challenge Rating Predictor
**By:** Aaron Go, John Alonzo, Sean Olores, and Sean Cardeño  
**Dataset:** [DnD 5e Bestiary](https://5e.tools/bestiary.html)  
**Course:** STINTSY Major Project

---

## Motivation

In Dungeons & Dragons 5th Edition, *Challenge Rating* (CR) is a numerical estimate of a monster's combat difficulty. It determines whether an encounter is trivially easy or potentially lethal for a given party level. Calculating it correctly involves cross-referencing offensive output, defensive resilience, and special abilities using a multi-step formula from the Dungeon Master's Guide. This is a process that is tedious and error-prone for custom *homebrew* content.

This project trains machine learning models to predict CR directly from a monster's raw statistics. A reliable predictor lets Game Masters instantly validate homebrew balance without doing the math by hand.

## Goal

Train and evaluate three supervised machine learning models — two classical and one neural network — that can accurately predict the Challenge Rating of a D&D 5e monster given its raw stat block.

---

## Setup

> This project uses [uv](https://docs.astral.sh/uv/getting-started/installation/) as its package manager. All other dependencies are declared in [`pyproject.toml`](./pyproject.toml) and handled automatically.

1. Clone the repository
2. Run `uv sync` to install all dependencies
3. Open notebooks in VSCode or PyCharm directly (run as a kernel), or launch a browser interface with:

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
| 07 | `07_classical_models.ipynb` | Random Forest and XGBoost training and evaluation | `tuned_rf_model.pkl`, `tuned_xgb_model.pkl` |
| 08 | `08_neural_network.ipynb` | MLP training, grid search, and evaluation | `nn_tuned.pth` |
| 09 | `09_evaluation_and_conclusion.ipynb` | Unified model comparison, error analysis, and recommendation | — |

---

## Data

The raw dataset (`raw_bestiary.csv`) contains 4,454 monsters from [5eTools](https://5e.tools/index.html), a community-maintained online reference that aggregates D&D 5e rules content into a structured, searchable database. After cleaning and deduplication, the working dataset is **3,119 unique monsters** with **28 engineered features**.

Key preprocessing decisions:
- Duplicates resolved by source release priority (MM'25 > MPMM > MM'14, etc.)
- HP and AC extracted from text strings via regex; fractions in CR converted to decimals
- Monster types consolidated into top 10 + "other" via one-hot encoding
- Hit Points log-transformed to tame the right skew; ability scores Z-score standardized

---

## Models

All three models are evaluated on the same held-out test set (15%, n=468) for a fair comparison. The classical models were trained on an 80/20 split; the neural network used a 70/15/15 split with a separate validation set for early stopping.

| Model | MAE | RMSE | R² | Within ±1 CR |
|---|---|---|---|---|
| Random Forest | 0.885 | 1.355 | 0.951 | 68.8% |
| **XGBoost** | **0.850** | **1.320** | **0.954** | **70.7%** |
| MLP Neural Network | 0.907 | 1.383 | 0.949 | 70.3% |

**Recommended model: XGBoost.** Best on all three metrics, most stable at high CR tiers (CR 20+ MAE: 1.28 vs MLP's 1.80), and runs in under 2 minutes on CPU with no GPU required.

### Model details

**Random Forest** — 100 estimators, max depth 20, tuned via 5-fold GridSearchCV. Bagging ensemble handles the mixed feature types and non-linear HP–CR relationship without aggressive tuning.

**XGBoost** — 250 estimators, max depth 5, learning rate 0.1, subsample 0.8, tuned via 5-fold GridSearchCV over 16 configurations. Boosting directly targets the systematic underprediction of high-CR monsters identified in EDA. Tuning improved MAE by 0.023 over the default baseline.

**MLP Neural Network** — 3-layer feedforward network (128→64→32), dropout 0.2, batch normalization, Huber loss, trained with early stopping. Architecture and hyperparameters selected via manual grid search over 54 configurations (3 learning rates × 3 batch sizes × 3 architectures × 2 dropout rates).

---

## Key Findings

- **HP dominates.** Log-transformed HP has a 0.93 correlation with CR — survivability is the strongest single predictor.
- **All models degrade at CR 15+.** High-CR monsters derive power from offensive mechanics (damage per round, multiattack) that are buried in unstructured text and not captured by the current feature set.
- **Classical models outperform the MLP** at this dataset scale (~2,000 training samples). XGBoost's discrete decision boundaries suit the step-function nature of D&D's CR system better than continuous neural network activations.
- **Data imbalance is the main bottleneck.** 60% of monsters are CR 5 or below; only 5.3% exceed CR 19. Future work should target synthetic data generation or additional collection at high tiers.

---

## AI Use Declaration

AI tools were used by individual team members for concept understanding, debugging assistance, and brainstorming. All AI responses were validated through the team's own understanding and independent research. All code, analysis, and written interpretation was authored by the team.

**Sean Olores** — Used AI to help with regex code during data extraction, and with seaborn syntax in EDA.

**Aaron Go** — Used Claude to review the notebook against the rubric and identify gaps; used Gemini and ChatGPT to understand suggested changes and debug issues; used Claude to outline Section 9 and critique the written analysis.

**Sean Cardeño** — Used Claude to discuss the MLP architecture design, help create the manual grid search, fix gaps in the code, and validate the initial evaluation results.

**John Leomarc Alonzo** — Used Gemini to understand GridSearchCV and XGBoost, validate code and graphs, and understand notebooks written by other team members.
