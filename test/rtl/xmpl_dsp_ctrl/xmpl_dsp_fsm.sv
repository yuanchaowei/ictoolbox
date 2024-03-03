module xmpl_dsp_fsm #(
)(
    // 123
    input               clk_i,
    input               reset_n_i,

    input               en_xmpl_dsp_fsm_i, //asdwad

    input               xmpl_dsp_cic_status_i,
    input               xmpl_dsp_fft_status_i,
    input               xmpl_dsp_flt_status_i,

    output              en_xmpl_dsp_cic_o,
    output              en_xmpl_dsp_fft_o,
    output              en_xmpl_dsp_dlt_o,

    output [14 - 1 : 0] xmpl_dsp_fsm_state_o

);

logic [32 - 1 : 0] sadwd;
logic              sxawd;
logic              123;
//awudhiuwha
