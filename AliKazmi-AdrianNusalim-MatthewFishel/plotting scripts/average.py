filepath = 'varied_density_output_algo1.txt'
import sys 
filepath = sys.argv[1]
avgDigs=0
avgTime=0
print("numsquares dig_count bomb_count time")
with open(filepath) as fp:
   line = fp.readline() #ignore first line 
   
   line=fp.readline()
   cnt = 1
   while line:
       linearr=line.split()
       avgDigs+=float(linearr[1])
       avgTime+=float(linearr[3])
       if(cnt % 5==0): 
           print(linearr[0]+" "+str(avgDigs)+" "+linearr[2]+" "+str(avgTime))
           avgDigs=0
           avgTime=0 
       line = fp.readline()
       line=fp.readline()
       cnt += 1
