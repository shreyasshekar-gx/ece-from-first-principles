`timescale 1ns/1ps
module counter_tb;
    logic clk=0, reset=1, enable=0;
    logic [3:0] count;
    counter dut(.*);
    always #5 clk=~clk;
    task tick;
        @(posedge clk); #1;
    endtask
    initial begin
        tick();
        if (count !== 0) $fatal(1,"reset failed");
        @(negedge clk); reset=0; enable=1;
        for (int i=1; i<=16; i++) begin
            tick();
            if (count !== (i % 16)) $fatal(1,"increment or wrap failed");
        end
        @(negedge clk); enable=0;
        tick();
        if (count !== 0) $fatal(1,"hold failed");
        $display("PASS: reset, increment, wrap, hold");
        $finish;
    end
endmodule
