import csv
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font

ROOT_DIR = Path(__file__).resolve().parents[1]
SOURCE_PATH = ROOT_DIR / "schemas" / "schema_mapping.csv"
OUTPUT_PATH = ROOT_DIR / "schemas" / "schema_mapping.xlsx"


def create_workbook() -> None:
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Schema Mapping"

    with SOURCE_PATH.open(newline="", encoding="utf-8") as source_file:
        for row_index, row in enumerate(csv.reader(source_file), start=1):
            for column_index, value in enumerate(row, start=1):
                cell = worksheet.cell(row=row_index, column=column_index, value=value)
                cell.alignment = Alignment(wrap_text=True, vertical="top")
                if row_index == 1:
                    cell.font = Font(bold=True)

    worksheet.freeze_panes = "A2"
    worksheet.auto_filter.ref = worksheet.dimensions
    worksheet.column_dimensions["A"].width = 24
    worksheet.column_dimensions["B"].width = 16
    worksheet.column_dimensions["C"].width = 12
    worksheet.column_dimensions["D"].width = 48
    worksheet.column_dimensions["E"].width = 24
    worksheet.column_dimensions["F"].width = 18
    worksheet.column_dimensions["G"].width = 24
    worksheet.row_dimensions[1].height = 32
    workbook.save(OUTPUT_PATH)


if __name__ == "__main__":
    create_workbook()
