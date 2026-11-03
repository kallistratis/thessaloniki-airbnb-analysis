# Thessaloniki Airbnb: data cleaning

Cleaning the Inside Airbnb data for Thessaloniki (data release of 24 September 2026) with pandas.
All the work is in one notebook, `01_data_cleaning.ipynb`, written as a step-by-step report.
The plan (Sections 1–9) is in the notebook's "How this notebook is organised" cell.

## Files
- `data/`: the raw CSVs (git-ignored).
  - `listings.csv`: one row per listing, 4,961 rows, 90 columns
  - `calendar.csv`: one row per listing per day, 1,810,765 rows
  - `reviews.csv`: one row per guest review, 244,369 rows
- `data_clean/`: git-ignored. The cleaned tables are exported here (Section 9).
- `01_data_cleaning.ipynb`: the notebook.

## Environment
- Python 3.13, pandas 3.x. Text columns have dtype `str`, not `object` (e.g. `s["dtype"] == "str"`).
- The notebook runs in VS Code with Jupyter.

## Working with the data
- IMPORTANT: Never change the files in `data/` or the raw DataFrames `listings`, `calendar` and `reviews`. Every fix goes on the `_clean` copies (`listings_clean`, `calendar_clean`, `reviews_clean`).
- After reassigning a `_clean` DataFrame, update the dict too: `dataframes_clean["listings"] = listings_clean`.
- To run the same check on all three tables, loop over `dataframes` / `dataframes_clean` instead of writing three copies of a cell.
- IMPORTANT: Id columns (`id`, `listing_id`, `host_id`, `host_profile_id`, `reviewer_id`) must stay `int64`. They have up to 19 digits and float64 corrupts them. After every merge or any step that can add NaN to an id column, print the dtypes of the id columns.
- Prices are in euros, even though `price` is written with a `$` sign.
- Do not open the CSVs with Read or cat (they are 14–73 MB). Inspect them with pandas: `head()`, `sample()`, `info()`, `column_summary()`.
- When dropping rows or columns, print the shape before and after, and list what was dropped in the findings cell.

## Notebook style
- Write everything in English.
- Put a short markdown cell (one or two sentences) before each code cell, saying what the code does.
- Start a group of checks with a **Hypothesis:** cell and end it with a **Findings:** cell that gives the actual numbers.
- Take every number in a findings cell from the output above it. Never estimate or invent numbers.
- Use only pandas and numpy, one idea per cell, and plain variable names (`empty_cols`, `cols_to_drop`).
- Reuse `column_summary(df)` from Section 3 instead of writing a new summary function.

## Git
- Commit messages: `Section <n>: <what was done>`, e.g. `Section 4a: convert date columns`.
- Before committing, restart the kernel and run all cells, so that every cell has its output.
- Push only when I ask. Before pushing, show me the following and wait for my OK:
  - the branch it will go to on GitHub
  - the commits that are not on GitHub yet (e.g. `git log origin/main..HEAD --oneline`)
  - the files those commits change (e.g. `git diff --stat origin/main..HEAD`)
  - a short summary of the changes. For the notebook, describe them by section and cell (cells added, changed or deleted), not as raw JSON.
