#!/usr/bin/env python3
"""
Client Work: CSV Event Analysis Pipeline

What this script does
---------------------
This script takes a CSV file that contains individual event records and produces two clean summary tables
(counts) grouped by **department**:

1) Event Category counts by Department
2) Event Type counts by Department (including any NEW event types found in the input file)

It is designed for recurring datasets: you point it at a new CSV, run it, and it generates the same
consistent outputs every time.

Input expectations (columns)
----------------------------
Your CSV should contain these columns (case-sensitive by default):

- DEPARTAMENTO
- CATEGORIA DEL EVENTO
- TIPO DE EVENTO

Other columns may exist (e.g., MUNICIPIO, DESCRIPCION PRELIMINAR DEL EVENTO); they are ignored for the
summary outputs.

Outputs
-------
Two CSV files will be written (UTF-8 with BOM for easy Excel opening):

- tabla_categorias_por_departamento.csv
- tabla_tipos_por_departamento.csv

How to run
----------
Basic usage:

    python csv_event_analysis_pipeline.py --input "your_file.csv"

Optional:

    python csv_event_analysis_pipeline.py --input "your_file.csv" --outdir "outputs" --encoding latin1

Notes
-----
- The "official" category/type lists below control the output column order and ensure missing columns
  still appear as 0.
- If the input file contains event types not in the official list, they are automatically appended to
  the end of the output (so nothing gets dropped).
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import pandas as pd


# Default official categories (controls output column ordering)
OFFICIAL_CATEGORIES = [
    "Acciones Armadas",
    "Acciones Institucionales",
    "Hechos contra La Población",
    "Otro Tipo de Evento",
]

# Default official event types (controls output column ordering)
OFFICIAL_EVENT_TYPES = [
    "Acciones Armadas",
    "Acciones Institucionales",
    "Amenazas e Intimidaciones",
    "Atentados",
    "Homicidios",
    "MAP MUSE AEI",
    "Otro Tipo de Evento",
    "Secuestro",
    "Vinculación de NNAJ a Actividades asociadas al Conflicto Armado",
]


REQUIRED_COLUMNS = {
    "DEPARTAMENTO": "department",
    "CATEGORIA DEL EVENTO": "category",
    "TIPO DE EVENTO": "event_type",
}


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Generate summary tables (counts) by department for event categories and event types."
    )
    p.add_argument(
        "--input",
        "-i",
        required=True,
        help="Path to the input CSV file.",
    )
    p.add_argument(
        "--outdir",
        "-o",
        default=".",
        help="Directory where output CSV files will be written (default: current directory).",
    )
    p.add_argument(
        "--encoding",
        default="latin1",
        help='CSV file encoding (default: "latin1"). Common alternatives: "utf-8", "utf-8-sig".',
    )
    return p


def validate_columns(df: pd.DataFrame) -> None:
    missing = [c for c in REQUIRED_COLUMNS.keys() if c not in df.columns]
    if missing:
        available = ", ".join(df.columns.astype(str).tolist())
        msg = (
            "Input CSV is missing required column(s): "
            + ", ".join(missing)
            + "\n\nAvailable columns are:\n"
            + available
            + "\n\nFix: rename columns in your CSV to match the required names, "
              "or export the dataset again with the expected headers."
        )
        raise ValueError(msg)


def normalize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Renames required columns to internal English names.
    Keeps all rows; only the relevant columns are used for pivot tables.
    """
    df = df.rename(
        columns={
            "DEPARTAMENTO": "department",
            "CATEGORIA DEL EVENTO": "category",
            "TIPO DE EVENTO": "event_type",
        }
    )
    return df


def updated_event_type_order(df: pd.DataFrame) -> list[str]:
    """
    Returns OFFICIAL_EVENT_TYPES plus any new event types found in the input file.
    New types are appended in alphabetical order for consistent outputs.
    """
    present = [t for t in df["event_type"].dropna().unique().tolist()]
    new_types = sorted([t for t in present if t not in OFFICIAL_EVENT_TYPES])
    return OFFICIAL_EVENT_TYPES + new_types


def write_category_table(df: pd.DataFrame, out_path: Path) -> None:
    table = pd.pivot_table(
        df,
        index="department",
        columns="category",
        aggfunc="size",
        fill_value=0,
    )

    # Ensure all official categories exist as columns (even if missing in the current dataset)
    for c in OFFICIAL_CATEGORIES:
        if c not in table.columns:
            table[c] = 0

    table = table[OFFICIAL_CATEGORIES]
    table.to_csv(out_path, encoding="utf-8-sig")


def write_event_type_table(df: pd.DataFrame, out_path: Path) -> None:
    event_type_order = updated_event_type_order(df)

    table = pd.pivot_table(
        df,
        index="department",
        columns="event_type",
        aggfunc="size",
        fill_value=0,
    )

    # Ensure all expected columns exist (official + new)
    for t in event_type_order:
        if t not in table.columns:
            table[t] = 0

    table = table[event_type_order]
    table.to_csv(out_path, encoding="utf-8-sig")


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    input_path = Path(args.input).expanduser().resolve()
    outdir = Path(args.outdir).expanduser().resolve()

    if not input_path.exists():
        print(f"ERROR: input file not found: {input_path}", file=sys.stderr)
        return 2

    outdir.mkdir(parents=True, exist_ok=True)

    try:
        df = pd.read_csv(input_path, encoding=args.encoding)
        validate_columns(df)
        df = normalize_dataframe(df)

        write_category_table(df, outdir / "tabla_categorias_por_departamento.csv")
        write_event_type_table(df, outdir / "tabla_tipos_por_departamento.csv")

    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    print("Done.")
    print(f"- {outdir / 'tabla_categorias_por_departamento.csv'}")
    print(f"- {outdir / 'tabla_tipos_por_departamento.csv'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
