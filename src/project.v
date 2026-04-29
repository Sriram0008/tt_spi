`default_nettype none

module tt_um_spi_example (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // will go high when the design is enabled
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

    // Map Tiny Tapeout pins to SPI signals
    wire sck  = ui_in[0];
    wire mosi = ui_in[1];
    wire cs_n = ui_in[2];
    wire miso;
    wire [7:0] data_out;
    wire data_ready;

    // Instantiate the SPI slave
    spi_slave spi_inst (
        .clk(clk),
        .rst_n(rst_n),
        .sck(sck),
        .mosi(mosi),
        .cs_n(cs_n),
        .miso(miso),
        .data_out(data_out),
        .data_ready(data_ready)
    );

    // Output assignments
    assign uo_out[0] = miso;
    assign uo_out[1] = data_ready;
    assign uo_out[7:2] = 6'b0;

    // Output received data to bidirectional IOs
    assign uio_out = data_out;
    assign uio_oe  = 8'hFF; // Configure all uio pins as outputs

endmodule
