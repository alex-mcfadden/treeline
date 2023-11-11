from compound_parser import (
    Compound, parse_ic50_file, parse_inhibition_xlsx_file, output_csv)
import os

class TestParser:
    def test_ic50_parser(self):
        ic50_filepath = os.path.join(os.path.dirname(__file__), "data", "ic50.xlsx")
        inhibition_filepath = os.path.join(os.path.dirname(__file__), "data", "inhibition.xlsx")
        inhibition_dict = parse_inhibition_xlsx_file(inhibition_filepath)
        compound_list = parse_ic50_file(ic50_filepath, inhibition_dict)
        assert len(compound_list) == 56
           
    def test_inhibition_parser(self):
        inhibition_filepath = os.path.join(os.path.dirname(__file__), "data", "inhibition.xlsx")
        inhibition_dict = parse_inhibition_xlsx_file(inhibition_filepath)
        assert len(inhibition_dict) == 13244
    
    def test_csv_writer(self):
        compound_list = [
            Compound(id="TCMDC-123456", pct_inhibition=99.9, pf_gametocyte_ic50_avg=1.0, pf_gametocyte_ic50_sd=0.1, hepg2_cytotoxicity_ic50=2.0, hepg2_pf_ic50_ratio=2.0, pc_asexual_ic50=3.0),
            Compound(id="TCMDC-123457", pct_inhibition=99.9, pf_gametocyte_ic50_avg=1.0, pf_gametocyte_ic50_sd=0.1, hepg2_cytotoxicity_ic50=2.0, hepg2_pf_ic50_ratio=2.0, pc_asexual_ic50=3.0),
            Compound(id="TCMDC-123458", pct_inhibition=99.9, pf_gametocyte_ic50_avg=1.0, pf_gametocyte_ic50_sd=0.1, hepg2_cytotoxicity_ic50=2.0, hepg2_pf_ic50_ratio=2.0, pc_asexual_ic50=3.0),
        ]
        output_filepath = os.path.join(os.path.dirname(__file__), "data", "output.csv")
        output_csv(compound_list, output_filepath)
        assert os.path.exists(output_filepath)
        with open(output_filepath) as f:
            lines = f.readlines()
            breakpoint()
            assert len(lines) == 4
            assert lines[0] == ",".join(Compound.__dataclass_fields__.keys()) + "\n"
            assert lines[1] == "TCMDC-123456,99.9,1.0,0.1,2.0,2.0,3.0\n"
            assert lines[2] == "TCMDC-123457,99.9,1.0,0.1,2.0,2.0,3.0\n"
            assert lines[3] == "TCMDC-123458,99.9,1.0,0.1,2.0,2.0,3.0\n"
        os.remove(output_filepath)

