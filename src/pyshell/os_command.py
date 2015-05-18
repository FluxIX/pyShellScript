from .command import Command

class OperatingSystemCommand( Command ):
    def __init__( self, moniker, parameters, *options, **kwargs ):
        Command.__init__( self, moniker, parameters, *options, **kwargs )

    def _do( self ):
        import subprocess
        subprocess.check_call( self.terms )
