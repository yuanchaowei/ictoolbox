`ifndef _{{name.upper()}}_MONITOR_SVH_
    `define _{{name.upper()}}_MONITOR_SVH_

class {{name}}_monitor#(type ITEM_T) extends uvm_monitor;

    uvm_analysis_port #(ITEM_T) analysis_port_monitor;

    virtual_interface vif; //virtual_interface is defined in *_types.svh.

    {{name}}_agent_config agent_config;
    
    `uvm_component_utils({{name}}_monitor#(ITEM_T))

    function new(string name, uvm_component parent);
        super.new(name, parent);
    endfunction : new

    extern  virtual function    void    build_phase(uvm_phase phase);
    extern  virtual function    void    connect_phase(uvm_phase phase);
    extern  virtual function    void    start_of_simulation_phase(input uvm_phase phase);
    extern  virtual task                run_phase(uvm_phase phase);
    extern  virtual task                wait_reset_end();
    extern  virtual task                collect_transaction();

endclass: {{name}}_monitor



function void {{name}}_monitor::build_phase(uvm_phase phase);
    super.build_phase(phase);

    analysis_port_monitor = new("analysis_port_monitor", this);

    if(!uvm_config_db #({{name}}_agent_config)::get(this, "", "{{name}}_agent_config", agent_config)) begin
        `uvm_fatal(get_full_name(), "In monitor, cannot get confirugation from configuration database!")
    end

endfunction: build_phase

function void {{name}}_monitor::connect_phase(uvm_phase phase);
    super.connect_phase(phase);
    vif = agent_config.vif;   
endfunction: connect_phase


function void {{name}}_monitor::start_of_simulation_phase(input uvm_phase phase);
    super.start_of_simulation_phase(phase);
    assert (agent_config != null) else begin
        `uvm_fatal(get_type_name(), "The pointer to the agent configuration is null - please make sure you set agent_config before \"Start of Simulation\" phase!");
    end
endfunction: start_of_simulation_phase

task {{name}}_monitor::run_phase(uvm_phase phase);
    forever begin    
        wait_reset_end(); 
    /*Please add something here*/        
        collect_transaction();
    end
endtask: run_phase

task {{name}}_monitor::wait_reset_end();
    if(vif.monitor.reset_n === 1'b0) begin
        @(posedge vif.monitor.reset_n);
        `uvm_info(get_type_name(), "Reset end in Monitor detected", UVM_MEDIUM)
    end
endtask: wait_reset_end

task {{name}}_monitor::collect_transaction();
    ITEM_T item;
    item = ITEM_T::type_id::create("item");
    `uvm_info(get_type_name(), "New transaction starts", UVM_HIGH)
    /*Please add something here*/
    analysis_port_monitor.write(item); 
    `uvm_info(get_type_name(), $psprintf("Monitor transaction: \n %s", item.convert2string()), UVM_MEDIUM);
endtask: collect_transaction

`endif