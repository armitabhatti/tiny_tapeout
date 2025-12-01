/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_example (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered
    input  wire       clk,      // system clock
    input  wire       rst_n     // reset_n - low to reset
);

    // // Unpacked aliases for Cocotb compatibility
    // wire uio_in_0 = uio_in[0];
    // wire uio_in_1 = uio_in[1];
    // wire uio_in_2 = uio_in[2];


    // ================================================================
    // 1. Position tracker
    // ================================================================
    wire [7:0] x_pos;
    wire [7:0] y_pos;

    position pos_inst (
        .x_pos   (x_pos),
        .y_pos   (y_pos),
        .dir_udlr(ui_in[3:0]),
        .clk     (clk),
        .rst_n   (rst_n)
    );

    assign uo_out = x_pos;


    // ================================================================
    // 2. I2C Slave Interface
    // ================================================================
    wire sda_oe_int;    // "output enable" for open-drain (1 = pull low)
    wire sda_out_int;   // not really needed (always 0 in your slave)

    // Hardcoded status byte (can be any value)
    wire [7:0] status_reg = 8'hC9;  // Fixed status value

    i2c_slave #(
        .I2C_ADDR(7'b1100100)   // 0x55
    ) i2c_slave_inst (
        .scl    (uio_in[2]),    // SCL from pad
        .sda_in (uio_in[1]),    // SDA from pad
        .sda_oe (sda_oe_int),   // open-drain enable from slave
        .sda_out(sda_out_int),  // always 0 inside slave
        .x_pos  (x_pos),
        .y_pos  (y_pos),
        .status (status_reg),
        .clk    (clk),
        .rst_n  (rst_n)
    );

    wire [2:0] i2c_state;
    assign i2c_state = i2c_slave_inst.state;

    // ================================================================
    // 3. Open-drain wiring on the chip pads
    // ================================================================
    // SDA (uio[1]) is open-drain:
    //  - we ALWAYS drive 0 on the data line
    //  - we ONLY enable the driver when sda_oe_int = 1
    
    // SDA = uio[1]
    assign uio_out[1] = 1'b0;        // open-drain drives only 0
    assign uio_oe[1]  = sda_oe_int;  // 1 = pull low, 0 = release

    // SCL = uio[2]
    assign uio_out[2] = 1'b0;        // input only
    assign uio_oe[2]  = 1'b0;
    
    // All other uio pins unused
    assign uio_out[7:3] = 5'b0;
    assign uio_oe[7:3]  = 5'b0;
    assign uio_out[0]   = 1'b0;
    assign uio_oe[0]   = 1'b0;


    // Avoid unused-signal warnings
    wire _unused = &{ena, 1'b0};
    wire _unused_ui = &ui_in;
    wire _unused_uio = &uio_in;
    wire _unused_sda_out = sda_out_int;
   // wire _unused_i2c = &{sda_rise};

endmodule


