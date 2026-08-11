# Knowledge graph statistics and validation

## Purpose

The `kg_statistics.ipynb` notebook generates descriptive statistics and quality
assessment reports for the populated European Fishing Fleet Knowledge Graph
(EFFKG).

The notebook executes a series of SPARQL queries against the public Wikibase
endpoint and exports reproducible CSV reports describing the structure,
coverage and consistency of the knowledge graph.

The notebook performs read-only queries. It does not modify Wikibase and does
not require authentication.

---

# Repository requirements

The notebook must be executed from the root of the EFFKG repository.

The repository root is detected automatically during execution.

---

# Endpoint configuration

The notebook queries the public EFFKG SPARQL endpoint.

Default configuration:

```text
https://effkg.wikibase.cloud/query/sparql
```

The endpoint URL is defined in the configuration section and may be modified if
the knowledge graph is deployed to another Wikibase instance.

No credentials are required.

---

# Generated reports

All reports are written to:

```text
validation/kg_statistics/
```

---

## Active vessel entities

**Output**

```text
(active vessels by class)
```

Reports the number of active vessel entities grouped by vessel class.

A vessel is considered active when it does not contain:

- a retirement date;
- a destruction date;
- the status "Baja Definitiva".

---

## Inactive vessel entities

**Output**

```text
(inactive vessels by class)
```

Reports inactive vessel entities grouped by vessel class.

A vessel is considered inactive when at least one of the following is present:

- retirement date;
- destruction date;
- status "Baja Definitiva".

---

## Items by class or category

**Output**

```text
items_by_class_or_category.csv
```

Reports:

- every class or category referenced through `instance of`;
- its parent relation (`subclass of` or `instance of`);
- the number of directly instantiated entities.

The report also includes:

- total unique classes or categories;
- total direct instance relations.

---

## Multilingual label coverage

**Output**

```text
(console report)
```

Calculates:

- entities having labels in more than one language;
- multilingual coverage over the complete knowledge graph.

---

## Category usage

**Output**

```text
category_items_second_level.csv
```

Reports:

- categories;
- parent categories;
- subcategories;
- number of entities classified in each subcategory.

---

## Statements by property

**Output**

```text
statements_by_property.csv
```

Reports the number of statements using every Wikibase property.

The report includes the total number of statements.

---

## Qualifiers by property

**Output**

```text
qualifiers_by_property.csv
```

Reports the number of qualified statements using every qualifier property.

The report includes the total number of qualified statements.

---

## References by source

**Output**

```text
references_by_source.csv
```

Counts statements referencing each canonical source resource used by EFFKG.

The current release evaluates references associated with:

- European Fleet Register;
- Spanish General Register of the Fishing Fleet;
- World Port Index;
- CNSP ERS ports;
- FAO ISSCFV;
- FAO ISSCFG;
- FAO Fishing Areas;
- SIGNA;
- BOE;
- MAPA fleet statistics.

The report includes:

- source URL;
- number of referenced statements;
- execution status;
- possible errors.

---

## Provenance coverage

**Outputs**

```text
provenance_coverage.csv
```

```text
provenance_coverage_by_property.csv
```

Reports:

- total statements;
- statements containing references;
- statements without references;
- percentage of referenced statements.

The property-level report additionally reports the same statistics for every
property individually.

---

## Identifier uniqueness

**Output**

```text
identifier_uniqueness.csv
```

Evaluates identifier uniqueness for the principal vessel identifiers:

- CFR;
- IMO;
- UVI;
- MMSI;
- Registration number;
- External marking.

For each identifier, the report includes:

- entities containing the identifier;
- distinct values;
- duplicated values;
- affected entities;
- uniqueness rates before placeholder filtering;
- uniqueness rates after placeholder filtering.

Placeholder values such as:

```text
-
--
N/A
NULL
```

are excluded from the filtered statistics.

---

## Broken Wikibase-item links

**Output**

```text
broken_wikibase_item_links.csv
```

Evaluates every WikibaseItem property and reports:

- total Wikibase-item links;
- broken links;
- percentage of broken links.

Broken links correspond to referenced entities that do not exist in the target
knowledge graph.

---

## Domain plausibility validation

**Output**

```text
domain_plausibility_validation.csv
```

Evaluates a series of domain-specific plausibility rules, including:

- positive vessel length;
- non-negative gross tonnage;
- positive engine power;
- construction date preceding entry into service;
- retirement date after entry into service;
- destruction date after construction.

For each validation rule the report provides:

- evaluated values;
- valid values;
- detected anomalies;
- validity percentage;
- anomaly percentage.

---

## Geospatial validation

**Outputs**

```text
geospatial_validation.csv
```

```text
invalid_port_coordinates.csv
```

Evaluates every port entity containing coordinates.

Coordinates are considered valid when:

- longitude lies within [-180, 180];
- latitude lies within [-90, 90].

The report includes:

- ports containing coordinates;
- valid coordinates;
- invalid coordinates;
- percentage of valid coordinates.

Invalid coordinates are exported separately for inspection.

---

# Execution

Open:

```text
code/kg_statistics.ipynb
```

Run all cells in order.

The notebook automatically:

- locates the repository root;
- connects to the configured SPARQL endpoint;
- executes all statistical and validation queries;
- exports every generated report.

No configuration is required apart from the Wikibase endpoint if another
deployment is analysed.

---

# Relationship with the EFFKG workflow

This notebook is intended for post-population assessment of the knowledge
graph.

The operational workflow is:

```text
Source datasets
        │
        ▼
Preparation notebooks
        │
        ▼
import_wikibase.ipynb
        │
        ▼
EFFKG Wikibase instance
        │
        ▼
kg_statistics.ipynb
        │
        ▼
Statistical reports and validation outputs
```

The notebook does not generate RDF data or populate Wikibase. It provides
descriptive statistics and quality assessment reports for an already populated
knowledge graph.