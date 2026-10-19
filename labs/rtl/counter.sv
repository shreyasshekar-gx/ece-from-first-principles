module counter #(parameter WIDTH=4)(
    input logic clk, reset, enable,
    output logic [WIDTH-1:0] count
);
    always_ff @(posedge clk) begin
        if (reset) count <= '0;
        else if (enable) count <= count + 1'b1;
    end
endmodule
