class Command( object ):
    def __init__( self, moniker, parameters, *options, **kwargs ):
        self.moniker = moniker

        if parameters is not None:
            self.parameters = parameters[:]
        else:
            self.parameters = []

        if options is not None and len( options ) > 0:
            self._options = options
        else:
            self._options = []

    def get_moniker( self ):
        return self._moniker

    def set_moniker( self, value ):
        self._moniker = value

    def get_parameters( self ):
        return self._parameters

    def set_parameters( self, value ):
        self._parameters = value

    def get_options( self ):
        return self._options

    def set_options( self, value ):
        self._options = value

    moniker = property( get_moniker, set_moniker, None, None )
    parameters = property( get_parameters, set_parameters, None, None )
    options = property( get_options, set_options, None, None )

    @property
    def terms( self ):
        result = [ self.moniker ]
        result.extend( self.options )
        result.extend( self.parameters )
        return result

    def __str__( self, *args, **kwargs ):
        return " ".join( self.terms )

    def execute( self ):
        raise NotImplementedError( "Must be implemented in a child class." )
