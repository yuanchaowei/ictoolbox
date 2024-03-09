`ifndef _{{projname.upper()}}_CONFIG_SVH_
    `define _{{projname.upper()}}_CONFIG_SVH_
  
class {{projname}}_config  extends uvm_component;

{% for agent in agentlist %}
    {{agent}}_agent_config {{agent}}_agent_config; 
{% endfor %}

    `uvm_component_utils({{projname}}_config)

    function new(string name = "{{projname}}_config", uvm_component parent = null);
        super.new(name, parent);

{% for agent in agentlist %}
        {{agent}}_agent_config = {{agent}}_agent_config::type_id::create("{{agent}}_agent_config", this); 
        {{agent}}_agent_config.is_active = UVM_ACTIVE;
{% endfor %}

    endfunction: new

endclass: {{projname}}_config

`endif

