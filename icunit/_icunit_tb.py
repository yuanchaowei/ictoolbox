import re
import os, sys
import json
import pandas as pd
import numpy as np
import warnings
from icunit import icunit_cnct

class icunit_tb(icunit_cnct):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def run_gen_tb(self, jsonfile, output2path, remove_anchor=True):
        self.run_gen_cnct_blks(jsonfile, output2path, remove_anchor)

