print("ECE366 Fall 2018 mini ISA assembler, supporting: lw, sw, init, shiftL, shiftR, ")
print("bgtR0, bltR0, sub, add, j")
print("--------")

input_file = open("ISA_machine_code.txt", "r")
output_file = open("ISA_asm.txt","w")

instList = []
instNum = []
count = 0
for code in input_file:
    code = code.replace("\t", "")
    code = code.replace(" ","")     # remove spaces anywhere in line
    if (code == "\n"):              # empty lines ignored
        continue
    instList = instList.replace("\n","")
    instList = instList[1:] #remove parity bit
    instList.append(code)
    instNum.append(count)
    count = count + 1
    
input_file.close()

input_file = open("PatternA.txt", "r")
memList = []
memNum = []
count = 0
for code in input_file:
    code = code.replace("\t", "")
    code = code.replace(" ","")     # remove spaces anywhere in line
    if (code == "\n"):              # empty lines ignored
        continue
    line = line.replace("\n","")
    memList.append(code)
    memNum.append(count)
    count = count + 1
    
input_file.close()
r0 = r1 = r2 = r3 = 0
pc = 0
while pc != 1000:
    line = instList[pc]
    #lw
    if(line[0:5] == '00001'):
        if(line[6] == '0'):          
            y = r0
        elif(line[6] == '1'):
            y = r2
        if line[5] == 0:
            r0 = memList[y]
        elif line[5] == 1:
            r1 = memList[y]
        
       #sw
    elif(line[0:3] == '001'): 
        if line[3] == '0':
            x = r0
        elif line[3] == '1':
            x = r1
        imm = int(line[4:7], 2)
        memList[imm] = x
       #init
    elif(line[0:3] == '011'):
       
        x = repr(int(line[3:5], 2))
        y = repr(int(line[5:7], 2))
        print("init $" + x + ", " + y + "\n")
        output_file.write("init $" + x + ", " + y + "\n")

    #shiftL
    elif(line[0:5] == '01010'):
        x = repr(int(line[5:7], 2))
        print("shiftL $" + x + "\n")
        output_file.write("shiftL $" + x + "\n")

   #shiftR
    elif(line[0:5] == '01011'):
        x = repr(int(line[5:7], 2))
        print("shiftR $" + x + "\n")
        output_file.write("shiftR $" + x + "\n")
        
    #sub
    elif(line[0:4] == '0100'):
        x = repr(int(line[4:6], 2))
        if(line[6] == '0'):          
            y = '0'
        elif(line[6] == '1'):
            y = '2'
        print("sub $" + x + ", $" + y + "\n")
        output_file.write("sub $" + x + ", $" + y + "\n")

    #addi
    elif(line[0:3] == '101'):
        x = repr(int(line[3:5], 2))
        if(line[5:7] == '10'):
            y = '-2'
        elif(line[5:7] == '11'):
            y = '-1'
        elif(line[5:7] == '00'):
            y = '0'
        elif(line[5:7] == '01'):
            y = '1'
        print("addi $" + x + ", " + y + "\n")
        output_file.write("addi $" + x + ", " + y + "\n")
        
    #add
    elif(line[0:4] == '1000'):
        x = repr(int(line[4:6], 2))
        if(line[6] == '0'):
            y = '0'
        else:
            y = '2'
        print("add $" + x + ", $" + y + "\n")
        output_file.write("add $" + x + ", $" + y + "\n")

        #jump
    elif(line[0:2] == '11'):
        x = repr(int(line[2:7], 2))
        print("j " + x + "\n")
        output_file.write("j " + x + "\n")
        
    #bgtR0
    elif(line[0:4] == '0001'):
        if(line[4] == '0'): 
            x = '1'
        elif(line[4] == '1'):
            x = '2'
        if(line[5:7] == '00'):
            y = '1'
        elif(line[5:7] == '01'):
            y = '2'
        elif(line[5:7] == '10'):
            y = '3'
        elif(line[5:7] == '11'):
            y = '4'
        print("bgtR0 $" + x + ", " + y + "\n")
        output_file.write("bgtR0 $" + x + ", " + y + "\n")
        
    #bltR0
    elif(line[0:4] == '1001'):
        if(line[4] == '0'): 
            x = '1'
        elif(line[4] == '1'):
            x = '2'
            
        if(line[5:7] == '00'):
            y = '1'
        elif(line[5:7] == '01'):
            y = '2'
        elif(line[5:7] == '10'):
            y = '3'
        elif(line[5:7] == '11'):
            y = '4'
        print("bgtR0 $" + x + ", " + y + "\n")
        output_file.write("bgtR0 $" + x + ", " + y + "\n")
        
    else:
        print("Unknown instruction:"+ line)

input_file.close()
output_file.close()
