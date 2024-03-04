import re
import os, sys
import json
import pandas as pd
import numpy as np
import warnings

class ic_cnct:
    def __init__(self, **kwargs):
        self.indent_default = kwargs.setdefault("indent_default", 4)
        self.indent = "    "    # later change
        self.debug = False

        self.json_data = []

        self.json_info          = [] 
        self.json_info_filelist = [] 
        self.json_archi         = [] 
        self.json_anchor        = [] 
        self.json_incl_imp      = [] 
        self.json_parameter     = [] 
        self.json_localpara     = [] 
        self.json_struct        = [] 
        self.json_wiring        = [] 
        self.json_code          = []

        self.gen_outpath        = []
        self.gen_archi          = []
        self.gen_instance       = []
        self.df_gen_instance    = []
        self.df_gen_wiring      = []
        self.dict_portinfo      = {}
        self.dict_parainfo      = {}
        self.df_paravalue       = []



 
    # Generation of para and ports in format .xxx(xxx)
    def _gen_para_port(self, lst, default_connect):
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
            #print("The \"list\" inputted to function _gen_para_port is empty, propably no parameter")
            pass
        return content 

    # Extract the parameters and ports
    def get_para_port(self, path2module):
        module_name = None
        dict_para = {'parameter': [], 'default_value': []}
        dict_port = {'direction': [], 'width': [], 'port': []}
        with open(path2module) as file_module:
            for line in file_module:
                line = re.sub(r"//.*", "", line) # delete all contents with beginning //
                if "module" in line:
                    module_name = line.split()[1]
                elif "parameter" in line: # Get the parameters
                    line_split = line.split()
                    dict_para['parameter'].append(line_split[1])
                    try:    # if default value exists, add. Otherwise add None
                        if line[3]:
                            dict_para['default_value'].append(line_split[3])
                    except:
                        sys.exit(f"{line_split[1]} has no default value, please add!")
                elif "input" in line or "output" in line: # get port
                    if ");" in line: # the ); should be in single line
                        sys.exit(f"Please split the ); to the newline!!!")
    
                    line_split = line.split() # split with spaces
                    dict_port['direction'].append(line_split[0]) # input and ooutput is always located in first place
                    width = re.search(r"(\[.*\])", line) # find the [WIDTH:0] content and extract it
                    if width == None:
                        dict_port['width'].append("1")
                    else:
                        width = width.group()
                        dict_port['width'].append(width)
                        line = line.replace(width, "")  # delete the width for port name extraction
                    line = line.replace("input", "")
                    line = line.replace("output", "")
                    line = line.replace(",", "")
                    line_split = line.split()
                    for port in line_split:
                        dict_port['port'].append(port)
                if ");" in line: # The end of module should be ");" and in new line
                    break

        if module_name == None:
            sys.exit(f"No module name from reading file")
        df_para = pd.DataFrame.from_dict(dict_para)
        df_port = pd.DataFrame.from_dict(dict_port)
        return module_name, df_para, df_port
    
    # Connect the single module
    def cnct_blk(self, path2module, instance_name="", output2path="", default_connect=False, doprint=True):
        # get info from readfile
        module_name, df_para, df_port = self.get_para_port(path2module)
        lst_para = list(df_para['parameter'])
        lst_port = list(df_port['port'])

        # set default instance name
        if instance_name == "":
            instance_name = f"i_{module_name}"
        # Add contents
        content = []
        if lst_para == []: # if no para
            content.append(f"{module_name} {instance_name}")
            content = content + self._gen_para_port(lst_para, default_connect=default_connect)
            content.append(f"(")
        else:
            content.append(f"{module_name} {instance_name} #(")
            content = content + self._gen_para_port(lst_para, default_connect=default_connect)
            content.append(f")(")
        content = content + self._gen_para_port(lst_port, default_connect=default_connect)
        content.append(f");")
        if output2path:
            with open(output2path, "w") as f:
                for line in content:
                    f.write(f"{line}\n")
        if doprint:
            for line in content:
                print(line)
        return content

    # Connect multiple modules
    def _cnct_blks_readjson(self, jsonfile, output2path):
        f = open(jsonfile)
        self.json_data = json.load(f)
        f.close()
        self.gen_outpath        = output2path

        self.json_info           = self.json_data['gen_info']
        self.json_info_filelist  = self.json_data['gen_info']['filelist']
        self.json_archi          = self.json_data['gen_archi']
        self.json_anchor         = self.json_data['gen_anchor']
        self.json_incl_imp       = self.json_data['gen_incl_imp']
        self.json_parameter      = self.json_data['gen_parameter']
        self.json_localpara      = self.json_data['gen_localpara']
        self.json_struct         = self.json_data['gen_struct']
        self.json_wiring         = self.json_data['gen_wiring']
        self.json_code           = self.json_data['gen_code']
        #if self.debug: print(self.json_structure)

    def _extract_archi(self):
        dict_archi = self.json_archi
        
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

        for i in range(10): # maxmal level is 10, safer choice than while 1
            nxt_dict_archi = {}
            for module in list(dict_archi.keys()):
                try: # if basic module is met("real module name"), there will no keys, so skip and not append
                    next_keys = list(dict_archi[module].keys())
                    self.gen_archi.append({module: next_keys})
                    nxt_dict_archi = {**nxt_dict_archi, **dict_archi[module]} 
                except:
                    #dict_single = {module: dict_archi[module]}
                    #nxt_dict_archi = {**nxt_dict_archi[0], **dict_single}
                    self.gen_instance.append([module, dict_archi[module]])
                    pass
            dict_archi = nxt_dict_archi # The dict is updated in each loop, process shown above
            if dict_archi == {}:
                break

        self.df_gen_instance = pd.DataFrame(np.array(self.gen_instance), columns=['instance_name', 'module_name'])
        print("\nConnections in each level:")
        for i in range(len(self.gen_archi)):
            print(f"Level Connections No.{i+1}: {self.gen_archi[i]}")
        print("\nBasic instances and its root module:")
        print(self.df_gen_instance)

    def _extract_wiring(self):
        self.df_gen_wiring = pd.DataFrame(self.json_wiring[1:], columns=self.json_wiring[0])
        #
        # The "port_name" is "not necessary" to avoid the duplication in different instances.
        #       Because the code will avoid wrong location. The connection will find "Anchor".
        # The port names in "cnct_name" with "see_point" MUST have no duplicaton!!! 
        #       Becasue there will be no code and no locating by "Anchor"
        #       So the cnct_name must be 
        #
        
        #
        # Check duplication of "cnct_name"
        #

        # Find all index with wire_name, connection in higher level
        #idx_list = self.df_gen_wiring.index[(self.df_gen_wiring['see_point'] != "NONE") & (self.df_gen_wiring['see_point'] != "")].tolist()
        idx_list = self.df_gen_wiring.index[self.df_gen_wiring['wire_name'] != ""].tolist()
        # Combine them to new dataframe
        df = self.df_gen_wiring.iloc[idx_list].reset_index(drop=False)
        # Check cnct_name duplications in the new dataframe
        for i in range(len(df)):
            if df['cnct_name'][i] in df['cnct_name'][1 + i:].tolist():
                sys.exit(f"In \"cnct_name\" port name {df['cnct_name'][i]} is duplicated.")

    def _extract_moduleinfo(self):
        # Only need the filelist in json file. extract the para and port names
        for module in list(self.json_info_filelist.keys()):
            path2module = self.json_info_filelist[module]
            module_name, df_para, df_port = self.get_para_port(path2module)
            if module_name != module:
                sys.exit(f"In json filelist, module name {module} is not match to the module name {module_name} in {path2module}")
            self.dict_portinfo = {**self.dict_portinfo, **{module_name: df_port}}
            self.dict_parainfo = {**self.dict_parainfo, **{module_name: df_para}} # out used actualy
        #print(self.dict_portinfo)

    def _extract_paravalue(self):
        # extract all para in cnct_type
        idx_list = self.df_gen_wiring.index[self.df_gen_wiring['cnct_type'] == "para"].tolist()
        self.df_paravalue = self.df_gen_wiring.iloc[idx_list].reset_index(drop=False)
        print(self.df_paravalue)

    def _fetch_portinfo(self, inst_name, port_name):
        module_name = self.df_gen_instance['module_name'][self.df_gen_instance['instance_name'] == inst_name].tolist()[0]
        df_portinfo = self.dict_portinfo[module_name]
        direction   = df_portinfo['direction'][df_portinfo['port'] == port_name].tolist()[0]
        width       = df_portinfo['width'][df_portinfo['port'] == port_name].tolist()[0]
        for i in range(len(self.df_paravalue)):
            para_inst  = self.df_paravalue['inst_name'][i]
            para_name  = self.df_paravalue['port_name'][i]
            para_value = self.df_paravalue['cnct_name'][i]
            if (para_name in width) and (para_inst == inst_name):
                #print(para_inst, inst_name)
                width = width.replace(para_name, para_value)
        if width == "1":
            width = ""
        #print(direction, width)
        return direction, width

    def __find_anchor_insert(self, anchor, content, insertion):
        for i in range(len(content)):
            if anchor in content[i]:
                content.insert(i, insertion)
                break
        return content

    def _cnct_blks_wiring(self, gen_module, gen_instance, content):
        print(f"\nStart wiring the {gen_instance} in {gen_module}")
        #print(self.df_gen_wiring)
        idx_list=[]
        for instance in gen_instance:
            idx_list = idx_list + self.df_gen_wiring.index[self.df_gen_wiring['inst_name'] == instance].tolist()

        idx_this_level = idx_list
        idx_low_level = self.df_gen_wiring.index[self.df_gen_wiring['see_point'] == gen_module].tolist()
        #print(idx_this_level, idx_low_level)

        wiring_this_level = self.df_gen_wiring.iloc[idx_this_level].reset_index(drop=True)
        wiring_low_level  = self.df_gen_wiring.iloc[idx_low_level].reset_index(drop=True)
        #print(wiring_this_level)
        #print(wiring_low_level)

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
                        else:
                            warnings.warn(f"Port {port_name} in {inst_name} is already connected")
                    elif ");" in content[i]:
                        warnings.warn(f"Port {port_name} in {inst_name} is not found")
                        break
            # If port, add to module interface, If wire, declaration. If para, do nothing. 
            if cnct_type == "port":
                direction, width = self._fetch_portinfo(inst_name, port_name)
                insert_content = f"{direction} {width} {cnct_name},"
                content = self.__find_anchor_insert(self.json_anchor['anchor_gen_port'], content, insert_content)
            elif cnct_type == "wire":
                direction, width = self._fetch_portinfo(inst_name, port_name)
                insert_content = f"logic {width} {cnct_name};"
                content = self.__find_anchor_insert(self.json_anchor['anchor_gen_wire_end'], content, insert_content)
            elif cnct_type == "para":
                pass

        for i in range(len(wiring_low_level)):
            inst_name = wiring_low_level['inst_name'][i]
            port_name = wiring_low_level['port_name'][i]
            cnct_name = wiring_low_level['cnct_name'][i]
            cnct_type = wiring_low_level['cnct_type'][i]
            see_point = wiring_low_level['see_point'][i]
            wire_name = wiring_low_level['wire_name'][i]
            for i in range(len(content)):
                if cnct_name in content[i]:
                    if "()" in content[i]:
                        content[i] = content[i].replace("()", f"({wire_name})")
                        break
                    else:
                        warnings.warn(f"Port {cnct_name} in {see_point} is already connected")
                elif "endmodule" in content[i]:
                    warnings.warn(f"Port {cnct_name} in {see_point} is not found")
                    break

            direction, width = self._fetch_portinfo(inst_name, port_name)
            insert_content = f"logic {width} {wire_name};"
            content = self.__find_anchor_insert(self.json_anchor['anchor_gen_wire_end'], content, insert_content)

        return content

    def _cnct_blks_wiring_post(self, gen_module, gen_instance, content):
        for instance in gen_instance:
            module_name = None
            instance_name = instance # assume the instance_name is the instance of a root module
            # check if is a root module name
            if self.df_gen_instance['instance_name'].isin([instance_name]).any():#.any():
                pass
            else: # if not a root module name, then it is a generated module
                module_name   = instance_name
                instance_name = f"i_{module_name}"
                found_anchor = False
                for i in range(len(content)):
                    if ("Anchor" in content[i]) and (module_name in content[i]):
                        found_anchor = True
                    if found_anchor == True:
                        if "()" in content[i]:
                            line_split = content[i].split()
                            cnct_name = line_split[0].replace(".", "")
                            content[i] = content[i].replace("()", f"({cnct_name})")
                            idx_list = self.df_gen_wiring.index[self.df_gen_wiring['cnct_name'] == cnct_name].tolist()
                            df = self.df_gen_wiring.loc[idx_list]
                            #print(df)
                            inst_name = df['inst_name'].tolist()[0]
                            port_name = df['port_name'].tolist()[0]
                            #print(inst_name, port_name)
                            direction, width = self._fetch_portinfo(inst_name, port_name)
                            insert_content = f"{direction} {width} {cnct_name},"
                            content = self.__find_anchor_insert(self.json_anchor['anchor_gen_port'], content, insert_content)
                        elif ");" in content[i]:
                            break
        return content

    def _cnct_blks_post_fix(self, content):
        # Fix issue in ports
        del_list = []
        dict_port = {'direction': [], 'width': [], 'port': []}
        for i in range(len(content)):
            line = content[i]
            if "input" in line or "output" in line or "logic" in line:
                del_list.append(i)
    
                line_split = line.split() # split with spaces
                dict_port['direction'].append(line_split[0]) # input and ooutput is always located in first place
                width = re.search(r"(\[.*\])", line) # find the [WIDTH:0] content and extract it
                if width == None:
                    dict_port['width'].append("")
                else:
                    width = width.group()
                    line = line.replace(width, "")  # delete the width for port name extraction
                    width = width.replace(" ", "")
                    dict_port['width'].append(width)
                line = line.replace("input", "")
                line = line.replace("output", "")
                line = line.replace("logic", "")
                line = line.replace(",", "")
                line = line.replace(";", "")
                line_split = line.split()
                #print(line_split)
                for port in line_split:
                    dict_port['port'].append(port)
            elif self.json_anchor['anchor_gen_wire_end'] in content[i]:
                break
        df = pd.DataFrame.from_dict(dict_port)
        print(df)
        df = df.drop_duplicates().reset_index(drop=True)
        print(df)
        for i in list(reversed(del_list)):  # del old ports
            content.pop(i)

        for i in range(len(df)):
            if i == len(df) - 1:
                insert_content = f"{df['direction'][i]} {df['width'][i]} {df['port'][i]}"
            else:
                insert_content = f"{df['direction'][i]} {df['width'][i]} {df['port'][i]},"
            content = self.__find_anchor_insert(self.json_anchor['anchor_gen_port'], content, insert_content)

        return content

    def _cnct_blks_post_beauty(self, content):
                #line = re.sub(r"//.*", "", line) # delete all contents with beginning //
        return content

    def _cnct_blks_main(self):
        for i in range(len(self.gen_archi))[:]:
            content = []
            dict_archi = self.gen_archi[-i-1] # the gen should backward
            print(dict_archi)
            gen_module = list(dict_archi.keys())[0] # the module name
            gen_instance = list(dict_archi.values())[0] # sub modules (instances) should in module
            print(f"\nStart gen block: {gen_module}. Needed sub level modules: {gen_instance}")

            # create top module name and anchors
            content.append(self.json_anchor["anchor_gen_incl_imp"])
            content.append(f"module {gen_module} #(")
            content.append(self.json_anchor["anchor_gen_parameter"])
            content.append(f")(")
            content.append(self.json_anchor["anchor_gen_port"])
            content.append(f");\n")

            content.append(self.json_anchor["anchor_gen_wire_begin"])
            content.append(self.json_anchor["anchor_gen_wire_end"])

            # gen instances sub modules
            for instance in gen_instance:
                module_name = None
                instance_name = instance # assume the instance_name is the instance of a root module
                # check if is a root module name
                if self.df_gen_instance['instance_name'].isin([instance_name]).any():#.any():
                    idx_list = self.df_gen_instance.index[self.df_gen_instance['instance_name'] == instance_name].tolist()
                    module_name = self.df_gen_instance['module_name'][idx_list].tolist()[0] # always pick the first one
                    try: # check if root module is given in filelist
                        path2module = self.json_info_filelist[module_name]
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
                content.append(f"// Anchor {module_name} {instance_name}")
                content = content + self.cnct_blk(path2module, instance_name, default_connect=False, doprint=False)
                content.append(f"\n")

            # endmodule
            content.append(f"endmodule")

            # wiring - most important part
            content = self._cnct_blks_wiring(gen_module, gen_instance, content)
            content = self._cnct_blks_wiring_post(gen_module, gen_instance, content)
            content = self._cnct_blks_post_fix(content)
            content = self._cnct_blks_post_beauty(content)

            # write the file
            with open(f"{self.gen_outpath}/{gen_module}.sv", "w") as f:
                for line in content:
                    f.write(f"{line}\n")




    def cnct_blks(self, jsonfile, output2path, debug=False):
        self.debug = debug
        # Read json file which has all connection setups
        self._cnct_blks_readjson(jsonfile, output2path)
        # Extract the project architecture, important setp for auto-connection
        self._extract_archi()
        self._extract_wiring()
        self._extract_moduleinfo()
        self._extract_paravalue()
        # Connect blocks
        self._cnct_blks_main()

