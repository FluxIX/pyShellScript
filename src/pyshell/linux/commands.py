from ..os_command import OperatingSystemCommand

class LinuxCommand( OperatingSystemCommand ):
    def __init__( self, moniker, parameters, *options, **kwargs ):
        OperatingSystemCommand.__init__( self, moniker, parameters, *options, **kwargs )

class SudoCommand( LinuxCommand ):
    def __init__( self, command, *options, **kwargs ):
        self.command = command
        LinuxCommand.__init__( self, "sudo", command.terms, *options, **kwargs )

    def get_command( self ):
        return self._command

    def _set_command( self, value ):
        self._command = value

    command = property( get_command, _set_command, None, None )

class ServiceCommand( LinuxCommand ):
    class Operations( object ):
        Start = "start"
        Stop = "stop"
        Restart = "restart"

    def __init__( self, service_name, operation, *options, **kwargs ):
        LinuxCommand.__init__( self, "service", [ service_name, operation ], *options, **kwargs )

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

        target_value = self._get_value( kwargs, MakeCommand.OptionalParameters.Target, None )
        if target_value is not None:
            parameters.append( target_value )

        LinuxCommand.__init__( self, "make", parameters, *options, **kwargs )

    def get_directory( self ):
        return self._directory

    def _set_directory( self, value ):
        self._directory = value

    directory = property( get_directory, _set_directory, None, None )

class ListDirectoryCommand( LinuxCommand ):
    class OptionalParameters( object ):
        Directory = "directory"

    def __init__( self, *options, **kwargs ):
        parameters = []

        directory = self._get_value( kwargs, ListDirectoryCommand.OptionalParameters.Directory )
        if directory is not None:
            parameters.append( directory )

        LinuxCommand.__init__( self, "ls", parameters, *options, **kwargs )

    def get_directory( self ):
        return self._directory

    def _set_directory( self, value ):
        self._directory = value

    directory = property( get_directory, _set_directory, None, None )

