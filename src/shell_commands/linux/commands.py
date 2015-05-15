from ..command import Command

class LinuxCommand( Command ):
    def __init__( self, executable_name, parameters = None, *options ):
        Command.__init__( self, executable_name, parameters, *options )

class SudoCommand( LinuxCommand ):
    def __init__( self, command, *options ):
        self.command = command
        LinuxCommand.__init__( self, "sudo", command.terms, *options )

    def get_command( self ):
        return self._command

    def set_command( self, value ):
        self._command = value

    command = property( get_command, set_command, None, None )

class ChangeDirectoryCommand( LinuxCommand ):
    def __init__( self, path, *options ):
        self.path = path
        LinuxCommand.__init__( self, "cd", [ path ], *options )

    def get_path( self ):
        return self._path

    def set_path( self, value ):
        self._path = value

    path = property( get_path, set_path, None, None )

class ServiceCommand( LinuxCommand ):
    class Operations( object ):
        Start = "start"
        Stop = "stop"
        Restart = "restart"

    def __init__( self, service_name, operation, *options ):
        LinuxCommand.__init__( self, "service", [ service_name, operation ], *options )

    def get_service_name( self ):
        return self._service_name

    def set_service_name( self, value ):
        self._service_name = value

    def get_operation( self ):
        return self._operation

    def set_operation( self, value ):
        self._operation = value

    service_name = property( get_service_name, set_service_name, None, None )
    operation = property( get_operation, set_operation, None, None )

class MakeCommand( LinuxCommand ):
    class OptionalParameters( object ):
        Target = "target"

    def __init__( self, *options, **kwargs ):
        parameters = []

        key = MakeCommand.OptionalParameters.Target
        if key in kwargs:
            value = kwargs[ key ]
            if value is not None:
                parameters.append( value )

        LinuxCommand.__init__( self, "make", parameters, *options )

    def get_target( self ):
        return self._target

    def set_target( self, value ):
        self._target = value

    target = property( get_target, set_target, None, None )
