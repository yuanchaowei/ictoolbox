`ifndef _{{name.upper()}}_ITEM_SVH_
    `define _{{name.upper()}}_ITEM_SVH_

class {{name}}_item extends uvm_sequence_item;

    rand bit /*Please add something here*/;

    `uvm_object_utils_begin({{name}}_item)
        `uvm_field_int(/*Please add something here*/, UVM_ALL_ON)
    `uvm_object_utils_end

    function new(string name = "{{name}}_item");
        super.new(name);
    endfunction
  
    constraint /*Please add something here*/ {
        /*Please add something here*/
    }

    
  
endclass: {{name}}_item

`endif