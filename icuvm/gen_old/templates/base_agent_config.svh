`ifndef _{{name.upper()}}_AGENT_CONFIG_SVH_
    `define _{{name.upper()}}_AGENT_CONFIG_SVH_

class {{name}}_agent_config  extends uvm_component;

    virtual_interface vif;  //virtual_interface is defined in *_types.svh.
    uvm_active_passive_enum is_active           = UVM_ACTIVE;
    protected bit           reset_active_level  = 0;

    extern virtual function virtual_interface get_vif();
    extern virtual function void    set_m_vif({{name}}_vif vif);
    extern virtual function bit     get_reset_active_level();
    extern virtual function void    set_reset_active_level(bit rst_lvl);


    `uvm_component_utils_begin({{name}}_agent_config)
        `uvm_field_enum(uvm_active_passive_enum, is_active, UVM_ALL_ON)
    `uvm_component_utils_end

    function new(string name = "{{name}}_agent_config", uvm_component parent = null);
        super.new(name, parent);
    endfunction

    extern virtual function void    start_of_simulation_phase(input uvm_phase phase);
    extern virtual task             wait_reset_start();
    extern virtual task             wait_reset_end();

endclass: {{name}}_agent_config


function virtual_interface {{name}}_agent_config::get_vif();
    return vif;
endfunction: get_vif

function void {{name}}_agent_config::set_m_vif(virtual_interface vif);
    this.vif = vif;
endfunction: set_m_vif

function bit {{name}}_agent_config::get_reset_active_level();
    return reset_active_level;
endfunction: get_reset_active_level

function void {{name}}_agent_config::set_reset_active_level(bit rst_lvl);
    this.reset_active_level = rst_lvl;
endfunction: set_reset_active_level


function void {{name}}_agent_config::start_of_simulation_phase(input uvm_phase phase);
    super.start_of_simulation_phase(phase);

    assert (vif != null) else begin
       `uvm_fatal(get_type_name(), "The pointer to the DUT interface is null - please make sure you set it via set_vif() function before \"Start of Simulation\" phase!");
    end
    
endfunction: start_of_simulation_phase

task {{name}}_agent_config::wait_reset_start();
    // if(reset_active_level == 0) begin
        @(negedge vif.reset_n);
    // end else begin
    //     @(posedge vif.reset_n);
    // end
endtask: wait_reset_start

task {{name}}_agent_config::wait_reset_end();
    // if(reset_active_level == 0) begin
        @(posedge vif.reset_n);
    // end else begin
    //     @(negedge vif.reset_n);
    // end
endtask: wait_reset_end

`endif