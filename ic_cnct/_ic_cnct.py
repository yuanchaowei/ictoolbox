import re
import os, sys
import json
import pandas as pd
import numpy as np

class ic_cnct:
    def __init__(self, **kwargs):
        self.module_info = 0
        self.indent_default = kwargs.setdefault("indent_default", 4)
        self.indent = "    "    # later change
        self.debug = False

        self.gen_load_json = []
        self.gen_outpath = []
        #self.gen_content = []

        self.top_archi = []
        self.top_instances = []

        self.gen_info           = [] 
        self.gen_info_filelist  = [] 
        self.gen_archi          = [] 
        self.gen_anchor         = [] 
        self.gen_incl_imp       = [] 
        self.gen_parameter      = [] 
        self.gen_localpara      = [] 
        self.gen_struct         = [] 
        self.gen_wiring         = [] 
        self.gen_code           = []
 
    # Generation of para and ports in format .xxx(xxx)
    def gen_para_port(self, lst, default_connect):
        content = []
        try:
            str1 = self.indent + "."        # indent
            num2 = len(max(lst, key=len))   # max length port name
            str2 = ""                       # port name
            str3 = "("                      # left bracket
            num4 = 0                        # length in bracket, 0 if no default port connected
            str4 = ""                       # default port or no
            str5 = "),"                     # right bracket
            for i in range(len(lst)):
                str2 = lst[i]
                if default_connect: num4 = num2; str4 = f"{lst[i]}"
                if i == len(lst) - 1 : str5 = ")"
                content.append("%s%-*s %s%-*s%s" %(str1, num2, str2, str3, num4, str4, str5))
        except:
            #print("The \"list\" inputted to function gen_para_port is empty, propably no parameter")
            pass
        return content 

    # Extract the parameters and ports
    def get_para_port(self, path2module, detail=False):
        module_name = None
        dic_para = {'parameter': [], 'default_value': []}
        dic_port = {'direction': [], 'width': [], 'portname': []}
        with open(path2module) as file_module:
            for line in file_module:
                line = re.sub(r"//.*", "", line) # delete all contents with beginning //
                if "module" in line:
                    module_name = line.split()[1]
                elif "parameter" in line: # Get the parameters
                    line_split = line.split()
                    dic_para['parameter'].append(line_split[1])
                    try:    # if default value exists, add. Otherwise add None
                        if line[3]:
                            dic_para['default_value'].append(line_split[3])
                    except:
                        sys.exit(f"{line_split[1]} has no default value, please add!")
                elif "input" in line or "output" in line: # get port
                    if ");" in line: # the ); should be in single line
                        sys.exit(f"Please split the ); to the newline!!!")
    
                    line_split = line.split() # split with spaces
                    dic_port['direction'].append(line_split[0]) # input and ooutput is always located in first place
                    width = re.search(r"(\[.*\])", line) # find the [WIDTH:0] content and extract it
                    if width == None:
                        dic_port['width'].append("1")
                    else:
                        width = width.group()
                        dic_port['width'].append(width)
                        line = line.replace(width, "")  # delete the width for port name extraction
                    line = line.replace("input", "")
                    line = line.replace("output", "")
                    line = line.replace(",", "")
                    line_split = line.split()
                    for portname in line_split:
                        dic_port['portname'].append(portname)
                if ");" in line: # The end of module should be ");" and in new line
                    break

        if module_name == None:
            sys.exit(f"No module name from reading file")
   
        if detail:
            return module_name, dic_para, dic_port
        else:
            return module_name, dic_para['parameter'], dic_port['portname']
    
    # Connect the single module
    def cnct_blk(self, path2module, instance_name="", output2path="", default_connect=False, doprint=True):
        # get info from readfile
        module_name, para, port = self.get_para_port(path2module, detail=False)
        # set default instance name
        if instance_name == "":
            instance_name = f"i_{module_name}"
        # Add contents
        content = []
        content.append(f"{module_name} {instance_name} #(")
        content = content + self.gen_para_port(para, default_connect=True)
        content.append(f")(")
        content = content + self.gen_para_port(port, default_connect=default_connect)
        content.append(f");")
        if output2path:
            with open(output2path, "w") as f:
                for line in content:
                    f.write(f"{line}\n")
        if doprint:
            for i in content:
                print(i)
        return content

    # Connect multiple modules
    def _cnct_blks_readjson(self, jsonfile, output2path):
        f = open(jsonfile)
        self.gen_load_json = json.load(f)
        f.close()
        self.gen_outpath        = output2path

        self.gen_info           = self.gen_load_json['gen_info']
        self.gen_info_filelist  = self.gen_load_json['gen_info']['filelist']
        self.gen_archi          = self.gen_load_json['gen_archi']
        self.gen_anchor         = self.gen_load_json['gen_anchor']
        self.gen_incl_imp       = self.gen_load_json['gen_incl_imp']
        self.gen_parameter      = self.gen_load_json['gen_parameter']
        self.gen_localpara      = self.gen_load_json['gen_localpara']
        self.gen_struct         = self.gen_load_json['gen_struct']
        self.gen_wiring         = self.gen_load_json['gen_wiring']
        self.gen_code           = self.gen_load_json['gen_code']
        #if self.debug: print(self.gen_structure)

    def _extract_archi(self):
        dict_archi = self.gen_archi
        
        #
        # Explanation
        #

        # After the first loop, following dict is changed to
        # {
        #     "top_xmpl": {
        #         "xmpl_peri": {
        #             "xmpl_dsp": {
        #                 "xmpl_dsp_core": {
        #                     "xmpl_fft": "",
        #                     "xmpl_flt": "",
        #                     "xmpl_cic": ""},
        #                 "xmpl_dsp_ctrl": {
        #                     "xmpl_dsp_msf": "",
        #                     "xmpl_dsp_fsm": ""}},
        #             "xmpl_sram": ""},
        #         "xmpl_processor": {
        #             "xmpl_riscv": "",
        #             "xmpl_loongson": "",
        #             "xmpl_stone": ""}}
        # },
        # {
        #     "xmpl_peri": {
        #         "xmpl_dsp": {
        #             "xmpl_dsp_core": {
        #                 "xmpl_fft": "",
        #                 "xmpl_flt": "",
        #                 "xmpl_cic": ""},
        #             "xmpl_dsp_ctrl": {
        #                 "xmpl_dsp_msf": "",
        #                 "xmpl_dsp_fsm": ""}},
        #         "xmpl_sram": ""},
        #     "xmpl_processor": {
        #         "xmpl_riscv": "",
        #         "xmpl_loongson": "",
        #         "xmpl_stone": ""}
        # },

        # while (1):
        for i in range(10): # maxmal level is 10, safer choice than while 1
            nxt_dict_archi = {}
            module_s = list(dict_archi.keys())
            for module in module_s:
                try: # if basic module is met("real module name"), there will no keys, so skip and not append
                    next_keys = list(dict_archi[module].keys())
                    self.top_archi.append({module: next_keys})
                    nxt_dict_archi = {**nxt_dict_archi, **dict_archi[module]} 
                except:
                    #dict_single = {module: dict_archi[module]}
                    #nxt_dict_archi = {**nxt_dict_archi[0], **dict_single}
                    self.top_instances.append([module, dict_archi[module]])
                    pass
            dict_archi = nxt_dict_archi # The dict is updated in each loop, process shown above
            if dict_archi == {}:
                break

        self.top_instances = pd.DataFrame(np.array(self.top_instances), columns=['instance_name', 'module_name'])
        print("\nConnections in each level:")
        for i in range(len(self.top_archi)):
            print(f"Level Connections No.{i+1}: {self.top_archi[i]}")
        print("\nBasic instances and its root module:")
        print(self.top_instances)
        #print(self.top_archi)

    def _extract_wiring(self):
        wiring = np.array(self.gen_wiring)
        self.gen_wiring = pd.DataFrame(wiring[1:], columns=wiring[0])
        #print(self.gen_wiring)
        #
        # The "port_name" is "not necessary" to avoid the duplication in different instances.
        #       Because the code will avoid wrong location. The connection will find "Anchor".
        # The port names in "cnct_name" with "see_point" MUST have no duplicaton!!! 
        #       Becasue there will be no code and no locating by "Anchor"
        #
        
        # Find all index with wire_name
        idx_list = self.gen_wiring.index[self.gen_wiring['wire_name'] != ""].tolist()
        #print(idx_list)
        #idx_list = self.gen_wiring.index[(self.gen_wiring['see_point'] != "NONE") & (self.gen_wiring['see_point'] != "")].tolist()
        #print(idx_list)
        # Get the new dataframe
        df = self.gen_wiring.iloc[idx_list].reset_index(drop=False)
        # Check duplication
        for i in range(len(df)):
            if df['cnct_name'][i] in df['cnct_name'][1 + i:].tolist():
                sys.exit(f"In \"cnct_name\" port name {df['cnct_name'][i]} is duplicated.")



    def _cnct_blks_main(self):
        for idx in range(len(self.top_archi))[:]:
            content = []
            dict_blk = self.top_archi[-idx-1] # the gen should backward
            gen_module_name = list(dict_blk.keys())[0] # the module name
            gen_sub_lvl_modules = list(dict_blk.values())[0] # sub modules (instances) should in module
            print(f"\nStart gen block: {gen_module_name}. Needed sub level modules: {gen_sub_lvl_modules}")

            # create top module name and anchors
            content.append(self.gen_anchor["anchor_gen_incl_imp"])
            content.append(f"module {gen_module_name} #(")
            content.append(self.gen_anchor["anchor_gen_parameter"])
            content.append(f")(")
            content.append(self.gen_anchor["anchor_gen_port"])
            content.append(f");\n")

            # gen instances sub modules
            for i in range(len(gen_sub_lvl_modules)):
                instance_name = gen_sub_lvl_modules[i]
                # check if is a root module name
                if self.top_instances['instance_name'].isin([instance_name]).any():#.any():
                    idx_instance = self.top_instances.index[self.top_instances['instance_name'] == instance_name].tolist()
                    module_name = self.top_instances['module_name'][idx_instance].tolist()[0]
                    try: # check if root module is given in filelist
                        path2module = self.gen_info_filelist[module_name]
                    except:
                        sys.exit(f"{module_name}, Module path is not given in filelist!!")
                    print(f"Root module detected: {path2module} {instance_name}")
                else: # if not a root module name, then it is a generated module
                    module_name   = instance_name
                    instance_name = f"i_{module_name}"
                    if os.path.isfile(f"{self.gen_outpath}/{module_name}.sv"): # check if module already generated
                        path2module = f"{self.gen_outpath}/{module_name}.sv"
                    else:
                        sys.exit(f"{module_name}, Module is not correctly generated!!")
                    print(f"Gen  module detected: {path2module} {instance_name} ")

                # instantiation
                content.append(f"// Anchor {instance_name}")
                content = content + self.cnct_blk(path2module, instance_name, default_connect=False, doprint=False)
                content.append(f"\n")

            # endmodule
            content.append(f"endmodule")

            # wiring - most important part
            content = self._cnct_blks_wiring(gen_module_name, gen_sub_lvl_modules, content)

            # write the file
            with open(f"{self.gen_outpath}/{gen_module_name}.sv", "w") as f:
                for line in content:
                    f.write(f"{line}\n")

    def _cnct_blks_wiring_get_width(self, path2module, port_name):
        pass

    def _cnct_blks_wiring(self, wiring_module, wiring_instances, wiring_content):
        print(f"\nStart wiring the {wiring_instances} in {wiring_module}")
        #print(self.gen_wiring)
        idx_list=[]
        for instance in wiring_instances:
            idx_list = idx_list + self.gen_wiring.index[self.gen_wiring['module_name'] == instance].tolist()

        idx_this_level = idx_list
        idx_low_level = self.gen_wiring.index[self.gen_wiring['see_point'] == wiring_module].tolist()
        #print(idx_this_level, idx_low_level)

        wiring_this_level = self.gen_wiring.iloc[idx_this_level].reset_index(drop=True)
        wiring_low_level  = self.gen_wiring.iloc[idx_low_level].reset_index(drop=True)
        #print(wiring_this_level)
        #print(wiring_low_level)

        for i in range(len(wiring_this_level)):
            module_name = wiring_this_level['module_name'][i]
            port_name   = wiring_this_level['port_name'][i]
            cnct_name   = wiring_this_level['cnct_name'][i]
            cnct_type   = wiring_this_level['cnct_type'][i]
            see_point   = wiring_this_level['see_point'][i]
            wire_name   = wiring_this_level['wire_name'][i]

        #for item in module_name:
        #    pass


        return wiring_content




    def cnct_blks(self, jsonfile, output2path, debug=False):
        self.debug = debug
        # Read json file which has all connection setups
        self._cnct_blks_readjson(jsonfile, output2path)
        # Extract the project architecture, important setp for auto-connection
        self._extract_archi()
        self._extract_wiring()
        # Connect blocks
        self._cnct_blks_main()

