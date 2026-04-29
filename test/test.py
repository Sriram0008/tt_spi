import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer

@cocotb.test()
async def test_spi(dut):
    dut._log.info("Starting SPI Test")
    
    # 10ns clock (100MHz)
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())

    # Initial states
    dut.rst_n.value = 0
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    
    await Timer(20, units="ns")
    dut.rst_n.value = 1
    await Timer(20, units="ns")
    
    # ui_in[0] = sck, ui_in[1] = mosi, ui_in[2] = cs_n
    dut.ui_in.value = 0b100 # cs_n = 1 (inactive)
    await RisingEdge(dut.clk)
    
    dut.ui_in.value = 0b000 # cs_n = 0 (active)
    await RisingEdge(dut.clk)
    
    # Send test byte 0xA5 (10100101)
    test_data = 0xA5
    for i in range(8):
        # Set MOSI (ui_in[1])
        bit = (test_data >> (7 - i)) & 1
        dut.ui_in.value = (dut.ui_in.value.integer & ~0x2) | (bit << 1)
        await RisingEdge(dut.clk)
        
        # SCK High
        dut.ui_in.value = dut.ui_in.value.integer | 0x1
        await RisingEdge(dut.clk)
        await RisingEdge(dut.clk)
        
        # SCK Low
        dut.ui_in.value = dut.ui_in.value.integer & ~0x1
        await RisingEdge(dut.clk)
        await RisingEdge(dut.clk)
        
    # Deactivate CS
    dut.ui_in.value = 0b100 # cs_n = 1
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)
    
    # Check if the received data matches the sent byte
    assert dut.uio_out.value == test_data, f"Expected {hex(test_data)}, got {hex(dut.uio_out.value.integer)}"
    dut._log.info(f"Test passed! Received data: {hex(dut.uio_out.value.integer)}")
