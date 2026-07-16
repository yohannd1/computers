TODO: fill this readme.

This CPU was designed to be very simple first and foremost, as it's the
first one I'm implementing.

## specs

Word size: 8 bits

Maximum memory: 256 bytes

### instruction set & encoding

The instruction opcode size is the same as the word size: 8 bits. As
such, every instruction has at least a byte in size, and can take more
depending on the opcode.

Addresses are always uint8. Values are always uint8, but the assembler
can convert int8 values into their two's complement version.

Format: `opcode_hex: name (args)`
  TODO: explain this better

- 00: ldi (value: uint8)
  Loads an integer value into the accumulator register.

- 01: add (addr: uint8)
  Performs `acc = acc + mem[addr]`

- 02: sub (addr: uint8)
  Performs `acc = acc - mem[addr]`

- 03: read (addr: uint8)
  Performs `acc = mem[addr]`

- 04: write (addr: uint8)
  Performs `mem[addr] = acc`

- 05: jmp (addr: uint8)
  Performs `pc = addr`

- 06: jz (addr: uint8)
  Performs `pc = addr` only if `acc = 0`

- 07: jnz (addr: uint8)
  Performs `pc = addr` only if `acc != 0`

- 08: jnz (addr: uint8)
  Performs `pc = addr` only if `acc != 0`

TODO
