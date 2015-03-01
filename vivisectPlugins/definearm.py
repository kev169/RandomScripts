__author__ = 'Kevin Haubris'


def armdefine(vw, line):
    functions = vw.getNames()
    functiondict = {}
    for item in functions:
        functiondict[item[0]] = item[1]
    opcodes = {}
    disassembly = {}
    calcdict = {}
    for fva in functions:
        locs, funcs, names, comments, extras = vw.getRenderInfo(fva[0], 12)
        vw.vprint("0x%08x - %s" % (fva))
        templist = []
        tempkey = ""
        if fva[1].startswith("sub_"):
            for item in locs:
                lva, lsize,temp1, temp2 = item
                if tempkey == "":
                    tempkey = lva
                try:
                    opcode = vw.readMemory(lva, lsize)
                    opcodes[lva] = opcode
                except:
                    continue
            for key in extras.keys():
                disassembly[key] = (opcodes[key].encode("hex"), extras[key])
                templist.append(extras[key])
            calcdict[tempkey] = templist
    for key in sorted(disassembly.iterkeys()):
        try:
            vw.vprint("\t0x%08x: %s %s\n"%(key,disassembly[key][0].ljust(20), disassembly[key][1]))
        except:
            continue

    for key in calcdict.keys():
        vw.vprint("%s - getName output %s" % (key, vw.getName(key)))
        calculated = 0
        for item in calcdict[key]:
            try:
                localint = int(str(item).split("0x")[1].replace("]!",""), 16)
                calculated += localint
                vw.vprint("\t%s" % (localint))
            except Exception as e:
                vw.vprint("%s"%(e))
        vw.vprint("calculated = %s" % (hex(calculated)))
        foundname = vw.getName(calculated).split(".")[1]
        if not str(foundname).startswith("_"):
            foundname = foundname.split("_")[0]
        vw.vprint("Name : %s" % ( foundname))
        vw.makeName(key, foundname)


def vivExtension( vw, vwgui ):
    # Lets make a new command!
    vw.registerCmdExtension( armdefine )