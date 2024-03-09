`ifndef _{{projname.upper()}}_TEST_SVH_
    `define _{{projname.upper()}}_TEST_SVH_

class {{projname}}_test  extends uvm_test;
    
    {{projname}}_virtual_seq virtual_seq;
    {{projname}}_environment env;

    `uvm_component_utils_begin({{projname}}_test)
        `uvm_field_object(virtual_seq, UVM_ALL_ON)
    `uvm_component_utils_end    

    function new (string name="{{projname}}_test", uvm_component parent=null);
    super.new(name, parent);
    endfunction: new

    extern virtual function void build_phase(uvm_phase phase);
    extern virtual task          run_phase(uvm_phase phase);

endclass: {{projname}}_test



function void {{projname}}_test::build_phase(uvm_phase phase);
    env = {{projname}}_environment::type_id::create("env", this);
endfunction: build_phase


task {{projname}}_test::run_phase(uvm_phase phase);

    virtual_seq = {{projname}}_virtual_seq::type_id::create("virtual_seq", this);
    phase.raise_objection(this);
        virtual_seq.start(env.virtual_sequencer);
    phase.drop_objection(this);
    
    
endtask: run_phase



`endif