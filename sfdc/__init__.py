from sfdc import client

# Adds the modules listed in sfdc.sobjects.__init__.__all__ to the sfdc.sobjects namespace
# This way I can simply import sfdc.sobjects and have all the modules organized there
# instead of doing from sfdc.sobjects import * which adds all the modules to the current module namespace
from sfdc.sobjects import *


SFDC = client.get_client_from_config()
