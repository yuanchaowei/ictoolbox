#!/usr/bin/env python3
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from ic_cnct import ic_cnct

BASEPATH="/home/chaov"

ic_cnct_i = ic_cnct(indent_default=4)


##########################
# To test basic functions please change to true
##########################
if False:
    port_lst = ['clk_i', 'reset_n_i', 'stall_i', 'bubble_i', 'kill_i', 'alu_out_c_i', 'alu_comp_true_i', 'instr_is_branch_i', 'rd_i', 
                'ls_en_w_i', 'ls_en_r_i', 'ls_mode_i', 'mux_sel_wbdata_i', 'wb_en_i', 'mem_wdata_i', 'alu_out_c_o', 'pc_en_load_branch_o', 
                'rd_o', 'ls_en_w_o', 'ls_en_r_o', 'ls_mode_o', 'ls_addr_o', 'ls_wdata_o', 'mux_sel_wbdata_o', 'wb_en_o']
    
    for i in ic_cnct_i._gen_para_port(port_lst, True):
        print(i)
     
    testpath = f"{BASEPATH}/ictoolbox/test/rtl/filelist.txt"
    content = []
    with open(testpath) as fp:
        for line in fp:
            content.append(line[:-1])
    testfile = content[0]
    ic_cnct_i.cnct_blk(testfile, default_connect=False, doprint=True)
    ic_cnct_i.cnct_blk(testfile, default_connect=True,  doprint=True)

##########################
# To gen with json
##########################

ic_cnct_i.cnct_blks(f"{BASEPATH}/ictoolbox/test/gen/top_proj.json", f"{BASEPATH}/ictoolbox/test/gen", debug=True)

