#!/usr/bin/env python3
"""
TFM Obfuscation Script
======================
Obfuscates all nvarchar (text) fields in CSV files:
  PLAN.csv -> CCP.csv -> LPA_GAM.csv -> LPA_GSM.csv

Rules:
- For each distinct value in a text column, assign {COLUMNA}_{n}
- Shared column names across files share the same mapping counter
- BOM and semicolon delimiter preserved
- Outputs obfuscated CSVs to datos_ofuscados/
- Outputs REGLA_OFUSCACION.csv with all original->obfuscated pairs
"""

import csv
import os
from collections import OrderedDict

DATA_DIR = "/workspace/projects/tfm/datos"
OUT_DIR = "/workspace/projects/tfm/datos_ofuscados"
RULES_DIR = "/workspace/projects/tfm/reglas_ofuscacion"

# Global mapping: { column_name: { original_value: obfuscated_value } }
global_mappings = OrderedDict()
# Global counter: { column_name: next_counter }
global_counts = OrderedDict()

# -----------------------------------------------------------
# Step 1: Determine nvarchar columns from type files
# -----------------------------------------------------------

def get_nvarchar_columns_ccp():
    """CCP_tipos.csv: semicolon-separated metadata table."""
    ncols = []
    with open(os.path.join(DATA_DIR, "..", "tipos_datos", "CCP_tipos.csv"), encoding="utf-8-sig") as f:
        reader = csv.reader(f, delimiter=";")
        header = next(reader)
        dtype_idx = header.index("DATA_TYPE")
        colname_idx = header.index("COLUMN_NAME")
        for row in reader:
            if len(row) > max(dtype_idx, colname_idx) and row[dtype_idx].strip() == "nvarchar":
                ncols.append(row[colname_idx].strip())
    return ncols

def get_nvarchar_columns_lpa():
    """LPA_GAM_tipos.csv / LPA_GSM_tipos.csv: same format as CCP."""
    ncols = []
    with open(os.path.join(DATA_DIR, "..", "tipos_datos", "LPA_GAM_tipos.csv"), encoding="utf-8-sig") as f:
        reader = csv.reader(f, delimiter=";")
        header = next(reader)
        dtype_idx = header.index("DATA_TYPE")
        colname_idx = header.index("COLUMN_NAME")
        for row in reader:
            if len(row) > max(dtype_idx, colname_idx) and row[dtype_idx].strip() == "nvarchar":
                ncols.append(row[colname_idx].strip())
    return ncols

def get_nvarchar_columns_plan():
    """
    PLAN_tipos.csv uses different column names than the actual CSV.
    Type file names: REFID, ITEMTID, WRKCTID, CUSTACCOUNT, etc.
    Actual CSV cols:  ORDEN, PARTNUMBER, CENTRO, CLIENTE, etc.
    Mapping by semantic equivalence for nvarchar fields.
    """
    plan_nvarchar = []
    with open(os.path.join(DATA_DIR, "..", "tipos_datos", "PLAN_tipos.csv"), encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(";")
            if len(parts) >= 3 and "nvarchar" in parts[2]:
                plan_nvarchar.append(parts[1].strip())

    mapping_name_to_csv = {
        "REFID": "ORDEN",
        "ITEMTID": "PARTNUMBER",
        "WRKCTID": "CENTRO",
        "ITEMTGROUPID": None,
        "OPRID": None,
        "CUSTACCOUNT": "CLIENTE",
        "REFTYPE": None,
        "JOBTYPE": None,
    }

    actual_nvarchar = []
    for col in plan_nvarchar:
        csv_name = mapping_name_to_csv.get(col)
        if csv_name and csv_name not in actual_nvarchar:
            actual_nvarchar.append(csv_name)

    return actual_nvarchar

# -----------------------------------------------------------
# Step 2: CSV read/write helpers
# -----------------------------------------------------------

def read_csv(path):
    """Read semicolon-delimited CSV with BOM, return (headers, rows)."""
    with open(path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=";")
        headers = reader.fieldnames
        rows = list(reader)
    return headers, rows

def write_csv(path, headers, rows):
    """Write semicolon-delimited CSV with BOM."""
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers, delimiter=";")
        writer.writeheader()
        writer.writerows(rows)

# -----------------------------------------------------------
# Step 3: Obfuscation engine
# -----------------------------------------------------------

def ensure_counter(col):
    """Initialize global counter for a column if not already present."""
    if col not in global_counts:
        global_counts[col] = 0
        global_mappings[col] = {}

def obfuscate_value(col, value):
    """Return obfuscated value for a given column+value, creating mapping if new."""
    if value in global_mappings[col]:
        return global_mappings[col][value]
    n = global_counts[col]
    obfuscated = f"{col}_{n}"
    global_mappings[col][value] = obfuscated
    global_counts[col] = n + 1
    return obfuscated

def process_file(csv_basename, nvarchar_cols):
    """Read CSV, obfuscate nvarchar columns, write obfuscated version."""
    in_path = os.path.join(DATA_DIR, csv_basename)
    out_path = os.path.join(OUT_DIR, csv_basename)

    print(f"Processing {csv_basename}...")
    headers, rows = read_csv(in_path)

    # Find which nvarchar cols actually exist in this CSV
    active_cols = [c for c in nvarchar_cols if c in headers]
    if active_cols:
        print(f"  Obfuscating {len(active_cols)} text columns: {active_cols}")

    # Handle extra text columns not in type definition but present in CSV
    # LPA files have GRUPO_RECURSO / TECNOLOGIA that appeared later
    skip_patterns = ["FECHA", "CANTIDAD", "TIEMPO", "OPERACION", "OEE",
                     "MULTIPLICIDAD", "DURACION", "PIEZAS", "POSTURA"]

    for col in headers:
        if col not in nvarchar_cols and col not in global_counts:
            is_skippable = any(pat in col.upper() for pat in skip_patterns)
            if not is_skippable:
                # Check a sample value to determine if text
                sample = rows[0][col] if rows else ""
                if sample:
                    try:
                        float(sample.replace(",", "."))
                        continue  # numeric, skip
                    except ValueError:
                        pass
                    # Text column not in type definitions - obfuscate it
                    print(f"  + Auto-detected text column: {col}")
                    ensure_counter(col)
                    if col not in active_cols:
                        active_cols.append(col)

    # Also check columns already seen in previous files (shared mapping)
    for col in headers:
        if col in global_counts and col not in active_cols:
            print(f"  + Reusing mapping for shared column: {col}")
            active_cols.append(col)

    # Ensure counters for ALL active columns (nvarchar_cols weren't
    # initialized by ensure_counter since they didn't trigger auto-detect)
    for col in active_cols:
        ensure_counter(col)

    # Perform obfuscation
    for row in rows:
        for col in active_cols:
            if col in headers:
                row[col] = obfuscate_value(col, row[col])

    write_csv(out_path, headers, rows)
    print(f"  -> Wrote {out_path} ({len(rows)} rows)")

# -----------------------------------------------------------
# Step 4: Write RULES file
# -----------------------------------------------------------

def write_rules():
    """Write REGLA_OFUSCACION.csv with all field->obfuscated pairs."""
    rules_path = os.path.join(RULES_DIR, "REGLA_OFUSCACION.csv")

    with open(rules_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["CAMPO_ORIGINAL", "VALOR_ORIGINAL", "VALOR_OFUSCADO"])

        for col, mapping in global_mappings.items():
            for orig_val, obf_val in mapping.items():
                writer.writerow([col, orig_val, obf_val])

    print(f" Rules -> {rules_path} ({sum(len(v) for v in global_mappings.values())} entries)")

# -----------------------------------------------------------
# Main
# -----------------------------------------------------------

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(RULES_DIR, exist_ok=True)

    # Determine nvarchar columns for each file
    plan_ncols = get_nvarchar_columns_plan()
    ccp_ncols = get_nvarchar_columns_ccp()
    lpa_ncols = get_nvarchar_columns_lpa()

    print(f"PLAN nvarchar cols: {plan_ncols}")
    print(f"CCP nvarchar cols: {ccp_ncols}")
    print(f"LPA nvarchar cols: {lpa_ncols}")

    # Process in required order
    process_file("PLAN.csv", plan_ncols)
    process_file("CCP.csv", ccp_ncols)
    process_file("LPA_GAM.csv", lpa_ncols)
    process_file("LPA_GSM.csv", lpa_ncols)

    # Write rules
    write_rules()

    # Summary
    print(f"\nDone. Total mappings: {sum(len(v) for v in global_mappings.values())}")
    for col, mapping in global_mappings.items():
        print(f"  {col}: {len(mapping)} distinct values obfuscated")

if __name__ == "__main__":
    main()