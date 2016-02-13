
# Foreground color sequences:
# GREY   = '\033[90m'
# RED    = '\033[91m'
# GREEN  = '\033[92m'
# YELLOW = '\033[93m'
# BLUE   = '\033[94m'
# PINK   = '\033[95m'
# CIAN   = '\033[96m'
# WHITE  = '\033[97m'
# BLACK  = '\033[98m'

# Background color sequences:
# GREY   = '\033[100m'
# RED    = '\033[101m'
# GREEN  = '\033[102m'
# YELLOW = '\033[103m'
# BLUE   = '\033[104m'
# PINK   = '\033[105m'
# CIAN   = '\033[106m'
# WHITE  = '\033[107m'

# Text attributes
# BOLD       = '\033[1m'
ENDC       = '\033[0m'
UNDERSCORE = '\033[4m'
BLINK      = '\033[5m'
REVERSE    = '\033[7m'

HEADER  = '\033[93m'
OKBLUE  = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[95m'
ERROR   = '\033[91m'


def info( msg ):
    print '[' + OKGREEN + 'INFO' + ENDC + '] ' + msg

def infob( msg ):
    print '[' + OKBLUE  + 'INFO' + ENDC + '] ' + msg

def warn( msg ):
    print '[' + WARNING + 'WARN' + ENDC + '] ' + msg

def err( msg ):
    print '[' + ERROR   + 'ERRR' + ENDC + '] ' + msg

def head( msg ):
    print len(msg)*'-'
    print OKBLUE + msg + ENDC
    print len(msg)*'-'
