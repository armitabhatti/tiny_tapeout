
module counter (
    output wire [7:0] counter_out,
    input wire oe,
    input wire load_select, // 0 for count, 1 for load
    input wire [7:0] load_in,
    input  wire  clk,      // clock
    input  wire  rst_n
);

//8 bit counter with syncronous load
//8 outputs, 2 inputs for tristate outputs

reg [7:0] counter_val;
reg out_en;

always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        counter_val <= 8'b0;
    end
    else if (load_select == 0) begin
        counter_val <= counter_val + 1; 
    end
    else if (load_select == 1) begin
        counter_val <= load_in;
    end
end

// if oe is enabled, counter out is counter value, otherwise high impedance
assign counter_out = oe ? counter_val : 8'bz;


endmodule