from source.header_operations import *
from source.header_common import * ##import s0, s1,s2, s3, s4, s5
#from caravansubmodnodia import *
from source.header_dialogs import *#anyone, plyr
from source.module_constants import trade_goods_begin, trade_goods_end
from source.header_parties import *#ai_bhvr_travel_to_party, ai_bhvr_travel_to_point, \
    #pf_default_behavior
from source.statement import StatementBlock
from source.header_items import *
from source.module_constants import *
from source.module_troops import troops
from source.module_quests import *
from source.header_troops import *
from source.lazy_flag import LazyFlag

    # the caravan being escorted (continues in `escort_quest.py`)
dialogs = [

##############caravan submod interactions
    # todo: are these ever spawn?
    
     # meet a friendly caravan
   
# ]

# _talk_dialogs = [

    # todo: quest related move to somewhere else.
    [anyone | plyr, "merchant_talk", [
         (check_quest_active, "qst_track_down_bandits"),
        ], "I am hunting a group of bandits with the following description... "
       "Have you seen them?", "merchant_bandit_information", []
    ],

    # todo: quest related move to somewhere else.
    # bandit information
    [anyone, "merchant_bandit_information", [
        (call_script, "script_get_manhunt_information_to_s15", "qst_track_down_bandits"),
        ], "{s15}", "merchant_pretalk", []
    ],

    # journey explanation
    [anyone | plyr, "merchant_talk", [
        (eq, "$talk_context", tc_party_encounter),
    ], "Tell me about your journey", "merchant_trip_explanation", []],

    # offer something
    [anyone | plyr, "merchant_talk", [
        (le, "$talk_context", tc_party_encounter),
        (eq, "$g_encountered_party_faction", "$players_kingdom"),
        (neg | check_quest_active, "qst_oim_deliver_caravan"),
        #(check_quest_active, "qst_oim_deliver_caravan"),
        #(neg | quest_slot_eq, "qst_oim_deliver_caravan", "slot_quest_target_party", "$g_encountered_party"),  
        ], "I have an offer for you.", "merchant_talk_offer", []],

    [anyone | plyr, "merchant_talk", [##gor caravan submod
        (le, "$talk_context", tc_party_encounter),
        #(eq, "$g_encountered_party_faction", "$players_kingdom")
        (neg |check_quest_active, "qst_oim_deliver_caravan"),
        #(quest_slot_eq, "qst_oim_deliver_caravan", "slot_quest_target_party", "$g_encountered_party"), 
        ], "I will protect you  Follow me.", "merchant_talk_offerprotect", []],

    # demand something
    [anyone | plyr, "merchant_talk", [
        (eq, "$talk_context", tc_party_encounter),
        #doesn'tseem towork properly(party_slot_lt, "$g_encountered_party", "slot_party_last_toll_paid_hours", "$g_current_hours"),
        (neg|party_slot_ge, "$g_encountered_party", slot_party_last_toll_paid_hours, "$g_current_hours"),
        # (party_get_slot, "$g_encountered_party_type", "$g_encountered_party", "slot_party_type"),
        # (quest_get_slot, "qst_oim_deliver_caravan", "slot_quest_target_party", "$g_encountered_party",),
       #prevent raid of a party you are guiding

        (neg |check_quest_active, "qst_oim_deliver_caravan"),
        #(neg | check_quest_concluded, "qst_oim_deliver_caravan"),
        #(neg | quest_slot_eq, "qst_oim_deliver_caravan", "slot_quest_target_party", "$g_encountered_party"),  
        #(neq,quest_slot_ge,"qst_oim_deliver_caravan","slot_quest_current_state", 0),
        #(neg|is_between, "$g_encountered_party_faction", kingdoms_begin, kingdoms_end),
        ], "I demand something from you!", "merchant_demand", []
     ],

    # if nothing, allow to leave.
    [anyone | plyr, "merchant_talk", [], "[Leave]", "close_window", [
        (assign, "$g_leave_encounter", 1)
    ]],
# ]


# _demand_dialogs = [

    # answer to demand request
    [anyone, "merchant_demand", [
        (eq, "$talk_context", tc_party_encounter),
        ], "What do you want?", "merchant_demand_2", []
     ],

    # see `attack` module
    [anyone | plyr, "merchant_demand_2", [
        (neq, "$g_encountered_party_faction", "$players_kingdom")
        ], "Hand over your gold and valuables now!", "merchant_attack_begin", []
     ],

    # see `demand_toll` module
    [anyone | plyr, "merchant_demand_2", [
        (neq, "$g_encountered_party_faction", "$players_kingdom"),
        ],
     "There is a toll for free passage here!", "merchant_demand_toll", []
     ],

    [anyone | plyr, "merchant_demand_2", [], "Nothing. Forget it.",
     "merchant_pretalk", []
     ],
# ]

# _offer_dialogs = [
    [anyone, "merchant_talk_offer", [], "What is it?",
     "merchant_talk_offer_2", []
     ],

    # offer protection
    [anyone | plyr, "merchant_talk_offer_2", [
        (eq, "$talk_context", tc_party_encounter),
        (eq, "$g_encountered_party_faction", "$players_kingdom"),
        (eq, "$caravan_escort_state", 0),
    ], "I can escort you to your destination for a price.",
       "caravan_offer_protection", []],

       [anyone, "merchant_talk_offerprotect", [(check_quest_active,"qst_oim_deliver_caravan"),(neg|check_quest_concluded, "qst_oim_deliver_caravan"),],
        "What is it caravan master?",
     "merchant_talk_offerprotect2", []
     ],

    # offer protection
    [anyone | plyr, "merchant_talk_offerprotect2", [
        # (eq, "$talk_context", tc_party_encounter),
        # (eq, "$g_encountered_party_faction", "$players_kingdom"),
       
        #(quest_set_slot, "qst_oim_deliver_caravan", "slot_quest_current_state",2),
    ], "You are following a dangerous route. I know a better way.",
       "caravan_offer_protectionfree", [(assign,"$mycaravanqst",1)]],
       
    [anyone | plyr, "merchant_talk_offerprotect2", [
    (neq,"$mycaravanqst",1),],
    "And what would you like now?", "merchant_talk",[]],
    # offer trade
    [anyone | plyr, "merchant_talk", [],
     "I'd like to trade goods with you.", "merchant_talk_offer_goods", []],

    # offer trade accepted
    [anyone, "merchant_talk_offer_goods", [],
     "Hmm. We don't normally pick up goods on the road, but...^I see that "
     "you have some goods worth buying.^Let us make an offer.",
     "merchant_pretalk", [
         (try_begin),
             (eq, "$g_caravan_master_gold_refilled", 0),
             (store_troop_gold, ":cur_gold", "trp_caravan_master"),
             (lt, ":cur_gold", 1000),
             (store_random_in_range, ":new_gold", 1000, 5000),
             (call_script, "script_troop_add_gold", "trp_caravan_master", ":new_gold"),
             (assign, "$g_caravan_master_gold_refilled", 1),
         (try_end),
         (change_screen_trade, "trp_caravan_master")]],

    [anyone | plyr, "merchant_talk_offer_2", [], "Nothing. Forget it",
     "merchant_pretalk", []],
]