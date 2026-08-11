[![Version Status](https://img.shields.io/badge/version-1.1.0-green.svg)](https://github.com/EnriqueJRodriguez/EFFKG)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-blue.svg)](https://creativecommons.org/licenses/by/4.0/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21885296.svg)](https://doi.org/10.5281/zenodo.21885296)

# EFFKG

This repository contains all supplementary materials — including datasets, source code, and validation artefacts — associated with the paper:

**A dataset of the European fishing fleet and maritime
infrastructure**

Submitted to [Scientific Data](https://www.nature.com/sdata/)

The **European Fishing Fleet Knowledge Graph (EFFKG)** is a semantic dataset integrating heterogeneous maritime data originating from multiple institutional layers, including international standards, European registries, and national administrative sources, within a unified semantic framework. All integrated resources were obtained from publicly accessible repositories. The knowledge graph is also deployed as a public Wikibase instance at [effkg.wikibase.cloud](https://effkg.wikibase.cloud/wiki/Main_Page).

The dataset is additionally archived on [Zenodo]()

## Table of Contents

- [Original Sources](#original-sources)
- [Knowledge Graph Scope and Data Model](#knowledge-graph-scope-and-data-model)
- [Dataset Versioning, Licensing, and Statistics](#dataset-versioning-licensing-and-statistics)
- [Reproducibility](#reproducibility)
- [Repository Structure](#repository-structure)
- [Intended Audience](#intended-audience)
- [Contact](#contact)

## Original Sources

The primary data sources and supporting resources used in the current release are grouped as follows:

* **Source categories**
  * **International standards and global datasets**
    * International Standard Statistical Classification of Fishery Vessels by Vessel Types (ISSCFV)
    * International Standard Statistical Classification of Fishing Gear (ISSCFG)
    * FAO Major Fishing Areas
    * World Port Index (WPI), providing globally standardised port identifiers and geospatial information
  * **Supranational data sources**
    * European Fleet Register, providing broad coverage of the European fishing fleet, including technical and administrative vessel information
    * List of ERS System Ports maintained by the Centre National de Surveillance des Pêches (CNSP)
  * **National data sources**
    * Spanish General Register of the Fishing Fleet (*Registro General de la Flota Pesquera*, Spain)
    * *Situación de la Flota Pesquera Española*, published by the Spanish fisheries administration
    * Instituto Geográfico Nacional (IGN) — SIGNA platform (Spain)
  * **Supporting normative resources**
    * Official Journal of the European Union, used to interpret and validate vessel-property definitions reported in the European Fleet Register

* **Document formats**: `.csv` and `.xlsx` files (e.g., vessels, ports, fishing areas), together with additional formats such as PDF and XML.
* **Geographical scope**: Europe
* **Temporal coverage**: 2005–2025
* **Languages**: English and Spanish

The integrated sources contain documentary and administrative records describing the European fishing fleet, maritime infrastructures, administrative divisions, and regulatory or international classification systems. Several sources required extensive preprocessing in order to generate machine-actionable semantic representations.

## Knowledge Graph Scope and Data Model

The dataset covers the European fishing fleet and selected components of the associated maritime infrastructure. Vessel entities are primarily derived from the European Fleet Register, which serves as the reference source to ensure comprehensive coverage of active fishing vessels at the European level.

Additional information from national administrative sources is incorporated to enrich vessel descriptions with attributes not available in supranational datasets. In the current release, detailed national-level data from Spain are included to provide extended information regarding vessel identifiers, administrative status, and operational context. These datasets are integrated as complementary semantic layers aligned with the European reference framework.

Maritime infrastructure is represented through the integration of port entities and administrative units. Port information is primarily derived from the World Port Index and complemented with European and national datasets in order to account for regional naming conventions and spatial heterogeneity.

Entities are incorporated based on their presence in at least one authoritative source and their compatibility with the unified semantic model. When multiple datasets describe the same real-world entity, records are reconciled and semantically integrated.

The dataset and its data model is designed to support incremental extension through the incorporation of additional national datasets and maritime-related domains. The current version data model:

<img src="data_model/data-model.png">


## Dataset Versioning, Licensing, and Statistics

### Version Information

* **Current version**: v1.1.0
* **Release date**: 15/05/2026
* **Last update**: 11/08/2026

### Licensing

* **Dataset license**: The dataset is distributed under the *Creative Commons Attribution 4.0 International (CC BY 4.0)* license.
* **Code license**: The source code included in this repository is distributed under the *MIT License*.

Users must comply with the corresponding licensing conditions when reusing either the data or the software components.

### Statistics (v1.1.0)

* Number of vessel entities: 188,170
* Number of port entities: 1,997
* Number of administrative units: 269
* Number of category entities: 73
* Total number of entities: 190,629
* Total number of statements: 3,707,656
* Total number of provenance references: 4,033,845

### Version History

**v1.1.0 (current release)**  
- Updated dataset release with accompanying code, documentation, validation, and reproducibility artefacts.

**v1.0.0**  
- Initial public release of the dataset.

## Reproducibility

This repository provides the data, code, documentation, and validation artefacts required to:

* Inspect the JSON and RDF representations of the released knowledge graph.
* Reproduce the source-data preprocessing and tabular consolidation workflows.
* Reproduce the CSV-to-Wikibase population workflow.
* Inspect and re-execute the knowledge graph export and validation procedures.
* Examine the Shape Expressions (ShEx), inferred schema, SPARQL validation queries, and knowledge graph statistics.

Software dependencies are fixed in `requirements.txt`. Input requirements and execution instructions for the processing workflows are documented under `code/documentation/`.

The JSON and RDF datasets correspond to the EFFKG v1.1.0 knowledge graph snapshot. The public Wikibase instance may continue to evolve as data are updated and corrected, with subsequent states frozen as new versioned releases.

## Repository Structure

## Repository Structure

* **code**: Contains the Python scripts and Jupyter notebooks implementing the main components of the EFFKG processing, population, export, and validation workflows.
   * **documentation**: Contains workflow-specific input requirements and execution instructions.

* **dataset**: Contains the released Wikibase JSON exports and RDF serialisations (Turtle format) of the knowledge graph.

* **schema**: Contains the Shape Expressions (ShEx) defining the entity structure of the dataset.

* **source_data**: Contains the original source data and processed intermediate datasets generated by the preprocessing and consolidation workflows, organised into source-specific and processing-specific subdirectories.

* **data_model**: Contains the current data model and documentation of its sources and interactions.

* **documentation**: Contains machine-readable documentation for the released dataset, including entity-class and property dictionaries, property provenance mappings, and the source-resource catalogue.

* **validation**: Contains validation and quality-assessment artefacts, including:
   * **inferred_schema**: Structural schema inferred from the exported knowledge graph.
   * **kg_statistics**: Knowledge graph statistics generated for the released snapshot.

## Intended Audience

The EFFKG is intended for:

* Blue Economy stakeholders, including researchers, policy makers, and maritime organisations.
* Semantic Web and Knowledge Graph researchers.
* The general public, as the dataset is derived from publicly accessible institutional resources.

## Contact

The EFFKG was developed by the [WESO Research Group](https://www.weso.es/).

Responsible researchers:

* **Enrique Rodriguez-Martin**, Universidad de Oviedo
* **Jorge Álvarez-Fidalgo**, Universidad de Oviedo
* **Manuel Luna**, Universidad de Oviedo
* **Jose Emilio Labra-Gayo**, Universidad de Oviedo

For inquiries, collaboration proposals, or technical issues, contact:  
`rodriguezmenrique@uniovi.es`

Alternatively, open an issue in this repository.
