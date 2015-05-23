from .exceptions import ExecutionException

class Command( object ):
    class States( object ):
        Initialized = 0
        Executing = 1
        SuccessfulExecution = 2
        FailedExecution = 3

    def __init__( self, moniker, parameters, *options, **kwargs ):
        self.moniker = moniker

        if parameters is not None:
            self.parameters = parameters[:]
        else:
            self.parameters = []

        if options is not None and len( options ) > 0:
            self.options = options
        else:
            self.options = []

        self.state = Command.States.Initialized

    def get_state( self ):
        return self.__state

    def set_state( self, value ):
        self.__state = value

    def _get_command_executer( self ):
        return self.__command_executer

    def _set_command_executer( self, value ):
        self.__command_executer = value

    def get_environment( self ):
        return self.__environment

    def set_environment( self, value ):
        self.__environment = value

    def get_moniker( self ):
        return self.__moniker

    def set_moniker( self, value ):
        self.__moniker = value

    def get_parameters( self ):
        return self.__parameters

    def set_parameters( self, value ):
        self.__parameters = value

    def get_options( self ):
        return self.__options

    def set_options( self, value ):
        self.__options = value

    moniker = property( get_moniker, set_moniker, None, None )
    parameters = property( get_parameters, set_parameters, None, None )
    options = property( get_options, set_options, None, None )
    _command_executer = property( _get_command_executer, _set_command_executer, None, None )
    environment = property( get_environment, set_environment, None, None )
    state = property( get_state, set_state, None, None )

    @property
    def terms( self ):
        result = [ self.moniker ]
        result.extend( self.options )
        result.extend( self.parameters )
        return result

    def __str__( self, *args, **kwargs ):
        return " ".join( self.terms )

    def execute( self, command_executer ):
        if self.state is Command.States.Initialized:
            self.state = Command.States.Executing

            self._command_executer = command_executer
            self.environment = self._command_executer.current_environment

            execution_result = self._do()
            if execution_result is None or execution_result:
                result = True
                state = Command.States.SuccessfulExecution
            else:
                result = False
                state = Command.States.FailedExecution

            self.state = state

            return result
        else:
            raise ExecutionException( "Unable to execute: command is in an incorrect state." )

    def _do( self ):
        raise NotImplementedError( "Must be implemented in a child class." )

    def _get_value( self, dictionary, key, default_value = None, typecast_funct = None ):
        if key in dictionary:
            value = dictionary[ key ]
            result = value
        else:
            result = default_value

        if result is not None and typecast_funct is not None:
            result = typecast_funct( result )

        return result

