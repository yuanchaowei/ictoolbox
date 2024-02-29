`ifndef _{{name.upper()}}_IF_SV_
    `define _{{name.upper()}}_IF_SV_

interface {{name}}_if #(/*Please add something here*/) (input clk, reset_n);

    localparam  /*Please add something here*/
    logic       /*Please add something here*/

    clocking monitor_cb @(posedge clk);
        default input #1 output #1;
        output /*Please add something here*/;
        input  /*Please add something here*/;
    endclocking
    modport monitor (clocking monitor_cb, input clk, reset_n);

    clocking driver_cb @(posedge clk);
        default input #1 output #1;
        output /*Please add something here*/;
        input  /*Please add something here*/;
    endclocking
    modport driver (clocking driver_cb, input clk, reset_n);

endinterface
`endif