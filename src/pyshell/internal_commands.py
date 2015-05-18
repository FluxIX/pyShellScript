from .internal_command import InternalCommand

class ChangeDirectoryCommand( InternalCommand ):
    def __init__( self, path, *options, **kwargs ):
        self.path = path
        InternalCommand.__init__( self, "cd", [ path ], *options, **kwargs )

    def get_path( self ):
        return self._path

    def set_path( self, value ):
        self._path = value

    path = property( get_path, set_path, None, None )

    def _do( self ):
        import os
        os.chdir( self.path )
