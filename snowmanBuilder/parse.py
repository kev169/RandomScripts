import os
import sys
import re

fin = open(sys.argv[1], "r")
readin = fin.read()
fin.close()
foundfunctions = []
r = re.compile("fun_.*.{\n.*.goto .*.\n}")
for match in re.finditer(r, readin):
    foundfunctions.append((match.group().split("(")[0], "%s"%(match.group().split("goto")[1].split(";")[0]).replace(" ", "")))
    #print("Found: %s"%(match.group()))

readin = re.sub(r"fun_.*.{\n.*.goto .*.\n}", "", readin)
for item in foundfunctions:
    #print("REPLACE : %s REPLACED : %s"%(item[0], item[1]))
    readin = readin.replace(item[0], item[1])

#readin = re.sub(r"uint.*.\(.*.\);\n\n", "", readin)
#readin = re.sub(r"int.*.\(.*.\);\n\n", "", readin)

print(readin);
