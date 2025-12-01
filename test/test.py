# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

# import cocotb
# from cocotb.clock import Clock
# from cocotb.triggers import ClockCycles


# @cocotb.test()
# async def test_project(dut):
#     dut._log.info("Start")

#     # Set the clock period to 10 us (100 KHz)
#     clock = Clock(dut.clk, 10, units="us")
#     cocotb.start_soon(clock.start())

#     # Reset
#     dut._log.info("Reset")
#     dut.ena.value = 1
#     dut.uio_in[0].value = 0
#     dut.uio_in[1].value = 1 
#     dut.rst_n.value = 0
#     await ClockCycles(dut.clk, 4)
#     dut.rst_n.value = 1
#     await ClockCycles(dut.clk, 1)
#     dut._log.info("Test project behavior")

#     # --- Test 1: Default counting behavior ---
#     dut._log.info("Test 1: Default counting")
#     await ClockCycles(dut.clk, 13)
#     expected_val = 13
#     assert dut.uo_out.value == expected_val, \
#         f"Counter mismatch: expected {expected_val}, got {int(dut.uo_out.value)}"

#      # --- Test 2: Load a new value ---
#     dut._log.info("Test 2: Load new value (8)")
#     dut.ui_in.value = 8
#     dut.uio_in[0].value = 1   # assert load enable
#     await ClockCycles(dut.clk, 2)
#     dut.uio_in[0].value = 0   # deassert load enable
#     await ClockCycles(dut.clk, 1)

#     expected_val = 8
#     assert dut.uo_out.value == expected_val, \
#         f"Load failed: expected {expected_val}, got {int(dut.uo_out.value)}"


#     # --- Test 3: Continue counting from loaded value ---
#     dut._log.info("Test 3: Counting continues from loaded value")
#     await ClockCycles(dut.clk, 10)
#     expected_val = (8 + 10)
#     assert dut.uo_out.value == expected_val, \
#         f"Counter did not increment correctly: expected {expected_val}, got {int(dut.uo_out.value)}"

#     # --- Test 4: High impedance ---
#     dut.log.info("Test 4: Tri state high impedance")
#     dut.uio_in[1].value = 0
#     await ClockCycles(dut.clk, 1)
#     # assert dut.uo_out.value == expected_val, \
#         # f"Counter did not have high impedance state."

#     dut._log.info("All tests passed ✅")

#     # The following assersion is just an example of how to check the output values.
#     # Change it to match the actual expected output of your module:
#     # assert dut.uo_out.value == 50

#     # Keep testing the module by changing the input values, waiting for
#     # one or more clock cycles, and asserting the expected output values.

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, Timer

SCL_FREQ_HZ = 100_000  # 100 kHz
SCL_PERIOD_NS = int(1e9 // SCL_FREQ_HZ)


@cocotb.test()
async def test_i2c_start_condition(dut):

    # Start system clock
    cocotb.start_soon(Clock(dut.clk, 20, units="ns").start())

    # Start SCL clock  (UPDATED → uio_in[2])
    scl_clock = Clock(dut.uio_in[2], SCL_PERIOD_NS, units="ns")
    cocotb.start_soon(scl_clock.start())

    # reset !
    dut.ena.value = 1
    dut.rst_n.value = 0
    dut.uio_in.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 5)

    # SDA high idle  
    dut.uio_in[1].value = 1

    await Timer(50, "us")

    # START
    dut._log.info("Driving START")
    while int(dut.uio_in[2].value) != 1:   
        await Timer(100, "ns")
    await Timer(500, "ns")
    dut.uio_in[1].value = 0              
    await ClockCycles(dut.clk, 5)

    # --------------------- Send address byte -----------------------
    ADDRESS_BYTE = 0b11001001
    for i in range(8):
        bit = (ADDRESS_BYTE >> (7-i)) & 1

        while int(dut.uio_in[2].value) != 0:   
            await Timer(50, "ns")

        dut.uio_in[1].value = bit              

        while int(dut.uio_in[2].value) != 1:   
            await Timer(50, "ns")

        await ClockCycles(dut.clk, 3)

    # Release SDA for slave ACK
    while int(dut.uio_in[2].value) != 0:       
        await Timer(50, "ns")
    dut.uio_in[1].value = 1                    
    await ClockCycles(dut.clk, 20)

    # ------------------------- Master ACK -------------------------
    dut._log.info("Master ACKing received byte")

    while int(dut.i2c_state) != 4:
        await Timer(20, "ns")

    # Wait for SCL low
    while int(dut.uio_in[2].value) != 0:   
        await Timer(20, "ns")

    dut.uio_in[1].value = 0                 

    # Wait for SCL high
    while int(dut.uio_in[2].value) != 1:    
        await Timer(100, "ns")

    await ClockCycles(dut.clk, 200)
    dut.uio_in[1].value = 1                    

    # ---------------- second ACK ----------------
    while int(dut.i2c_state) != 4:
        await Timer(20, "ns")

    while int(dut.uio_in[2].value) != 0:       
        await Timer(20, "ns")

    dut.uio_in[1].value = 0                    

    while int(dut.uio_in[2].value) != 1:       
        await Timer(100, "ns")

    await ClockCycles(dut.clk, 200)
    dut.uio_in[1].value = 1                    

    # ---------------- third ACK ----------------
    while int(dut.i2c_state) != 4:
        await Timer(20, "ns")

    while int(dut.uio_in[2].value) != 0:       
        await Timer(20, "ns")

    dut.uio_in[1].value = 0                    

    while int(dut.uio_in[2].value) != 1:      
        await Timer(100, "ns")

    await ClockCycles(dut.clk, 200)
    dut.uio_in[1].value = 1                   

    dut.ui_in.value = 0b0001     # UP
    await ClockCycles(dut.clk, 1)
    dut.ui_in.value = 0          # release

    await ClockCycles(dut.clk, 10000)
