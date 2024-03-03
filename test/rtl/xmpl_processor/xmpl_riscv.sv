module xmpl_riscv #(
)(
    // 123
    input                   clk_i,
    input                   reset_n_i,

    // wd1
    output [12 - 1 : 0]     riscv_dsp_cic_a12_o,
    output [15 - 1 : 0]     riscv_dsp_cic_b15_o,
    input  [32 - 1 : 0]     riscv_dsp_cic_c32_i,

    output [2 - 1 : 0]      riscv_dsp_fft_a2_o,
    output [4 - 1 : 0]      riscv_dsp_fft_b4_o,
    input  [16 - 1 : 0]     riscv_dsp_fft_c16_i,

    output [7 - 1 : 0]      riscv_dsp_flt_a7_o,
    output [8 - 1 : 0]      riscv_dsp_flt_b8_o,
    input  [23 - 1 : 0]     riscv_dsp_flt_c23_i,


    input                   riscv_en_dsp_fsm_o,
    input  [14 - 1 : 0]     riscv_dsp_fsm_state_i,

    // 1df1234
    output [32 - 1 : 0]     riscv_2loongson_o,
    output [32 - 1 : 0]     riscv_2stone_o

);

logic [32 - 1 : 0] sadwd;
logic              sxawd;
logic              123;
//awudhiuwha

logic [32 - 1 : 0] sadwd;
logic              sxawd;
logic              123;
//awudhiuwha
