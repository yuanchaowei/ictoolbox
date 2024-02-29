import re
import sys

class ic_cnct:
    def __init__(self, **kwargs):
        self.module_info = 0
        self.indent_default = kwargs.setdefault("indent_default", 4)
        self.indent = "    "    # later change

    def gen_para_port(self, lst, default_connect):
        content = []
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
        return content 


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
    
    def cnct_blk(self, blockname, path2block, output2path="", default_connect=False):
        para, port = self.get_para_port(path2block, detail=False)
        content = []
        content.append(f"{blockname} i_{blockname} #(")
        content = content + self.gen_para_port(para, default_connect=True)
        content.append(f")(")
        content = content + self.gen_para_port(port, default_connect=default_connect)
        content.append(f");")
        if output2path:
            with open(output2path, "w") as f:
                for line in content:
                    f.write(f"{line}\n")
        for i in content:
            print(i)
        return content

