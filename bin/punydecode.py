#!/usr/bin/env python

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))

from splunklib.searchcommands import dispatch, StreamingCommand, Configuration, Option, validators
import idna

@Configuration()
class PunyDecode(StreamingCommand):
    """ 
    The PunyDecode command encodes urls that contain none ASCII characters

    """
    def stream(self, events):
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
                        punydecode = event[arg]

                    field_name = arg + "_decoded"
                    event[field_name] = punydecode

                yield event

dispatch(PunyDecode, sys.argv, sys.stdin, sys.stdout, __name__)