__author__ = 'Kevin Haubris'


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


def diff(vw, line):
    file1 = line.split(" ")[0]
    file2 = line.split(" ")[1]
    if file1 == "" or file2 == "":
        vw.vprint("Please enter 2 arguments different files.")
        vw.vprint(file1)
        vw.vprint(file2)
        return
    vw.vprint(file1)
    vw.vprint(file2)
    fp1 = open(file1, "r")
    fp1read = fp1.readlines()
    fp2 = open(file2, "r")
    fp2read = fp2.readlines()
    vw.vprint("Starting File 1")
    functions1 = {}
    functions2 = {}
    mapping = []
    start = 0
    for line in fp1read:
        if line.startswith("+++++"):
            start = 1
        if start == 1 and not line.startswith("\t"):
            if "." in line:
                functions1[line.split(".")[1]] = line
            else:
                functions1[line] = line
    start = 0
    vw.vprint("Comparing Second File to First...")
    for line in fp2read:
        if line.startswith("+++++"):
            start = 1
        if start == 1 and not line.startswith("\t"):
            if "." in line:
                functions2[line.split(".")[1]] = line
                try:
                    equivfunc = functions1[line.split(".")[1]]
                except:
                    equivfunc = ""
            else:
                try:
                    equivfunc = functions1[line]
                except:
                    equivfunc = ""
            #if equivfunc != "":
            mapping.append((line.strip(), equivfunc.strip()))
    codeDiff = {}
    go = 0
    for item in mapping:
        fp1func = item[1]
        fp2func = item[0]
        templist =[]
        for line in fp1read:
            if line.startswith(fp1func):
                go = 1
            elif line.startswith("\t") and go == 1:
                #print(line.strip())
                templist.append(line.strip())
            elif go == 1:
                go = 0
                #print("+++++++++++++++++++++")
            else:
                continue
        templist2 = []
        for line in fp2read:
            if line.startswith(fp2func):
                go = 1
            elif line.startswith("\t") and go == 1:
                #print(line.strip())
                templist2.append(line.strip())
            elif go == 1:
                go = 0
                #print("++++++++++++++++++++")
            else:
                continue
        codeDiff[item] = (templist, templist2)

    for item in codeDiff.keys():
        print("%s %s"%(item[1].ljust(75), item[0].ljust(75)))
        list1 = codeDiff[item][0]
        list2 = codeDiff[item][1]
        #print(type(list1))
        #print(type(list2))
        import itertools
        import regex
        try:
            for x,y in itertools.izip_longest(list1, list2):
                try:
                    match = regex.search(r'(%s){e<=6}' % x, y)
                except:
                    match = None
                if match:
                    matchchar = "\033[32m++>"
                else:
                    matchchar = "\033[31m-->"
                if x == None:
                    print("%s\t%s  : \t%s\033[39m" % (matchchar,"".ljust(71), y.ljust(71)))
                elif y == None:
                    print("%s\t%s  : \t%s\033[39m" % (matchchar,x.strip().ljust(71), "".ljust(71)))
                else:
                    print("%s\t%s  : \t%s\033[39m" % (matchchar,x.strip().ljust(71), y.ljust(71)))
        except Exception, e:
            print(e)

def vivExtension( vw, vwgui ):
    # Lets make a new command!
    vw.registerCmdExtension( diff )
