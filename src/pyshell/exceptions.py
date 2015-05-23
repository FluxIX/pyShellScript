class ExecutionException( Exception ):
    def __init__( self, message ):
        self.message = message

        Exception.__init__()

        def __str__( self, *args, **kwargs ):
            return repr( self.message )

    def get_message( self ):
        return self.__message

    def set_message( self, value ):
        self.__message = value

    message = property( get_message, set_message, None, None )

class ExecutionValueException( ExecutionException ):
    def __init__( self, message ):
        ExecutionException.__init__( self, message )

class NotSupportPlatformException( Exception ):
    def __init__( self, message ):
        self.message = message

        Exception.__init__()

        def __str__( self, *args, **kwargs ):
            return repr( self.message )

    def get_message( self ):
        return self.__message

    def set_message( self, value ):
        self.__message = value

    message = property( get_message, set_message, None, None )
