`ifndef _{{projname.upper()}}_VIRTUAL_SEQUENCER_SVH_
    `define _{{projname.upper()}}_VIRTUAL_SEQUENCER_SVH_

class {{projname}}_virtual_sequencer  extends uvm_virtual_sequencer;

{% for agent in agentlist %}
    {{agent}}_sequencer {{agent}}_seqr;
{% endfor %}
    
    {{projname}}_config config;
    
    `uvm_component_utils({{projname}}_virtual_sequencer)

    function new(string name = "{{projname}}_virtual_sequencer", uvm_component parent = null);
        super.new(name, parent);
    endfunction: new

endclass : {{projname}}_virtual_sequencer

`endif