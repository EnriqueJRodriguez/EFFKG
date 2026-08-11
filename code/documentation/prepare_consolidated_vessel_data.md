# Consolidated vessel data preparation

## Purpose

The `prepare_consolidated_vessel_data.ipynb` notebook prepares the harmonised
vessel datasets consumed by the EFFKG Wikibase import pipeline.

It integrates European Fleet Register records with country-specific national
fleet registries, reconciles vessels through exact CFR matches, normalises
heterogeneous source fields and exports a unified intermediate dataset matching
the schema expected by `import_wikibase.ipynb`.

The notebook prepares data only. It does not create or modify Wikibase
entities.

---

# Execution modes

Two processing modes are supported.

## `national_eu`

Combines national vessel records with the European Fleet Register.

The consolidation procedure:

1. retains every national registry record;
2. enriches national records with European Fleet Register information when an
   exact CFR match exists;
3. appends European Fleet Register records whose CFR does not appear in the
   national dataset;
4. generates reconciliation statistics after consolidation.

## `eu_only`

Processes only European Fleet Register records.

---

# Repository requirements

The notebook must be executed from the root of the EFFKG repository.

The repository root is detected automatically.

---

# Required input files

## European Fleet Register

**Expected location**

```text
source_data/eufr_data_by_country/eufr_data_<country>.csv
```

Example:

```text
source_data/eufr_data_by_country/eufr_data_ESP.csv
```

Required for both execution modes.

Expected format:

- semicolon-separated CSV;
- UTF-8 encoding.

Minimum required column:

| Column | Purpose |
|----------|---------|
| `CFR` | Primary reconciliation identifier |

Additional recognised columns include:

- MMSI
- Country of Registration
- Registration Number
- External marking
- Place of registration name
- Tonnage GT
- Other tonnage
- GTs
- LOA
- LBP
- Power of main engine
- Power of auxiliary engine
- Hull material
- Vessel Type
- Main fishing gear
- Subsidiary fishing gears
- Segment
- UVI
- IMO
- Event
- Event Start Date
- Date of entry into service
- Year of construction

Missing optional fields are automatically created as empty columns when
supported by the notebook.

---

## National registry

**Expected location**

```text
source_data/national_data_by_country/national_<country>_data.csv
```

Example:

```text
source_data/national_data_by_country/national_ESP_data.csv
```

Required only in `national_eu` mode.

Expected format:

- semicolon-separated CSV;
- UTF-8 encoding.

The current release includes a complete source mapping for Spain.

The Spanish dataset is expected to contain at least:

- CFR
- Nombre
- Estado
- Administración responsable del Registro
- Alta en RGFP
- Código
- Censo por modalidad
- Potencia
- Material del casco
- Imagen
- Puerto base

Additional columns are used whenever available.

---

# Vessel reconciliation

In `national_eu` mode, vessels are reconciled exclusively through exact CFR
equality.

The notebook does **not** perform:

- vessel-name matching;
- fuzzy matching;
- approximate identifier matching.

Records without a valid CFR remain in the consolidated dataset but are excluded
from reconciliation statistics.

National identifiers remain available as fallback identifiers for subsequent
Wikibase import.

---

# Missing CFR values

The following values are interpreted as missing identifiers:

- empty string
- `-`
- `--`
- `N/A`
- `NA`
- `NAN`
- `NONE`
- `NULL`

Leading and trailing whitespace is removed before evaluation.

---

# Harmonisation

The notebook produces a unified vessel schema by:

- aligning equivalent source fields;
- preserving distinct values originating from different sources;
- combining fishing-gear fields;
- mapping European hull-material codes to controlled labels;
- extracting destruction and retirement dates from EUFR events;
- normalising registration-place names;
- repairing common UTF-8 / Latin-1 encoding artefacts.

---

# Output

The generated dataset is written to:

```text
source_data/processed/consolidated_data_by_country/<input_mode>/
```

using the filename:

```text
consolidated_data_<country>.csv
```

Example:

```text
source_data/processed/consolidated_data_by_country/national_eu/consolidated_data_ESP.csv
```

The output:

- uses semicolon-separated values;
- is encoded in UTF-8;
- is consumed directly by `import_wikibase.ipynb`.

---

# Reconciliation statistics

When `INPUT_MODE="national_eu"`, the notebook prints a reconciliation report
including:

- national source records;
- European Fleet Register records;
- valid CFR counts;
- exact CFR matches;
- national-only CFR values;
- EUFR-only CFR values;
- total CFR union;
- overlap percentages.

These statistics are generated independently of the exported dataset and do not
modify the consolidation results.

---

# Execution

Configure:

```python
COUNTRY = "ESP"
INPUT_MODE = "national_eu"
```

Run all notebook cells in order.

The notebook automatically:

- locates the repository root;
- validates the required input files;
- creates the output directory;
- exports the consolidated dataset;
- prints reconciliation statistics.

No Wikibase credentials are required.

---

# Relationship with the population pipeline

The notebook prepares the intermediate vessel dataset used during knowledge
graph population.

The operational workflow is:

```text
National registry
European Fleet Register
        │
        ▼
prepare_consolidated_vessel_data.ipynb
        │
        ▼
consolidated_data_<country>.csv
        │
        ▼
import_wikibase.ipynb
        │
        ▼
Creation and update of vessel entities
```

The notebook performs data preparation only and never writes directly to
Wikibase.