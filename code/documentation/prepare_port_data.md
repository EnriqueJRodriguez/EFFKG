# Port reference data preparation

## Purpose

The `prepare_port_reference_data.ipynb` notebook prepares the external
port-reference files used by the EFFKG Wikibase import pipeline and performs a
complementary overlap analysis between two port resources:

- the World Port Index (WPI);
- the *Liste des ports du système ERS avec données de position* published by
  the Centre National de Surveillance des Pêches (CNSP).

The notebook has two distinct functions.

### Operational preparation

It generates the filtered WPI and CNSP files used by
`import_wikibase.ipynb` to resolve or create vessel registration ports during
vessel ingestion.

### Cross-source analysis

It compares both prepared resources using deterministic identifier- and
name-based matching and generates analytical and audit outputs describing their
overlap.

The notebook:

1. filters the World Port Index to the configured European geographic scope;
2. normalizes WPI UN/LOCODE values and coordinates;
3. filters the CNSP dataset to European Union countries and associated overseas
   territories;
4. normalizes CNSP identifiers, coordinates and FAO fishing-area values;
5. exports the prepared WPI and CNSP files required by the Wikibase import
   pipeline;
6. compares both sources using exact UN/LOCODE correspondence;
7. compares remaining records using exact equality of normalized port names;
8. generates an analytical consolidated port-reference table;
9. exports audit files describing normalized-name matches and match-cardinality
   issues.

---

## Required input files

### World Port Index

**Expected location**

```text
source_data/wpi_ports.csv
```

**Source resource**

World Port Index, National Geospatial-Intelligence Agency.

**Snapshot used for the EFFKG release**

March 2026.

**Expected format**

Comma-separated CSV readable by `pandas.read_csv()`.

**Columns required by the notebook**

| Column | Use |
|---|---|
| `Main Port Name` | Port name used for display and normalized-name comparison |
| `UN/LOCODE` | Identifier used for exact cross-source matching |
| `Country Code` | Country name used to filter the configured European scope |
| `Region Name` | Regional context preserved for port creation |
| `Harbor Type` | Port-type information used in entity descriptions |
| `Latitude` | Port latitude in the official WPI export |
| `Longitude` | Port longitude in the official WPI export |

The notebook uses the official World Port Index export directly.

Latitude and longitude values represented in spreadsheet-style scientific
notation are converted to decimal degrees and validated against the geographic
ranges:

```text
Latitude:  -90 to 90
Longitude: -180 to 180
```

Normalized coordinates are exported in the format:

```text
latitude,longitude,precision
```

The WPI input is filtered using the country names defined in:

```text
WPI_EUROPEAN_COUNTRIES
```

---

### CNSP ERS port list

**Expected location**

```text
source_data/cnsp_ports.csv
```

**Source resource**

*Liste des ports du système ERS avec données de position*, Centre National de
Surveillance des Pêches.

**Snapshot used for the EFFKG release**

March 2026.

**Expected format**

Comma-separated CSV readable by `pandas.read_csv()`.

**Columns required by the notebook**

| Column | Use |
|---|---|
| `port_name` | Port name used for display and normalized-name comparison |
| `locode` | UN/LOCODE value used for exact matching |
| `country_code_iso2` | ISO 3166-1 alpha-2 code used for geographic filtering |
| `region` | Regional context preserved for port creation |
| `latitude` | Latitude used to construct coordinates |
| `longitude` | Longitude used to construct coordinates |
| `fao_areas` | FAO fishing-area values preserved in the prepared output |

The CNSP dataset is filtered using:

- the EU country codes listed in `EU_COUNTRIES`;
- the associated overseas-territory codes listed in
  `EU_OVERSEAS_TERRITORIES`.

The prepared CNSP file also includes the canonical source URL used by the
Wikibase import pipeline when constructing statement-level references.

---

## Operational outputs

The following files are generated in:

```text
source_data/processed/ports/
```

### `wpi_european_ports.csv`

Filtered and normalized World Port Index records for the configured European
geographic scope.

This file is consumed by:

```text
code/import_wikibase.ipynb
```

It is used when a vessel registration place cannot be resolved against an
existing Wikibase port entity. The importer may use the prepared WPI record to
create the missing port entity with its name, UN/LOCODE, coordinates, regional
context and source reference.

---

### `cnsp_ports_ue_filtered.csv`

Filtered and normalized CNSP records for EU countries and associated overseas
territories.

This file is also consumed by:

```text
code/import_wikibase.ipynb
```

It acts as a secondary port-reference source when no suitable World Port Index
record is found.

---

## Matching procedure

The analytical comparison is performed in two stages.

### 1. Exact UN/LOCODE matching

Records with non-empty UN/LOCODE values are merged when the cleaned identifier
values are identical.

UN/LOCODE normalization:

- removes internal spaces;
- converts values to uppercase;
- discards empty or header-like values.

### 2. Exact normalized-name matching

Records not matched by UN/LOCODE are compared using normalized port names.

Name normalization:

- converts text to uppercase;
- replaces punctuation with spaces;
- collapses repeated whitespace;
- removes empty or header-like values.

This stage uses exact equality of normalized names.

It does not calculate:

- edit distance;
- fuzzy similarity;
- geographic proximity;
- manually adjudicated equivalence.

---

## Analytical outputs

### Consolidated overlap table

**Directory**

```text
source_data/processed/ports/
```

#### `port_reference_overlap.csv`

Analytical combined table representing matched and unmatched WPI and CNSP
records.

This file is not imported directly into Wikibase.

The output contains:

| Column | Description |
|---|---|
| `sources` | Source markers associated with the record |
| `port_name` | Selected port name |
| `coordinates` | Coordinates in `latitude,longitude,precision` format |
| `locode` | Cleaned UN/LOCODE value |
| `country_region` | Combined country and regional context |
| `fao_areas` | FAO fishing-area values when supplied by CNSP |

---

## Audit outputs

The following files are generated in:

```text
validation/ports/
```

They are produced by `audit_port_overlap()` and do not modify the operational
prepared files or the consolidated overlap table.

### `ports_textual_matches.csv`

Records matched by exact equality of normalized port names after the
UN/LOCODE-matching stage.

### `ports_cardinality_issues.csv`

Summary of duplicated matching keys producing one-to-many or many-to-many merge
results.

The file reports:

- matching method;
- matching key;
- number of distinct CNSP source rows;
- number of distinct WPI source rows;
- number of generated merge rows;
- number of additional rows explained by match cardinality.

### `ports_cardinality_issue_rows.csv`

Detailed WPI and CNSP source rows involved in the reported cardinality issues.

---

## Execution

Open:

```text
code/prepare_port_reference_data.ipynb
```

Run all cells in order.

The configuration cell:

- locates the repository root;
- validates that the required source files exist;
- creates the operational and audit output directories;
- defines all input and output paths;
- records the source identifiers used downstream.

No credentials are required.

---

## Relationship with the Wikibase import pipeline

The notebook must be executed before vessel import when the prepared WPI and
CNSP files are not already available.

The operational sequence is:

```text
prepare_port_reference_data.ipynb
        ↓
wpi_european_ports.csv
cnsp_ports_ue_filtered.csv
        ↓
import_wikibase.ipynb
        ↓
resolution or creation of vessel registration ports
```

The analytical consolidated table and audit reports are not consumed by the
Wikibase importer.

---

## Scope

This notebook does not create Wikibase entities directly.

It prepares the port-reference inputs used by the import pipeline and separately
produces analytical outputs for assessing source overlap and matching
cardinality.