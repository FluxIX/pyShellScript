class Environment( object ):
    class CloneOptions( object ):
        InheritVariables = "inherit"
        MakeParentLink = "parent_link"

    def __init__( self, starting_directory = None, parent = None, starting_variables = None ):
        if starting_directory is None:
            import os
            starting_directory = os.curdir

        self.directory_stack = []
        self.push_directory( starting_directory )

        self.parent = parent

        if starting_variables is None:
            starting_variables = {}

        self.variables = starting_variables

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
            inherit_vars = kwargs[ key ]
        else:
            inherit_vars = False

        key = Environment.CloneOptions.MakeParentLink
        if key in kwargs:
            parent_link = kwargs[ key ]
        else:
            parent_link = False

        if parent_link:
            parent = self
        else:
            parent = None

        variables = {}
        if inherit_vars:
            for key in self.variables.keys():
                variables[ key ] = self.variables[ key ]

        result = Environment( self.current_directory, parent, variables )

        return result

class EnvironmentBuilder( object ):
    def __init__( self ):
        self.starting_directory = None
        self.parent = None
        self.starting_variables = None

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

    def build( self ):
        return Environment( self.starting_directory, self.parent, self.starting_variables )
