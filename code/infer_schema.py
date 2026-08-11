#!/usr/bin/env python3
"""
infer_schema.py

Infer a statistical schema summary from exported Wikibase JSON batches.

The script scans all exported entities and reconstructs a lightweight
class-level schema based on the configured instance-of property (`P35`).

For each detected class, the inferred schema includes observed properties, Wikibase datatypes, entity-level property coverage,
statement cardinality statistics, qualifier usage statistics, and aggregate statement counts.

The resulting schema is exported as a JSON document intended for ontology inspection and data quality assessment.

The schema is inferred empirically from the exported data rather than from
formal ontology constraints. Consequently, the output reflects actual usage
patterns present in the knowledge graph.

Processing pipeline
-------------------
1. Load all exported Wikibase batch JSON files.
2. Index entity labels for human-readable reporting.
3. Infer entity classes using the configured instance-of property.
4. Aggregate property usage statistics by class.
5. Infer property datatypes and statement cardinalities.
6. Aggregate qualifier usage statistics.
7. Export the inferred schema as JSON.

Output structure
----------------
The generated schema JSON contains, for each class:

- class label,
- entity count,
- properties observed for the class,
- property coverage statistics,
- statement cardinalities,
- qualifier statistics.
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Optional

import tarfile
import zipfile


# =============================================================================
# REPOSITORY LOCATION
# =============================================================================

def find_repository_root(start: Optional[Path] = None) -> Path:
    """
    Locate the EFFKG repository root.

    The root is identified through the principal directories distributed with
    the project. This implementation is compatible with Python 3.9.
    """
    current = (start or Path.cwd()).resolve()

    required_directories = {
        "code",
        "dataset",
        "schema",
        "source_data",
        "data_model",
        "validation",
    }

    for candidate in [current] + list(current.parents):
        try:
            existing_directories = {
                path.name
                for path in candidate.iterdir()
                if path.is_dir()
            }
        except (PermissionError, OSError):
            continue

        if required_directories.issubset(existing_directories):
            return candidate

    raise RuntimeError(
        "The EFFKG repository root could not be located. "
        "Run this script from within a cloned EFFKG repository."
    )


REPOSITORY_ROOT = find_repository_root()


# =============================================================================
# CONFIGURATION
# =============================================================================

DATASET_DIRECTORY = REPOSITORY_ROOT / "dataset"
VALIDATION_DIRECTORY = REPOSITORY_ROOT / "validation"

BATCHES_DIRECTORY = (
    DATASET_DIRECTORY
    / "exported_items_json"
)

ZIP_ARCHIVE = (
    DATASET_DIRECTORY
    / "batches_json.zip"
)

TAR_ARCHIVE = (
    DATASET_DIRECTORY
    / "batches_json.tar.gz"
)

def ensure_batches_directory() -> Path:
    """
    Ensure that the exported Wikibase JSON batches are available.

    If the extracted directory does not exist, it is created automatically
    from the distributed ZIP or TAR.GZ archive.
    """

    if BATCHES_DIRECTORY.is_dir():
        return BATCHES_DIRECTORY

    if ZIP_ARCHIVE.is_file():
        print("[INFO] Extracting {}".format(ZIP_ARCHIVE.name))

        with zipfile.ZipFile(ZIP_ARCHIVE) as archive:
            archive.extractall(BATCHES_DIRECTORY)

        return BATCHES_DIRECTORY

    if TAR_ARCHIVE.is_file():
        print("[INFO] Extracting {}".format(TAR_ARCHIVE.name))

        with tarfile.open(TAR_ARCHIVE, "r:gz") as archive:
            archive.extractall(BATCHES_DIRECTORY)

        return BATCHES_DIRECTORY

    raise FileNotFoundError(
        "Neither an extracted batch directory nor a distributed archive "
        "could be found."
    )

# Directory containing Wikibase JSON exports named batch_*.json.
BATCHES_DIR = ensure_batches_directory()

# Directory containing the inferred statistical schema.
OUTPUT_DIRECTORY = (
    VALIDATION_DIRECTORY
    / "inferred_schema"
)

OUTPUT_FILE = (
    OUTPUT_DIRECTORY
    / "inferred_schema.json"
)

# Wikibase property used to assign entities to classes.
CLASS_PROP = "P35"


# =============================================================================
# CONFIGURATION VALIDATION
# =============================================================================

if not BATCHES_DIR.is_dir():
    raise FileNotFoundError(
        "The Wikibase JSON batch directory was not found:\n"
        "  {}\n\n"
        "Place the exported batch files in "
        "dataset/exported_items_json/ or update BATCHES_DIR."
        .format(BATCHES_DIR)
    )

BATCH_FILES = sorted(
    BATCHES_DIR.glob("batch_*.json")
)

if not BATCH_FILES:
    raise FileNotFoundError(
        "No Wikibase batch files matching 'batch_*.json' were found in:\n"
        "  {}".format(BATCHES_DIR)
    )

OUTPUT_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True
)


print("EFFKG empirical schema inference")
print("--------------------------------")
print("Repository root: {}".format(REPOSITORY_ROOT))
print("Input batches: {}".format(BATCHES_DIR))
print("Batch files found: {:,}".format(len(BATCH_FILES)))
print("Output file: {}".format(OUTPUT_FILE))

PROPERTY_LABELS = {
    "P1":  "defined by",
    "P2":  "ID",
    "P3":  "belongs to administrative unit",
    "P4":  "has delimitation",
    "P5":  "plate name",
    "P6":  "flag",
    "P7":  "has ports",
    "P8":  "has demarcation",
    "P9":  "external marking",
    "P10": "registration number",
    "P11": "registration place",
    "P12": "CFR",
    "P13": "IRCS",
    "P14": "UVI",
    "P15": "MMSI",
    "P16": "LOA",
    "P17": "LBP",
    "P18": "has parent category",
    "P19": "Wikidata reference",
    "P20": "GT Tonnage",
    "P21": "other tonnage",
    "P22": "safety tonnage GTs",
    "P23": "main engine power",
    "P24": "auxiliar engine power",
    "P25": "has fishing gear category",
    "P26": "code",
    "P27": "hull material",
    "P28": "on board equipment",
    "P29": "entry into service date",
    "P30": "date of construction",
    "P31": "registration on national registry",
    "P32": "status on national registry",
    "P33": "since",
    "P34": "image",
    "P35": "instance of",
    "P36": "division of",
    "P37": "name",
    "P38": "subarea of",
    "P39": "has divisions",
    "P40": "has subareas",
    "P41": "operates at",
    "P42": "coordinates",
    "P43": "contains administrative unit",
    "P44": "date",
    "P45": "number of vessels",
    "P46": "source",
    "P47": "start date",
    "P48": "end date",
    "P49": "IMO",
    "P50": "category of",
    "P51": "has vessel category",
    "P52": "subclass of",
    "P53": "abbreviation",
    "P54": "superseded by",
    "P55": "country of registration",
    "P56": "administration responsible of registration",
    "P57": "date of destruction",
    "P58": "date of retirement",
    "P59": "segment",
    "P60": "administrated by",
}

# =========================
# MAIN
# =========================

def get_claim_values(claim_list: list) -> list[str]:
    """
    Extract raw claim values from a Wikibase statement list.

    The function reads the `mainsnak` values associated with a property
    and returns their normalized string representation. Entity references
    are returned as QIDs whenever possible.
    """
    values = []
    for statement in claim_list:
        snak = statement.get("mainsnak", {})
        if snak.get("snaktype") == "value":
            dv = snak.get("datavalue", {})
            v = dv.get("value")
            if isinstance(v, dict):
                values.append(v.get("id", str(v)))
            else:
                values.append(str(v))
    return values

def get_datatype(claim_list: list) -> str:
    """
    Infer the Wikibase datatype used by a property.

    The datatype is extracted from the first valid statement found in the
    provided claim list.
    """
    for statement in claim_list:
        dt = statement.get("mainsnak", {}).get("datatype")
        if dt:
            return dt
    return "unknown"

def get_qualifiers(claim_list: list) -> dict[str, list[int]]:
    """
    Extract qualifier usage statistics from a statement list.

    For each qualifier property, the function records how many qualifier
    values appear in each statement.
    """
    qualifier_counts: dict[str, list[int]] = defaultdict(list)
    for statement in claim_list:
        qualifiers = statement.get("qualifiers", {})
        for qprop, qsnak_list in qualifiers.items():
            qualifier_counts[qprop].append(len(qsnak_list))
    return qualifier_counts

def build_qid_labels(batches_dir: Path) -> dict[str, str]:
    """
    Build a lookup table mapping QIDs to human-readable labels.

    English labels are preferred whenever available. Spanish labels are
    used as fallback values.
    """
    labels = {}
    batch_files = sorted(batches_dir.glob("batch_*.json"))
    for batch_file in batch_files:
        data = json.loads(batch_file.read_text(encoding="utf-8"))
        for qid, entity in data.get("entities", {}).items():
            entity_labels = entity.get("labels", {})
            label = (
                entity_labels.get("en", {}).get("value")
                or entity_labels.get("es", {}).get("value")
                or qid
            )
            labels[qid] = label
    return labels

def main() -> None:
    """
    Infer a class-level statistical schema from exported Wikibase batches.

    The procedure iterates over all exported entities, groups them by class,
    aggregates property statistics, computes statement cardinalities and
    qualifier coverage metrics, and exports the resulting schema summary
    as JSON.
    """
    batch_files = sorted(BATCHES_DIR.glob("batch_*.json"))
    print(f"[INFO] {len(batch_files)} batch files found.")
    
    print("[INFO] Indexing entity labels...")
    qid_labels = build_qid_labels(BATCHES_DIR)

    schema: dict[str, dict[str, dict]] = defaultdict(lambda: defaultdict(lambda: {"datatype": "unknown", "counts": []}))
    class_entity_count: dict[str, int] = defaultdict(int)

    for i, batch_file in enumerate(batch_files):
        data = json.loads(batch_file.read_text(encoding="utf-8"))
        entities = data.get("entities", {})

        for qid, entity in entities.items():
            if entity.get("type") != "item":
                continue

            claims = entity.get("claims", {})

            class_values = get_claim_values(claims.get(CLASS_PROP, []))
            if not class_values:
                class_values = ["class"]

            for cls in class_values:
                class_entity_count[cls] += 1

                for prop, claim_list in claims.items():
                    if prop == CLASS_PROP:
                        continue
                    schema[cls][prop]["datatype"] = get_datatype(claim_list)
                    schema[cls][prop]["counts"].append(len(claim_list))
                    schema[cls][prop]["total_statements"] = (
                        schema[cls][prop].get("total_statements", 0) + len(claim_list)
                    )
                    
                    for qprop, qcounts in get_qualifiers(claim_list).items():
                        schema[cls][prop].setdefault("qualifiers", defaultdict(lambda: {"statements_with": 0, "counts": []}))
                        schema[cls][prop]["qualifiers"][qprop]["statements_with"] += len(qcounts)
                        schema[cls][prop]["qualifiers"][qprop]["counts"].extend(qcounts)

        if i % 100 == 0:
            print(f"  -> {i}/{len(batch_files)} processed batches...")

    # Calcular cardinalidades
    print("[INFO] Calculating cardinalities...")
    output = {}
    for cls, props in schema.items():
        output[cls] = {
            "label":        qid_labels.get(cls, cls), 
            "entity_count": class_entity_count[cls],
            "properties": {}
        }
        for prop, info in props.items():
            counts = info["counts"]
            n_entities = class_entity_count[cls]
            
            qualifier_summary = {}
            
            for qprop, qinfo in info.get("qualifiers", {}).items():
                n_parent_statements = sum(info["counts"])
                n_with_qualifier = qinfo["statements_with"]
                qcounts = qinfo["counts"]
                qualifier_summary[qprop] = {
                    "label":                PROPERTY_LABELS.get(qprop, qprop),
                    "statements_with":      n_with_qualifier,                                               
                    "statement_coverage":   round(n_with_qualifier / n_parent_statements, 3),             
                    "min_per_statement":    min(qcounts),
                    "max_per_statement":    max(qcounts),
                    "avg_per_statement":    round(sum(qcounts) / len(qcounts), 2),
                }
                
            output[cls]["properties"][prop] = {
                "label":       PROPERTY_LABELS.get(prop, prop),
                "datatype":    info["datatype"],
                "entities_with_prop":  len(counts),                          
                "entity_coverage":    round(len(counts) / n_entities, 3),  
                "total_statements":   info.get("total_statements", 0),          
                "min_per_entity":     min(counts),                              
                "max_per_entity":     max(counts),                              
                "avg_per_entity":     round(sum(counts) / len(counts), 2),      
                "qualifiers":         qualifier_summary,
            }

    OUTPUT_FILE.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n[OK] Inferred schema -> {OUTPUT_FILE.resolve()}")
    print(f"     Found classes: {sorted(output.keys())}")

if __name__ == "__main__":
    main()