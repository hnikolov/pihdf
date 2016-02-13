from str_builder import StrBuilder
from pihdf import mylog

def print_dotty_file(mfdo):
    '''|
    | Create <module_name>.dot, a dotty graph representing the connections between the modules of a structured design
    |________'''
    s = StrBuilder()
    filename =  mfdo.c_path + '/' + mfdo.module_name + ".dot"

    my_graph = []

    for i in mfdo.interfaces:
        if "direction" in i:
            if i["direction"]=="IN":
                my_graph.append([i["name"], "IN", ''])
            elif i["direction"]=="OUT":
                my_graph.append([i["name"], '', "OUT"])
        else: # TODO: Bus interface
            mylog.warn("Top-level interface '{:}' has no direction! This interface will not be present in the .dot file!".format(i["name"]))
            #my_graph.append([i["name"], '', ''])

    for i in mfdo.local_interfaces:
        my_graph.append([i["name"], '', ''])

    # What about parameters?
    # What about single source multiple destinations?
    for m in mfdo.modules:
        for c in m["connections"]:
            for i in my_graph:
                if c["connect_to"] == i[0]:
                    my_position = 1 if c["direction"]=='OUT' else 2
                    i[my_position] = m["name"]

    # Perform some checks on the graph
    errs = False
    for e in my_graph:
        if e[1]=='':
            mylog.warn("Interface '{:}' has destination ({:}) but no source!".format(e[0],e[2]))
            e[1] = "ERR_SRC"
            errs = True

        if e[2]=='':
            mylog.warn("Interface '{:}' has source ({:}) but no destination!".format(e[0],e[1]))
            e[2] = "ERR_DST"
            errs = True

    # Consolidate all in and out edges between two nodes into single in and single out edge
    my_new_graph = []
    my_dict = {}
    for e in my_graph:
        my_name = e[0]
        my_dst  = e[1]
        my_src  = e[2]
        my_new_name = ''
        for ee in my_graph:
            if ee[1] == my_dst and ee[2] == my_src:
                my_new_name += ee[0] + "\\n"

        if not (my_dst,my_src) in my_dict:
            my_dict[(my_dst,my_src)]=1
            my_new_graph.append([my_new_name, my_dst, my_src])

    s += 'digraph ' + mfdo.module_name + ' {\n'
    s += s.indent() + 'bgcolor=white\n'
#         s += 'splines=compound;\n'
#         s += 'splines=true\n'
    s += 'rankdir=LR;\n'
    if errs:
        s += 'node [shape=ellipse, style=filled, color=orange]; ERR_SRC ERR_DST;\n'
    s += 'node [shape=doublecircle, style=filled, color=lightgray]; IN OUT;\n'
    s += 'node [shape=ellipse]; IN OUT;\n'

    for i in my_new_graph:
        s += i[1] + ' -> ' + i[2] + ' [ label = "' + i[0] + '" ];\n'
    s += '}\n'

#         s += 'a1 -> b3 [dir=both color="red:blue"];\n'
#         s += 'b2 -> a3 [dir=none color="green:red;0.25:blue"];\n'

    s.write(filename, overwrite = mfdo.overwrite)
