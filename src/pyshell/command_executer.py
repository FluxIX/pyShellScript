from .environment import EnvironmentBuilder

class CommandExecuter( object ):
    def __init__( self, environment = None ):
        if environment is None:
            environment = EnvironmentBuilder().build()

        self.environment_stack = [ environment ]
        self.history = []

        self.current_environment._attach()

    def _get_environment_stack( self ):
        return self.__environment_stack

    def _set_environment_stack( self, value ):
        if value is not None:
            self.__environment_stack = value
        else:
            raise ValueError( "Environment stack cannot be None." )

    environment_stack = property( _get_environment_stack, _set_environment_stack, None, None )

    @property
    def current_environment( self ):
        return self.environment_stack[ -1 ]

    def get_history( self ):
        return self.__history

    def _set_history( self, value ):
        if value is not None:
            self.__history = value
        else:
            raise ValueError( "History cannot be None." )

    history = property( get_history, _set_history, None, None )

    def execute_command( self, command ):
#        print( "Executing command: %s" % str( command ) )
        result = command.execute( self )

        if result:
            self.history.append( command )

        return result

    def execute_commands( self, commands, stopOnError = True ):
        result = True

        for command in commands:
            execution_result = self.execute_command( command )

            result = result and execution_result

            if not execution_result and stopOnError:
                break

        return result
