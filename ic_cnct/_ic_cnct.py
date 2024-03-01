import re
import sys
import json

class ic_cnct:
    def __init__(self, **kwargs):
        self.module_info = 0
        self.indent_default = kwargs.setdefault("indent_default", 4)
        self.indent = "    "    # later change
        self.debug = False

        self.top_json = []
        self.top_outpath = []
        self.top_content = []

        self.top_info           = [] 
        self.top_info_filelist  = [] 
        self.top_sub_modules    = [] 
        self.top_timescale      = []
        self.top_incl_imp       = [] 
        self.top_para           = [] 
        self.top_localpara      = [] 
        self.top_struct         = [] 
        self.top_wiring         = [] 
        self.top_code           = [] 

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
            print("Input list in gen_para_port function is empty, propably no parameter")
        return content 

    # Extract the parameters and ports
    def get_para_port(self, path2block, detail=False):
        dic_para = {"parameter": [], "default_value": []}
        dic_port = {"direction": [], "width": [], "portname": []}
        with open(path2block) as file_block:
            for line in file_block:
                line = re.sub(r"//.*", "", line) # delete all contents with beginning //
                if "parameter" in line: # Get the parameters
                    line_split = line.split()
                    dic_para["parameter"].append(line_split[1])
                    try:    # if default value exists, add. Otherwise add None
                        if line[3]:
                            dic_para["default_value"].append(line_split[3])
                    except:
                        sys.exit(f"{line_split[1]} has no default value, please add!")
                elif "input" in line or "output" in line: # get port
                    if ");" in line: # the ); should be in single line
                        sys.exit(f"Please split the ); to the newline!!!")
    
                    line_split = line.split() # split with spaces
                    dic_port["direction"].append(line_split[0]) # input and ooutput is always located in first place
                    width = re.search(r"(\[.*\])", line) # find the [WIDTH:0] content and extract it
                    if width == None:
                        dic_port["width"].append("1")
                    else:
                        width = width.group()
                        dic_port["width"].append(width)
                        line = line.replace(width, "")  # delete the width for port name extraction
                    line = line.replace("input", "")
                    line = line.replace("output", "")
                    line = line.replace(",", "")
                    line_split = line.split()
                    for portname in line_split:
                        dic_port["portname"].append(portname)
                if ");" in line: # The end of module should be ");" and in new line
                    break
    
        if detail:
            return dic_para, dic_port
        else:
            return dic_para["parameter"], dic_port["portname"]
    
    # Connect the single block
    def cnct_blk(self, blockname, instance_name, path2block, output2path="", default_connect=False, doprint=True):
        para, port = self.get_para_port(path2block, detail=False)
        content = []
        content.append(f"{blockname} {instance_name} #(")
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

    # Connect multiple blocks
    def _cnct_blks_readjson(self, jsonfile, output2path):
        f = open(jsonfile)
        self.top_json = json.load(f)
        f.close()
        self.top_outpath = output2path
        #if self.debug: print("all json info is:\n", self.top_json)

    def _get_info(self):
        self.top_info           = self.top_json["top_info"]
        self.top_info_filelist  = self.top_json["top_info"]["filelist"]
        self.top_sub_modules    = self.top_json["top_sub_modules"]
        self.top_timescale      = self.top_json["top_timescale"]
        self.top_incl_imp       = self.top_json["top_incl_imp"]
        self.top_para           = self.top_json["top_para"]
        self.top_localpara      = self.top_json["top_localpara"]
        self.top_struct         = self.top_json["top_struct"]
        self.top_wiring         = self.top_json["top_wiring"]
        self.top_code           = self.top_json["top_code"]
        #if self.debug: print("The top info is:\n", self.top_info)

    def _cnct_blks_gen1(self):
        content = self.top_content

        # Add the includes and imports firstly
        if self.top_incl_imp["include"] != []:
            for item in self.top_incl_imp["include"]:
                content.append(f"`include \"{item}\"")
        if self.top_incl_imp["import"] != []:
            for item in self.top_incl_imp["import"]:
                content.append(f"import {item}::*;")
        content.append(f"\n")

        # create top module name
        content.append(f"module {self.top_info['top_name']} #(")
        content.append(f")(")
        content.append(f");\n")

        # gen sub modules
        for i in range(len(self.top_sub_modules)):
            module_name   = self.top_sub_modules[i]['module_name']
            instance_name = self.top_sub_modules[i]['instance_name']
            if self.top_sub_modules[i]["instance_name"] == "":
                instance_name = f"i_{self.top_sub_modules[i]['module_name']}"

            if self.top_info_filelist[module_name] == "":
                sys.exit(f"module path is not given in filelist!!")
            else:
                path2block = self.top_info_filelist[module_name]
            content.append(f"// Anchor {instance_name}")
            content = content + self.cnct_blk(module_name, instance_name, path2block, default_connect=False, doprint=False)
            content.append(f"\n")
        self.top_content = content

    def cnct_blks(self, jsonfile, output2path, debug=False):
        self.debug = debug
        self._cnct_blks_readjson(jsonfile, output2path)
        self._get_info()
        self._cnct_blks_gen1()
        if output2path:
            with open(output2path, "w") as f:
                for line in self.top_content:
                    f.write(f"{line}\n")

