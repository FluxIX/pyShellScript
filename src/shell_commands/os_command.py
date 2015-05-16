from shell_commands.command import Command

class OperatingSystemCommand( Command ):
    def __init__( self, moniker, parameters, *options, **kwargs ):
        Command.__init__( self, moniker, parameters, *options, **kwargs )

    def execute( self ):
        import subprocess
        subprocess.check_call( self.terms )
