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
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

  // All output pins must be assigned. If not used, assign to 0.
//  assign uo_out  = 0;  // Example: ou_out is the sum of ui_in and uio_in
  assign uio_out = 0;
  assign uio_oe  = 0;

  // List all unused inputs to prevent warnings
// wire _unused = &{ena, clk, rst_n, 1'b0};
 wire _unused = &{ena, 1'b0};




counter counter_inst(
    .counter_out(uo_out),
    .oe(uio_in[1]), // 1 for output enable
    .load_select(uio_in[0]), // 0 for count, 1 for load
    .load_in(ui_in),
    .clk(clk),      // clock
    .rst_n(rst_n)
);




endmodule



// task: 8-bit programmable counter with tri-state outputs

// for high impedance: when output enable is low uio_out is high impedance uio_in can be read safely

// so usually, output of counter will be on uio_out, unless you want to program, then push onto uoi_in


//assign uio_oe is  high
//when user puts on input for a load, uio_oe assigned low
// at the positive edge of the clock
    // if reset: uio_out = 0
    // if load: count = uio_in  
    // else: count ++
//cts:
// uio_out = count
// uio_oe = loadn sig

//inputs mapping
//in[0]= load
//in[1]= tri state

//outputs mapping
//



