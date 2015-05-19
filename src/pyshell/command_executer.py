from .environment import EnvironmentBuilder

class CommandExecuter( object ):
    def __init__( self, environment = None ):
        if environment is None:
            environment = EnvironmentBuilder().build()

        self.environment_stack = [ environment ]

    def _get_environment_stack( self ):
        return self.__environment_stack

    def _set_environment_stack( self, value ):
        if value is not None:
            self.__environment_stack = value
        else:
            raise ValueError( "Environment stack cannot be None" )

    environment_stack = property( _get_environment_stack, _set_environment_stack, None, None )

    def create_child_environment( self, **kwargs ):
        child = self.current_environment.clone( **kwargs )
        self.environment_stack.append( child )

    def pop_environment( self ):
        result = self.environment_stack.pop
        return result

    @property
    def current_environment( self ):
        return self.environment_stack[ -1 ]

    def execute_command( self, command ):
#        print( "Executing command: " + str( command ) )
        return command.execute( self )

    def execute_commands( self, commands, stopOnError = True ):
        result = True

        for command in commands:
            execution_result = self.execute_command( command )

            result = result and execution_result

            if not execution_result and stopOnError:
                break

        return result
