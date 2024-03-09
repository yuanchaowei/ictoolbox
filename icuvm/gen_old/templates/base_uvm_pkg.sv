`ifndef _{{name.upper()}}_UVM_PKG_SV_
    `define _{{name.upper()}}_UVM_PKG_SV_

	`include "{{name}}_if.sv"

package {{name}}_uvm_pkg;

	import uvm_pkg::*;
    import {{name}}_uvm_pkg_gen::*;

	`include "uvm_macros.svh"

	`include "{{name}}_def.svh"
    `include "{{name}}_types.svh"
    
    `include "{{name}}_item.svh"
    `include "{{name}}_agent_config.svh"
    `include "{{name}}_driver.svh"
    `include "{{name}}_monitor.svh"
    `include "{{name}}_sequencer.svh"
    
    `include "{{name}}_agent.svh"

endpackage: {{name}}_uvm_pkg


`endif 