# Empirical schema inference

## Purpose

The `infer_schema.py` script infers a statistical schema from exported Wikibase
JSON batches.

Rather than relying on ontology constraints, the script analyses the populated
knowledge graph empirically and summarises the observed structural patterns for
each entity class.

The inferred schema includes:

- detected entity classes;
- observed properties;
- Wikibase datatypes;
- entity-level property coverage;
- statement cardinalities;
- qualifier usage statistics.

The resulting schema is intended for ontology inspection, structural analysis
and data quality assessment.

The script operates exclusively on exported Wikibase JSON batches. It does not
query or modify Wikibase.

---

# Repository requirements

The script must be executed from the root of the EFFKG repository.

The repository root is detected automatically.

---

# Required input

The script expects the Wikibase JSON export distributed with the repository.

The repository may contain either:

```text
dataset/batches_json.zip
```

or

```text
dataset/batches_json.tar.gz
```

Both archives contain the exported Wikibase entities organised as batch JSON
files.

---

## Automatic extraction

If the directory

```text
dataset/exported_items_json/
```

does not already exist, the script automatically extracts the first available
archive (`batches_json.zip` or `batches_json.tar.gz`) into that location.

Subsequent executions reuse the extracted directory without performing the
extraction again.

---

## Expected batch structure

After extraction, the script expects files following the pattern:

```text
dataset/exported_items_json/
    batch_0001.json
    batch_0002.json
    ...
```

Each batch corresponds to a standard Wikibase JSON entity export.

---

# Processing workflow

The script performs the following operations:

1. locate the EFFKG repository root;
2. ensure that the exported JSON batches are available;
3. index entity labels;
4. identify entity classes using the configured `instance of` property;
5. aggregate observed property usage for each class;
6. infer Wikibase datatypes;
7. calculate statement cardinality statistics;
8. analyse qualifier usage;
9. export the inferred statistical schema.

---

# Class inference

Entity classes are determined through the configured Wikibase property:

```text
P35 (instance of)
```

Entities lacking this property are assigned to a generic fallback class named:

```text
class
```

This behaviour allows every exported entity to contribute to the statistical
summary.

---

# Generated schema

The inferred schema contains, for every detected class:

- class label;
- number of entities;
- observed properties.

For every observed property, the script reports:

- property label;
- Wikibase datatype;
- entities containing the property;
- entity coverage;
- total number of statements;
- minimum statements per entity;
- maximum statements per entity;
- average statements per entity.

Whenever qualifiers are present, the schema additionally reports:

- qualifier property;
- number of qualified statements;
- qualifier coverage;
- minimum qualifiers per statement;
- maximum qualifiers per statement;
- average qualifiers per statement.

The generated schema reflects the observed contents of the exported knowledge
graph rather than the intended ontology.

---

# Output

The inferred schema is written to:

```text
validation/inferred_schema/inferred_schema.json
```

The output is formatted as human-readable JSON using UTF-8 encoding and
two-space indentation.

---

# Execution

Run:

```bash
python code/infer_schema.py
```

The script automatically:

- locates the repository root;
- extracts the JSON archive when necessary;
- loads every exported batch;
- infers the statistical schema;
- exports the resulting JSON document.

No credentials are required.

---

# Relationship with the validation workflow

The script is executed after Wikibase export.

The operational workflow is:

```text
EFFKG Wikibase instance
        │
        ▼
Exported JSON batches
        │
        ▼
infer_schema.py
        │
        ▼
inferred_schema.json
        │
        ▼
Structural validation
Shape-expression comparison
Ontology inspection
```

The inferred schema is an empirical description of the populated knowledge
graph and is intended to support validation and structural analysis. It is not
used during Wikibase population.