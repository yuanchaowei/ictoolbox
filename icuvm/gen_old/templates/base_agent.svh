`ifndef _{{name.upper()}}_AGENT_SVH_
    `define _{{name.upper()}}_AGENT_SVH_

class {{name}}_agent extends uvm_agent;

    uvm_analysis_port #({{name}}_item) analysis_port_driver;
    uvm_analysis_port #({{name}}_item) analysis_port_monitor;

    {{name}}_agent_config agent_config;
    {{name}}_driver driver;
    {{name}}_monitor monitor;
    {{name}}_sequencer sequencer;

    `uvm_component_utils({{name}}_agent)
    
    function new(string name = "{{name}}_agent", uvm_component parent);
        super.new(name, parent);
    endfunction

    extern virtual function void    build_phase(uvm_phase phase);
    extern virtual function void    connect_phase(uvm_phase phase);
    extern virtual task             wait_reset_start();
    extern virtual task             wait_reset_end();
    extern virtual task             run_phase(uvm_phase phase);
    
endclass: {{name}}_agent



function void {{name}}_agent::build_phase(uvm_phase phase);
    super.build_phase(phase);

    if(!uvm_config_db #({{name}}_agent_config)::get(this, "", "{{name}}_agent_config", agent_config)) begin
        `uvm_fatal("", $sformatf("Agent configuration was not set in database for agent %s", get_full_name()));
    end
    is_active = agent_config.is_active;

    analysis_port_monitor = new("analysis_port_monitor", this);
    monitor = {{name}}_monitor#({{name}}_item)::type_id::create("monitor", this);

    if(is_active == UVM_ACTIVE) begin
        analysis_port_driver = new("analysis_port_driver", this);
        driver = {{name}}_driver#({{name}}_item)::type_id::create("driver", this);
        sequencer = {{name}}_sequencer#({{name}}_item)::type_id::create("sequencer", this);
    end
    uvm_config_db #({{name}}_agent_config)::set(this, "*", "{{name}}_agent_config", agent_config);

endfunction: build_phase

function void {{name}}_agent::connect_phase(uvm_phase phase);
    super.connect_phase(phase);
    
    if(driver != null) begin
        driver.agent_config = agent_config;
        driver.rsp_port.connect(analysis_port_driver);
        driver.seq_item_port.connect(sequencer.seq_item_export);
    end
    if(sequencer != null) begin
        sequencer.agent_config = agent_config;
    end

    monitor.agent_config = agent_config;
    monitor.analysis_port_monitor.connect(analysis_port_monitor);
    
endfunction: connect_phase

task {{name}}_agent::wait_reset_start();
    agent_config.wait_reset_start();
endtask: wait_reset_start

task {{name}}_agent::wait_reset_end();
    agent_config.wait_reset_end();
endtask: wait_reset_end

task {{name}}_agent::run_phase(uvm_phase phase);
    forever begin
        `uvm_info(get_type_name(), "Detecting of reset start is running!", UVM_HIGH)
        wait_reset_start();
        `uvm_info(get_type_name(), "Reset start detected", UVM_HIGH)
        wait_reset_end();
        `uvm_info(get_type_name(), "Reset end detected", UVM_HIGH)
    end
endtask:run_phase

`endif