class Command( object ):
    def __init__( self, executable_name, parameters = None, *options ):
        self.executable_name = executable_name

        if parameters is not None:
            self.parameters = parameters
        else:
            self.parameters = []

        if options is not None and len( options ) > 0:
            self._options = options
        else:
            self._options = []

    def get_executable_name( self ):
        return self._executable_name

    def set_executable_name( self, value ):
        self._executable_name = value

    def get_parameters( self ):
        return self._parameters

    def set_parameters( self, value ):
        self._parameters = value

    def get_options( self ):
        return self._options

    def set_options( self, value ):
        self._options = value

    executable_name = property( get_executable_name, set_executable_name, None, None )
    parameters = property( get_parameters, set_parameters, None, None )
    options = property( get_options, set_options, None, None )

    @property
    def terms( self ):
        result = [ self.executable_name ]
        result.extend( self.options )
        result.extend( self.parameters )
        return result

    def __str__( self, *args, **kwargs ):
        return " ".join( self.terms )
