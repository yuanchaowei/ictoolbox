`ifndef _{{projname.upper()}}_VIRTUAL_SEQ_SVH_
    `define _{{projname.upper()}}_VIRTUAL_SEQ_SVH_

class {{projname}}_virtual_seq extends uvm_sequence;

    `uvm_object_utils({{projname}}_virtual_seq)
    `uvm_declare_p_sequencer({{projname}}_virtual_sequencer)
    
    function new (string name="{{projname}}_virtual_seq");
        super.new(name);
    endfunction : new


    task body();
{% for agent in agentlist %}
        // {{agent}}_seq {{agent}}_seqc;
        // {{agent}}_seqc = {{agent}}_seq::type_id::create("{{agent}}_seqc");
{% endfor %}

{% for agent in agentlist %}
        // {{agent}}_seqc.start(p_sequencer.{{agent}}_seqr);
{% endfor %}

    endtask : body
  

endclass : {{projname}}_virtual_seq

`endif