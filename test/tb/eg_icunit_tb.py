#!/usr/bin/env python3
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from icunit import icunit_tb

BASEPATH=os.environ.get("HOME")
icunit_tb_i = icunit_tb()



##########################
# To gen with json
##########################
icunit_tb_i.run_gen_tb(f"{BASEPATH}/ictoolbox/test/rtl/xmpl_sram/xmpl_sram.sv", f"{BASEPATH}/ictoolbox/test/tb", remove_anchor=False)

#icunit_tb_i = icunit_tb()
#icunit_tb_i.run_gen_tb(f"{BASEPATH}/ictoolbox/test/tb/tb_xmpl.json", f"{BASEPATH}/ictoolbox/test/tb", remove_anchor=False)

