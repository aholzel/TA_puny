#!/usr/bin/env python

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))

from splunklib.searchcommands import dispatch, StreamingCommand, Configuration, Option, validators
import idna

@Configuration()
class PunyEncode(StreamingCommand):
    """ 
    The PunyEncode command encodes urls that contain none ASCII characters

    """
    def stream(self, events):
        if len(sys.argv) < 2:
            print('No field found to encode')
        else:
            arguments = sys.argv[2:]
        
            for event in events:
                for arg in arguments:
                    if arg.startswith('__'):
                        continue

                    try:
                        if type(event[arg]) is list:
                            
                            punyencode = []

                            for item in event[arg]:
                                dec = idna.encode(item, uts46=True).decode()
                                punyencode.append(dec)
                        else:
                            punyencode = idna.encode(event[arg], uts46=True).decode()
                    except:
                        punyencode = event[arg]

                    field_name = arg + "_encoded"
                    event[field_name] = punyencode

                yield event

dispatch(PunyEncode, sys.argv, sys.stdin, sys.stdout, __name__)