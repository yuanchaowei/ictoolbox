import re
import os, sys
import json
import pandas as pd
import numpy as np
import warnings

# ########################################################
# ########################################################
class icrf_gen:
    def __init__(self, **kwargs):
        self.json_data = []

        self.json_info              = [] 
        self.json_anchor            = [] 
        self.json_reg32b            = [] 
        self.json_customized_code   = []

        self.gen_outpath        = []
        self.dict_portinfo      = {}
        self.dict_parainfo      = {}
        self.df_paravalue       = []
        self.df_customized_code = []

    def _read_json(self, jsonfile):
        f = open(jsonfile)
        self.json_data = json.load(f)
        f.close()
        self.json_info                  = self.json_data['gen_info']
        self.json_anchor                = self.json_data['gen_anchor']
        self.json_reg32b                = self.json_data['gen_reg32b']
        self.json_customized_code       = self.json_data['gen_customized_code']
        print(self.json_info)

    # Common function: _find_anchor_insert to insert a line to an anchor position
    def _find_anchor_insert(self, anchor, content, insert_content):
        for i in range(len(content)):
            if anchor in content[i]:
                content.insert(i, insert_content)
                break
        return content

    def _extract_reg32b(self):

        pass

    def _extract_custmozized_code(self):
        pass

    def _icrf_gen_structure(self, content):
        content.append(f"module {self.json_info['regfile_name']} (")
        content.append(self.json_anchor["anchor_gen_port"])
        content.append(f");")
        content.append("")
        content.append(self.json_anchor["anchor_gen_para"])
        content.append(self.json_anchor["anchor_gen_wire"])
        content.append(self.json_anchor["anchor_gen_pack"])
        content.append(self.json_anchor["anchor_gen_write"])
        content.append(self.json_anchor["anchor_gen_read"])
        content.append(self.json_anchor["anchor_gen_crc"])
        content.append(self.json_anchor["anchor_gen_error"])
        content.append(self.json_anchor["anchor_gen_code"])
        content.append("")
        content.append(f"endmodule")
        content.append(f"")
        return content

    def _icrf_gen_reg32b(self, content):
        return content

    def _icrf_gen_customcode(self, content):
        return content

    def _icrf_gen_beauty(self, content, remove_anchor):
        return content


    def run_gen(self, jsonfile, output2path, remove_anchor=True):
        # Read json file which has all connection setups
        self._read_json(jsonfile)
        self.gen_outpath = output2path
        # Extract the project architecture and prepare data for main process
        self._extract_reg32b()
        self._extract_custmozized_code()
        # Main process, Do generation per level
        content = []
        print(f"\nStart gen filelist: {self.json_info['regfile_name']}.sv")

        content = self._icrf_gen_structure(content)
        content = self._icrf_gen_reg32b(content)
        content = self._icrf_gen_customcode(content)
        content = self._icrf_gen_beauty(content, remove_anchor=remove_anchor)

        # write the file
        with open(f"{self.gen_outpath}/{self.json_info['regfile_name']}.sv", "w") as f:
            for line in content:
                f.write(f"{line}\n")




