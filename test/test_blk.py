#!/usr/bin/env python3
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from ic_cnct import ic_cnct

ic_cnct_i = ic_cnct(indent_default=4)
port_lst = ['clk_i', 'reset_n_i', 'stall_i', 'bubble_i', 'kill_i', 'alu_out_c_i', 'alu_comp_true_i', 'instr_is_branch_i', 'rd_i', 
            'ls_en_w_i', 'ls_en_r_i', 'ls_mode_i', 'mux_sel_wbdata_i', 'wb_en_i', 'mem_wdata_i', 'alu_out_c_o', 'pc_en_load_branch_o', 
            'rd_o', 'ls_en_w_o', 'ls_en_r_o', 'ls_mode_o', 'ls_addr_o', 'ls_wdata_o', 'mux_sel_wbdata_o', 'wb_en_o']

for i in ic_cnct_i.gen_para_port(port_lst, True):
    print(i)
 
testpath = f"test_module.sv"
ic_cnct_i.cnct_blk("adder", testpath, "", default_connect=False)
ic_cnct_i.cnct_blk("adder", testpath, "", default_connect=True)



