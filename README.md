# Pulse-12 CPU

A 12-bit educational CPU architecture with 18-bit instruction words and support for multiple addressing modes.

## Overview

- **Word Size**: 12 bits
- **Instruction Size**: 18 bits
- **Memory**: 4096 × 18 bits
- **Addressing Modes**: Direct, Indirect, Index

## Instruction Format

```
[I1 I0] [O3 O2 O1 O0] [A11 A10 A9 A8 A7 A6 A5 A4 A3 A2 A1 A0]
  ├─┬─┘    ├────┬───┘              ├──────────┬──────────┘
    │           │                             │
Addressing   Opcode                       Address
 (2 bits)   (4 bits)                     (12 bits)
```

## Registers

| Register | Size | Description |
|----------|------|-------------|
| AC | 12 bit | Accumulator |
| PC | 12 bit | Program Counter |
| AR | 12 bit | Address Register |
| DR | 12 bit | Data Register |
| TR | 12 bit | Temporary Register |
| IX | 12 bit | Index Register |
| IR | 18 bit | Instruction Register |
| INPR | 8 bit | Input Register |
| OUTR | 8 bit | Output Register |

## Addressing Modes

| I1 I0 | Mode | Description |
|-------|------|-------------|
| 00 | Direct | Use address directly |
| 01 | Indirect | AR ← M[AR] |
| 10 | Index | AR ← M[AR + IX] |
| 11 | - | Not used |

## Instruction Set

### Memory Reference Instructions (MRI)

| Opcode | Mnemonic | Operation | Description |
|--------|----------|-----------|-------------|
| D0 | AND | AC ∧ DR | Logical AND |
| D1 | ADD | AC + DR, E ← Cout | Add with carry |
| D2 | LDA | AC ← M[AR] | Load to accumulator |
| D3 | STA | M[AR] ← AC | Store accumulator |
| D4 | BUN | PC ← AR | Branch unconditional |
| D5 | BSA | M[AR] ← PC, PC ← AR + 1 | Branch and save address |
| D6 | ISZ | M[AR] ← M[AR] + 1, skip if zero | Increment and skip if zero |
| D7 | SUB | AC - DR, E ← Cout | Subtract |
| D8 | LIX | IX ← DR | Load index register |
| D9 | LIA | IX ← AC | Load index from accumulator |
| D10 | INX | IX ← IX + AR | Increment index register |
| D11 | JZ | if (AC = 0) then PC ← AR | Jump if zero |
| D12 | JNZ | if (AC ≠ 0) then PC ← AR | Jump if not zero |
| D13 | JP | if (AC > 0) then PC ← AR | Jump if positive |
| D14 | JN | if (AC < 0) then PC ← AR | Jump if negative |

### Register Reference Instructions (RRI)

| Bit | Mnemonic | Operation | Description |
|-----|----------|-----------|-------------|
| B0 | CLA | AC ← 0 | Clear accumulator |
| B1 | INC | AC ← AC + 1 | Increment accumulator |
| B2 | HLT | S ← 0 | Halt |

### I/O Instructions (IOI)

| Bit | Mnemonic | Operation | Description |
|-----|----------|-----------|-------------|
| B0 | ION | R ← 1 | Interrupt on |
| B1 | INP | AC(0-7) ← INPR | Input character |
| B2 | OUT | OUTR ← AC(0-7) | Output character |

## Bus Architecture

### Source/Destination Selection

| S3 S2 S1 S0 | Register |
|-------------|----------|
| 0000 | AC |
| 0001 | PC |
| 0010 | AR |
| 0011 | DR |
| 0100 | TR |
| 0101 | IX |
| 0110 | IR |
| 0111 | INPR |
| 1000 | OUTR |
| 1001 | Memory |
| 1010 | Data |

**Example**: `AC ← DR`
- Source: 0011 (DR)
- Destination: 0000 (AC)

## ALU Operations

| S1 S0 Cin | Operation | Description |
|-----------|-----------|-------------|
| 0 0 0 | D = A + B | Add |
| 0 0 1 | D = A + B + 1 | Add with carry |
| 0 1 0 | D = A + B' | Subtract with borrow |
| 0 1 1 | D = A + B' + 1 | Subtract |
| 1 0 0 | D = A | Transfer A |
| 1 0 1 | D = A + 1 | Increment A |
| 1 1 0 | D = A - 1 | Decrement A |
| 1 1 1 | D = A | Transfer A |

### Register Selection for ALU

| Selection | Register |
|-----------|----------|
| 000 | IX |
| 001 | TR |
| 010 | DR |
| 011 | AR |
| 100 | PC |
| 101 | AC |

## Instruction Cycle

### Fetch Phase

```
R'T0: AR ← PC
R'T1: IR ← M[AR], PC ← PC + 1
R'T2: I ← IR(16-17), O ← Decoded(IR(12-15)), AR ← IR(0-11)
```

### Interupt Phase

```
R.T0: AR ← fff
R.T1: INPR ← M[AR], R ← 0
```

### Execute Phase Examples

#### Direct Addressing (LDA)
```
Program: LDA 10 (I=00, O=D2, Address=10)

T0: AR ← PC
T1: IR ← M[AR], PC ← PC + 1
T2: I ← IR(16-17), O ← Decoded(IR(12-15)), AR ← IR(0-11)
    I = 00, O = D2, AR = 10
T3: I0.D15'.T3: NOP (Direct mode, no address translation)
T4: DR ← M[AR]
T5: AC ← DR, SC ← 0
```

#### Indirect Addressing (LDA)
```
Program: LDA [10] (I=01, O=D2, Address=10)

T0: AR ← PC
T1: IR ← M[AR], PC ← PC + 1
T2: I ← IR(16-17), O ← Decoded(IR(12-15)), AR ← IR(0-11)
    I = 01, O = D2, AR = 10
T3: AR ← M[AR] (Indirect addressing)
T4: AC ← M[AR], SC ← 0
```

## Example Program
Load value from memory location 10, add value from 20, store in 30
```assembly
D LDA 10
D ADD 20
D STA 30
HLT
```
