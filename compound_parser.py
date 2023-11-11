from dataclasses import dataclass
from csv import DictWriter  
from openpyxl import load_workbook


@dataclass
class Compound:
    id: str
    pct_inhibition: float
    pf_gametocyte_ic50_avg: float
    pf_gametocyte_ic50_sd: float
    hepg2_cytotoxicity_ic50: str # ">25" is an option
    hepg2_pf_ic50_ratio: str
    pc_asexual_ic50: float


def parse_inhibition_xlsx_file(filepath):
    """
    Parses the inhibition file, which follows the repeating column format:

    <unused> | Compound | Inhibition | ...

    Args:
        filepath (str): Path to the xlsx file.
    
    Returns:    
        inhibition_dict: A dict with compound ID as keys, and inhibition values as values.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file does not follow the expected format.
    """
    inhibition_dict = {}
    wb = load_workbook(filepath)
    ws = wb.active
    for i in range(2, ws.max_column, 3): # iterate over columns in threes to match the format
        values = ws.iter_rows(min_col=i, max_col=i+1, values_only=True)
        for value in values:
            if not str(value[0]).startswith("TCMDC"): # skip rows without data in them
                continue
            if value[1] is None:
                raise ValueError("Expected inhibition value, but got None.")
            inhibition_dict[value[0]] = value[1]
    return inhibition_dict

def parse_ic50_file(filepath, inhibition_dict):
    """
    Parses the IC50 file, which follows the column format:

    TCAMS ID | Structure | <unused> |  Pf Gametocyte IC50 average | Pf Gametocyte IC50 SD | <unused> | Cytotoxicity HepG2 IC50 | <unused> | HepG2 / Pf IC50 | PC Asexual Stages IC50
    
    Args:
        filepath (str): Path to the xlsx file.
        inhibition_dict (dict): A dict with compound ID as keys, and inhibition values as values.
    
    Returns:
        compound_list: A list of Compound objects.
    """
    compound_list = []
    wb = load_workbook(filepath)
    ws = wb.active
    values = ws.iter_rows(values_only=True)
    for value in values:
        if not str(value[0]).startswith("TCMDC"):
            continue
        compound = Compound(
            id=value[0],
            pct_inhibition=inhibition_dict[value[0]],
            pf_gametocyte_ic50_avg=value[3],
            pf_gametocyte_ic50_sd=value[4],
            hepg2_cytotoxicity_ic50=value[6],
            hepg2_pf_ic50_ratio=value[8],
            pc_asexual_ic50=value[9]
        )
        compound_list.append(compound)
    return compound_list

def output_csv(compound_list, output_filepath):
    """
    Outputs the compound list as a CSV file.

    Args:
        compound_list (list): A list of Compound objects.
        output_filepath (str): Path to the output CSV file.
    """
    with open(output_filepath, "w") as f:
        writer = DictWriter(f, fieldnames=Compound.__dataclass_fields__.keys())
        writer.writeheader()
        for compound in compound_list:
            writer.writerow(compound.__dict__)

def main():
    inhibition_dict = parse_inhibition_xlsx_file("data/inhibition.xlsx")
    compound_list = parse_ic50_file("data/ic50.xlsx", inhibition_dict)
    output_csv(compound_list, "output.csv")

if __name__ == "__main__":
    main()