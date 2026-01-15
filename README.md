#Client Work: Event Analysis Pipeline

This project is a small, practical tool that takes a CSV file containing event records and turns it into clear summary tables you can use immediately.

It was built for a real client workflow where the same type of dataset arrives repeatedly (monthly / weekly), and the goal is to reduce manual counting and keep outputs consistent over time—even when new event types appear.

WHAT THIS TOOL DOES
- Reads event data from a CSV file
- Groups events by Department
- Counts occurrences by Event Category and Event Type
- Automatically detects new event types and includes them in the output
- Exports clean CSV summary tables ready for Excel or Google Sheets

INPUT REQUIREMENTS
Your CSV file must contain the following columns:
- DEPARTAMENTO
- MUNICIPIO
- CATEGORIA DEL EVENTO
- TIPO DE EVENTO
- DESCRIPCION PRELIMINAR DEL EVENTO

OUTPUT FILES
1. tabla_categorias_por_departamento.csv
   Counts of events per department by event category.

2. tabla_tipos_por_departamento.csv
   Counts of events per department by event type, including any new types found.

HOW TO RUN
1. Install dependencies:
   pip install pandas

2. Run the script:
   python csv_event_analysis_pipeline.py --input your_file.csv

Optional arguments:
--outdir   Choose output directory
--encoding Specify file encoding (e.g. latin1)

EXAMPLE
python csv_event_analysis_pipeline.py --input "Clean data for this month(Sheet1).csv" --outdir results --encoding latin1

NOTES
- New event types are automatically added to outputs.
- Outputs are UTF-8 encoded and spreadsheet-friendly.
- This tool produces count-based summaries, not advanced analytics.

TECHNOLOGIES
Python 3
Pandas
