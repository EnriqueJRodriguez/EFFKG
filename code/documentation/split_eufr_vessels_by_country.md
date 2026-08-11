# European Fleet Register partitioning by country

## Purpose

The `split_eufr_vessels_by_country.ipynb` notebook partitions the complete
European Fleet Register (EUFR) export into one country-specific dataset per
value of the **Country of Registration** field.

The generated files constitute the European input datasets consumed by
`prepare_consolidated_vessel_data.ipynb`, where they are reconciled with the
corresponding national vessel registries.

The notebook prepares source data only. It does not interact with Wikibase.

---

# Repository requirements

The notebook must be executed from the root of the EFFKG repository.

The repository root is detected automatically during execution.

---

# Required input file

## European Fleet Register export

**Expected location**

```text
source_data/eufr_data.csv
```

**Source resource**

European Fleet Register.

**Snapshot used for the current EFFKG release**

December 2025.

**Expected format**

Semicolon-separated CSV encoded in UTF-8.

The notebook loads every source column as a string in order to preserve:

- identifiers;
- registration numbers;
- dates;
- leading zeros;
- source formatting.

---

## Required columns

The input dataset must contain the following column:

| Column | Description |
|----------|-------------|
| `Country of Registration` | Country used to partition the complete EUFR dataset |

Additional columns are preserved unchanged in the generated country-specific
files.

---

# Processing workflow

The notebook performs the following operations:

1. loads the complete European Fleet Register export;
2. validates the presence of the country-of-registration field;
3. removes rows with missing or empty country values;
4. groups vessel records by country of registration;
5. exports one CSV file per country.

No source records are modified apart from excluding rows without a usable
country value.

---

# Country-name handling

Country values are:

- stripped of leading and trailing whitespace;
- converted into filesystem-safe filenames;
- preserved unchanged inside the exported CSV files.

Filename generation replaces characters that are invalid on common filesystems
and converts repeated whitespace into underscores.

---

# Output

The generated datasets are written to:

```text
source_data/eufr_data_by_country/
```

Each output file follows the naming convention:

```text
eufr_data_<country>.csv
```

For example:

```text
eufr_data_ESP.csv
eufr_data_FRA.csv
eufr_data_ITA.csv
```

Each generated file:

- contains only vessels registered in the corresponding country;
- preserves the original EUFR schema;
- uses semicolon-separated values;
- is encoded in UTF-8.

---

# Excluded records

Rows whose **Country of Registration** value is:

- empty;
- missing;
- composed only of whitespace;

are excluded from the exported datasets.

The notebook reports the number of excluded records during execution.

---

# Execution

Open:

```text
code/split_eufr_vessels_by_country.ipynb
```

Run all cells in order.

The notebook automatically:

- locates the repository root;
- validates the input dataset;
- creates the output directory if necessary;
- generates one country-specific CSV per country represented in the source
  dataset.

No credentials are required.

---

# Relationship with the population pipeline

This notebook prepares the European vessel datasets used during national
consolidation.

The operational workflow is:

```text
European Fleet Register
        │
        ▼
split_eufr_vessels_by_country.ipynb
        │
        ▼
eufr_data_<country>.csv
        │
        ▼
prepare_consolidated_vessel_data.ipynb
        │
        ▼
consolidated_data_<country>.csv
        │
        ▼
import_wikibase.ipynb
```

The notebook performs dataset partitioning only. Harmonisation,
cross-source reconciliation and Wikibase population are carried out by the
subsequent stages of the EFFKG pipeline.