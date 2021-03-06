#!/usr/bin/python
import os
import math
#import time
def transform(col1,colLs1,col2,colLs2,src,dest,annotations,structures):

	#print "Read"
	#start = time.clock()
	dictList = {}
	index = 0
	scoreSumPerGene = {}
	scoreSqSumPerGene = {}
	countPerGene = {}
	for annot in annotations:
		#header =  col1
		for f in annot:
			#header = header+","+str(f['sample'])  #read sample names
			typeFile = src+str(f['uri']).split("..")[1]  #read file names
			with open(typeFile) as fn:
				
				flines = fn.readlines()
				
				
				fpkmDict = {}
				for lines in flines:

					temp = lines.rstrip().split("	")
					#print len(temp)
					if len(temp) < 9:
						print typeFile
						print lines
						continue
					gid = ""
					tif = ""
					fpkm = ""
					# if "feature" column (col 3) is "transcript", only read that line

					if "transcript" in temp[2]:
						temp2 = temp[colLs1[index]].split(";")
						for elem2 in range(len(temp2)):
							if col1 in temp2[elem2]:
								gid = temp2[elem2].rstrip().lstrip().split(" ")[1]
							#print gid

						temp2 = temp[colLs2[index]].split(";")
						for elem2 in range(len(temp2)):
							#print temp2[elem2]
							if col2 in temp2[elem2]:
								fpkm = float(temp2[elem2].rstrip().lstrip().split(" ")[1].replace("\"",''))
					
						if len(gid)>0: #if gene id non-empty

							fpkmDict[gid] = fpkm 
							if gid not in countPerGene:
								countPerGene[gid] = 1
								scoreSumPerGene[gid] = float(fpkm)
								scoreSqSumPerGene[gid] = float(fpkm)*float(fpkm)
							else:
								countPerGene[gid] = countPerGene[gid]+1
								scoreSumPerGene[gid] = scoreSumPerGene[gid]+float(fpkm)
								scoreSqSumPerGene[gid] = scoreSqSumPerGene[gid]+float(fpkm)*float(fpkm) 
					

				dictList[str(f['sample'])] = fpkmDict

		index = index+1
	keyList = set()
	header = " \t"
	for d in dictList:
		for key in dictList[d]:
			keyList.add(key)

	#print time.clock()-start

	#print "write"
	#start = time.clock()
	f = open(dest+'bagit_data.df','w')

	##header
	

	for key in keyList:
		header =  header + "\t" + key

	header = header+'\n'
	f.write(header.replace("\"",'')) 

	
	### each row
	for d in dictList:
		#line = d
		f.write(d)
		for key in keyList:
			if key in dictList[d]:
				#line = line+"\t"+str(dictList[d][key])
				f.write('\t')

				mean = scoreSumPerGene[key]/countPerGene[key]
				sqVal = (scoreSumPerGene[key]*scoreSumPerGene[key])/countPerGene[key]
				

				if sqVal < scoreSqSumPerGene[key]:
					stdev = math.sqrt((scoreSqSumPerGene[key] - sqVal)/countPerGene[key])
					normalizedValue = abs(dictList[d][key]-mean)/stdev
				else:
					normalizedValue = dictList[d][key]

				f.write(str(normalizedValue))
			else:
				#line = line+"\t "
				f.write('\t ')
		#line = line+'\n'
		f.write('\n')
	
		   	
	f.close()
	#print time.clock()-start
