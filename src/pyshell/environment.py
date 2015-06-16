from .tee_output_file import TeeOutputFile

class Environment( object ):
    class CloneOptions( object ):
        InheritVariables = "inherit_vars"
        InheritStreams = "inherit_streams"
        MakeParentLink = "parent_link"

    def __init__( self, starting_directory = None, parent = None, starting_variables = None, standard_output = None, error_output = None ):
        if starting_directory is None:
            import os
            starting_directory = os.curdir

        self.directory_stack = []
        self.push_directory( starting_directory )

        self.parent = parent

        if starting_variables is None:
            starting_variables = {}

        self.variables = starting_variables

        if standard_output is None:
            standard_output = TeeOutputFile()
        self.__standard_output = standard_output

        if error_output is None:
            error_output = TeeOutputFile()
        self.__error_output = error_output

        self._attached = False

    def __del__( self ):
        if self._detach():
            def is_internal_stream( stream ):
                import sys
                return stream is sys.__stdout__ or stream is sys.__stderr__ or stream is sys.__stdin__

            if not is_internal_stream( self.standard_output ):
                del self.__standard_output

            if not is_internal_stream( self.error_output ):
                del self.__error_output

    def get_directory_stack( self ):
        return self.__directory_stack

    def _set_directory_stack( self, value ):
        if value is not None:
            self.__directory_stack = value
        else:
            raise ValueError( "Directory stack cannot be None." )

    directory_stack = property( get_directory_stack, _set_directory_stack, None, None )

    def push_directory( self, directory, suppress_errors = False ):
        if directory is not None:
            import os

            if not os.path.isabs( directory ):
                d = os.path.abspath( directory )
            else:
                d = directory

            d = os.path.normpath( d )

            if os.path.isdir( d ):
                self.directory_stack.append( d )
                result = True
            elif not suppress_errors:
                raise ValueError( "Only directories can be pushed." )
            else:
                result = False

        elif not suppress_errors:
            raise ValueError( "Pushed directory cannot be None." )
        else:
            result = False

        return result

    def pop_directory( self ):
        return self.directory_stack.pop()

    @property
    def current_directory( self ):
        return self.directory_stack[ -1 ]

    def get_parent( self ):
        return self.__parent

    def _set_parent( self, value ):
        self.__parent = value

    parent = property( get_parent, _set_parent, None, None )

    @property
    def has_parent( self ):
        return self.parent is not None

    def get_variables( self ):
        return self.__variables

    def set_variables( self, value ):
        self.__variables = value

    variables = property( get_variables, set_variables, None, None )

    def clone( self, **kwargs ):
        key = Environment.CloneOptions.InheritVariables
        if key in kwargs:
            inherit_vars = bool( kwargs[ key ] )
        else:
            inherit_vars = False

        key = Environment.CloneOptions.MakeParentLink
        if key in kwargs:
            parent_link = bool( kwargs[ key ] )
        else:
            parent_link = False

        if parent_link:
            parent = self
        else:
            parent = None

        variables = {}
        if inherit_vars:
            for key in self.variables:
                variables[ key ] = self.variables[ key ]

        key = Environment.CloneOptions.InheritStreams
        if key in kwargs:
            inherit_streams = bool( kwargs[ key ] )
        else:
            inherit_streams = False

        if inherit_streams:
            standard_output = self.standard_output.clone()
            error_output = self.error_output.clone()
        else:
            standard_output = None
            error_output = None

        result = Environment( self.current_directory, parent, variables, standard_output, error_output )

        return result

    @property
    def standard_output( self ):
        return self.__standard_output

    @property
    def error_output( self ):
        return self.__error_output

    def _attach( self ):
        result = not self._attached

        if result:
            import os
            import sys
            self._previous_working_directory = os.getcwd()
            self._previous_standard_output = sys.stdout
            self._previous_error_output = sys.stderr
            self._previous_environment_variables = os.environ

            os.chdir( self.current_directory )
            sys.stdout = self.standard_output
            sys.stderr = self.error_output
            os.environ = self.variables

            self._attached = True

        return result

    def _detach( self ):
        result = self._attached

        if result:
            import os
            import sys
            os.chdir( self._previous_working_directory )
            sys.stdout = self._previous_standard_output
            sys.stderr = self._previous_error_output
            os.environ = self._previous_environment_variables

            self._attached = False

        return result

class EnvironmentBuilder( object ):
    def __init__( self ):
        self.starting_directory = None
        self.parent = None
        self.starting_variables = None
        self.standard_output = None
        self.error_output = None

    def get_starting_directory( self ):
        return self.__starting_directory

    def set_starting_directory( self, value ):
        self.__starting_directory = value
        return self

    starting_directory = property( get_starting_directory, set_starting_directory, None, None )

    def get_parent( self ):
        return self.__parent

    def set_parent( self, value ):
        self.__parent = value
        return self

    parent = property( get_parent, set_parent, None, None )

    def get_starting_variables( self ):
        return self.__starting_variables

    def set_starting_variables( self, value ):
        self.__starting_variables = value
        return self

    starting_variables = property( get_starting_variables, set_starting_variables, None, None )

    def get_standard_output( self ):
        return self.__standard_output

    def set_standard_output( self, value ):
        self.__standard_output = value
        return self

    standard_output = property( get_standard_output, set_standard_output, None, None )

    def get_error_output( self ):
        return self.__error_output

    def set_error_output( self, value ):
        self.__error_output = value
        return self

    error_output = property( get_error_output, set_error_output, None, None )

    def inherit_starting_variables( self ):
        starting_variables = {}

        import os
        for key in os.environ:
            starting_variables[ key ] = os.environ[ key ]

        self.starting_variables = starting_variables

        return self

    def build( self ):
        return Environment( self.starting_directory, self.parent, self.starting_variables, self.standard_output, self.error_output )
