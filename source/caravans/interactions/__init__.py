from source.header_common import s9
from source.header_dialogs import *
from source.module_constants import *
from source.header_operations import *
from source.lazy_flag import LazyFlag
import attack
import attack_quest
import demand_toll
import journey_explanation
import escort_quest
import caravaninter
#import trade
# import initialize_trade_routes
# import caravansubmodnodia #import menus #, simple_triggers, scripts, triggers, party_templates
# import caravandial 
# from source.statement import StatementBlock
# from source.header_operations import *
# #from source.header_common import s2, s3
# from source.module_constants import *
#from source.header_operations import *
dialogs = caravaninter.dialogs \
          + escort_quest.dialogs \
          + demand_toll.dialogs \
          + attack.dialogs \
          + journey_explanation.dialogs \


triggers = escort_quest.triggers
scripts = []



simple_triggers = [
    # avoids the caravan master to be an infinite source of money
    # by only making him receive money every 3 hours.
    # todo: make this a consequence of its profit.
    (3, [(assign, "$g_caravan_master_gold_refilled", 0),
        (try_begin),
                  (ge, "$cheat_mode", 1),
                  (display_message, "@{!}DEBUG: g_caravan_master_gold_refilled"),
        (try_end),])
]


simple_triggers += escort_quest.simple_triggers