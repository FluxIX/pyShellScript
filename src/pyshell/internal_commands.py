import os

from pyshell.exceptions import ExecutionValueException
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
        os.chdir( self.path )

class PushDirectoryCommand( InternalCommand ):
    def __init__( self, directory = None, *options, **kwargs ):
        if directory is None:
            directory = os.getcwd()
        elif( not os.path.isdir( directory ) ):
            raise ValueError( str( directory ) + " is not a directory." )

        self.directory = directory

        InternalCommand.__init__( self, "pushd", [ directory ], *options, **kwargs )

    def get_directory( self ):
        return self.__directory

    def _set_directory( self, value ):
        self.__directory = value

    directory = property( get_directory, _set_directory, None, None )

    def _do( self ):
        return self.environment.push_directory( self.directory )

class PopDirectoryCommand( InternalCommand ):
    class OptionalParameters( object ):
        ChangeDirectory = "change_directory"
        SuppressExecutionQuantityValueError = "suppress_quantity_value_error"

    def __init__( self, quantity = 1, *options, **kwargs ):
        if quantity < 0:
            raise ValueError( "Quantity must be non-negative." )
        self.quantity = quantity

        self.change_directory = self._get_value( kwargs, PopDirectoryCommand.OptionalParameters.ChangeDirectory, True, bool )
        self.suppress_quantity_value_error = self._get_value( kwargs, PopDirectoryCommand.OptionalParameters.SuppressExecutionQuantityValueError, False, bool )

        InternalCommand.__init__( self, "popd", [ self.quantity, self.change_directory, self.suppress_quantity_value_error ], *options, **kwargs )

    def get_quantity( self ):
        return self.__quantity

    def _set_quantity( self, value ):
        self.__quantity = value

    quantity = property( get_quantity, _set_quantity, None, None )

    def get_change_directory( self ):
        return self.__change_directory

    def _set_change_directory( self, value ):
        self.__change_directory = value

    change_directory = property( get_change_directory, _set_change_directory, None, None )

    def get_suppress_quantity_value_error( self ):
        return self.__suppress_quantity_value_error

    def _set_suppress_quantity_value_error( self, value ):
        self.__suppress_quantity_value_error = value

    suppress_quantity_value_error = property( get_suppress_quantity_value_error, _set_suppress_quantity_value_error, None, None )

    def _do( self ):
        if self.quantity <= len( self.environment.directory_stack ):
            if self.suppress_quantity_value_error:
                quantity = len( self.environment.directory_stack ) - 1
            else:
                raise ExecutionValueException( "Not enough directories in the stack." )
        else:
            quantity = self.quantity

        i = 0
        while i < quantity:
            last_directory = self.environment.directory_stack.pop()
            i += 1

        if quantity > 0 and self.change_directory:
            os.chdir( last_directory )

        return quantity == 0 or last_directory is not None

class PushEnvironmentCommand( InternalCommand ):
    def __init__( self, new_environment = None, *options, **kwargs ):
        self.new_environment = new_environment
        self.new_environment_args = kwargs

        InternalCommand.__init__( self, "pushenv", [ self.new_environment ], *options, **kwargs )

    def get_new_environment( self ):
        return self.__new_environment

    def _set_new_environment( self, value ):
        self.__new_environment = value

    new_environment = property( get_new_environment, _set_new_environment, None, None )

    def get_new_environment_args( self ):
        return self.__new_environment_args

    def _set_new_environment_args( self, value ):
        self.__new_environment_args = value

    new_environment_args = property( get_new_environment_args, _set_new_environment_args, None, None )

    def _do( self ):
        if self.new_environment is None:
            self.new_environment = self.environment.clone( self.new_environment_args )

        self._command_executer.environment_stack.push( self.new_environment )

class PopEnvironmentCommand( InternalCommand ):
    def __init__( self, quantity = 1, *options, **kwargs ):
        if quantity < 0:
            raise ValueError( "Quantity must be non-negative." )
        self.quantity = quantity

        InternalCommand.__init__( self, "popenv", [ self.quantity, self.change_directory, self.suppress_quantity_value_error ], *options, **kwargs )

    def get_quantity( self ):
        return self.__quantity

    def _set_quantity( self, value ):
        self.__quantity = value

    quantity = property( get_quantity, _set_quantity, None, None )

    def _do( self ):
        if self.quantity <= len( self._command_executer.environment_stack ):
            if self.suppress_quantity_value_error:
                quantity = len( self._command_executer.environment_stack ) - 1
            else:
                raise ExecutionValueException( "Not enough environments in the stack." )
        else:
            quantity = self.quantity

        i = 0
        while i < quantity:
            last_environment = self._command_executer.environment_stack.pop()
            i += 1

        return quantity == 0 or last_environment is not None

class SetVariableCommand( InternalCommand ):
    def __init__( self, name, value, *options, **kwargs ):
        self.variable_name = name
        self.variable_value = value

        InternalCommand.__init__( self, "setvar", [ self.variable_name, self.variable_value ], *options, **kwargs )

    def get_variable_name( self ):
        return self.__variable_name

    def _set_variable_name( self, value ):
        self.__variable_name = value

    def get_variable_value( self ):
        return self.__variable_value

    def _set_variable_value( self, value ):
        self.__variable_value = value

    def get_new_variable( self ):
        return self.__new_variable

    def _set_new_variable( self, value ):
        self.__new_variable = value

    variable_name = property( get_variable_name, _set_variable_name, None, None )
    variable_value = property( get_variable_value, _set_variable_value, None, None )
    new_variable = property( get_new_variable, _set_new_variable, None, None )

    def _do( self ):
        self.new_variable = self.variable_name in self.environment.variables

        self.environment.variables[ self.variable_name] = self.variable_value

class RemoveVariableCommand( InternalCommand ):
    def __init__( self, name, *options, **kwargs ):
        self.variable_name = name

        InternalCommand.__init__( self, "delvar", [ self.variable_name ], *options, **kwargs )

    def get_variable_name( self ):
        return self.__variable_name

    def _set_variable_name( self, value ):
        self.__variable_name = value

    variable_name = property( get_variable_name, _set_variable_name, None, None )

    def _do( self ):
        result = self.variable_name in self.environment.variables

        if result:
            try:
                del self.environment.variables[ self.variable_name ]
            except KeyError:
                result = False

        return result
