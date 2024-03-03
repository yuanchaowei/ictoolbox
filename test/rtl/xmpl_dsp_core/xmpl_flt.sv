module xmpl_flt #(
)(
    // 123
    input                           clk_i,
    input                           reset_n_i,

    // wd1
    input                           en_flt_i,
    input  [7 - 1 : 0]              flt_a7_i, //asdwad
    input  [8 - 1 : 0]              flt_b8_i, //asdwad

    // 1df1234
    output [23 - 1 : 0]             flt_c23_o,
    output                          flt_status_o

);

logic [32 - 1 : 0] sadwd;
logic              sxawd;
logic              123;
//awudhiuwha
//
