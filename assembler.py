#!/bin/python
import sys

RRIS = {
    "CLA": "000000000000",
    "INC": "000000000001",
    "HLT": "000000000010"
}

IOIS = {
    "ION": "000000000000",
    "INP": "000000000001",
    "OUT": "000000000010",
}

MRIS = {
    "AND": "0000",
    "ADD": "0001",
    "LDA": "0010",
    "STA": "0011",
    "BUN": "0100",
    "BSA": "0101",
    "ISZ": "0110",
    "SUB": "0111",
    "LIX": "1000",
    "LIA": "1001",
    "INX": "1010",
    "JZ":  "1011",
    "JNZ": "1100",
    "JP":  "1101",
    "JN":  "1110"
}

AMS = {
    "D": "00",
    "I": "01",
    "X": "10"
}


def main():
    try:
        with open(sys.argv[1], 'r') as file:
            for line_num, line in enumerate(file, start=1):
                c_line = line.strip()
                if not c_line:
                    continue

                token = c_line.split()
                output = ""

                # ---------- RRIS ----------
                if token[0] in RRIS:
                    ins = token[0]
                    output += "00"
                    output += "1111"
                    output += RRIS[ins]

                # ---------- IOIS ----------
                elif token[0] in IOIS:
                    ins = token[0]
                    output += "11"
                    output += "1111"
                    output += IOIS[ins]

                # ---------- MRIS ----------
                else:
                    if len(token) < 3:
                        raise Exception(
                            f"LINE {line_num}: MRIS requires <addressing_mode> <instruction> <address>"
                        )

                    am, ins, addr = token[0], token[1], token[2]

                    if am not in AMS:
                        raise Exception(
                            f"LINE {line_num}: Addressing Mode -> {am} not supported"
                        )

                    if ins not in MRIS:
                        raise Exception(
                            f"LINE {line_num}: Instruction -> {ins} not supported"
                        )

                    output += AMS[am]
                    output += MRIS[ins]

                    addr = int(addr)
                    if addr < 0:
                        addr_bin = format((1 << 12) + addr, "012b")
                    else:
                        addr_bin = format(addr, "012b")

                    output += addr_bin

                print(format(int(output, 2), "05X"))

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
