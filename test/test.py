# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.uio_in[0].value = 0
    dut.uio_in[1].value = 1 
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 4)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)
    dut._log.info("Test project behavior")

    # --- Test 1: Default counting behavior ---
    dut._log.info("Test 1: Default counting")
    await ClockCycles(dut.clk, 13)
    expected_val = 13
    assert dut.uo_out.value == expected_val, \
        f"Counter mismatch: expected {expected_val}, got {int(dut.uo_out.value)}"

     # --- Test 2: Load a new value ---
    dut._log.info("Test 2: Load new value (8)")
    dut.ui_in.value = 8
    dut.uio_in[0].value = 1   # assert load enable
    await ClockCycles(dut.clk, 2)
    dut.uio_in[0].value = 0   # deassert load enable
    await ClockCycles(dut.clk, 1)

    expected_val = 8
    assert dut.uo_out.value == expected_val, \
        f"Load failed: expected {expected_val}, got {int(dut.uo_out.value)}"


    # --- Test 3: Continue counting from loaded value ---
    dut._log.info("Test 3: Counting continues from loaded value")
    await ClockCycles(dut.clk, 10)
    expected_val = (8 + 10)
    assert dut.uo_out.value == expected_val, \
        f"Counter did not increment correctly: expected {expected_val}, got {int(dut.uo_out.value)}"

    # --- Test 4: High impedance ---
    dut.log.info("Test 4: Tri state high impedance")
    dut.uio_in[1].value = 0
    await ClockCycles(dut.clk, 1)
    # assert dut.uo_out.value == expected_val, \
        # f"Counter did not have high impedance state."

    dut._log.info("All tests passed ✅")

    # The following assersion is just an example of how to check the output values.
    # Change it to match the actual expected output of your module:
    # assert dut.uo_out.value == 50

    # Keep testing the module by changing the input values, waiting for
    # one or more clock cycles, and asserting the expected output values.
