module xmpl_cic #(
)(
    // 123
    input                           clk_i,
    input                           reset_n_i,

    // wd1
    input                           en_cic_i,
    input  [12 - 1 : 0]             cic_a12_i, //asdwad
    input  [15 - 1 : 0]             cic_b15_i, //asdwad

    // 1df1234
    output [32 - 1 : 0]             cic_c32_o,
    output                          cic_status_o

);

logic [32 - 1 : 0] sadwd;
logic              sxawd;
logic              123;
//awudhiuwha
