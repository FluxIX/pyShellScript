class CommandExecuter( object ):
    def __init__( self ):
        pass

    def execute_commands( self, commands ):
        for command in commands:
            print( "Executing command: " + str( command ) )
#             command.execute()
