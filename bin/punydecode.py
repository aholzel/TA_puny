import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))

from splunklib.searchcommands import dispatch, StreamingCommand, Configuration, Option, validators
import idna

__version__ = "1.0.2"

@Configuration()
class PunyDecode(StreamingCommand):
    """ 
    The PunyDecode command encodes urls that contain none ASCII characters

    """
    def stream(self, events):
        debug = False 
        
        if len(sys.argv) < 2:
            print('No field found to decode')
        else:
            arguments = sys.argv[2:]
        
            for event in events:
                for arg in arguments:
                    if arg.startswith('__'):
                        continue

                    try:
                        if type(event[arg]) is list:
                            
                            punydecode = []

                            for item in event[arg]:
                                enc = idna.decode(item)
                                punydecode.append(enc)
                        else:
                            punydecode = idna.decode(event[arg])
                    except:
                        try:
                            punydecode = str.encode(event[arg]).decode('idna')
                            error = "The field contains a invalid domain."
                        except Exception as e:
                            punydecode = event[arg]
                            error = e

                    field_name = arg + "_decoded"
                    event[field_name] = punydecode

                    if debug and error:
                        error_field = arg + "_error"
                        event[error_field] = error

                yield event

dispatch(PunyDecode, sys.argv, sys.stdin, sys.stdout, __name__)