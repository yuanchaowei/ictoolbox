`ifndef _{{projname.upper()}}_UVM_PKG_SV_
    `define _{{projname.upper()}}_UVM_PKG_SV_

package {{projname}}_uvm_pkg;
    import uvm_pkg::*;

{% for agent in agentlist %}
    import {{agent}}_uvm_pkg::*;
{% endfor %}

    `include "uvm_macros.svh"

    `include "{{projname}}_config.svh"
    `include "{{projname}}_virtual_sequencer.svh"
    `include "{{projname}}_scoreboard.svh"
    `include "{{projname}}_env.svh"
    
    `include "{{projname}}_virtual_seq.svh"
    `include "{{projname}}_test.svh"

endpackage: {{projname}}_uvm_pkg

`endif
