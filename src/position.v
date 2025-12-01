// Tracks an 8-bit X,Y position on a 256×256 grid.
// Movement wraps around at edges.

module position (
    output reg [7:0] x_pos,
    output reg [7:0] y_pos,
    input  wire [3:0] dir_udlr, // {UP, DOWN, LEFT, RIGHT}
    input  wire clk,
    input  wire rst_n
);

always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        x_pos <= 8'd0;
        y_pos <= 8'd0;
    end
        else begin
            // Priority: only one direction active per cycle
            // (0,0) is bottom-left corner (math coordinates)
            if (dir_udlr[3])       // RIGHT
                x_pos <= x_pos + 1;
            else if (dir_udlr[2])  // LEFT
                x_pos <= x_pos - 1;
            else if (dir_udlr[1])  // DOWN (decreases y, moves down)
                y_pos <= y_pos - 1;
            else if (dir_udlr[0])  // UP (increases y, moves up)
                y_pos <= y_pos + 1;
        end
end

endmodule
