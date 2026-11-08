# Airbnb Thessaloniki: data cleaning and EDA

Cleaning and exploratory analysis of the [Inside Airbnb](https://insideairbnb.com/get-the-data/) data for Thessaloniki, Central Macedonia, Greece: about 5,000 listings, their calendar for the next year and about 244,000 guest reviews.

## Status

Cleaning done, EDA next.

| notebook | what it does | status |
|---|---|---|
| `01_data_cleaning.ipynb` | Audits the three tables and writes the cleaned versions to `data_clean/` | Done |
| EDA notebook | Exploratory analysis of the cleaned tables | Next |

## What the cleaning notebook covers

The grain of each table, dtypes, empty and constant columns, missing values by group, keys and duplicates, referential integrity, cross-table consistency (the summary columns of `listings` recomputed from `calendar` and `reviews`), value ranges, typos and date order.

No row is dropped and no value is filled in. Values that cannot be true are marked with flag columns instead of being changed. The summary at the end of the notebook lists what was changed, what was left alone and what the analysis has to keep in mind.

## Data

Source: [Inside Airbnb](https://insideairbnb.com/get-the-data/), Thessaloniki, data release of 24 September 2026, licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

## Running it

1. From the Thessaloniki section of the Inside Airbnb *Get the Data* page, download `listings.csv.gz` (the detailed listings), `calendar.csv.gz` and `reviews.csv.gz`. Unzip them into `data/` as `listings.csv`, `calendar.csv` and `reviews.csv`.
2. Install the dependencies, preferably in a virtual environment.
   ```
   pip install -r requirements.txt
   ```
3. Run `01_data_cleaning.ipynb` top to bottom. It writes the cleaned tables as parquet to `data_clean/`.

Built with Python 3.13 and pandas 3. `data/` and `data_clean/` are not tracked by git.

## Repository layout

```
01_data_cleaning.ipynb   cleaning notebook
geo.py                   haversine distance in km, used in the notebooks
requirements.txt         pandas, numpy, pyarrow
CLAUDE.md, .claude/      instructions and hooks for Claude Code, used while writing the notebook
data/                    raw Inside Airbnb CSVs (not tracked)
data_clean/              cleaned tables as parquet (not tracked, rebuilt by the notebook)
```
