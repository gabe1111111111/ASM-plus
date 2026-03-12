package com.example;
/*
0x00 ADD
0x01 AND
0x02 OR
0x03 XOR
0x04 ECHO
0x05 LSFT
0x06 SUB
0x07 NAND
0x08 NOR
0x09 XNOR
0x0A NOT
0x0B RSFT
0x0C NOOP
0x0D NOOP
0x0E NOOP
0x0F NOOP
0x10 BREQ
0x11 BRGT
0x12 BRLT
0x13 BRNEQ
0x14 BRGEQ
0x15 BRLEQ
0x16 LDA
0x17 LDB
0x18 ST
0x19 LDRF
0x1A STRF
0x1B LEA
0x1C STI
0x1D PERADD
0x1E PEROPP
0x1F PERDAT
0x20 PEREXE
0x22 PERLD
0x23 TRAP
*/



/**
 * assembler for custom architecture to be built on bread boards
 * @author Gabriel Lacey
 */


public class MyComputerAssembler implements Assembler{
    
    @Override
    public String getName() {
        return "MyComputer";
    }

    @Override
    public Error assemble(ArrayList<ArrayList<String>> input, String outputFile) {
        ArrayList<MapEntry<String, Integer>> symbolTable = new ArrayList<>();
        for (int i = 0; i < input.size(); i++){
            if(input.get(i).size() == 1){
                symbolTable.add(new MapEntry<>(input.get(i).get(0), i));
            }
        }
        ArrayList<Byte> output = new ArrayList<>();
        for (int i = 0; i < input.size(); i++){
            byte opp = -1;//noop, last instruction in bit opp code so last one to get used as isa expands 
            byte bottom = 0;
            switch(input.get(i).get(0)){
            case "ADD"://adds a register to b register and stores it to specified register
                opp = 0;
                bottom = (byte) (Integer.parseInt(input.get(i).get(1)));
                break;
            case "AND"://ands a register with b register and stores it to specified register
                opp = 1;
                bottom = (byte) (Integer.parseInt(input.get(i).get(1)));
                break;
            case "OR"://ors a register with b register and stores it to specified register
                opp = 2;
                bottom = (byte) (Integer.parseInt(input.get(i).get(1)));
                break;
            case "XOR"://xors a register with b register and stores it to specified register
                opp = 3;
                bottom = (byte) (Integer.parseInt(input.get(i).get(1)));
                break;
            case "ECHO"://pushes A register through to output and saves to specifies register register allows things like storing to ram and moving within register file
                opp = 4;
                bottom = (byte) (Integer.parseInt(input.get(i).get(1)));
                break;
            case "LSFT"://left shifts a register and stores it to specified register
                opp = 5;
                bottom = (byte) (Integer.parseInt(input.get(i).get(1)));
                break;
            case "SUB"://subtracts a register from b register and stores it to specified register
                opp = 6;
                bottom = (byte) (Integer.parseInt(input.get(i).get(1)));
                break;
            case "NAND"://nands a register with b register and stores it to specified register
                opp = 7;
                bottom = (byte) (Integer.parseInt(input.get(i).get(1)));
                break;
            case "NOR"://nors a register with b register and stores it to specified register
                opp = 8;
                bottom = (byte) (Integer.parseInt(input.get(i).get(1)));
                break;
            case "XNOR"://xnors a register with b register and stores it to specified register
                opp = 9;
                bottom = (byte) (Integer.parseInt(input.get(i).get(1)));
                break;
            case "NOT"://inverts a register and stores it to specified register
                opp = 10;
                bottom = (byte) (Integer.parseInt(input.get(i).get(1)));
                break;
            case "RSFT"://right shifts a register and stores it to specified register
                opp = 11;
                bottom = (byte) (Integer.parseInt(input.get(i).get(1)));
                break;
            case "BREQ"://branches to immediate value or label if a and b registers are equal
                opp = 16;
                try {
                    bottom = (byte) Integer.parseInt(input.get(i).get(1));
                } catch (NumberFormatException e) {
                    bottom = (byte)(int) symbolTable.contains(new MapEntry<>(input.get(i).get(1), 0), false).value;
                }
                break;
            case "BRGT"://branches to immediate value or label if a > b 
                opp = 17;
                try {
                    bottom = (byte) Integer.parseInt(input.get(i).get(1));
                } catch (NumberFormatException e) {
                    bottom = (byte)(int) symbolTable.contains(new MapEntry<>(input.get(i).get(1), 0), false).value;
                }
                break;
            case "BRLT"://branches to immediate value or label if a < b
                opp = 18;
                try {
                    bottom = (byte) Integer.parseInt(input.get(i).get(1));
                } catch (NumberFormatException e) {
                    bottom = (byte)(int) symbolTable.contains(new MapEntry<>(input.get(i).get(1), 0), false).value;
                }
                break;
            case "BRNEQ"://branches to immediate value or label if a and b registers are not equal
                opp = 19;
                try {
                    bottom = (byte) Integer.parseInt(input.get(i).get(1));
                } catch (NumberFormatException e) {
                    bottom = (byte)(int) symbolTable.contains(new MapEntry<>(input.get(i).get(1), 0), false).value;
                }
                break;
            case "BRGEQ"://branches to immediate value or label if a >= b
                opp = 20;
                try {
                    bottom = (byte) Integer.parseInt(input.get(i).get(1));
                } catch (NumberFormatException e) {
                    bottom = (byte)(int) symbolTable.contains(new MapEntry<>(input.get(i).get(1), 0), false).value;
                }
                break;
            case "BRLEQ"://branches to immediate value or label if a <= b
                opp = 21;
                try {
                    bottom = (byte) Integer.parseInt(input.get(i).get(1));
                } catch (NumberFormatException e) {
                    bottom = (byte)(int) symbolTable.contains(new MapEntry<>(input.get(i).get(1), 0), false).value;
                }
                break;
            case "LDA"://loads specified register to a register
                opp = 22;
                bottom = (byte) (Integer.parseInt(input.get(i).get(1)));
                break;
            case "LDB"://loads specified register to a register
                opp = 23;
                bottom = (byte) (Integer.parseInt(input.get(i).get(1)));
                break;
            case "ST"://stores output register to ram address
                opp = 24;
                try {
                    bottom = (byte) Integer.parseInt(input.get(i).get(1));
                } catch (NumberFormatException e) {
                    bottom = (byte)(int) symbolTable.contains(new MapEntry<>(input.get(i).get(1), 0), false).value;
                }
                break;
            case "PUSH"://push specified register to stack
                opp = 25;
                bottom = (byte) (Integer.parseInt(input.get(i).get(1)));
                break;
            case "POP"://pops stack to specifies register
                opp = 26;
                bottom = (byte) (Integer.parseInt(input.get(i).get(1)));
                break;
            case "LEA"://loads current address to specified register
                opp = 27;
                bottom = (byte) (Integer.parseInt(input.get(i).get(1)));
                break;
            case "LDI":// loads immediate value to a register
                opp = 28;
                bottom = (byte) (Integer.parseInt(input.get(i).get(1)));
                break;
            case "PERADD"://loads specified register to port as a device address
                opp = 29;
                bottom = (byte) (Integer.parseInt(input.get(i).get(1)));
                break;
            case "PEROPP"://loads specified register to port as a opp code
                opp = 30;
                bottom = (byte) (Integer.parseInt(input.get(i).get(1)));
                break;
            case "PERDAT"://loads specified register to port as data
                opp = 31;
                bottom = (byte) (Integer.parseInt(input.get(i).get(1)));
                break;
            case "PEREXE"://tells peripheral to execute command
                opp = 32;
                break;
            case "PERLD"://loads peripheral input data to ram
                opp = 33;
                bottom = (byte) (Integer.parseInt(input.get(i).get(1)));
                break;
            case "JMP"://unconditional jump
                opp = 34;
                try {
                    bottom = (byte) Integer.parseInt(input.get(i).get(1));
                } catch (NumberFormatException e) {
                    bottom = (byte)(int) symbolTable.contains(new MapEntry<>(input.get(i).get(1), 0), false).value;
                }
                break;
            case "TRAP"://executes a trap instruction(os api)
                opp = 35;
                bottom = (byte) (Integer.parseInt(input.get(i).get(1)));
                break;
            default:
                break;
        }
        output.add(opp);
        output.add(bottom);
        }
        return new Error(Errors.noError);
    }

    @Override
    public String[] supportedOps() {
        return new String[] {"ADD", "AND", "OR", "XOR", "ECHO", "LSFT", "SUB", "NAND", "NOR", "XNOR", "NOT", "RSFT", "NOOP", "NOOP", "NOOP", "NOOP", "BREQ", "BRGT", "BRLT", "BRNEQ", "BRGEQ", "BRLEQ", "LDA", "LDB", "ST", "LDRF", "STRF", "LEA", "PERADD", "PEROPP", "PERDAT", "PEREXE", "PERLD", "TRAP"};
    }

}
