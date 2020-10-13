#!/usr/bin/python
import os
import sys

"""
Initialization:
  1. Parse text file
  2. Symbol table

First Pass:
  1. Read all commands, labels and updating the symbol table

Main Loop:
  1. Get the next Assembly Language Command and parse it
  2. For A-commands: Translate symbols to binary address
  3. For C-commands: get code for each part and put together
  Output the resulting machine language command
"""
variableSpot = 16       # memory address for user variables
fileName = sys.argv[1]  # assembler file name


class SymbolTables():
    """
    class containing symbol tables
    """

    # dictionary for standard codes
    table = {
        "SP": 0,
        "LCL": 1,
        "ARG": 2,
        "THIS": 3,
        "THAT": 4,
        "SCREEN": 16384,
        "KBD": 24576,
    }

    # dictionaries to store translations of c-instructions
    comp = {
        "0": "0101010",
        "1": "0111111",
        "-1": "0111010",
        "D": "0001100",
        "A": "0110000",
        "!D": "0001101",
        "!A": "0110001",
        "-D": "0001111",
        "-A": "0110011",
        "D+1": "0011111",
        "A+1": "0110111",
        "D-1": "0001110",
        "A-1": "0110010",
        "D+A": "0000010",
        "D-A": "0010011",
        "A-D": "0000111",
        "D&A": "0000000",
        "D|A": "0010101",
        "M": "1110000",
        "!M": "1110001",
        "-M": "1110011",
        "M+1": "1110111",
        "M-1": "1110010",
        "D+M": "1000010",
        "D-M": "1010011",
        "M-D": "1000111",
        "D&M": "1000000",
        "D|M": "1010101"
    }
    dest = {
        "null": "000",
        "M": "001",
        "D": "010",
        "A": "011",
        "MD": "100",
        "AM": "101",
        "AD": "110",
        "AMD": "111",
    }
    jump = {
        "null": "000",
        "JGT": "001",
        "JEQ": "010",
        "JGE": "011",
        "JLT": "100",
        "JNE": "101",
        "JLE": "110",
        "JMP": "111",
        "R0": 0,
        "R1": 1,
        "R2": 2,
        "R3": 3,
        "R4": 4,
        "R5": 5,
        "R6": 6,
        "R7": 7,
        "R8": 8,
        "R9": 9,
        "R10": 10,
        "R11": 11,
        "R12": 12,
        "R13": 13,
        "R14": 14,
        "R15": 15,
    }

    pass


class Parser():
    """
    Parses the input assembler file
    """

    def removeWhitespace(line):
        character = line[0]
        if character == "/" or character == "\n":
            return ""
        elif character == " ":
            return Parser.removeWhitespace(line[1:])
        else:
            return character + Parser.removeWhitespace(line[1:])

    def consistency(line):
        line = line[:-1]
        if "=" not in line:
            line = "null=" + line
        if ";" not in line:
            line = line + ";null"
        return line

    pass


class CodeOps():
    """
    Different code operations
    """

    def addUserVariable(label):
        global variableSpot
        SymbolTables.table[label] = variableSpot
        variableSpot += 1
        return SymbolTables.table[label]

    def aInstruction(line):
        if line[1].isalpha():
            label = line[1:-1]
            a = SymbolTables.table.get(label, -1)
            if a == -1:
                a = CodeOps.addUserVariable(label)
        else:
            a = int(line[1:])
        binary = bin(a)[2:].zfill(16)
        return binary

    def cInstruction(line):
        line = Parser.consistency(line)
        temp = line.split("=")
        destination = SymbolTables.dest.get(temp[0], "destination failure")
        temp = temp[1].split(";")
        computation = SymbolTables.comp.get(temp[0], "computation failure")
        jumping = SymbolTables.jump.get(temp[1], "jump failure")
        return computation, destination, jumping

    def translation(line):
        if line[0] == "@":
            return CodeOps.aInstruction(line)
        else:
            bins = CodeOps.cInstruction(line)
            return "111" + bins[0] + bins[1] + bins[2]
    pass


def main():
    assembly = open(fileName + ".asm")
    temp = open(fileName + ".tmp", "w")

    lineVal = 0
    for line in assembly:
        noWhite = Parser.removeWhitespace(line)
        if noWhite != "":
            if noWhite[0] == "(":
                label = noWhite[1:-1]
                SymbolTables.table[label] = lineVal
                noWhite = ""
            else:
                lineVal += 1
                temp.write(noWhite + "\n")
    assembly.close()

    temp = open(fileName + ".tmp")
    hack = open(fileName + ".hack", "w")
    for line in temp:
        translated = CodeOps.translation(line)
        hack.write(translated + "\n")
    temp.close()
    hack.close()
    os.remove(fileName + ".tmp")


""" running the program """
main()
