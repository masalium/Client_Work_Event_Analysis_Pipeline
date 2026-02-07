# Client Work: Event Analysis Pipeline

A small, practical **data pipeline** that takes a recurring events CSV and outputs clean summary tables you can use immediately for reporting.

Built for a real client workflow where the same type of dataset arrives repeatedly (monthly/weekly). The key constraint: **input categories evolve** (new event types appear), but reporting outputs must remain consistent over time.

---

## Overview

This tool replaces manual spreadsheet counting by automating:
- dataset cleaning/normalization
- grouping and aggregation
- repeatable, spreadsheet-ready summary outputs

The result is a stable workflow where the pipeline keeps working even as the data changes.

---

## What it does

- Reads event records from a CSV file
- Cleans/standardizes key fields (basic normalization suitable for reporting)
- Groups events by **DEPARTAMENTO** (and optionally MUNICIPIO if extended later)
- Produces two output tables:
  1) counts by **CATEGORIA DEL EVENTO** per department  
  2) counts by **TIPO DE EVENTO** per department (auto-includes new types)
- Exports clean CSV summary tables ready for Excel / Google Sheets

---

## Inputs

Your CSV must contain the following columns:

- `DEPARTAMENTO`
- `MUNICIPIO`
- `CATEGORIA DEL EVENTO`
- `TIPO DE EVENTO`
- `DESCRIPCION PRELIMINAR DEL EVENTO`

---

## Outputs

- `tabla_categorias_por_departamento.csv`  
  Counts of events per department by event category.

- `tabla_tipos_por_departamento.csv`  
  Counts of events per department by event type, including any new types found.

---

## How to run

### Install dependency
```bash
pip install pandas

