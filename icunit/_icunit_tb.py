import re
import os, sys
import json
import pandas as pd
import numpy as np
import warnings
from icunit import icunit_cnct

class icunit_tb(icunit_cnct):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _cnct_blks_gen_structure(self, gen_module, gen_instance, content):
        # create top module name and anchors
        content.append(self.json_anchor["anchor_gen_incl_imp"])
        content.append(f"module {gen_module} ();")
        #content.append(f"module {gen_module}")
        #content.append(f"(")
        #content.append(self.json_anchor["anchor_gen_port"])
        #content.append(f");")
        content.append("")
        content.append(self.json_anchor["anchor_gen_localpara"])
        content.append(self.json_anchor["anchor_gen_struct"])
        content.append(self.json_anchor["anchor_gen_wire_begin"])
        content.append(self.json_anchor["anchor_gen_wire_end"])
        content.append(self.json_anchor["anchor_gen_assign"])
        content.append("")

        # gen instances sub modules
        content.append(self.json_anchor["anchor_gen_inst_begin"])

        for instance in gen_instance:
            module_name = None
            instance_name = instance # assume the instance_name is the instance of a root module
            if self.df_gen_instance['instance_name'].isin([instance_name]).any():
                idx_list = self.df_gen_instance.index[self.df_gen_instance['instance_name'] == instance_name].tolist()
                module_name = self.df_gen_instance['module_name'][idx_list].tolist()[0] # always pick the first one
                try: # check if root module is given in filelist
                    path2module = self.json_info_filelist[module_name]
                except:
                    sys.exit(f"{module_name}, Module path is not given in filelist!!")
                print(f"Root module detected: {path2module} {instance_name}")
            else: # if not a root module name, then it is a generated module
                sys.exit(f"{module_name}, Module is not found")

            content.append(f"// Anchor {module_name} {instance_name}")
            content = content + self.run_gen_cnct_blk(path2module, instance_name, default_connect=False, doprint=False)
            content.append("")

        content.append(self.json_anchor["anchor_gen_inst_end"])

        # Customized code
        content = content + [
                "parameter CLKPERIODE = 100; // Change clk periode when needed",
                "",
                "initial clk_i = 1'b1;",
                "",
                "always #(CLKPERIODE/2.0) clk_i = !clk_i;",
                "",
                "initial begin",
                "    reset_n_i = 1'b0;",
                "    #(CLKPERIODE/3)",
                "    reset_n_i = 1'b1;",
                "end"
                ]
        content = content + [
                "// Include testcase file, don't forget to include path in filelist when do sim",
                "// `ifndef TESTCASE",
                "//     `define TESTCASE test_default.svh",
                "// `endif",
                "// `define STRINGIFY(x) `\"x`\"",
                "// `define TESTCASE_FILE ```TESTCASE``.svh // passing from simulator",
                "// `include `STRINGIFY(`TESTCASE_FILE)"
                ]
        content = content + [
                "initial begin",
                "$display(\"#################################################\");",
                "$display(\"################ Test Starts ####################\");",
                "$display(\"#################################################\");",
                "#(2000*CLKPERIODE);",
                "$display(\"#################################################\");",
                "$display(\"################ Test Stops  ####################\");",
                "$display(\"#################################################\");",
                "$finish();",
                "end"
                ]
        content.append(self.json_anchor["anchor_gen_code"])
        content.append(f"endmodule")
        content.append(f"")
        return content

    def _cnct_blks_gen_wiring(self, gen_module, gen_instance, content):
        print(f"\nStart wiring the {gen_instance} in {gen_module}")
        #print(self.df_gen_wiring)
        idx_list=[]
        for instance in gen_instance:
            idx_list = idx_list + self.df_gen_wiring.index[self.df_gen_wiring['inst_name'] == instance].tolist()

        idx_this_level = idx_list
        wiring_this_level = self.df_gen_wiring.iloc[idx_this_level].reset_index(drop=True)

        for i in range(len(wiring_this_level)): # loop to connect each port_name to cnct_name
            inst_name = wiring_this_level['inst_name'][i]
            port_name = wiring_this_level['port_name'][i]
            cnct_name = wiring_this_level['cnct_name'][i]
            cnct_type = wiring_this_level['cnct_type'][i]
            see_point = wiring_this_level['see_point'][i]
            wire_name = wiring_this_level['wire_name'][i]
            found_anchor= False
            # Find Anchor and connect the port
            for i in range(len(content)):
                if "Anchor" in content[i] and inst_name in content[i]:
                    found_anchor = True
                if found_anchor:
                    if port_name in content[i]:
                        if "()" in content[i]:
                            content[i] = content[i].replace("()", f"({cnct_name})")
                            break
                        else: # This else maybe never happens
                            warnings.warn(f"Port {port_name} in {inst_name} is already connected")
                            break
                    elif ");" in content[i]:
                        warnings.warn(f"Port {port_name} in {inst_name} is not found")
                        break
            # All should be logic as wire declared
            direction, width = self._fetch_portinfo(inst_name, port_name)
            insert_content = f"logic {width} {cnct_name};"
            content = self._find_anchor_insert(self.json_anchor['anchor_gen_wire_end'], content, insert_content)

        print(f"Finish wiring the {gen_instance} in {gen_module}")

        return content

    def _cnct_blks_gen_wiring_post(self, gen_module, gen_instance, content):
        print(f"\nStart post wiring the {gen_instance} in {gen_module}")
        for instance in gen_instance:
            instance_name = instance
            module_name = self.df_gen_instance[self.df_gen_instance['instance_name'] == instance_name]['module_name'].tolist()[0]
            df = self.dict_portinfo[module_name]
            if self.df_gen_instance['instance_name'].isin([instance_name]).any():
                found_anchor = False
                for i in range(len(content)):
                    if ("Anchor" in content[i]) and (instance_name in content[i]):
                        found_anchor = True
                    if found_anchor == True:
                        if "()" in content[i]:
                            line_split = content[i].split()
                            port_name = line_split[0].replace(".", "")
                            content[i] = content[i].replace("()", f"({port_name})")
                            direction = "logic"                            
                            width = df[df['port'] == port_name]['width'].tolist()[0]
                            if width == "1":
                                width = ""
                            width = width.replace(" ", "")
                            insert_content = f"{direction} {width} {port_name},"
                            content = self._find_anchor_insert(self.json_anchor['anchor_gen_wire_end'], content, insert_content)
                        elif ");" in content[i]:
                            break
        print(f"Finish post wiring the {gen_instance} in {gen_module}")

        return content

    def _run_gen_tb_blks(self, jsonfile, output2path, remove_anchor):
        self.gen_outpath = output2path
        # Read json file which has all connection setups
        self._read_json(jsonfile)
        # Extract the project architecture and prepare data for main process
        self._extract_archi()
        self._extract_wiring()
        self._extract_moduleinfo()
        self._extract_paravalue()
        self._extract_custmozized_code()
        # Main process, Do generation per level
        for i in range(len(self.gen_archi))[:]:
            content = []
            dict_archi = self.gen_archi[-i-1] # the gen should backward
            gen_module   = list(dict_archi.keys())[0] # the module name
            gen_instance = list(dict_archi.values())[0] # sub modules (instances) should in module
            print(f"\nStart gen block: {gen_module}. Needed sub level modules: {gen_instance}")

            # Most important steps
            content = self._cnct_blks_gen_structure(gen_module, gen_instance, content)
            content = self._cnct_blks_gen_wiring(gen_module, gen_instance, content)
            content = self._cnct_blks_gen_wiring_post(gen_module, gen_instance, content)
            content = self._cnct_blks_gen_bugfix(content)
            content = self._cnct_blks_gen_customcode(gen_module, gen_instance, content)
            content = self._cnct_blks_gen_beauty(content, remove_anchor=remove_anchor)

            # write the file
            with open(f"{self.gen_outpath}/{gen_module}.sv", "w") as f:
                for line in content:
                    f.write(f"{line}\n")

    def _run_gen_tb_blk(self, file, output2path, remove_anchor):
        pass

    def run_gen_tb(self, file, output2path, remove_anchor=True):
        if file[-4:] == "json":
            print(f"Jsonfile detected: {file}")
            self._run_gen_tb_blks(file, output2path, remove_anchor)
        elif file[-2:] == "sv":
            print(f"Module file detected: {file}")
            self._run_gen_tb_blk(file, output2path, remove_anchor)
        else:
            sys.exit(f"Path is not a jsonfile or a sv module file: {file}")

