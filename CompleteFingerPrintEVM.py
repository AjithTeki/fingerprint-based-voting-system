from time import sleep
import serial



vfyPwd = [239, 1, 255, 255, 255, 255, 1, 0, 7, 19, 0, 0, 0, 0, 0, 27]
genImg =[239, 1, 255, 255, 255, 255, 1, 0, 3, 1, 0, 5]
img2tz =[239, 1, 255, 255, 255, 255, 1, 0, 4, 2, 1, 0, 8]
img2tz2 =[239, 1, 255, 255, 255, 255, 1, 0, 4, 2, 2, 0, 9]
regModel = [239, 1, 255, 255, 255, 255, 1, 0, 3, 5, 0, 9]


def findChkSum(pack):
	sum=0
	for i in pack[6::]:
		sum+=i
	return sum



def store_fingr(PageIDLSB):
	storeT =[239, 1, 255, 255, 255, 255, 1, 0, 6,6,1,0,PageIDLSB]
	chkSum = findChkSum(storeT)
	storeT.append(chkSum/256)
	storeT.append(chkSum-256*(chkSum/256))

	print "StoreT:"
	print storeT
	print "Confirm codes and press key to continue.."
	raw_input()
	#import serial
	#b = serial.Serial(PORT,57600)

	#b.timeout = 20
	b.write(vfyPwd)
	result = b.read(12)
	
	if result[9] != '\x00':
		print "PasswordErr"
		#b.close
		return False
	####################################################
	print "Put Finger\n"
	sleep(1)
	while True:
		b.write(genImg)
		result = b.read(12)
		if result[9] != '\x00':
			print "."
		else:
			break
		sleep(1)
	b.write(img2tz)
	result = b.read(12)
	result
	if result[9] != '\x00':
		print "Can't generate Chr file"
		#b.close
		return False
	####################################################
	print "Put Finger again and press key\n"
	raw_input()
	while True:
		sleep(1)
		b.write(genImg)
		result = b.read(12)
		if result[9] != '\x00':
			print "."
		else:
			break
	b.write(img2tz2)
	result = b.read(12)
	

	if result[9] != '\x00':
		print "Can't generate Chr file"
		#b.close
		return False
	print "Chr files Generated"
	####################################################

	b.write(regModel)
	result = b.read(12)
	result
	if result[9] != '\x00':
		print "Something Is wrong"
		if result[9] != '\x00':
			print "Can't compare fingers"
		#b.close
		return False

	print "Template Created"
	####################################################
	print "Storing Template"
	b.write(storeT)
	result=b.read(12)
	result
	if result[9]!='\x00':
		print "Storage Failed"
		print result[9]
		if result[9] == '\x01':
			print "Error Receiving Package"
		if result[9] == '\x0b':
			print "address out of range"
		#b.close
		return False
	print "Template Stored"
	return True
	#print "CooL!!!"
	#raw_input()
	##b.close
#####################################################	
#####################################################
#####################################################
#####################################################



def searchFinger():
	print "Put Finger\n"
	sleep(1)
	while True:
		b.write(genImg)
		result = b.read(12)
		if result[9] != '\x00':
			print "."
		else:
			break
		sleep(1)
	b.write(img2tz)
	result = b.read(12)
	result
	if result[9] != '\x00':
		print "Can't generate Chr file"
		##b.close
		return False
	print "Chr file generated"
	####################################################
	print "Put Finger again and press key\n"
	raw_input()
	while True:
		sleep(1)
		b.write(genImg)
		result = b.read(12)
		if result[9] != '\x00':
			print "."
		else:
			break
	b.write(img2tz2)
	result = b.read(12)
	result

	if result[9] != '\x00':
		print "Can't generate Chr file"
		#b.close
		return False
	print "Chr files Generated"
	####################################################

	b.write(regModel)
	result = b.read(12)
	result
	if result[9] != '\x00':
		print "Something Is wrong"
		if result[9] != '\x00':
			print "Can't compare fingers"
		#b.close
		return False

	print "Template Created"
	####################################################
	b.write(searchPack)
	result = b.read(16)
	result
	if result[9]!='\x00':
		print "Something Is Wrong"
		if result[9]=="\x09":
			print "No match"
		#b.close
		return False
	#print "Match Found at %d with score %d"%(ord(result[10])*256+ord(result[11]),ord(result[12])*256+ord(result[13]))
	print "Match Found"
	print "Press Key to continue"
	raw_input()
	return True

#####################################################
#####################################################
#####################################################
def castVote():
	print "::::Cast Your Vote::::"
	for i in range(3):
		print "%d)Party-%d"%(i+1,i+1)
	voteTo = raw_input("VoteTo:")
	voteTo = int(voteTo)
	if voteTo>3 or voteTo<1:
		print "IncorrectVote"
		return -1
	else:
		votes[voteTo-1] += 1
		print "Vote Sucess To Party:%d"%(voteTo)
		return voteTo

#####################################################
#####################################################
#####################################################
def show():
	print "Results are:::::"
	for i in range(3):
		print "Party-%d\nVotes:%d"%(i+1,votes[i])
	
	maxVotes = max(votes)
	if votes.count(maxVotes) ==1: #Only one winner party votes.count(maxVotes) counts no. of occurance of maxVotes in votes
		print "Winner is Party-%d with %d votes"%(votes.find(maxVotes)+1,maxVotes) #votes.find(maxVote) finds the index of the maxVote
	else:
		#Find all parties with the same max votes
		print "There is a tie between following parties with same votes of %d"%(maxVotes)
		for i in range(3):
			if votes[i] == maxVotes:
				print "Party-%d"%(i+1)


#####################################################
############Finger Pring Storing#####################
#####################################################
#####################################################
fingerPrintID = [] 
for i in range(256):
	fingerPrintID.append(True) 
# fingerPrintID is array of 256. its elements are either true or false
# True indicates that PageID has not been used in r305
# False indcates that PageID has already been used in r305
#####################################################
def getFingerPrintID():
	fingerPrintFile = open("fingers.txt","r") #Open file in read mode
	# fingers.txt stores all the finger prints PageID of r305 which has already been used.
	tmp = fingerPrintFile.readline()
	fingerPrintFile.close()
	if tmp == "":
		return 6
	tmp = tmp.split(',') # Split the string with comma, tmp is now an array of char
	for i in tmp: # for every element of tmp
		fingerPrintID[int(i)] = False

	for i in range(5,256):
		if fingerPrintID[i] == True:
			return i
	print "All fingerPrintID has been used"
	return 6 #If all finger prints has been used, overwrite on 6th postion
#####################################################
def storeFingerPrintID():
	fingerPrintFile = open("fingers.txt","w") #open file in write mode
	tmp = []
	for i in range(256):
		if fingerPrintID[i] == False:
			tmp.append(str(i))
	fingerPrintFile.write(",".join(tmp)) # ",".join(tmp) gives a sting with elemetns of tmp joined with comma (,)
	fingerPrintFile.close()
#####################################################
#####################################################
#####################################################



#####################################################
#############        Vote Storing            ########
#####################################################
#####################################################
votes = [0,0,0]
def loadVotes():
	voteFile = open("votes.txt","r")
	tmp = voteFile.readline()
	tmp = tmp.split(',')
	
	for i in range(3):
		votes[i] = int(tmp[i])
	voteFile.close()
#####################################################
def storeVotes():
	voteFile = open("votes.txt","w")
	tmp = []
	for i in votes:
		tmp.append(str(i)) #convert array of int to array of string, so that it can be writtne like ",".join(ArrayOfStr)
	voteFile.write(",".join(tmp))
	voteFile.close()
#####################################################
#####################################################
#####################################################


#####################################################
###############      Main Loop        ###############
#####################################################
def main():
	PORT = raw_input("PORT:")
	b = serial.Serial(PORT,57600)
	b.timeout = 20
	while True:
		print '''
		operation list:
		1)Store Finger Print
		2)Cast Vote
		3)Show Results
		4)Exit
		'''
		selection=raw_input("Selaect Operation:")
		selection=int(selection)
		if selection==1:
			ID = getFingerPrintID()
			if store_fingr(ID): #IF store sucess mark that id as used
				fingerPrintID[ID] = False
				storeFingerPrintID() #Store finger print PageID list into file again
		elif selection==2:
			if searchFinger()==True:
				loadVotes()	#load votes from file to votes array
				tmp = -1
				while tmp<0:	#Loop till valid vote is casted
					tmp = castVote()	#cast vote returns the party ID which was voted
				storeVotes()	#Store votes array back to file
		elif selection==3:
			loadVotes()	#load votes from file to votes array
			show()
		elif selection==4:
			exit(1)
		else:
			print "Wrong Selection"

if __name__ == '__main__': ## This is to call main function (More formal and easy to debug)
	main()
