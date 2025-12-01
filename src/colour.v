module colour (
    input  wire        clk,
    input  wire        rst_n,

    input  wire        sel_red,    
    input  wire        sel_green,  
    input  wire        sel_blue,   
    input  wire        sel_yellow, 

    output reg  [7:0]  status_byte
);

    // color_bits = status_byte[7:6]
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            status_byte[7:6] <= 2'b00;  // default red
        else begin
            if (sel_red)
                status_byte[7:6] <= 2'b00;
            else if (sel_green)
                status_byte[7:6] <= 2'b01;
            else if (sel_blue)
                status_byte[7:6] <= 2'b10;
            else if (sel_yellow)
                status_byte[7:6] <= 2'b11;
        end
    end

    // bottom 6 bits = fixed zero
    always @(*) begin
        status_byte[5:0] = 6'b000000;
    end

endmodule
