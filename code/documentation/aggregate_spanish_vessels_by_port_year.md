# Spanish vessel statistics by port and year

## Purpose

The `aggregate_spanish_vessels_by_port_year.ipynb` notebook prepares the annual
vessel-count dataset used by the EFFKG Wikibase population pipeline.

Starting from the historical Spanish General Register of the Fishing Fleet
(RGFP), the notebook aggregates the number of active vessels by base port and
observation year and exports the resulting time series.

The generated dataset is consumed directly by
`import_wikibase.ipynb` during the `RUN_PORT_STATS` stage.

The notebook prepares data only and does not interact with Wikibase.

---

# Repository requirements

The notebook must be executed from the root of the EFFKG repository.

The repository root is detected automatically during execution.

---

# Required input file

## Historical RGFP workbook

**Expected location**

```text
source_data/rgfp_bi_excel_2006_2025_20260127.xlsx
```

**Source resource**

Spanish General Register of the Fishing Fleet (RGFP).

**Snapshot used for the current EFFKG release**

January 2026.

**Expected format**

Microsoft Excel workbook (`.xlsx`).

The notebook reads the worksheet:

```text
Datos
```

---

## Required columns

The source worksheet must contain the following columns:

| Column | Description |
|----------|-------------|
| `AÑO` | Observation year |
| `CODIGOBUQUE` | Vessel identifier (one row per vessel-year) |
| `PUERTO BASE` | Registered base port |

Additional columns may be present but are ignored.

---

# Processing workflow

The notebook performs the following operations:

1. loads the RGFP workbook;
2. validates the required source columns;
3. normalises base-port names;
4. removes incomplete records;
5. groups records by base port and observation year;
6. counts active vessels for each combination;
7. exports the aggregated dataset.

Each input row is assumed to represent one active vessel during one observation
year.

---

# Port-name normalisation

Before aggregation, base-port names are normalised by:

- removing leading and trailing whitespace;
- collapsing repeated internal whitespace;
- treating empty values as missing.

Rows lacking either the observation year or the base-port name are excluded
from the aggregation.

No additional name harmonisation or fuzzy matching is performed.

---

# Output

The generated dataset is written to:

```text
source_data/processed/stats/vessels_year_port.csv
```

The output is:

- UTF-8 encoded;
- semicolon-separated.

The exported file contains one row per:

- base port;
- observation year.

---

## Output schema

| Column | Description |
|----------|-------------|
| `PUERTO BASE` | Normalised base-port name |
| `AÑO` | Observation year |
| `NUM_BARCOS` | Number of active vessels registered at the base port during the corresponding year |

---

# Execution

Open:

```text
code/aggregate_spanish_vessels_by_port_year.ipynb
```

Run all cells in order.

The configuration cell automatically:

- locates the repository root;
- validates the input workbook;
- creates the output directory if necessary;
- exports the aggregated dataset.

No credentials are required.

---

# Relationship with the population pipeline

The generated statistics are imported during the `RUN_PORT_STATS` stage of the
Wikibase population pipeline.

The operational workflow is:

```text
Spanish General Register of the Fishing Fleet
                │
                ▼
aggregate_spanish_vessels_by_port_year.ipynb
                │
                ▼
vessels_year_port.csv
                │
                ▼
import_wikibase.ipynb
                │
                ▼
Annual vessel-count statements (P45)
qualified by observation year (P44)
```

The notebook prepares the statistical input dataset only. Creation and update
of Wikibase statements are performed exclusively by
`import_wikibase.ipynb`.