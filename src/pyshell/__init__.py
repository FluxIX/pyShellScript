import sys

from .command import Command
from .command_executer import CommandExecuter
from .environment import Environment, EnvironmentBuilder
from .exceptions import *
from .internal_commands import *

# See https://docs.python.org/2/library/sys.html#sys.platform for idiom.
if sys.platform.startswith( "freebsd" ) or sys.platform.startswith( "linux" ) or sys.platform.startswith( "darwin" ):
    from .linux.commands import *
elif sys.platform.startswith( "win32" ) or sys.platform.startswith( "cygwin" ):
    raise NotImplementedError( "Windows is not supported at this time." )
else:
    raise NotSupportedPlatformException( "Platform is not supported." )
