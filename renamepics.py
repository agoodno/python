import sys, os, os.path

def padNum(num):
	if int(num) < 10:
		return "000" + str(num)
	else:
		return "00" + str(num)
		
def rename(picroot, seednum, newprefix="img_"):
	print "Renaming using seed %s" % seednum
	pics = os.listdir(picroot)
	for pic in pics:
		(picbase, picext) = os.path.splitext(pic)
		if picext == ".jpg":
			fullpic = os.path.abspath(os.path.join(picroot, pic))
			newpicbase = padNum(int(picbase) + int(seednum))			
			fullnewpic = os.path.abspath(os.path.join(picroot, newprefix + newpicbase + picext))
			print "Renaming %s to %s" % (fullpic, fullnewpic)
			os.rename(fullpic, fullnewpic)

if __name__ == "__main__":
	rename(sys.argv[1], sys.argv[2])

