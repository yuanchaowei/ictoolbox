`ifndef _{{projname.upper()}}_ENVIRONMENT_SVH_
    `define _{{projname.upper()}}_ENVIRONMENT_SVH_

class {{projname}}_environment extends uvm_component;

{% for agent in agentlist %}
    {{agent}}_agent {{agent}}_agent;
{% endfor %}
    
    {{projname}}_virtual_sequencer  virtual_sequencer;
    {{projname}}_scoreboard  scoreboard;
    {{projname}}_config  config;
    
    `uvm_component_utils({{projname}}_environment )

    function new(string name = "{{projname}}_environment", uvm_component parent = null);
        super.new(name, parent);
    endfunction: new

    extern virtual function void build_phase(uvm_phase phase);
    extern virtual function void connect_phase(uvm_phase phase);

endclass : {{projname}}_environment

function void {{projname}}_environment::build_phase(uvm_phase phase);
    super.build_phase(phase);
    
    //Get config(vif) from tb_* file. {{projname}}_config from tb. config is from env. 
    if(! uvm_config_db#({{projname}}_config)::get(this,"","{{projname}}_config", config) ) begin
        `uvm_fatal("ENV CFG MISSING", "no configuration found!")
    end

    scoreboard = {{projname}}_scoreboard::type_id::create("scoreboard", this);
    virtual_sequencer = {{projname}}_virtual_sequencer::type_id::create("virtual_sequencer", this);

{% for agent in agentlist %}
    {{agent}}_agent = {{agent}}_agent::type_id::create("{{agent}}_agent", this);;
    uvm_config_db#({{agent}}_agent_config)::set(this, "{{agent}}_agent", "{{agent}}_agent_config", config.{{agent}}_agent_config);
{% endfor %}
    
    scoreboard.config = config;
    virtual_sequencer.config = config;

endfunction: build_phase

function void {{projname}}_environment::connect_phase(input uvm_phase phase);
    super.connect_phase(phase);
    
    scoreboard.agent_config = agent_config;

{% for agent in agentlist %}
    {{agent}}_agent.analysis_port_driver.connect(scoreboard.{{agent}}_agent_analysis_export_driver);
    {{agent}}_agent.analysis_port_monitor.connect(scoreboard.{{agent}}_agent_analysis_export_monitor);
    {{agent}}_agent = {{agent}}_agent::type_id::create("{{agent}}_agent", this);;
    virtual_sequencer.{{agent}}_sequencer = {{agent}}_agent.sequencer;

{% endfor %}
endfunction: connect_phase

`endif