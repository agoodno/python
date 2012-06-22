import sys, os, os.path

def padNum(num):
	if int(num) < 10:
		return "000" + str(num)
	else:
		return "0" + str(num)
		
def fix(picroot):
	print "Renaming %s" % picroot
	pics = os.listdir(picroot)
	for pic in pics:
		(picbase, picext) = os.path.splitext(pic)
		if (picext == ".jpg" or picext == ".mvi") and len(picbase) == 9:
			fullpic = os.path.abspath(os.path.join(picroot, pic))
			newpicbase = padNum(int(picbase[4:]))
			fullnewpic = os.path.abspath(os.path.join(picroot, "img_" + newpicbase + picext))
			print "Renaming %s to %s" % (fullpic, fullnewpic)
			os.rename(fullpic, fullnewpic)

if __name__ == "__main__":
	fix(sys.argv[1])
