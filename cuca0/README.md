# cuca0

My first properly defined CPU project, designed to be very simple first
and foremost. Highly inspired by the "CUCA" series of CPU projects given
in a class from [my
teacher](https://sites.google.com/site/alvarodegas/degas-home-page).

## specs

Word size: 8 bits

Maximum memory: 256 bytes

Registers (all word-sized):

  - Accumulator (`acc`): general-purpose register for storing
    calculations;

  - Program counter (`pc`): points to the next instruction in memory to
    be read;

The ROM is the entire memory state, at the moment.

### instruction set & encoding

The instruction opcode size is the same as the word size: 8 bits. As
such, every instruction has at least a byte in size, and can take more
depending on the opcode.

Addresses are always uint8. Values are always uint8, but the assembler
can convert int8 values into their two's complement version.

Format: `opcode_hex: name (arg0: type0, arg1: type1, ...)`

- 00: ldi (value: uint8)

  Loads an integer value into the accumulator.

  i.e., `acc = value`

- 01: add (addr: uint8)

  Adds the value at a specific address of memory back to the
  accumulator.

  i.e., `acc += mem[addr]`

- 02: sub (addr: uint8)

  Subtracts the value at a specific address of memory from the
  accumulator.

  i.e., `acc -= mem[addr]`

- 03: read (addr: uint8)

  Reads a value from memory at a specific address, into the accumulator.

  i.e., `acc = mem[addr]`

- 04: write (addr: uint8)

  Writes the value in the accumulator into a specific address of memory.

  i.e., `mem[addr] = acc`

- 05: readoff (addr: uint8, offset: uint8)

  Reads a value from memory at a specific address, with a byte offset,
  into the accumulator.

  i.e., `acc = mem[addr + offset]`

- 06: writeoff (addr: uint8, offset: uint8)

  Writes the value in the accumulator into a specific address, with a
  byte offset, of memory.

  i.e., `mem[addr + offset] = acc`

- 07: jmp (addr: uint8)

  Jumps to the specified address.

  i.e., `pc = addr`

- 08: jz (addr: uint8)

  Jumps to the specified address only if the accumulator is zero.

  i.e., `pc = addr` only if `acc == 0`

- 09: jnz (addr: uint8)

  Jumps to the specified address only if the acumulator is nonzero.

  i.e., `pc = addr` only if `acc != 0`

- 0a: jn (addr: uint8)

  Jumps to the specified address only if the acumulator is negative.

  i.e., `pc = addr` only if `acc & (1 << 7) != 0`

- 0b: jp (addr: uint8)

  Jumps to the specified address only if the acumulator is positive.

  i.e., `pc = addr` only if `acc & (1 << 7) == 0`

- 0c: halt

  Stops the CPU.

### assembly directives

- `name:` defines a label at that point;

- `.var name value` creates a single byte slot for a variable, with the
    address label `name` and the value `value`;

## implementation details

- instructions divided into microinstructions and microprograms;

- single bus, controlled through tri-state buffers;

- no pipelining;

## extras

I tried doing this once before, see [cuca-sv](https://github.com/yohannd1/cuca-sv).
