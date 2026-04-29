---
title: SPI Peripheral
author: Your Name
language: Verilog
---

## How it works

This project implements a simple SPI slave peripheral. It receives an 8-bit value via the standard SPI pins (SCK, MOSI, CS_N) and outputs the received data to the bidirectional pins.

## How to test

To test the design, act as an SPI Master:
1. Bring `cs_n` (Chip Select) low.
2. Toggle the `sck` (Clock) pin while feeding data bits into the `mosi` pin.
3. Observe the `miso` pin for data out, and the `data_ready` pin indicating a full byte has been received.
4. The fully assembled byte will be available on the bidirectional IOs (`uio_out`).
