module xmpl_sram #(
    parameter HAWDAS = 2,
    parameter XNAIS = 2
)(
    // 123
    input                           clk_i,
    input                           reset_n_i,

    // wd1
    input reg                       en_sram_i,
    input  logic [12 - 1 : 0]             sram_addr_i, //asdwad

    input                           sram_rw_i,
    // 1df1234
    input  signed [32 - 1 : 0]             sram_data_i,
    output unsigned [32 - 1 : 0]             sram_data_o

);

logic [32 - 1 : 0] sadwd;
logic              sxawd;
logic              123;
//awudhiuwha

logic [32 - 1 : 0] sadwd;
logic              sxawd;
logic              123;
//awudhiuwha
