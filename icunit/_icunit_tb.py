import re
import os, sys
import json
import pandas as pd
import numpy as np
import warnings
from icunit import icunit_cnct

class icunit_tb(icunit_cnct):
    def __init__(self, **kwargs):
        self.indent_default = kwargs.setdefault("indent_default", 4)
        self.indent = "    "    # later change

        self.json_data = []

        self.json_info          = [] 
        self.json_info_filelist = {}
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
        self.df_customized_code = []
 
