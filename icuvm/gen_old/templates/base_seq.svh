`ifndef _{{name.upper()}}_SEQ_SVH_
    `define _{{name.upper()}}_SEQ_SVH_

class {{name}}_seq extends uvm_sequence #(spinnedge_memory_item);

    `uvm_object_utils({{name}}_seq)
    `uvm_declare_p_sequencer(spinnedge_memory_sequencer)
    
    function new (string name="{{name}}_seq");
        super.new(name);
    endfunction : new


    task body();
        for (int i_val = 0; i_val < 10; i_val++) begin

            spinnedge_memory_item item;
            
            item = spinnedge_memory_item::type_id::create("item");
            
            `uvm_info(get_type_name(), $sformatf("Hello from the example seq!"), UVM_LOW)
            `uvm_info(get_type_name(), $sformatf("Start item in Seq!"), UVM_LOW)
            start_item(item);
            
            if(!(item.randomize())) begin
                `uvm_fatal("NOSEQITEM_MSEQ_ERR", "The sequence item could not be generated");
            end

            finish_item(item);
            `uvm_info(get_type_name(), $sformatf("Finish item in Seq!"), UVM_LOW)
        end

    endtask : body
  

endclass : {{name}}_seq

`endif