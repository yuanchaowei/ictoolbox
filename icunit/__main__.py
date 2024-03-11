import os, sys
import argparse
import textwrap

from _icunit_cnct import icunit_cnct
from _icunit_tb import icunit_tb

def main():

    # parser
    parser = argparse.ArgumentParser(
            description="icunit",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            epilog=textwrap.dedent('''\
                additional information:\n
                    I have indented it
                    exactly the way
                    I want it
                '''))

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
            "-c0", "--cnct-blk",
            action="store_true",
            dest="gen_cnct_blk",
            help="generate single block connection, e.g -c0 src=<path to module>")

    group.add_argument(
            "-c1", "--cnct-blks",
            action="store_true",
            dest="gen_cnct_blks",
            help="generate block connections, need json, e.g. -c1 src=<json>")

    group.add_argument(
            "-tb", "--testbench",
            action="store_true",
            dest="gen_tb",
            help="generate testbench, default for single blk or with json for multi blks e.g. -tb src=<path to module or json file>")

    parser.add_argument(
            "src",
            help="Source file location, module file or json")

    parser.add_argument(
            "-outpath",
            action="store",
            default="./",
            dest="outpath",
            help="Destination location to store generated file")

    parser.add_argument(
            "-clean",
            action="store_false",
            dest="rm_anchor",
            help="remove anchor after generation")

    args = parser.parse_args()
    #config = vars(args)
    #print(config)

    
    try:
        if args.gen_cnct_blk:
            icunit_cnct_i = icunit_cnct(indent_default=4)
            icunit_cnct_i.run_gen_cnct_blk(args.src, default_connect=True,  doprint=True)
    except:
        sys.exit(f"***F: Run blocks connection failed, please check source module file")
    
    try:
        if args.gen_cnct_blks:
            icunit_cnct_i = icunit_cnct(indent_default=4)
            icunit_cnct_i.run_gen_cnct_blks(args.src, args.outpath, remove_anchor=args.rm_anchor)
    except:
        sys.exit(f"***F: Run blocks connection failed, please check source json file")
 
    try:
        if args.gen_tb:
            icunit_tb_i = icunit_tb()
            icunit_tb_i.run_gen_tb(args.src, args.outpath, remove_anchor=args.rm_anchor)
    except:
        sys.exit(f"***F: Run blocks connection failed, please check given source file")
 

if __name__ == "__main__":
    sys.exit(main())
    # python icunit -c0 test/rtl/xmpl_common/xmpl_clkgating.sv
    # python icunit -c1 test/gen/xmpl_top.json -outpath=test/gen/
    # python icunit -tb test/tb/tb_xmpl.json -outpath=test/tb
    # python icunit -tb test/rtl/xmpl_dsp_core/xmpl_flt.sv -outpath=test/tb

