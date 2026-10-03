# IMPPAT Database Automated Scraper

A Python-based database scraping project built to systematically extract, clean, and structure phytochemical data from the IMPPAT (Indian Medicinal Plants, Phytochemistry And Therapeutics) web portal.

## 📊 Project Overview

| Overview | Description |
| :--- | :--- |
| **What the Project Is** | A database scraping project designed to extract large-scale phytochemical compound records from a specialized medicinal database. |
| **What It Does** | • Systematically navigates the IMPPAT web database to scrape phytochemical records.<br>• Extracts critical 2D/3D chemical identifiers including **SMILES**, **InChI**, **InChIKey**, and **DeepSMILES**.<br>• Cleans and compiles the unstructured web data into a single, structured `.csv` format. |
| **Data Source** | The **IMPPAT database** (Indian Medicinal Plants, Phytochemistry And Therapeutics). |
| **Results & Insights** | Successfully scraped and structured **~190,000 phytochemical records** into a comprehensive `imppat_all_plants.csv` file, providing analysis-ready data for downstream machine learning pipelines. |

## 📂 Output Format

The scraper outputs a clean, relational CSV file containing the following structured features for nearly 190,000 scraped records:

* `Selected plant from drop-down:` (Botanical source name)
* `Processed Phytochemical Name` (Standardized IMPPHY ID)
* `Plant part` (e.g., flower, root, leaf)
* `Phytochemical name` (Common chemical name)
* `SMILES` (Simplified Molecular-Input Line-Entry System)
* `InChI` (International Chemical Identifier)
* `InChIKey` (Hashed InChI)
* `DeepSMILES` (Optimized SMILES for machine learning)
* `References` (Source literature/ISBN)


 

