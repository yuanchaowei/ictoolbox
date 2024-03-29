#!/usr/bin/env python3
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from icunit import icunit_cnct

BASEPATH=os.environ.get("HOME")
icunit_cnct_i = icunit_cnct(indent_default=4)


##########################
# To test basic functions please change to true
##########################
if False:
    lst_port = ['clk_i', 'reset_n_i', 'stall_i', 'bubble_i', 'kill_i', 'alu_out_c_i', 'alu_comp_true_i', 'instr_is_branch_i', 'rd_i', 
                'ls_en_w_i', 'ls_en_r_i', 'ls_mode_i', 'mux_sel_wbdata_i', 'wb_en_i', 'mem_wdata_i', 'alu_out_c_o', 'pc_en_load_branch_o', 
                'rd_o', 'ls_en_w_o', 'ls_en_r_o', 'ls_mode_o', 'ls_addr_o', 'ls_wdata_o', 'mux_sel_wbdata_o', 'wb_en_o']
    
    for i in icunit_cnct_i._cnct_blk_gen_paraport(lst_port, default_connect = True):
        print(i)
    print()
    lst_cnct = ['siduahiuwdhiauwhduihauiwdhuiawhduihawiud', 'reset_n_i', 'stall_i', 'bubble_i', 'kill_i', 'alu_out_c_i', 'alu_comp_true_i', 'instr_is_branch_i', 'rd_i', 
                'ls_en_w_i', 'ls_en_r_i', 'ls_mode_i', 'mux_sel_wbdata_i', 'wb_en_i', 'mem_wdata_i', 'alu_out_c_o', 'pc_en_load_branch_o', 
                'rd_o', 'ls_en_w_o', 'ls_en_r_o', 'ls_mode_o', 'ls_addr_o', 'ls_wdata_o', 'mux_sel_wbdata_o', 'wb_en_o']
    
    for i in icunit_cnct_i._cnct_blk_gen_paraport(lst_port, lst_cnct, default_connect = False):
        print(i)
     
    testpath = f"{BASEPATH}/ictoolbox/test/rtl/filelist.txt"
    content = []
    with open(testpath) as fp:
        for line in fp:
            content.append(line[:-1])
    testfile = content[0]
    icunit_cnct_i.run_gen_cnct_blk(testfile, default_connect=False, doprint=True)
    icunit_cnct_i.run_gen_cnct_blk(testfile, default_connect=True,  doprint=True)

##########################
# To gen with json
##########################

icunit_cnct_i.run_gen_cnct_blks(f"{BASEPATH}/ictoolbox/test/gen/xmpl_top.json", f"{BASEPATH}/ictoolbox/test/gen", remove_anchor=False)

