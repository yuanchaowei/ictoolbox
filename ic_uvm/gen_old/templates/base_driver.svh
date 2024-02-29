`ifndef _{{name.upper()}}_DRIVER_SVH_
    `define _{{name.upper()}}_DRIVER_SVH_

class {{name}}_driver #(type ITEM_T) extends uvm_driver#(ITEM_T);

    virtual_interface vif; //virtual_interface is defined in *_types.svh.
    {{name}}_agent_config agent_config;

    `uvm_component_param_utils({{name}}_driver#(.ITEM_T(ITEM_T)))

    function new(string name = "{{name}}_driver", uvm_component parent);
        super.new(name, parent);
    endfunction : new

    extern  virtual function    void    build_phase(uvm_phase phase);
    extern  virtual function    void    connect_phase(uvm_phase phase);
    extern  virtual function    void    start_of_simulation_phase(input uvm_phase phase);
    extern  virtual task                run_phase(uvm_phase phase);
    extern  virtual task                wait_reset_end();
    extern  virtual task                {{name}}_drive(ITEM_T req);
    extern  virtual function    void    init_if();

endclass : {{name}}_driver



function void {{name}}_driver::build_phase(input uvm_phase phase);
    super.build_phase(phase);

    if(!uvm_config_db #({{name}}_agent_config)::get(this, "", "{{name}}_agent_config", agent_config)) begin
        `uvm_fatal("", $sformatf("Agent configuration was not set in database for agent %s", get_full_name()));
    end

endfunction: build_phase


function void {{name}}_driver::connect_phase(uvm_phase phase);
    super.connect_phase(phase);
    vif = agent_config.get_vif();
endfunction: connect_phase

function void {{name}}_driver::start_of_simulation_phase(input uvm_phase phase);
    super.start_of_simulation_phase(phase);

    assert (agent_config != null) else begin
        `uvm_fatal(get_type_name(), "The pointer to the agent configuration is null - please make sure you set agent_config before \"Start of Simulation\" phase!");
    end

endfunction: start_of_simulation_phase

task {{name}}_driver::run_phase(uvm_phase phase);
    init_if();
    forever begin
        ITEM_T req;
        wait_reset_end();
        `uvm_info(get_type_name(), "Starting drive_transactions()...", UVM_MEDIUM)
        seq_item_port.get_next_item(req);
        {{name}}_drive(req);
        rsp_port.write(req);
        seq_item_port.item_done();
    end
endtask : run_phase
    
task {{name}}_driver::wait_reset_end();
    if(vif.driver.reset_n === 0) begin
        @(posedge vif.driver.reset_n);
        `uvm_info(get_type_name(), "Reset end in Driver detected", UVM_MEDIUM)
    end
endtask: wait_reset_end

task {{name}}_driver::{{name}}_drive(ITEM_T req);
   
endtask : {{name}}_drive

function void {{name}}_driver::init_if();
    
endfunction: init_if
   
`endif