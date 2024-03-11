#!/usr/bin/env python3
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from icrf import icrf_gen

BASEPATH=os.environ.get("HOME")
icrf_gen_i = icrf_gen()


##########################
# To test basic functions please change to true
##########################
icrf_gen_i.run_gen(f"{BASEPATH}/ictoolbox/test/regfile/xmpl_dsp_regfile.json", f"{BASEPATH}/ictoolbox/test/regfile", remove_anchor=False)

