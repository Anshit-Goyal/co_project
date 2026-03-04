import sys

registers={"zero":"00000","ra":"00001","sp":"00010","gp":"00011","tp":"00100","t0":"00101","t1":"00110","t2":"00111","s0":"01000","fp":"01000","s1":"01001",
             "a0":"01010","a1":"01011","a2":"01100","a3":"01101","a4":"01110","a5":"01111","a6":"10000","a7":"10001","s2":"10010","s3":"10011",
             "s4":"10100","s5":"10101","s6":"10110","s7":"10111","s8":"11000","s9":"11001","s10":"11010","s11":"11011","t3":"11100",
             "t4":"11101","t5":"11110","t6":"11111"}
opcode={
    "add":("R","0000000","000","0110011"),
    "sub":("R","0100000","000","0110011"),
    "sll":("R","0000000","001","0110011"),
    "slt":("R","0000000","010","0110011"),
    "sltu":("R","0000000","011","0110011"),
    "xor":("R","0000000","100","0110011"),
    "srl":("R","0000000","101","0110011"),
    "or":("R","0000000","110","0110011"),
    "and":("R","0000000","111","0110011"),
    "addi":("I",None,"000","0010011"),
    "sltiu":("I",None,"011","0010011"),
    "lw":("I",None,"010","0000011"),
    "jalr":("I",None,"000","1100111"),
    "sw":("S",None,"010","0100011"),
    "beq":("B",None,"000","1100011"),
    "bne":("B",None,"001","1100011"),
    "blt":("B",None,"100","1100011"),
    "bge":("B",None,"101","1100011"),
    "bltu":("B",None,"110","1100011"),
    "bgeu":("B",None,"111","1100011"),
    "lui":("U",None,None,"0110111"),
    "auipc":("U",None,None,"0010111"),
    "jal":("J",None,None,"1101111")
}
def To_Binary(num,bits):
    num1=int(num)
    if num1<0:
        num1=(2**bits)+num
    B=""
    while num1>0:
        rem=num1%2
        B=str(rem)+B
        num1=num1//2
    while len(B)<bits:
        B="0"+B
    return B

def R_type(arr,funct7,funct3,op):
    rd=arr[1]
    rs1=arr[2]
    rs2=arr[3]
    binary=funct7+registers[rs2]+registers[rs1]+funct3+registers[rd]+op
    return binary

def I_type(arr,funct7,funct3,op):
    if arr[0]=="lw":         #lw has format rd,imm,rs1 
        rd=arr[1]
        imm=arr[2]
        rs1=arr[3]
    else:                  #other I type have rd,rs1,imm/offset
        rd=arr[1]
        rs1=arr[2]
        imm=arr[3]
    imm_bin=To_Binary(imm,12)
    binary=imm_bin+registers[rs1]+funct3+registers[rd]+op
    return binary

def S_type(arr,funct7,funct3,op):
    rs2=arr[1]
    imm=arr[2]
    rs1=arr[3]
    imm_bin=To_Binary(imm,12)
    binary=imm_bin[:7]+registers[rs2]+registers[rs1]+funct3+imm_bin[7:]+op    #in string format
    return binary

def B_type(arr,funct7,funct3,op,labels,pc):
    rs1=arr[1]
    rs2=arr[2]
    label=arr[3]
    if label in labels:    #if it is of label format like loop,exit 
        imm=labels[label]-pc
    else:                   #if it is of immediate format
        imm=int(label)
    imm_bin=To_Binary(imm,13)
    binary=imm_bin[0]+imm_bin[2:8]+registers[rs2]+registers[rs1]+funct3+imm_bin[8:12]+imm_bin[1]+op
    return binary

def U_type(arr,funct7,funct3,op):
    rd=arr[1]
    imm=arr[2]
    imm_bin=To_Binary(imm,20)
    binary=imm_bin+registers[rd]+op
    return binary

def J_type(arr,funct7,funct3,op,labels,pc):
    rd=arr[1]
    label=arr[2]
    if label in labels:
        imm=labels[label]-pc
    else:
        imm=int(label)
    imm_bin=To_Binary(imm,21)
    binary=imm_bin[0]+imm_bin[10:20]+imm_bin[9]+imm_bin[1:9]+registers[rd]+op
    return binary

PC=0
labels={}
Inst=[]


def assembler(input_file, output_file):
     global PC, labels, Inst 
     f=open(input_file,"r")
     lines=f.readlines()
     for line in lines:
        line=line.strip()
        if line=="": 
            continue
        if ":" in line: 
            label,Inst=line.split(":") 
            labels[label.strip()]=PC
            line=Inst.strip() 
            if line=="": 
                continue 
        Inst.append(line) 
        PC=PC+4
     PC=0
     output=[]
     for x in Inst:
        x=x.replace(','," ")
        x=x.replace('('," ")
        x=x.replace(')'," ")
        arr=x.split()
        Ist_1=arr[0]
        if Ist_1 not in opcode:
            print("Invalid instruction:",Ist_1)
            continue
        inst_type,funct7,funct3,opc=opcode[Ist_1]
        
        if inst_type=="R":
            binary=R_type(arr,funct7,funct3,opc)
        elif inst_type=="I":
            binary=I_type(arr,funct7,funct3,opc)
        elif inst_type=="S":
            binary=S_type(arr,funct7,funct3,opc)
        elif inst_type=="B":
            binary=B_type(arr,funct7,funct3,opc,labels,PC)
        elif inst_type=="J":
            binary=J_type(arr,funct7,funct3,opc,labels,PC)
        elif inst_type=="U":
           binary=U_type(arr,funct7,funct3,opc)
        output.append(binary)
        PC=PC+4
     with open(output_file,"w") as f:
          for line in output:
               f.write(line+"\n")

def main():
    input_file = "input.txt"
    output_file = "output.txt"

    assembler(input_file, output_file)

if __name__ == "__main__":
    main()


