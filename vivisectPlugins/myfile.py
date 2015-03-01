__author__ = 'Kevin Haubris'


def dump(vw, line="Defaultfile.code"):
    '''
    Call plugin with dump filename.asm
    '''
    vw.vprint('Starting Assembly Dump....')
    fout = open(line, "w")
    # Any vivisect API is usable here...
    # see any of the do_<blah> methods in vivisect/cli.py
    # for examples...
    #functions = vw.getFunctions()
    functions = vw.getNames()
    functiondict = {}
    fout.write("FunctionList:\n")
    for item in functions:
        #print("\t"+str(item))
        fout.write("\t0x%08x: %s\n"%(item))
        functiondict[item[0]] = item[1]
    fout.write("+++++++++++++++++++++++++++++++++++++++++++++++\n")
    opcodes = {}
    disassembly = {}
    vw.vprint("Found functions..")
    for fva in functions:
        locs, funcs, names, comments, extras = vw.getRenderInfo(fva[0],3000)
        vw.vprint("0x%08x - %s" % (fva))
        for item in locs:
            lva, lsize,temp1, temp2 = item
            try:
                opcode = vw.readMemory(lva, lsize)
                opcodes[lva] = opcode
            except:
                continue
        for key in extras.keys():
                    disassembly[key] = (opcodes[key].encode("hex"), extras[key])
    for key in sorted(disassembly.iterkeys()):
        try:
            fout.write("%s\n"%(functiondict[key]))
            fout.write("\t0x%08x: %s %s\n"%(key,disassembly[key][0].ljust(20),disassembly[key][1]))
        except:
            fout.write("\t0x%08x: %s %s\n"%(key,disassembly[key][0].ljust(20),disassembly[key][1]))


def vivExtension( vw, vwgui ):
    # Lets make a new command!
    vw.registerCmdExtension( dump )
