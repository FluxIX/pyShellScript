class TeeOutputFile( object ):
    def __init__( self, autoclose_streams = False ):
        self.__closed = False
        self.streams = []
        self.autoclose_streams = autoclose_streams

    def get_autoclose_streams( self ):
        return self.__autoclose_streams

    def set_autoclose_streams( self, value ):
        self.__autoclose_streams = value

    autoclose_streams = property( get_autoclose_streams, set_autoclose_streams, None, None )

    def __del__( self ):
        if self.autoclose_streams:
            self.close()

    def _get_errors( self ):
        return self.__unicode_error_handler

    def _set_errors( self, value ):
        self.__unicode_error_handler = value

    errors = property( _get_errors, _set_errors, None, None )

    def _get_softspace( self ):
        return self.__softspace

    def _set_softspace( self, value ):
        self.__softspace = value

    softspace = property( _get_softspace, _set_softspace, None, None )

    @property
    def closed( self ):
        return self.__closed

    def close( self ):
        if not self.closed:
            for stream in self.streams:
                if not stream.closed:
                    stream.close()

            self.__closed = True

        return self.closed

    def next( self ):
        raise NotImplementedError( "Only output functionality is provided." )

    def read( self, size = -1 ):
        raise NotImplementedError( "Only output functionality is provided." )

    def readline( self, size = -1 ):
        raise NotImplementedError( "Only output functionality is provided." )

    def readlines( self, sizehint = None ):
        raise NotImplementedError( "Only output functionality is provided." )

    def xreadlines( self ):
        raise NotImplementedError( "Only output functionality is provided." )

    def seek( self, offset, whence = None ):
        raise NotImplementedError( "Only output functionality is provided." )

    def tell( self ):
        raise NotImplementedError( "Only output functionality is provided." )

    def truncate( self, size = None ):
        raise NotImplementedError( "Only output functionality is provided." )

    def flush( self ):
        if not self.closed:
            for stream in self.streams:
                stream.flush()

    def write( self, message, autoflush = False ):
        if self.closed:
            raise ValueError( "Attempting to write to a closed file." )
        else:
            output_message = str( message )

            for stream in self.streams:
                stream.write( output_message )

                if autoflush:
                    stream.flush()

    def writelines( self, messages, autoflush = False ):
        if self.closed:
            raise ValueError( "Attempting to write to a closed file." )
        else:
            output_messages = [ str( message ) for message in messages ]

            for stream in self.streams:
                stream.writelines( output_messages )

                if autoflush:
                    stream.flush()

    def _get_streams( self ):
        return self.__streams

    def _set_streams( self, value ):
        self.__streams = value

    streams = property( _get_streams, _set_streams, None, None )

    def add_stream( self, stream, allow_duplicates = True ):
        if stream is None:
            raise ValueError( "Streams cannot be None." )
        else:
            result = allow_duplicates or stream not in self.streams

            if result:
                self.streams.append( stream )

            return result

    def remove_stream( self, stream, remove_all_instances = False ):
        if stream is None:
            raise ValueError( "Streams cannot be None." )
        else:
            result = []

            index = 0
            for s in self.streams:
                if s is stream:
                    result.append( s )
                    self.streams.pop( index )

                    if not remove_all_instances:
                        break
                else:
                    index += 1

            return result

class TeeOutputFileBuilder( object ):
    def __init__( self ):
        self.autoclose_streams = False
        self.streams = []

    def get_autoclose_streams( self ):
        return self.__autoclose_streams

    def set_autoclose_streams( self, value = True ):
        self.__autoclose_streams = value
        return self

    autoclose_streams = property( get_autoclose_streams, set_autoclose_streams, None, None )

    def get_streams( self ):
        return self.__streams

    def set_streams( self, value ):
        self.__streams = value
        return self

    streams = property( get_streams, set_streams, None, None )

    def add_stream( self, stream, allow_duplicates = True ):
        self.streams.append( ( stream, allow_duplicates ) )
        return self

    def build( self ):
        result = TeeOutputFile( self.autoclose_streams )

        for stream, allow_duplicates in self.streams:
            result.add_stream( stream, allow_duplicates )

        return result
