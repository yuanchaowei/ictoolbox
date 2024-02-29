`ifndef _{{name.upper()}}_SEQUENCER_SVH_
    `define _{{name.upper()}}_SEQUENCER_SVH_

class {{name}}_sequencer #(type ITEM_T)  extends uvm_sequencer#(ITEM_T);

    {{name}}_agent_config agent_config;

    `uvm_component_param_utils({{name}}_sequencer#(.ITEM_T(ITEM_T)))

    function new(string name = "{{name}}_sequencer", uvm_component parent);
        super.new(name,parent);
    endfunction
    
endclass
`endif