f = open('flags.txt','r')
while True:
    
  
    # Get next line from file
    line = f.readline()
    
    # if line is empty
    # end of file is reached
    if not line:
        break
    print(line)