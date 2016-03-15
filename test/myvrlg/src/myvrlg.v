module myvrlg (
        input  wire 		rst,
        input  wire 		clk,

        // rx_hs (consume data)
        output wire     	rx_hs_ready,
        input  wire     	rx_hs_valid,
        input  wire [63:0]	rx_hs_data,

        // tx_hs (produce data)
        input  wire     	tx_hs_ready,
        output wire     	tx_hs_valid,
        output wire [63:0]	tx_hs_data        
        );

/* Custom code begin */
reg inst_inst_tx_hs_valid;
wire inst_inst_rx_hs_valid;
reg [63:0] inst_inst_tx_hs_data;
reg inst_inst_hs_en;
reg inst_inst_rx_hs_ready;
wire inst_inst_tx_hs_ready;
reg inst_inst_hs_en_inst_state;
wire inst1_snk_valid;
wire inst1_snk_ready;
wire [63:0] inst1_inst_snk_data;
wire [63:0] inst0_snk_data;


assign inst1_snk_ready = (!0) ? tx_hs_ready : 1;
assign tx_hs_valid = inst1_snk_valid;

assign inst1_snk_valid = inst_inst_tx_hs_valid;
assign inst_inst_tx_hs_ready = (!0) ? inst1_snk_ready : 1;
assign inst1_inst_snk_data = inst_inst_tx_hs_data;

assign tx_hs_data = inst1_inst_snk_data[64-1:0];

assign inst_inst_rx_hs_valid = rx_hs_valid;
assign rx_hs_ready = (!0) ? inst_inst_rx_hs_ready : 1;
assign inst0_snk_data = rx_hs_data;


always @(inst_inst_tx_hs_ready, inst_inst_rx_hs_valid, inst_inst_hs_en_inst_state) begin: PT_HS_TOP_INST_HS_EN_INST_RDY
    if (((inst_inst_hs_en_inst_state == 0) || inst_inst_tx_hs_ready)) begin
        inst_inst_rx_hs_ready = 1;
        inst_inst_hs_en = inst_inst_rx_hs_valid;
    end
    else begin
        inst_inst_rx_hs_ready = 0;
        inst_inst_hs_en = 0;
    end
end


always @(posedge clk) begin: PT_HS_TOP_INST_HS_EN_INST_CLK_PRCS
    if (rst) begin
        inst_inst_hs_en_inst_state <= 0;
        inst_inst_tx_hs_valid <= 0;
    end
    else begin
        if (inst_inst_rx_hs_ready) begin
            inst_inst_hs_en_inst_state <= inst_inst_rx_hs_valid;
            inst_inst_tx_hs_valid <= inst_inst_rx_hs_valid;
        end
    end
end


always @(posedge clk, posedge rst) begin: PT_HS_TOP_INST_CLK_PRCS_HS
    if (rst == 1) begin
        inst_inst_tx_hs_data <= 0;
    end
    else begin
        if (inst_inst_hs_en) begin
            inst_inst_tx_hs_data <= inst0_snk_data[64-1:0];
        end
    end
end
/* Custom code end */

endmodule
