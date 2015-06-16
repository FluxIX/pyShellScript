from pyshell.tee_output_file import TeeOutputFileBuilder
from .environment import EnvironmentBuilder

class CommandExecuter( object ):
    class OptionalArguments( object ):
        DryRun = "dry_run"

    def __init__( self, environment = None, **kwargs ):
        if environment is None:
            import sys
            standard_output = TeeOutputFileBuilder().add_stream( sys.__stdout__ ).build()
            error_output = TeeOutputFileBuilder().add_stream( sys.__stderr__ ).build()

            environment = EnvironmentBuilder().set_standard_output( standard_output ).set_error_output( error_output ).build()

        if self.OptionalArguments.DryRun in kwargs:
            self.dry_run = kwargs[ self.OptionalArguments.DryRun ]
        else:
            self.dry_run = False

        self.environment_stack = [ environment ]
        self.history = []

        self.current_environment._attach()

    def _get_dry_run( self ):
        return self.__dry_run

    def _set_dry_run( self, value ):
        self.__dry_run = bool( value )

    dry_run = property( _get_dry_run, _set_dry_run, None, None )

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
        if self.dry_run:
            print( "Executing command: %s" % str( command ) )
            result = True
        else:
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
