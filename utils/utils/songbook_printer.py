FIELD_ORDER = ["start_at", "time"]
EDGE_FIELD_ORDER = ["edge", "flame", "dir", "distance"]
INDENT = 2


def songbook_printer(y, prefactor=1, file=None, indent=INDENT):
    print("version: 1.0", file=file)
    if "author" in y:
        print("author: {}".format(y['author']), file=file)
    if "mp3" in y:
        print("mp3: {}".format(y['mp3']), file=file)
    print("songbook:")
    for measure in y['songbook']:
        tab = " "*indent
        for ix in range(len(FIELD_ORDER)):
            f = FIELD_ORDER[ix]
            if ix == 0:
                idt = tab + "- "
            else:
                idt = tab + "  "
            print("{}{}: {}".format(idt, f, measure[f]*prefactor))
        print(idt + "edges:")
        for edge in measure['edges']:
            for jx in range(len(EDGE_FIELD_ORDER)):
                ef = EDGE_FIELD_ORDER[jx]
                etab = " "*indent*2
                if jx == 0:
                    idt = etab + " - "
                else:
                    idt = etab + "   "
                if ef in edge:
                    print("{}{}: {}".format(idt, ef, edge[ef]))
