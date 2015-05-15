class CommandExecuter( object ):
    def __init__( self ):
        pass

    def execute_commands( self, commands ):
        import subprocess

        for command in commands:
            subprocess.check_call( command.terms )
#            print( "Executing command: " + str( command ) )
