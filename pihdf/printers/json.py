import simplejson
from str_builder import StrBuilder
import pihdf


def print_design(mfdo, s):
    s += '{\n'
    s += s.indent() + '"design":\n'
    s += '{\n'
    s += s.indent() + '"name": "' + mfdo.module_name + '",\n'
    s += '"interfaces":\n'
    s += '[\n'
    s.indent()
    if mfdo.Reset != None:
        s += simplejson.dumps(mfdo.Reset) + ',\n'

    if mfdo.Clock != None:
        s += simplejson.dumps(mfdo.Clock) + ',\n'

    for i in mfdo.interfaces:
        s += simplejson.dumps(i) + ',\n'

    s = s-2 + (s.noIndent() + '\n')
    s += s.dedent() + ']\n'

    if mfdo.parameters != []:
        s = s-1 + (s.noIndent() + ',\n') # insert a comma
        s += '"parameters":\n'
        s += '[\n'
        s.indent()

        for p in mfdo.parameters:
            s += simplejson.dumps(p) + ',\n'

        s = s-2 + (s.noIndent() + '\n')
        s += s.dedent() + ']\n'

    s += s.dedent() + '}\n'
    
def print_structure(mfdo, s):
    s = s-1 + (s.noIndent() + ',\n') # insert a comma
    s += '"structure":\n'
    s += '{\n'
    s.indent()

    if mfdo.local_interfaces != []:
        s += '"local_interfaces":\n'
        s += '[\n'
        s.indent()
        for i in mfdo.local_interfaces:
            s += simplejson.dumps(i) + ',\n'

        s = s-2 + (s.noIndent() + '\n')
        s += s.dedent() + '],\n'

    if mfdo.modules != []:
        s += '"design_modules":\n'
        s += '[\n'
        s.indent()
        for i in mfdo.modules:
            s += '{\n'
            s.indent()
            s += '"name": "' + i["name"] + '", "type": "' + i["type"] + '",\n'
            s += '"path": "' + i["path"] + '",\n'

            s += '"connections":\n'
            s += '[\n'
            s.indent()
                            
            for j in i["connections"]:
                sd = '"direction": "' + j["direction"] + '", ' if "direction" in j else ''
                sn = '"local_name": "' + j["local_name"] + '", '
                sc = '"connect_to": "' + j["connect_to"] + '"'

                s += '{' + sd + sn + sc + '},\n'

            s = s-2 + '\n'
            s += s.dedent() + '],\n'

        s = s-2 + (s.noIndent() + '\n')
        s += s.dedent() + '}\n'

    s += s.dedent() + ']\n'
    s += s.dedent() + '}\n'


def print_json_file(mfdo):
    '''|
    | Create/Update a .json file containing the description of a module (interfaces as well as topology if present)
    |________'''
    s = StrBuilder()
    filename =  mfdo.c_path + '/' + mfdo.module_name + '.json'

    print_design(mfdo, s)

    try:
        with open(filename) as f:
            # The .json file exist, we use the existing 'structure' section (DO NOT UPDATE)
            gdf = pihdf.MFDesign()
            gdf.initialize( filename )
            if gdf.modules != []:
                print_structure(gdf, s)

    except IOError as e:
        if mfdo.modules != []:
            print_structure(mfdo, s)

    s += s.dedent() + '}\n'
    
    s.write(filename, overwrite = mfdo.overwrite)