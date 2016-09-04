from source.header_operations import *
from source.header_common import * ##reg0, s1, reg2, s3, reg3, reg4
from source.header_parties import *
from source.header_dialogs import * ##anyone, plyr
from source.lazy_flag import * ##LazyFlag
from source.module_constants import * ##_party_encounter


dialogs = [

    [anyone, "caravan_offer_protection", [],
     "These roads are dangerous indeed. One can never have enough protection.",
     "caravan_offer_protection_2", [
        (get_party_ai_object, ":caravan_destination", "$g_encountered_party"),
        (store_distance_to_party_from_party, "$caravan_distance_to_target", ":caravan_destination", "$g_encountered_party"),
        (assign, "$caravan_escort_offer", "$caravan_distance_to_target"),
        (val_sub, "$caravan_escort_offer", 10),
        (call_script, "script_party_calculate_strength", "p_main_party", 0),
        (assign, ":player_strength", reg0),
        (val_min, ":player_strength", 200),
        (val_add, ":player_strength", 20),
        (val_mul, "$caravan_escort_offer", ":player_strength"),
        (val_div, "$caravan_escort_offer", 65),#gdw50
        (val_max, "$caravan_escort_offer", 5),
        (assign, "$caravan_escort_state",0 ),#move this later to the start quest important for simple trigger
      ]],

    # reject offer
    [anyone, "caravan_offer_protection_2", [
        (lt, "$caravan_distance_to_target", 10)
    ], "An escort? We're almost there already! Thank you for the offer, though.",
     "close_window", [
         (assign, "$g_leave_encounter", 1)
     ]],

    # suggest value offer
    [anyone, "caravan_offer_protectionfree", [
        (get_party_ai_object, ":caravan_destination", "$g_encountered_party"),
        (str_store_party_name, s1, ":caravan_destination"),
        #(assign, reg15, "$caravan_escort_offer"),

        ], "We are heading to {s1}. We accept your help as long as we can see you.", "caravan_offer_protectionfree2", []
     ],

     [anyone, "caravan_offer_protection_2", [
        (get_party_ai_object, ":caravan_destination", "$g_encountered_party"),
        (str_store_party_name, s1, ":caravan_destination"),
        (assign, reg15, "$caravan_escort_offer"),

        ], "We are heading to {s1}. I will pay you {reg15} scillingas if you "
           "escort us there.", "caravan_offer_protection_3", []
     ],

    # player agrees to value
    [anyone | plyr, "caravan_offer_protection_3", [],
     "Agreed.", "caravan_offer_protection_4", []],

    # chat after accepting
    [anyone, "caravan_offer_protection_4", [],
     "I want you to stay close to us along the way. We'll need your help if "
     "we get ambushed by bandits.", "caravan_offer_protection_5", []],

    # chat after accepting
    [anyone | plyr, "caravan_offer_protection_5", [],
     "Don't worry, you can trust me.", "caravan_offer_protection_6", []],

     [anyone | plyr, "caravan_offer_protectionfree2", [
       ],"Don't worry, you can trust me. I'm your caravan sponsor after all", "close_window", [
(quest_get_slot, "$town_suggested_to_go_to","qst_oim_deliver_caravan", "slot_party_ai_object", ),
(quest_get_slot, ":oim_caravan", "qst_oim_deliver_caravan","slot_quest_target_party", ),  
        #(get_party_ai_object, ":caravan_destination", "$g_encountered_party"),
        (assign, "$caravan_escort_destination_town", "$town_suggested_to_go_to"),
        (assign, "$caravan_escort_party_id", "$g_encountered_party"),
        #(assign, "$caravan_escort_agreed_reward", "$caravan_escort_offer"),
        (assign, "$caravan_escort_state", 0),
        (assign, "$mycaravan_escort_state", 1),
        
    (party_set_ai_behavior, ":oim_caravan", ai_bhvr_track_party),
    (party_set_ai_object, ":oim_caravan","p_main_party"),
    #(party_set_slot, "qst_oim_deliver_caravan", "slot_party_ai_object", "p_main_party"),
    (party_set_flags, ":oim_caravan", pf_default_behavior, 0),
    (assign, "$g_leave_encounter", 1),
    #(quest_set_slot, "qst_oim_deliver_caravan", "slot_quest_target_party", ":quest_target_party"),]
        ]],
# (get_party_ai_object, ":caravan_destination", "$g_encountered_party"),
#         (str_store_party_name, s7, ":caravan_destination"),
    # chat after accepting
    [anyone, "caravan_offer_protection_6", [
        
        ], "Good. Come and collect your money when we're within sight of {s1}. "
           "For now, let's just get underway.", "close_window", [
           (get_party_ai_object, ":caravan_destination", "$g_encountered_party"),
        (str_store_party_name, s1, ":caravan_destination"),
        #(assign, "$caravan_escort_party_id", "$g_encountered_party"),
        #(get_party_ai_object, ":caravan_destination", "$g_encountered_party"),
        (assign, "$caravan_escort_destination_town", ":caravan_destination"),
        (assign, "$caravan_escort_party_id", "$g_encountered_party"),
        (assign, "$caravan_escort_agreed_reward", "$caravan_escort_offer"),
        (party_set_ai_behavior, "$caravan_escort_party_id", ai_bhvr_track_party),
    (party_set_ai_object, "$caravan_escort_party_id", "p_main_party"),
    (party_set_flags, "$caravan_escort_party_id", pf_default_behavior, 0),
        (assign, "$mycaravan_escort_state", 0),
        (assign, "$caravan_escort_state", 1),

        (assign, "$g_leave_encounter", 1),
        
    #(quest_set_slot, "qst_oim_deliver_caravan", "slot_quest_target_party", ":quest_target_party"),
      ]],

    # player refuses with value
    [anyone | plyr, "caravan_offer_protection_3", [],
     "Forget it.", "caravan_offer_protection_4b", []
     ],
     [anyone | plyr, "caravan_offer_protectionfree2", [],
     "Forget it.", "caravan_offer_protection_4b", []
     ],

    # caravan replies to refusal
    [anyone, "caravan_offer_protection_4b", [],
     "Perhaps another time, then.", "close_window", [
         (assign, "$g_leave_encounter", 1)]
     ],
]

# dialogs triggered when `$caravan_escort_state = 1`
dialogs += [
##not on quest
[party_tpl|LazyFlag("pt_merchant_caravan"),"start", [
                                           (eq,"$g_encountered_party","$caravan_escort_party_id"), 
                                           (eq, "$caravan_escort_state", 1),
                                           #(get_party_ai_object, ":caravan_destination", "$g_encountered_party"),
                                           #(quest_get_slot, "$town_suggested_to_go_to", "qst_oim_deliver_caravan", "slot_quest_target_center"),
                                           (store_distance_to_party_from_party, reg5, "$caravan_escort_destination_town", "$caravan_escort_party_id"),
                                           (lt,reg5,4),
                                           (str_store_party_name, s3, "$caravan_escort_destination_town"),
                                           (assign, reg16, "$caravan_escort_agreed_reward"),
    # [anyone, "event_triggered", [
    #     (eq, "$caravan_escort_state", 1),
    #     (neq, "$mycaravan_escort_state", 1),
    #     (neq, "$mycaravan_escort_state", 2),
    #     (eq, "$g_encountered_party", "$caravan_escort_party_id"),
    #     (le, "$talk_context", tc_party_encounter),
    #     (store_distance_to_party_from_party, reg0, "$caravan_escort_destination_town", "$caravan_escort_party_id"),
    #     (lt, reg0, 3),
    #     (str_store_party_name, s3, "$caravan_escort_destination_town"),
    #     (assign, reg16, "$caravan_escort_agreed_reward"),
                                        ], "There! I can see the walls of {s3} in the distance. We've made it "
                                           "safely. Here, take this purse of {reg16} scillingas, as I promised. "
                                           "I hope we can travel together again someday.", "close_window", 
                                        [ (party_set_ai_object, "$caravan_escort_destination_town","$caravan_escort_party_id"),## "$caravan_escort_destination_town"),
                                         (assign, "$caravan_escort_state", 0),
                                         (call_script, "script_troop_add_gold", "trp_player",
                                          "$caravan_escort_agreed_reward"),
                                         # (assign, reg6 "$caravan_escort_agreed_reward"),
                                         # (val_mul, reg6,2),
                                         # (add_xp_as_reward, reg6),
                                         (assign, "$g_leave_encounter", 1),
                                     ]],

     [party_tpl|LazyFlag("pt_oim_merchant_caravan2"),"start", [(quest_get_slot, ":oim_caravan", "qst_oim_deliver_caravan", "slot_quest_target_party"),
                                           (eq,"$g_encountered_party",":oim_caravan"),
                                           (quest_get_slot, "$town_suggested_to_go_to", "qst_oim_deliver_caravan", "slot_quest_target_center"),
                                           (store_distance_to_party_from_party, ":dist", "$town_suggested_to_go_to",":oim_caravan"),
                                           (lt,":dist",4),
                                          (str_store_party_name, s21, "$town_suggested_to_go_to"),
                                           #(eq, "$mycaravan_escort_state", 1),
                                           #(quest_slot_eq, "qst_oim_deliver_caravan", "slot_quest_current_state", 1),
                                           ],
   "Well, we have almost reached {s21}. We can cover the rest of the way ourselves.I will spread word about your good deed amongst the merchants once I reach town."+
           "I hope we can travel together again someday.", "close_window",[(quest_get_slot, ":oim_caravan", "qst_oim_deliver_caravan", "slot_quest_target_party"),
                                                       (quest_get_slot, ":quest_target_center", "qst_oim_deliver_caravan", "slot_quest_target_center"),
                                                       # (quest_get_slot, ":quest_giver_center", "qst_oim_deliver_caravan", "slot_quest_giver_center"),
                                                       # (quest_get_slot, ":quest_gold_reward", "qst_oim_deliver_caravan", "slot_quest_gold_reward"),
                                                       (party_set_ai_object, ":oim_caravan", ":quest_target_center"),
                                                       (party_set_ai_behavior, ":oim_caravan", ai_bhvr_travel_to_party),
                                                       
                                                       (party_set_flags, ":oim_caravan", pf_default_behavior, 0),
                                                       #str_store_party_name, s21, ":quest_target_center"),
                                                       (quest_set_slot, "qst_oim_deliver_caravan", "slot_quest_target_center", ":quest_target_center"),
                                                      #(call_script, "script_change_player_relation_with_center", ":quest_giver_center", 1),
                                                      #(call_script, "script_end_quest","qst_oim_deliver_caravan"),
                                                       (quest_set_slot, "qst_oim_deliver_caravan", "slot_quest_current_state", 2),
                                                       (assign, "$caravan_escort_destination_town", ":quest_target_center"),
                                                      #(call_script, "script_troop_add_gold", "trp_player", ":quest_gold_reward"),
                                                      #(assign, ":xp_reward", ":quest_gold_reward"),
                                                       #(val_mul, ":xp_reward", 5),#gdw5 drastically raised gold reward
                                                       #(val_add, ":xp_reward", 100),gdw
                                                       #add_xp_as_reward, ":xp_reward"),
                                                      #(call_script, "script_change_troop_renown", "trp_player", 2),
                                                       #assign, reg14, ":quest_gold_reward"),
                                                       (assign, "$g_leave_encounter", 1),
                                                       ]],
# [anyone, "event_triggered", [##for caravan submod
#         (eq, "$mycaravan_escort_state", 1),
#         (eq, "$g_encountered_party", "$caravan_escort_party_id"),
#         (le, "$talk_context", tc_party_encounter),
#         (quest_get_slot, "slot_quest_target_center","qst_oim_deliver_caravan",  "$town_suggested_to_go_to"),  ##slot_party_ai_object
#         (store_distance_to_party_from_party, reg3, "$town_suggested_to_go_to", "$caravan_escort_party_id"),
        
#         (lt, reg3, 2),
#         (str_store_party_name, s3, "$town_suggested_to_go_to"),
#         #assign, reg16, "$caravan_escort_agreed_reward"),
#         ], "There! I can see the walls of {s3} in the distance. We've made it "
#            "safely. I will spread word about your good deed amongst the merchants once I reach town."
#            "I hope we can travel together again someday.", "close_window", 
#         [         (assign, "$mycaravan_escort_state", 2),
#          #(quest_set_slot, "$town_suggested_to_go_to","qst_oim_deliver_caravan", "slot_quest_target_center"),
#       #(add_xp_as_reward, 233),
#         (quest_get_slot, ":oim_caravan", "qst_oim_deliver_caravan","slot_quest_target_party", ),  
#        (party_set_ai_behavior, ":oim_caravan", ai_bhvr_travel_to_party),       
#         (party_set_ai_object, ":oim_caravan", "$town_suggested_to_go_to"),
#           (quest_set_slot, "qst_oim_deliver_caravan", "slot_quest_target_center", "$town_suggested_to_go_to"),
#     #(party_set_slot, "qst_oim_deliver_caravan", "slot_party_ai_object", "p_main_party"),
#     (party_set_flags, ":oim_caravan", pf_default_behavior, 0),
         
#          (assign, "$g_leave_encounter", 1),
#      ]],
    
[anyone | plyr, "talk_caravan_escort", [],
     "There might be bandits nearby. Stay close.", "talk_caravan_escort_2a", []
     ],

    [anyone, "talk_caravan_escort_2a", [],
     "Trust me, {playername}, we're already staying as close to you as we can. "
     "Lead the way.", "close_window", [
         (assign, "$g_leave_encounter", 1),
     ]],

    [anyone | plyr, "talk_caravan_escort", [],
     "No sign of trouble, we can breathe easy.", "talk_caravan_escort_2b", []
     ],

    [anyone, "talk_caravan_escort_2b", [],
     "I'll breathe easy when we reach {s1} and not a moment sooner. Let's "
     "keep moving.", "close_window", [
        (str_store_party_name, s1, "$caravan_escort_destination_town"),
        (assign, "$g_leave_encounter", 1)
     ]],
]

simple_triggers = [
    # (0.15, [
    #     # escort caravan quest auto dialog trigger
        
    #         (this_or_next|eq, "$caravan_escort_state", 1),
    #         (eq, "$mycaravan_escort_state", 1),
    #         (party_is_active, "$caravan_escort_party_id"),
    #     (try_begin),
    #         (store_distance_to_party_from_party, ":caravan_distance_to_destination", "$caravan_escort_destination_town", "$caravan_escort_party_id"),
    #         (lt, ":caravan_distance_to_destination", 1),

    #         (store_distance_to_party_from_party, ":caravan_distance_to_player", "p_main_party", "$caravan_escort_party_id"),
    #         (lt, ":caravan_distance_to_player", 3),

    #         (assign, "$talk_context", tc_party_encounter),
    #         (assign, "$g_encountered_party", "$caravan_escort_party_id"),
    #         (party_stack_get_troop_id, ":caravan_leader", "$caravan_escort_party_id", 0),
    #         (party_stack_get_troop_dna, ":caravan_leader_dna", "$caravan_escort_party_id", 0),

    #         (start_map_conversation, ":caravan_leader", ":caravan_leader_dna"),
    #     (try_end),
    # ]),

    (1, [##move up to 8 since stay captive 30 hours
        # captured player
        (try_begin),
                    (eq, "$cheat_mode", 1),
                    (display_message, "@{!}DEBUG : Simplerigger for losing escortstart"),
         (try_end),
        (try_begin),
            (eq,"$g_player_surrenders",1),##later add if escort strays too far
            (try_begin),
             (eq, "$caravan_escort_state", 1),##just reset target
             (neq, "$mycaravan_escort_state", 1),
               (party_set_ai_object, "$caravan_escort_destination_town","$caravan_escort_party_id"),## "$caravan_escort_destination_town"),
                (party_set_ai_behavior, "$caravan_escort_party_id", ai_bhvr_travel_to_party),
                (assign, "$caravan_escort_state", 0), 
            (else_try),##just reset target
                (eq, "$mycaravan_escort_state", 1),
                    (quest_get_slot, ":quest_target_center", "qst_oim_deliver_caravan", "slot_quest_target_center"),
                                                       (quest_get_slot, ":oim_caravan", "qst_oim_deliver_caravan", "slot_quest_target_party"),
                                                       # (quest_get_slot, ":quest_gold_reward", "qst_oim_deliver_caravan", "slot_quest_gold_reward"),
                                                       (party_set_ai_behavior, ":oim_caravan", ai_bhvr_travel_to_party),
                                                       (party_set_ai_object, ":oim_caravan", ":quest_target_center"),
                                                       (party_set_flags, ":oim_caravan", pf_default_behavior, 0),
                                                       (str_store_party_name, s21, ":quest_target_center"),
                                                       (quest_set_slot, "qst_oim_deliver_caravan", "slot_quest_target_center", ":quest_target_center"),
                                                      #(call_script, "script_change_player_relation_with_center", ":quest_giver_center", 1),
                                                      #(call_script, "script_end_quest","qst_oim_deliver_caravan"),
                                                       (quest_set_slot, "qst_oim_deliver_caravan", "slot_quest_current_state", 2),
                                                       (assign, "$caravan_escort_destination_town", ":quest_target_center"),
            (try_end),
        (try_end),
        (try_begin),
                    (eq, "$cheat_mode", 1),
                    (display_message, "@{!}DEBUG : Simplerigger for losing escorts end"),
         (try_end),
        
    ]),
]

triggers = [
    # cancel escort quest if caravan is no longer active
    (6.0, 0, 0.0, [
        #(try_begin),
        (assign, ":cancel_quest", 0),
        (this_or_next|eq, "$caravan_escort_state", 1),
        (eq, "$mycaravan_escort_state", 1),
        (try_begin),
                    (eq, "$cheat_mode", 1),
                    (display_message, "@{!}DEBUG : Trigger for losing caravan to banditsstart"),
         (try_end),
        (try_begin),
            (neg | party_is_active, "$caravan_escort_party_id"),
            (assign, ":cancel_quest", 1),
        (else_try),
            (get_party_ai_object, ":ai_object", "$caravan_escort_party_id"),
            (this_or_next|neq, ":ai_object", "$caravan_escort_destination_town"),
            (neq, ":ai_object", "p_main_party"),
            (assign, ":cancel_quest", 1),
            #(party_set_ai_object, "$caravan_escort_party_id", "p_main_party"),
        (try_end),

        #(try_end),
        (eq, ":cancel_quest", 1),
        ],
     [(assign, "$caravan_escort_state", 0),
     (assign, "$mycaravan_escort_state", 0),
     (try_begin),
                    (eq, "$cheat_mode", 1),
                    (display_message, "@{!}DEBUG : Trigger for losing caravan to bandits end"),
         (try_end),
    ]),
]
