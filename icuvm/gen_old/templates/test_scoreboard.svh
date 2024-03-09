`ifndef _{{projname.upper()}}_SCOREBOARD_SVH_
    `define _{{projname.upper()}}_SCOREBOARD_SVH_

class {{projname}}_scoreboard extends uvm_scoreboard;
    
    {{projname}}_config config;

    `uvm_component_utils({{projname}}_scoreboard)
    
{% for agent in agentlist %}
    uvm_analysis_export   #({{agent}}_item) {{agent}}_analysis_export_driver;
    uvm_analysis_export   #({{agent}}_item) {{agent}}_analysis_export_monitor;
    uvm_tlm_analysis_fifo #({{agent}}_item) {{agent}}_analysis_fifo_driver;
    uvm_tlm_analysis_fifo #({{agent}}_item) {{agent}}_analysis_fifo_monitor;

{% endfor %}

    function new(string name = "{{projname}}_scoreboard", uvm_component parent = null);
        super.new(name, parent);
    endfunction: new
    
    extern virtual function void build_phase(uvm_phase phase);
    extern virtual function void connect_phase(uvm_phase phase);
    extern virtual task          run_phase(uvm_phase phase);
    //extern virtual function void check_phase(uvm_phase phase);
    //extern virtual function void check_fifo_empty(int fifo_elements, string fifo_name);

endclass: {{projname}}_scoreboard



function void {{projname}}_scoreboard::build_phase(uvm_phase phase);
    super.build_phase(phase);

{% for agent in agentlist %}
    {{agent}}_analysis_export_driver  = new("{{agent}}_analysis_export_driver", this);
    {{agent}}_analysis_export_monitor = new("{{agent}}_analysis_export_monitor", this);
    {{agent}}_analysis_fifo_driver    = new("{{agent}}_analysis_fifo_driver", this);
    {{agent}}_analysis_fifo_monitor   = new("{{agent}}_analysis_fifo_monitor", this);

{% endfor %}
    `uvm_info("", $sformatf("Build phase of scoreboard is done."), UVM_HIGH);

endfunction: build_phase



function void {{projname}}_scoreboard::connect_phase(uvm_phase phase);
    super.connect_phase(phase);

{% for agent in agentlist %}
    {{agent}}_analysis_export_driver.connect({{agent}}_analysis_fifo_driver.analysis_export);
    {{agent}}_analysis_export_monitor.connect({{agent}}_analysis_fifo_monitor.analysis_export);

{% endfor %}
    `uvm_info("", $sformatf("connect phase of scoreboard is done."), UVM_HIGH)
endfunction: connect_phase


task {{projname}}_scoreboard::run_phase(uvm_phase phase);
    forever begin
{% for agent in agentlist %}
        {{agent}}_item {{agent}}_item_driver;
        {{agent}}_item {{agent}}_item_monitor;
        {{agent}}_analysis_fifo_driver.get_peek_export.peek({{agent}}_item_driver);
        {{agent}}_analysis_fifo_monitor.get_peek_export.peek({{agent}}_item_monitor);

{% endfor %}

        `uvm_info(get_name(),"Scoreboard receives item",UVM_LOW)
        /*Please Add you scoreboard here*/

{% for agent in agentlist %}
        {{agent}}_analysis_fifo_driver.get_peek_export.get({{agent}}_item_driver);
        {{agent}}_analysis_fifo_monitor.get_peek_export.get({{agent}}_item_monitor);

{% endfor %}

    end
endtask: run_phase



`endif