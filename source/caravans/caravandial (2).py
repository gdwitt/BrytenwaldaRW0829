from source.header_operations import *
from source.header_common import s0, s1,s2, s3, s4, s5
from caravansubmodnodia import *
from source.header_dialogs import *#anyone, plyr
from source.module_constants import trade_goods_begin, trade_goods_end
from source.header_parties import ai_bhvr_travel_to_party, ai_bhvr_travel_to_point, \
    pf_default_behavior
from source.statement import StatementBlock
from source.header_items import *
from source.module_constants import *
from source.module_troops import troops
from source.module_quests import *
from source.header_troops import *
#from source.module_strings import *

dialogs = [
     ####caravan start##  ##repeat belowgdw
 # [anyone,"mayor_investment_purchase",[], "Very good. Your enterprise should be up and running in about a week. When next you come, and thereafter, you should speak to your {s4} about its operations.", "mayor_pretalk",[
 #  (store_sub, ":current_town_order", "$current_town", towns_begin), 
 #  (store_add, ":craftsman_troop", ":current_town_order", "trp_town_1_master_craftsman"),
 #  (str_store_troop_name, s4, ":craftsman_troop"),  
  
 #  ]],
  
  ###################   
##  OiM GE Code
### 
   #    [anyone ,"start", [(is_between,"$g_talk_troop",mayors_begin,mayors_end),(eq,"$g_talk_troop_met",0),#from BW
   #                   (str_store_party_name, s9, "$current_town")],
   # "Hello stranger, you seem to be new to {s9}. I am the guild master of the town.", "mayor_talk",[]],
    #oim_guild_master_talk
    [anyone,"oim_guild_master_talk", [], "Yes, {playername}.", "oim_guild_master_ask", 
    [
        #(jump_to_menu, "mnu_auto_return_to_map"),
    ]], 
    # [LazyFlag('trp_recruiter') | plyr, "dplmc_recruiter_talk", [],
    #  "Ok, keep going.", "close_window", [
    #      (assign, "$g_leave_encounter", 1)
    # ]],
    [anyone | plyr,"oim_guild_master_ask", [], "What can I gain from a caravan?", "oim_send_caravan_generik_descr", []],          

    [anyone,"oim_send_caravan_generik_descr", [], "Well, you can buy a load of goods here on a discount, and send the caravan to another city, where you'd sell the goods -- for a profit or a loss, depends on how good a trader you are.", "oim_guild_master_talk", []],  
    
    [anyone | plyr,"oim_guild_master_ask", 
    [
        (this_or_next|quest_slot_eq, "qst_oim_deliver_caravan", "slot_quest_target_center", -1),  
        (neg|check_quest_active, "qst_oim_deliver_caravan"),
    ], "Yes, I'd like to send a caravan.", "oim_send_caravan_generik", []],     

    [anyone|plyr,"oim_guild_master_ask", 
    [
        (quest_slot_eq, "qst_oim_trade_pantent", "slot_quest_current_state", 1),
    ], "I would like to get a trade permit.", "oim_buy_trayd_patend", []],  
    
    [anyone,"oim_buy_trayd_patend", [], "I should think that for you, {playername}, a trade permit can be issued on the spot for a mere 2500 scillingas.", "oim_buy_trayd_patend_1", []],   

    [anyone|plyr,"oim_buy_trayd_patend_1", 
    [
        (store_troop_gold, ":gold", "trp_player"), 
        (ge, ":gold", 2500),
    ], "I am willing to pay this amount. ", "oim_buy_trayd_patend_2", []],  

    [anyone,"oim_buy_trayd_patend_2", [], "Excellent. Here is the document and the seal... ", "oim_guild_master_talk", 
    [
        (quest_set_slot, "qst_oim_trade_pantent", "slot_quest_current_state", 2),
        (str_store_string, s4, "str_oim_trade_pantent_granted"),  
        (add_quest_note_from_sreg, "qst_oim_trade_pantent", 4, s2, 1),
        (troop_remove_gold, "trp_player", 2500),
        
        #(check_quest_active, "qst_oim_trade_pantent"), 
        #(quest_slot_eq, "qst_oim_trade_pantent", slot_quest_current_state, 2),
        (call_script, "script_end_quest", "qst_oim_trade_pantent"),
    ]], 

    [anyone|plyr,"oim_buy_trayd_patend_1", [], "That is too expensive for me.", "oim_guild_master_talk", []],           
        
    [anyone|plyr,"oim_guild_master_ask", [], "Let's talk about something else.", "mayor_pretalk", []],          

    [anyone,"oim_send_caravan_generik", [
      (assign, ":there_are_items_avaliable", 0),
      (assign, ":there_are_items_avaliable_and_enought_money", 0),

      (store_troop_gold, ":gold", "trp_player"), 

      (try_for_range, ":goods", trade_goods_begin, trade_goods_end),
        (party_get_slot, ":cur_merchant", "$g_encountered_party", "slot_town_merchant"),
        (assign, ":num_items", 0),       
        (try_for_range, ":i_slot", num_equipment_kinds, max_inventory_items + num_equipment_kinds),
          (troop_get_inventory_slot, ":slot_item", ":cur_merchant", ":i_slot"),
          (try_begin),
            (eq, ":slot_item", ":goods"),
            (val_add, ":num_items", 1),##look at each item and check if it is a trade good
          (try_end),
        (try_end),

        (ge, ":num_items", 7),

        (assign, ":there_are_items_avaliable", 1),      
        (call_script, "script_oim_get_item_base_price", ":goods"), 
      
        (assign, ":base_price", reg0),
        (ge, ":base_price", 15), #no need to make trade with less valueable items. its impossible to make profit because of trade expenses.   

        (call_script, "script_game_get_item_buy_price_factor", ":goods"),#, "$g_encountered_party"), 
        (assign, ":price_factor", reg0),      
        (store_mul, ":price", ":base_price", ":price_factor"), 
        (val_div, ":price", 100),
        (assign, reg0, ":price"),         
        (val_mul, ":price", 5), 
      
        (store_div, ":price_for_escort", ":base_price", 2), #escort price = 0.5x base price
        (val_add, ":price", ":price_for_escort"), #price for escourt
        
        (ge, ":gold", ":price"),

        (assign, ":there_are_items_avaliable_and_enought_money", 1),
      (try_end),

      (str_store_party_name, s1, "$town_suggested_to_go_to"),

      (assign, "$g_trade_next_menu", 0),
      (try_begin),      
        (eq, ":there_are_items_avaliable", 0),      
        (assign, "$g_trade_next_menu", 1),
      (else_try),
        (eq, ":there_are_items_avaliable_and_enought_money", 0),
        (assign, "$g_trade_next_menu", 2),
      (try_end),        

      (eq, ":there_are_items_avaliable_and_enought_money", 1),

      (store_distance_to_party_from_party, ":dist", "$town_suggested_to_go_to", "$g_encountered_party"),
      (store_div, ":travel_time", ":dist", 4),
      (assign, reg1, ":travel_time"),
    ], "Which goods do you want to trade?   ", "oim_send_caravan_which_goods", []],         
    
    [anyone,"oim_send_caravan_generik", [   
    (eq, "$g_trade_next_menu", 1),  
    ], "I am afraid, we don't have enough items in stock to furnish the caravan.", "oim_send_caravan_give_up", []],         
    
    [anyone,"oim_send_caravan_generik", [   
    (eq, "$g_trade_next_menu", 2),  
    ], "You do not have enough money to afford the caravan.", "oim_send_caravan_give_up", []],          

    [anyone|plyr,"oim_send_caravan_give_up", [(str_store_string, s2, "str_return_later"),], "{s2}", "mayor_pretalk", []],   

    [anyone|plyr|repeat_for_1000,"oim_send_caravan_which_goods", [
      (store_repeat_object, ":goods"),
      (is_between,":goods", trade_goods_begin, trade_goods_end),
      (call_script, "script_oim_is_trade_good_availible", "$g_encountered_party", ":goods"),
      (gt, reg0, 0),

      (party_get_slot, ":cur_merchant", "$g_encountered_party", "slot_town_merchant"),
      (assign, ":num_items", 0),       
      (try_for_range, ":i_slot", num_equipment_kinds ,max_inventory_items + num_equipment_kinds),
        (troop_get_inventory_slot, ":slot_item", ":cur_merchant", ":i_slot"),
        (try_begin),
          (eq, ":slot_item", ":goods"),
          (val_add, ":num_items", 1),
        (try_end),
      (try_end),

      (ge, ":num_items", 5),

      (str_store_item_name, s5 ,":goods"),
      (call_script, "script_oim_get_item_base_price", ":goods"), 
      
      (assign, ":base_price", reg0),
      (ge, ":base_price", 10), #no need to make trade with less valueable items. its impossible to make profit because of trade expenses.     

      (call_script, "script_game_get_item_buy_price_factor", ":goods"),
      (assign, ":price_factor", reg0),    
      (store_mul, ":price", ":base_price", ":price_factor"), 
      (val_div, ":price", 100),

      (assign, reg0, ":price"),   
      
      (val_mul, ":price", 5), 

      (val_add, ":price", 100), #minimum caravan cost is 100 (50 for caravan master + 50 for one guard)
      
      (store_troop_gold, ":gold", "trp_player"), 
      (ge, ":gold", ":price"),
    ],
    "{s5}, price: {reg0} scillingas.", "oim_send_caravan_which_town",[
      (store_repeat_object, ":goods"),
      (assign, "$town_suggested_goods", ":goods"),
    ]],
       
    [anyone|plyr,"oim_send_caravan_which_goods", [(str_store_string, s2, "str_reason_high_price"),], "{s2}", "mayor_pretalk", []],          
    [anyone,"oim_send_caravan_which_town", [], "And where would you like to send the caravan?", "oim_send_caravan_town_selected", []],          
    
    [anyone|plyr|repeat_for_parties,"oim_send_caravan_town_selected", 
    [
        (store_repeat_object, ":center_no"),
        (party_slot_eq,":center_no",slot_party_type, spt_town),        
        (neq, ":center_no", "$g_encountered_party"),
        (str_store_party_name, s1, ":center_no"),       
        (str_store_item_name, s2, "$town_suggested_goods"),
        
        (set_fixed_point_multiplier, 100),  

        (store_distance_to_party_from_party, ":dist", ":center_no", "$g_encountered_party"),

        (call_script, "script_get_max_skill_of_player_party", "skl_trade"),
        (assign, ":trade_skill", reg0),
        
        (store_mul, ":trade_skill_mul_10", ":trade_skill", 10),
        (store_add, ":trade_skill_mul_10_plus_20", ":trade_skill_mul_10", 20),

        (str_store_party_name, s1, ":center_no"),       

        (try_begin),
          (le, ":dist", ":trade_skill_mul_10_plus_20"),
          
          (call_script, "script_oim_get_item_base_price", "$town_suggested_goods"), 
          
          (assign, ":base_price", reg0),
          (assign, ":temp_g_encountered_party", "$g_encountered_party"),
          (assign, "$g_encountered_party", ":center_no"),
          (call_script, "script_game_get_item_sell_price_factor", "$town_suggested_goods"),
          (assign, "$g_encountered_party", ":temp_g_encountered_party"),
          (assign, ":price_factor", reg0),
          (store_mul, ":price", ":base_price", ":price_factor"), 
          (val_div, ":price", 100),
          (assign, reg1, ":price"),

          (str_store_string, s1, "str_price_there_known"),      
        (else_try),
          (str_store_string, s1, "str_price_there_unknown"),        
        (try_end),

    ], "{s1}", "oim_send_caravan_finish",[(store_repeat_object, "$town_suggested_to_go_to")]],
      
    [anyone|plyr,"oim_send_caravan_town_selected", [], "Some other time.", "mayor_pretalk", []],               

    [anyone,"oim_send_caravan_finish", 
    [
      (store_distance_to_party_from_party, ":dist", "$town_suggested_to_go_to", "$g_encountered_party"),
      (store_div, ":travel_time", ":dist", 10),
      (assign, reg1, ":travel_time"),

      (str_store_item_name, s2, "$town_suggested_goods"),
      (str_store_party_name, s1, "$town_suggested_to_go_to"),

      (party_get_slot, ":cur_merchant", "$g_encountered_party", "slot_town_merchant"),
       (assign, "$g_num_town_suggested_goods", 0),       
       (try_for_range, ":i_slot", num_equipment_kinds, max_inventory_items + num_equipment_kinds),
         (troop_get_inventory_slot, ":slot_item", ":cur_merchant", ":i_slot"),
         (try_begin),
           (eq, ":slot_item", "$town_suggested_goods"),
           (val_add, "$g_num_town_suggested_goods", 1),
         (try_end),
       (try_end),
    ], "Very well, that shouldn't be a problem. The caravan shall head to {s1}. I guess the journey will take {reg1} hours. And how many {s2} would you like to send?", "oim_send_caravan_town_select_go_on4", []],         
        
    [anyone|plyr,"oim_send_caravan_town_select_go_on4", [
        (ge, "$g_num_town_suggested_goods", 20),

        (call_script, "script_oim_get_item_base_price", "$town_suggested_goods"), 
        (assign, ":price", reg0),

        (str_store_item_name, s2, "$town_suggested_goods"),
        (call_script, "script_oim_game_get_item_buy_price_factor", "$town_suggested_goods", "$g_encountered_party"), 
        (assign, ":price_factor", reg0),
        (val_mul, ":price", ":price_factor"), 
        (val_div, ":price", 100),
        (val_mul, ":price", 20), #count

        (store_troop_gold, ":gold", "trp_player"), 
        (store_sub, ":gold_minus_minimum_caravan_expense", ":gold", 100), #minimum caravan expense is 100 (50 for caravan master + 50 for one guard)
        (ge, ":gold_minus_minimum_caravan_expense", ":price"),
        (assign, reg0, ":price"),
        (assign, "$g_total_caravan_cost_huge", ":price"),
    ], "A great caravan ({reg0} scillingas, 20 goods).", "oim_send_caravan_town_select_go_on4b", [(assign, "$oim_count_to_deliver", 20),(assign, "$g_total_caravan_cost", "$g_total_caravan_cost_huge"),]],         
    [anyone|plyr,"oim_send_caravan_town_select_go_on4", [
        (ge, "$g_num_town_suggested_goods", 15),

        (call_script, "script_oim_get_item_base_price", "$town_suggested_goods"), 
        (assign, ":price", reg0),

        (str_store_item_name, s2, "$town_suggested_goods"),
        (call_script, "script_oim_game_get_item_buy_price_factor", "$town_suggested_goods", "$g_encountered_party"), 
        (assign, ":price_factor", reg0),
        (val_mul, ":price", ":price_factor"), 
        (val_div, ":price", 100),
        (val_mul, ":price", 15), #count

        (store_troop_gold, ":gold", "trp_player"), 
        (store_sub, ":gold_minus_minimum_caravan_expense", ":gold", 100), #minimum caravan expense is 100 (50 for caravan master + 50 for one guard)
        (ge, ":gold_minus_minimum_caravan_expense", ":price"),
        (assign, reg0, ":price"),
        (assign, "$g_total_caravan_cost_large", ":price"),
    ], "A big caravan ({reg0} scillingas, 15 goods).", "oim_send_caravan_town_select_go_on4b", [(assign, "$oim_count_to_deliver", 15),(assign, "$g_total_caravan_cost", "$g_total_caravan_cost_large"),]],          
    [anyone|plyr,"oim_send_caravan_town_select_go_on4", [
        (ge, "$g_num_town_suggested_goods", 10),

        (call_script, "script_oim_get_item_base_price", "$town_suggested_goods"), 
        (assign, ":price", reg0),

        (call_script, "script_oim_game_get_item_buy_price_factor", "$town_suggested_goods", "$g_encountered_party"), 
        (assign, ":price_factor", reg0),
        (val_mul, ":price", ":price_factor"), 
        (val_div, ":price", 100),
        (val_mul, ":price", 10), #count
        
        (store_troop_gold, ":gold", "trp_player"), 
        (store_sub, ":gold_minus_minimum_caravan_expense", ":gold", 100), #minimum caravan expense is 100 (50 for caravan master + 50 for one guard)
        (ge, ":gold_minus_minimum_caravan_expense", ":price"),
        (assign, reg0, ":price"),
        (assign, "$g_total_caravan_cost_medium", ":price"),
    ], "A medium caravan ({reg0} scillingas, 10 goods).", "oim_send_caravan_town_select_go_on4b", [(assign, "$oim_count_to_deliver", 10),(assign, "$g_total_caravan_cost", "$g_total_caravan_cost_medium"),]],          
    [anyone|plyr,"oim_send_caravan_town_select_go_on4", [
        (ge, "$g_num_town_suggested_goods", 5),

        (call_script, "script_oim_get_item_base_price", "$town_suggested_goods"), 
        (assign, ":price", reg0),

        (call_script, "script_oim_game_get_item_buy_price_factor", "$town_suggested_goods", "$g_encountered_party"), 
        (assign, ":price_factor", reg0),
        (val_mul, ":price", ":price_factor"), 
        (val_div, ":price", 100),
        (val_mul, ":price", 5), #count

        (store_troop_gold, ":gold", "trp_player"), 
        (store_sub, ":gold_minus_minimum_caravan_expense", ":gold", 100), #minimum caravan expense is 100 (50 for caravan master + 50 for one guard)
        (ge, ":gold_minus_minimum_caravan_expense", ":price"),
        (assign, reg0, ":price"),
        (assign, "$g_total_caravan_cost_small", ":price"),
    ], "A small caravan ({reg0} scillingas, 5 goods).", "oim_send_caravan_town_select_go_on4b", [(assign, "$oim_count_to_deliver", 5),(assign, "$g_total_caravan_cost", "$g_total_caravan_cost_small"),]],          
    
    [anyone|plyr,"oim_send_caravan_town_select_go_on4", [
        (str_store_string, s2, "str_reason_high_price"), 
    ], "{s2} ", "mayor_pretalk", []], #was close_window

    [anyone,"oim_send_caravan_town_select_go_on4b", [
    ], "All right. There will be one caravan master leading the caravan. How many caravan guards do you want as escort?", "oim_send_caravan_town_select_go_on4c", []],          

    [anyone|plyr,"oim_send_caravan_town_select_go_on4c", 
    [
      (assign, reg5, 2), 
      (assign, reg0, 100),
    ], "{reg5}, price: {reg0} scillingas.", "oim_send_caravan_town_select_go_on5", [(assign, "$g_number_of_escorts", 2),]],         

    [anyone|plyr,"oim_send_caravan_town_select_go_on4c", 
    [
      (store_troop_gold, ":gold", "trp_player"), 
      (store_sub, ":gold_minus_200", ":gold", 200), 
      (ge, ":gold_minus_200", "$g_total_caravan_cost"), 
      (assign, reg5, 4), 
      (assign, reg0, 200),
    ], "{reg5}, price: {reg0} scillingas.", "oim_send_caravan_town_select_go_on5", [(assign, "$g_number_of_escorts", 4),]],         

    [anyone|plyr,"oim_send_caravan_town_select_go_on4c", 
    [
      (store_troop_gold, ":gold", "trp_player"), 
      (store_sub, ":gold_minus_400", ":gold", 400), 
      (ge, ":gold_minus_400", "$g_total_caravan_cost"), 
      (assign, reg5, 8), 
      (assign, reg0, 400),
    ], "{reg5}, price: {reg0} scillingas.", "oim_send_caravan_town_select_go_on5", [(assign, "$g_number_of_escorts", 8),]],         

    [anyone|plyr,"oim_send_caravan_town_select_go_on4c", 
    [
      (store_troop_gold, ":gold", "trp_player"), 
      (store_sub, ":gold_minus_600", ":gold", 600), 
      (ge, ":gold_minus_600", "$g_total_caravan_cost"), 
      (assign, reg5, 12), 
      (assign, reg0, 600),
    ], "{reg5}, price: {reg0} scillingas.", "oim_send_caravan_town_select_go_on5", [(assign, "$g_number_of_escorts", 12),]],            
    
    [anyone|plyr,"oim_send_caravan_town_select_go_on4c", 
    [
      (store_troop_gold, ":gold", "trp_player"), 
      (store_sub, ":gold_minus_1000", ":gold", 1000), 
      (ge, ":gold_minus_1000", "$g_total_caravan_cost"), 
      (assign, reg5, 20), 
      (assign, reg0, 1000),
    ], "{reg5}, price: {reg0} scillingas.", "oim_send_caravan_town_select_go_on5", [(assign, "$g_number_of_escorts", 20),]],            

    [anyone,"oim_send_caravan_town_select_go_on5", 
    [       
        (str_store_item_name, s1, "$town_suggested_goods"), 
        (str_store_party_name, s2, "$town_suggested_to_go_to"),         

        (try_begin),
          (eq, "$oim_count_to_deliver", 20),
          (assign, "$g_total_caravan_cost", "$g_total_caravan_cost_huge"),        
        (else_try),
          (eq, "$oim_count_to_deliver", 15),
          (assign, "$g_total_caravan_cost", "$g_total_caravan_cost_large"),
        (else_try),
          (eq, "$oim_count_to_deliver", 10),
          (assign, "$g_total_caravan_cost", "$g_total_caravan_cost_medium"),
        (else_try),       
          (assign, "$g_total_caravan_cost", "$g_total_caravan_cost_small"),
        (try_end),
      
        (assign, "$g_total_caravan_cost_pure", "$g_total_caravan_cost"),
        (assign, reg10,"$g_total_caravan_cost_pure"),
        (store_mul, ":number_of_escorts_mul_50", "$g_number_of_escorts", 50),       
        (val_add, "$g_total_caravan_cost", ":number_of_escorts_mul_50"),        
        (assign, reg11,"$g_total_caravan_cost"),
        (try_begin),
                  (ge, "$cheat_mode", 1),
                  (display_message, "@{!}DEBUG: pretrip: $g_total_caravan_cost_pure is {reg10}; $g_total_caravan_cost is {reg11}"),
        (try_end),
    ], "All right, that should be just fine. {s2} -- that will cost you {reg1} scillingas.", "close_window", [
        #spawning caravan
        (set_spawn_radius,1),
        (spawn_around_party,"p_main_party", "pt_oim_merchant_caravan2"),
        (assign, ":oim_caravan", reg0),
        
        (party_set_slot, ":oim_caravan", "slot_party_type", spt_kingdom_caravan),
        (party_set_slot, ":oim_caravan", "slot_party_ai_state", spai_undefined),

        (party_set_ai_behavior, ":oim_caravan", ai_bhvr_travel_to_party),       
        (party_set_ai_object, ":oim_caravan", "$town_suggested_to_go_to"),

        (party_set_flags, ":oim_caravan", pf_default_behavior, 0),
        (party_add_leader, ":oim_caravan", "trp_caravan_master"),
        (party_add_members, ":oim_caravan", "trp_merc_infantryt3", "$g_number_of_escorts"), #was fix 10 for every kind of caravan
        
        (try_begin),
          (gt, "$players_kingdom", 0),
          (party_set_faction, ":oim_caravan", "$players_kingdom"),
        (else_try),
          (party_set_faction, ":oim_caravan", "fac_player_faction"),
        (try_end),

        (troop_clear_inventory, "trp_caravan_master"),
        (troop_add_items, "trp_caravan_master", "$town_suggested_goods", "$oim_count_to_deliver"),
        
        #starting quest
        #qst_oim_deliver_caravan
        (call_script, "script_start_quest", "qst_oim_deliver_caravan", "trp_player"), 
        (quest_set_slot, "qst_oim_deliver_caravan", "slot_quest_current_state", 0),
        (quest_set_slot, "qst_oim_deliver_caravan", "slot_quest_giver_troop", "trp_player"),  
        (quest_set_slot, "qst_oim_deliver_caravan", "slot_quest_target_center", "$town_suggested_to_go_to"),  
        (quest_set_slot, "qst_oim_deliver_caravan", "slot_quest_target_item", "$town_suggested_goods"),  
        (quest_set_slot, "qst_oim_deliver_caravan", "slot_quest_target_amount", "$oim_count_to_deliver"),  
        (quest_set_slot, "qst_oim_deliver_caravan", "slot_quest_target_party", ":oim_caravan"),  
        (setup_quest_text, "qst_oim_deliver_caravan"),  
        (str_store_party_name_link, s1, "$g_encountered_party"), 
        (str_store_party_name_link, s5, "$town_suggested_to_go_to"), 
        (str_store_item_name, s3, "$town_suggested_goods"), 
        (assign, reg0, "$oim_count_to_deliver"),
        (str_store_string, s2, "str_caravan_develireg_descr"),
          
        
        #removing gold
        (troop_remove_gold, "trp_player", "$g_total_caravan_cost"),

        (assign, ":num_taken_goods", 0),
        (party_get_slot, ":cur_merchant", "$g_encountered_party", "slot_town_merchant"),       
        (try_for_range, ":i_slot", num_equipment_kinds, max_inventory_items + num_equipment_kinds),
          (troop_get_inventory_slot, ":slot_item", ":cur_merchant", ":i_slot"),
          (try_begin),
            (eq, ":slot_item", "$town_suggested_goods"),
            (lt, ":num_taken_goods", "$oim_count_to_deliver"),
            (troop_set_inventory_slot, ":cur_merchant", ":i_slot", -1),
            (val_add, ":num_taken_goods", 1),
          (try_end),
        (try_end),

        #Setting up new price factors
        (call_script, "script_oim_change_price_factors", "$g_encountered_party", "$town_suggested_goods", "$oim_count_to_deliver", 0),

        (assign, reg1, "$g_total_caravan_cost"),     
        (try_begin),
                  (ge, "$cheat_mode", 1),
                  (display_message, "@{!}DEBUG: Charged player for $g_total_caravan_cost is {reg1}"),
        (try_end),
        (str_store_party_name, s2, "$town_suggested_to_go_to"), 
    ]],         
    

    [anyone|auto_proceed, "start", [
        (eq, "$g_talk_troop", "trp_caravan_master"), 
    ], "{!}NOT SHOWN", "oim_caravan_master_dlg",[]],    
    

    #oim_caravan_master_dlg
    [anyone,"oim_caravan_master_dlg", [], "Yes, let's move out as soon as possible!", "close_window", [
        (jump_to_menu, "mnu_auto_return_to_map"),
    ]], 
#####################################
##TRAINING
# ###
#  [anyone|plyr,"trainer_talk", [
#      (store_current_hours,":cur_hours"),
#       (val_sub, ":cur_hours", 24 * 30),
#       (gt, ":cur_hours", "$train_time"),
#       ],
#     "I want to train myself .", "special_train_start",[]],
   
#     [anyone|plyr,"trainer_talk", [],
#     "I want to train my companion.", "ms_npc_dialog_start",[]],

# [anyone|auto_proceed, "start", 
#     [
#         (eq, "$g_is_npc_dialog", 1),
#     ], 
#     "{!}NOT SHOWN", "ms_npc_dialog_start",[]], 

#  [anyone,"ms_npc_dialog_start", [], "Which of your companions would you like to train?",
#  "ms_npc_list", []], 
#  [anyone|plyr|repeat_for_troops,"ms_npc_list", [
#                                 (store_repeat_object, ":troop_no"),
#                                 (is_between, ":troop_no", companions_begin, companions_end),
#                                 (str_store_troop_name, s0, ":troop_no"),
#                                 (troop_slot_eq, ":troop_no", "slot_troop_occupation", slto_player_companion),
#                                 ], "{s0}", "ms_npc_variants",
#                              [
#                                 (store_repeat_object, "$g_cur_npc"),
#                             ]],
#  [anyone|plyr,"ms_npc_list", [], "I've changed my mind.", "close_window",[ (assign, "$g_is_npc_dialog", 0),]],
 
#  #slot_troop_studing_count
#  #slot_troop_studing_war
#  #slot_troop_studing_medicine
#  #slot_troop_studing_war_work
 
#  [anyone, "ms_npc_variants", [
#     (troop_slot_eq, "$g_cur_npc", "slot_troop_studing_count", 4),
#  ], "We can teach him nothing more!", "ms_npc_dialog_start", []], 
 
#  [anyone, "ms_npc_variants", [], "Very well, pick an art you would like to master.", "ms_nps_variant_descr", []], 
#  [anyone|plyr, "ms_nps_variant_descr", [
#     (neg|troop_slot_eq, "$g_cur_npc", "slot_troop_studing_medicine", 1),
#  ], "Special Training", "ms_nps_variant_selected",[(assign, "$g_cur_npc_branch", ms_flag_medicine),]],
 
#  [anyone|plyr, "ms_nps_variant_descr", [
#     (neg|troop_slot_eq, "$g_cur_npc", "slot_troop_studing_war_work", 1),  
#  ], "Tactics", "ms_nps_variant_selected",[(assign, "$g_cur_npc_branch", ms_flag_war_work),]],
 
#  [anyone|plyr, "ms_nps_variant_descr", [
#     (neg|troop_slot_eq, "$g_cur_npc", "slot_troop_studing_war", 1),   
#  ], "Military training", "ms_nps_variant_selected",[(assign, "$g_cur_npc_branch", ms_flag_war_prepare),]],
 
#  [anyone|plyr, "ms_nps_variant_descr", [
#     (neg|troop_slot_eq, "$g_cur_npc", "slot_troop_studing_attribute", 1), 
#  ], "Attribute and Weapon training", "ms_nps_variant_selected",[(assign, "$g_cur_npc_branch", ms_flag_attribute),]],
 
#  [anyone|plyr,"ms_nps_variant_descr", [], "Return...", "ms_npc_dialog_start",[]],
     
#  [anyone,"ms_nps_variant_selected", [       
#                                         (try_begin),
#                                             (store_character_level, ":npc_level", "$g_cur_npc"),
#                                             (store_mul, "$g_study_price", ":npc_level", 5),
#                                             (val_mul, "$g_study_price", 2000),
#                                             (troop_get_slot, ":count", "$g_cur_npc", "slot_troop_studing_count"), 
#                                             (try_begin),
#                                                 (gt, "$g_study_count", 0),
#                                                 (store_mul, ":koef", "$g_study_count", 5),
#                                                 (val_mul, ":koef", ":koef"),
#                                             (try_end),
#                                             (assign, ":koef", 0),
#                                             (try_begin),
#                                                 (gt, ":count", 0),
#                                                 (store_mul, ":koef", ":count", 5),
#                                                 (val_mul, "$g_study_price", ":koef"),
#                                             (try_end),
#                                             (assign, reg0, "$g_study_price"),
#                                         (try_end),
#                                     ], "The cost of training will be {reg0} scillingas.", "ms_npc_agree_disagree", []],  
    
#     [anyone|plyr,"ms_npc_agree_disagree", [ 
#                                             (try_begin),
#                                                 (store_troop_gold, ":player_gold", "trp_player"),
#                                             (try_end),
#                                             (ge, ":player_gold", "$g_study_price"),
#                                            ], "All right, here's the pay.", "ms_npc_dialog_start", 
#                                                                    [
#                                                                         (call_script, "script_ms_start_npc_study"),
                                                                                                                                                
#                                                                    ]], 
#     [anyone|plyr,"ms_npc_agree_disagree", [],  "Some other time.", "ms_npc_variants",[]],               
    

    
# [anyone|auto_proceed, "start",
#     [
#         (eq, "$g_is_npc_dialog", 1),
#     ], 
#     "{!}NOT SHOWN", "special_train_start",[]], 
#  [anyone|plyr, "special_train_start", [], "I want you to train me.", "special_train", []],
   
#   [anyone,"special_train", [(troop_slot_ge, "trp_player", "slot_troop_renown", 100),], "Of course.", "special_train1",[]],
#   [anyone,"special_train", [], "Sorry, friend, you need 100 renown.", "close_window",[]],

#   [anyone,"special_train1", [], "I can train to increase your attribute points(5 for each)and weapon points(50 for each) for 10000 scillingas.", "special_choose1",[]],

#   [anyone|plyr,"special_choose1", [], "Yes, train me.", "special_window1",[
#       (store_troop_gold,":money","trp_player"),
#       (try_begin),
#         (gt,":money",9999),
#        (troop_remove_gold, "trp_player", 10000),
#                     (troop_raise_proficiency, "trp_player",wpt_one_handed_weapon,50),

#                     (troop_raise_proficiency, "trp_player",wpt_two_handed_weapon,50),
#                     (troop_raise_proficiency, "trp_player",wpt_archery,50),
#                     (troop_raise_proficiency, "trp_player",wpt_throwing,50),
#                     (troop_raise_proficiency, "trp_player",wpt_polearm,50),
#                     (troop_raise_proficiency, "trp_player",wpt_crossbow,50),
#                     (troop_raise_attribute, "trp_player" , ca_strength,5),
#                     (troop_raise_attribute, "trp_player" , ca_agility,5),
#                     (troop_raise_attribute, "trp_player" , ca_intelligence,5),
#                     (troop_raise_attribute, "trp_player" , ca_charisma,5),
                    
#       (else_try),
#         (display_message,"str_money"),
#         (store_current_hours,":cur_hours"),
#         (assign, "$train_time", ":cur_hours"),
#       (try_end),
# ]],
    
#   [anyone|plyr,"special_choose1", [], "Nothing. Thank you.", "close_window",[]],

#   [anyone,"special_window1", [], "Good Luck. Remember my name if you need training. Farewell.", "close_window",[]],
################### 

]
