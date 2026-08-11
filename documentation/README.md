# EFFKG Schema Documentation

This directory contains the machine-readable documentation describing the semantic model implemented in the **European Fishing Fleet Knowledge Graph (EFFKG)**. These files complement the Shape Expressions (ShEx) schemas by documenting the conceptual model, Wikibase properties, and provenance mappings used in the current release.

The documentation is intended to facilitate interpretation of the dataset, schema reuse, validation, and reproducibility.

---

# Contents

This directory contains the following files:

| File | Description |
|------|-------------|
| `effkg_property_dictionary.csv` | Complete dictionary of all Wikibase properties implemented in EFFKG. |
| `effkg_entity_classes.csv` | Documentation of the principal entity classes and their semantic relationships. |
| `effkg_property_sources.csv` | Mapping between Wikibase properties and the source datasets contributing values to each property. |

---

# Property Dictionary

**File:** `effkg_property_dictionary.csv`

This file documents every Wikibase property implemented in the current EFFKG release.

Each row corresponds to one Wikibase property.

| Column | Description |
|---------|-------------|
| `property_id` | Wikibase property identifier (e.g. `P23`). |
| `label` | English property label. |
| `definition` | Human-readable definition of the property. |
| `wikibase_datatype` | Native Wikibase datatype. |
| `unit` | Expected measurement unit, when applicable. Empty if not applicable. |
| `property_roles` | Current role of the property within Wikibase (main statement property, qualifier property, reference property, or reserved for future extensions). |
| `used_as_main_property` | Indicates whether the property is currently used in main statements. |
| `used_as_qualifier` | Indicates whether the property is currently used as a qualifier. |
| `used_as_reference_property` | Indicates whether the property is currently used as a reference property. |
| `qualifies_properties` | Statement properties that may be qualified by this property. Only applicable to qualifier properties. |
| `domain` | Subject entity class for ordinary properties, or qualified statement property for qualifier properties. |
| `range_type` | Expected value type (e.g. entity class, literal datatype, unrestricted). |
| `range_or_controlled_values` | Expected target entity class, XML datatype, or controlled vocabulary. |
| `cardinality` | Allowed multiplicity for each applicable domain. |
| `minimum_count` | Minimum permitted number of occurrences. |
| `maximum_count` | Maximum permitted number of occurrences. |
| `allowed_qualifiers` | Properties that may qualify this property. |

## Cardinality notation

Cardinality is expressed independently for each applicable domain.

| Symbol | Meaning |
|--------|---------|
| `1` | Exactly one occurrence |
| `?` | Zero or one occurrence |
| `+` | One or more occurrences |
| `*` | Zero or more occurrences |
| `unbounded` | No upper limit |

Examples:

- `FishingVessel:1` — every Fishing Vessel must have exactly one value.
- `Port:*` — a Port may have zero or more values.
- `P28:+` — qualifier cardinality expressed relative to statements using property `P28`.

Properties marked as **"Defined for future extensions"** are included in the ontology but are not instantiated in the current EFFKG release.

---

# Entity Class Dictionary

**File:** `effkg_entity_classes.csv`

This file documents the principal semantic classes represented in EFFKG.

Each row corresponds to one entity class.

| Column | Description |
|---------|-------------|
| `entityschema` | EntitySchema containing the class definition. |
| `class_name` | English class name. |
| `definition` | Human-readable class definition. |
| `parent_class` | Direct superclass, if any. |
| `instance_of_controlled_value` | Controlled value used with the `instance of` property to instantiate this class. |
| `direct_properties` | Properties directly declared for the class. |
| `inherited_properties` | Properties inherited from ancestor classes. |
| `effective_properties` | Complete set of properties available to the class after inheritance. |

---

# Property Provenance Mapping

**File:** `effkg_property_sources.csv`

This file summarises the provenance coverage of Wikibase properties.

Each row corresponds to one implemented property.

| Column | Description |
|---------|-------------|
| `property_id` | Wikibase property identifier. |
| `property_label` | English property label. |
| `source_count` | Number of source datasets contributing values to the property. |
| `sources` | Source datasets contributing values to the property. |

This mapping documents provenance at the **dataset level**. Individual statements preserve provenance using native Wikibase references.

---

# Notes

- This documentation corresponds to the released EFFKG snapshot and is generated automatically from the implemented Wikibase schema.
- Empty fields indicate that the corresponding attribute is not applicable.
- Property identifiers (`Pxx`) and entity classes correspond to the identifiers used throughout the released knowledge graph.
- The documentation complements, but does not replace, the Shape Expressions (ShEx) schemas distributed with the dataset.