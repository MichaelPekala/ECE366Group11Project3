input_file = open("i_mem.txt", "r")
output_file = open("d_mem_output.txt","w")

instList = []
count = 0
for code in input_file:
    line = code.replace("\t", "")
    line = line.replace(" ","")     # remove spaces anywhere in line
    if (line == "\n"):              # empty lines ignored
        continue
    line = line.replace("\n","")
    line = line[1:] #remove parity bit
    instList.append(line)
    count = count + 1
    
input_file.close()

input_file = open("d_mem.txt", "r")
memList = []
count = 0
for code in input_file:
    line = code.replace("\t", "")
    line = line.replace(" ","")     # remove spaces anywhere in line
    if (line == "\n"):              # empty lines ignored
        continue
    line = line.replace("\n","")
    line = int(line,2)
    memList.append(line)
    
input_file.close()
r = [0,0,0,0]
pc = 0
for foo in range(len(instList)):
    line = instList[pc]
    #lw
    if(line[0:5] == '00001'):
        if(line[6] == '0'):          
            y = r[0]
        elif(line[6] == '1'):
            y = r[2]
        x = int(line[5],2)
        r[x] = memList[y]
                
       #sw
    elif(line[0:3] == '001'): 
        imm = int(line[4:7], 2)
        memList[imm] = r[int(line[3],2)] #line[3] is Rx
       
        #init
    elif(line[0:3] == '011'):
        x = int(line[3:5], 2)
        imm = int(line[5:7], 2)
        r[x] = imm

    #shiftL
    elif(line[0:5] == '01010'):
        x = int(line[5:7], 2)
        r[x] = r[x]*2

   #shiftR
    elif(line[0:5] == '01011'):
        x = int(line[5:7], 2)
        r[x] = r[x]*2
        
    #sub
    elif(line[0:4] == '0100'):
        x = int(line[4:6], 2)
        if(line[6] == '0'):          
            y = r[0]
        elif(line[6] == '1'):
            y = r[2]
        r[x] = r[x] - y

    #addi
    elif(line[0:3] == '101'):
        x = int(line[3:5], 2)
        if(line[5:7] == '10'):
            y = -2
        elif(line[5:7] == '11'):
            y = -1
        elif(line[5:7] == '00'):
            y = 0
        elif(line[5:7] == '01'):
            y = 1
        r[x] = r[x] + y
        
    #add
    elif(line[0:4] == '1000'):
        x = int(line[4:6], 2)
        if(line[6] == '0'):
            y = r[0]
        else:
            y = r[2]
        r[x] = r[x] + y

        #jump
    elif(line[0:2] == '11'):
        imm = repr(int(line[2:7], 2))
        #pc= pc + 1
        pc = imm
        
    #bgtR0
    elif(line[0:4] == '0001'):
        if(line[4] == '0'): 
            x = r[1]
        elif(line[4] == '1'):
            x = r[2]
        if(line[5:7] == '00'):
            y = 1
        elif(line[5:7] == '01'):
            y = 2
        elif(line[5:7] == '10'):
            y = 3
        elif(line[5:7] == '11'):
            y = 4
        if (x > 0):
            pc = pc + imm
        
    #bltR0
    elif(line[0:4] == '1001'):
        if(line[4] == '0'): 
            x = r[1]
        elif(line[4] == '1'):
            x = r[2]
            
        if(line[5:7] == '00'):
            y = 1
        elif(line[5:7] == '01'):
            y = 2
        elif(line[5:7] == '10'):
            y = 3
        elif(line[5:7] == '11'):
            y = 4
        if (x < 0):
            pc = pc + imm
        
    else:
        print("Unknown instruction:"+ line)
    pc = pc + 1
    count = count + 1

for j in memList:
    j = format(j, '016b')
    output_file.write(j + '\n')
    
output_stats = open("stat_mem.txt","w")
r[0] = repr(r[0])
r[1] = repr(r[1])
r[2] = repr(r[2])
r[3] = repr(r[3])
output_stats.write("r0 = " + r[0] + '\n')
output_stats.write("r1 = " + r[1] + '\n')
output_stats.write("r2 = " + r[2] + '\n')
output_stats.write("r3 = " + r[3] + '\n')
output_stats.write("DIC count = " + repr(count) + '\n')
output_stats.close()   
print("Final DIC count is: {}".format(count))
input_file.close()
output_file.close()
