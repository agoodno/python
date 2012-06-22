import sys, os, os.path

def padNum(num):
	return "0" + str(num)
		
def fix(picroot, fixnum):
	print "Renaming %s" % picroot
	pics = os.listdir(picroot)
	pics.sort(reverse=True)
	for pic in pics:
		(picbase, picext) = os.path.splitext(pic)
		#print picbase, picext, int(picbase[4:])
		if (picext == ".jpg" or picext == ".avi") and (int(picbase[4:]) > int(fixnum)):
			fullpic = os.path.abspath(os.path.join(picroot, pic))
			newpicbase = padNum(int(picbase[4:]) + 1)
			fullnewpic = os.path.abspath(os.path.join(picroot, "img_" + newpicbase + picext))
			print "Renaming %s to %s" % (fullpic, fullnewpic)
			#os.rename(fullpic, fullnewpic)

if __name__ == "__main__":
	fix(sys.argv[1], sys.argv[2])
