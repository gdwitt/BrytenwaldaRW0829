from . import interactions
import trade
import initialize_trade_routes
import caravansubmodnodia #import menus #, simple_triggers, scripts, triggers, party_templates
import caravandial 
from source.statement import StatementBlock
from source.header_operations import *
#from source.header_common import s2, s3
from source.module_constants import *
from source.header_operations import *

# from source.header_troops import *
# from source.header_skills import *
# #from source.header_parties import *
# from source.lazy_flag import LazyFlag
# from source.statement import StatementBlock
# from source.module_quests import *
# #from source.module_scripts import *
# from source.header_common import *

# from source.header_parties import ai_bhvr_travel_to_party, pf_default_behavior


dialogs = interactions.dialogs + caravandial.dialogs
simple_triggers = trade.simple_triggers + interactions.simple_triggers + caravansubmodnodia.simple_triggers
scripts = trade.scripts + interactions.scripts + initialize_trade_routes.scripts  + caravansubmodnodia.scripts 
triggers = interactions.triggers+ caravansubmodnodia.triggers
#party_templates = caravansubmodnodia.party_templates
menus = caravansubmodnodia.menus
# 

