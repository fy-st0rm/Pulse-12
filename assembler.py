#!/bin/python
import sys

RRIS = {
    "CLA": "000000000000",
    "INC": "000000000001",
    "HLT": "000000000010"
}

IOIS = {
    "INP": "000000000000",
    "OUT": "000000000001",
    "SKI": "000000000010",
    "SKO": "000000000011",
    "ION": "000000000100",
    "IOF": "000000000101"
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
            line_num = 0
            for line in file:
                line_num += 1
                c_line = line.replace('\n', '')
                token = c_line.split(' ')
                am = token[0]
                ins = token[1]

                if not am in AMS:
                    raise Exception(f"LINE {line_num}: Addressingg Mode -> {am} not supported")
                
                output = ""
                if ins in RRIS:
                    output += "00"
                    output += "1111"
                    output += RRIS[ins]
                elif ins in IOIS:
                    output += "11"
                    output += "1111"
                    output += IOIS[ins]
                elif ins in MRIS:
                    output += AMS[am]
                    output += MRIS[ins]

                    if len(token) >= 3:
                        res=''
                        if int(token[2]) < 0:
                            res = format((1 << 12)+ token[2], '012b')
                        else:
                            res = format(int(token[2]), '012b')
                        output += res 
                    else:
                        raise Exception(f"LINE {line_num}:{line} [address_data] Memory Register Instructions require a address at the end")
                else:
                    raise Exception(f"LINE {line_num}: Instruction -> {ins} not supported")
                print(format(int(output,2), '05X'))
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
