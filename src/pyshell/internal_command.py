from shell_commands.command import Command

class InternalCommand( Command ):
    def __init__( self, moniker, parameters = None, *options, **kwargs ):
        Command.__init__( self, moniker, parameters, *options, **kwargs )
