module xmpl_fft #(
)(
    // 123
    input                           clk_i,
    input                           reset_n_i,

    // wd1
    input                           en_fft_i,
    input  [2 - 1 : 0]fft_a2_i, //test special cases
    input  [4 - 1 : 0]fft_b4_i, //asdwad

    // 1df1234
    output [16 - 1 : 0]             fft_c16_o,
    output                          fft_status_o

);

logic [32 - 1 : 0] sadwd;
logic              sxawd;
logic              123;
//awudhiuwha
