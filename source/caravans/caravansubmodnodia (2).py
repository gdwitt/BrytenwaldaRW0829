##################trading
	# (store_skill_level, ":leadership_lvl", "skl_leadership", "trp_player"),
 #            (store_skill_level, ":persuasion_lvl", "skl_leadership", "trp_player"),
 #            (val_add, ":leadership_lvl", ":persuasion_lvl"),
 #            #(val_div, ":leadership_lvl",2),
            
 #            (this_or_next|troop_slot_ge, "trp_player", "slot_troop_renown", 30),
 #            (ge, ":leadership_lvl", 3),
  #oim_cravan_delivered
from ..header_operations import *
from ..header_common import *
from  caravandial import *
from ..header_items import *
from ..header_item_modifiers import *
#from ..header_parties import *
from ..header_troops import *
from ..header_skills import *
from ..header_terrain_types import *
from ..header_game_menus import *
from ..header_mission_templates import *
from ..header_music import *
#############not sure about the ones above

from source.module_constants import *
from source.header_operations import *
from source.header_common import *
from source.header_troops import *
from source.header_skills import *
from source.header_parties import *
from source.lazy_flag import LazyFlag
from source.statement import StatementBlock
from source.module_quests import *
from ..module_constants import *

party_templates = [
    ("recruiter", "Recruiter", LazyFlag("icon_gray_knight")|pf_show_faction, 0, "fac_neutral", merchant_personality, [("trp_recruiter", 1, 1)]),
]
menus = [

  (
    "oim_caravan_delivered",0,"All the caravan goods have been sold. After calculating all your expenses, you count a profit of {reg11} scillingas. {s11}",
    "none",
    [
			#code
			(quest_get_slot, ":goods", "qst_oim_deliver_caravan","slot_quest_target_item"), 
			(str_store_item_name, s2, ":goods"),
			(quest_get_slot, ":count", "qst_oim_deliver_caravan","slot_quest_target_amount"),
			(try_begin),
                  (ge, "$cheat_mode", 1),
                  (assign, reg2, ":count"),
                  (display_message, "@{!}DEBUG: count for qst caravan {reg2}"),
              (try_end),
			(quest_get_slot, ":party", "qst_oim_deliver_caravan","slot_quest_target_center"),
			(call_script, "script_oim_get_item_base_price", ":goods"), 
			(assign, ":price", reg0),
			 (try_begin),
                  (ge, "$cheat_mode", 1),
                  (display_message, "@{!}DEBUG: get_item_base_price is {reg0}"),
             (try_end),
			
			(assign, ":base_price", reg0),
			(try_begin), 
			    (ge, ":base_price", 150), 
				(neg|check_quest_active, "qst_oim_trade_pantent"), 
				(neg|quest_slot_eq, "qst_oim_trade_pantent","slot_quest_current_state", 2),
				(quest_set_slot, "qst_oim_trade_pantent","slot_quest_current_state", 1),
				(quest_set_slot, "qst_oim_trade_pantent","slot_quest_giver_troop", "trp_player"),  
				(setup_quest_text, "qst_oim_trade_pantent"),	
				(str_store_string, s2, "str_trade_patent_text"),
				(call_script, "script_start_quest", "qst_oim_trade_pantent", "trp_player"),	
				(assign, "$g_notification_menu_var1", "str_oim_trade_troubles_descr"),
				(assign, "$g_notification_menu_var2", "mnu_oim_caravan_delivered"),
				(jump_to_menu, "mnu_notification_simple_str"),
			(else_try), 			
			  (call_script, "script_oim_game_get_item_buy_price_factor", ":goods", ":party"), 
			  (assign, ":price_factor", reg0),
			  (try_begin),
                  (ge, "$cheat_mode", 1),
                  (display_message, "@{!}DEBUG: game_get_item_buy_price_factor {reg0}"),
              (try_end),
			  (val_mul, ":price", ":price_factor"), 
			  (val_div, ":price", 100),			

			  (val_mul, ":price", ":count"), #count

			  (store_sub, ":profit", ":price", "$g_total_caravan_cost_pure"),
			  (try_begin),
                  (ge, "$cheat_mode", 1),
                  (assign, reg3, ":profit"),
                  (assign, reg4, "$g_total_caravan_cost_pure"),
                  (display_message, "@{!}DEBUG: profit is {reg3}  for g_total_caravan_cost_pure: {reg4}"),
              (try_end),
			  (try_begin),
			    (get_achievement_stat, ":total_profit_till_now", ACHIEVEMENT_TRADER, 0),
				(val_add, ":total_profit_till_now", ":profit"),
				(set_achievement_stat, ACHIEVEMENT_TRADER, 0, ":total_profit_till_now"),
				(try_begin),
				  (ge, ":total_profit_till_now", 100000),
				  (unlock_achievement, ACHIEVEMENT_TRADER),				  
				(try_end),

				(try_begin),
				  (ge, ":total_profit_till_now", 1000000),
				  (unlock_achievement, ACHIEVEMENT_GREAT_TRADER),				  
				(try_end),

				(try_begin),
			      (ge, ":profit", 3000),
				  (unlock_achievement, ACHIEVEMENT_WHEELER_DEALER),				
				(try_end),
			  (try_end),

			  (try_begin), 
			    (ge, ":base_price", 300), #if base price is more than 300 and trade patent is not yet taken, 10% of payment is taken as tax.
				(this_or_next|quest_slot_eq, "qst_oim_trade_pantent","slot_quest_current_state", 0),
				(quest_slot_eq, "qst_oim_trade_pantent","slot_quest_current_state", 1),				
				(assign, ":initial_price", ":price"),
				(val_mul, ":price", 90),
				(val_div, ":price", 100), 				
				(store_sub, reg2, ":initial_price", ":price"),##Why is this value not being used?
				(try_begin),
                  (ge, "$cheat_mode", 1),
                  (display_message, "@{!}DEBUG: tax paid is 10%:{reg2}"),
              	(try_end),
				(str_store_string, s3, "str_percent_10_tax_is_paid"),
				
				(display_message, s3), 
			  (else_try), 
			    (ge, ":base_price", 150), #if base price is more than 200 and trade patent is not yet taken, 5% of payment is taken as tax.
				(this_or_next|quest_slot_eq, "qst_oim_trade_pantent","slot_quest_current_state", 0),
				(quest_slot_eq, "qst_oim_trade_pantent","slot_quest_current_state", 1),				
				(assign, ":initial_price", ":price"),
				(val_mul, ":price", 95),
				(val_div, ":price", 100),				
				(store_sub, reg3, ":initial_price", ":price"),
				(try_begin),
                  (ge, "$cheat_mode", 1),
                  (display_message, "@{!}DEBUG: tax paid is 5%:{reg3}"),
              	(try_end),
				(str_store_string, s3, "str_percent_5_tax_is_paid"),
				(display_message, s3), 
			  (end_try), 
			
			  (call_script, "script_troop_add_gold", "trp_player", ":price"),
			  (assign, reg11, ":price"),##don't touch reg1 This is what you make!!!
			  (str_clear,s11),
			  (str_store_string, s11, "@^String report:a profit of {reg11} scillingas."),
				(try_begin),
                  (ge, "$cheat_mode", 1),
                  (display_message, "@{!}DEBUG: Total earnings:{reg11}"),
              	(try_end),
			  (call_script, "script_oim_change_price_factors", ":party", ":goods", "$oim_count_to_deliver", 1),

			  (assign, "$oim_count_to_deliver", 0),
            (try_end),
	],
    [
		("continue",[],"Continue...",[
			(call_script, "script_end_quest", "qst_oim_deliver_caravan"),
			(quest_set_slot, "qst_oim_deliver_caravan","slot_quest_target_center", -1),  
			(quest_set_slot, "qst_oim_deliver_caravan","slot_quest_target_item", -1),  
			(quest_set_slot, "qst_oim_deliver_caravan","slot_quest_target_amount", -1),  
			(quest_get_slot, ":party_no", "qst_oim_deliver_caravan","slot_quest_target_party"),  
			(try_begin),
			  (party_is_active, ":party_no"),
			  (remove_party, ":party_no"),
            (try_end),
			(quest_set_slot, "qst_oim_deliver_caravan","slot_quest_target_party", -1),  
			(change_screen_return),
			#(jump_to_menu, "mnu_castle_outside"),
		]),
    ],
    ),
	#notification_simple_str
  (
    "notification_simple_str",0,"{s2}",
    "none",
    [
	  (str_store_string, s2, "$g_notification_menu_var1"),
      ],
    [
      ("continue",[],"Continue...",
       [
	    (try_begin), 
			(eq, "$g_notification_menu_var2", "mnu_oim_caravan_delivered"),
			(assign, "$g_notification_menu_var2", -1),
			(jump_to_menu, "mnu_oim_caravan_delivered"),
		(else_try), 
			(change_screen_return),
		(end_try), 
        ]),
     ]
  ),	
]	
scripts = [ ###trade and training
 ("oim_game_get_item_buy_price_factor",
    [
      (store_script_param_1, ":item_kind_id"),
	  (store_script_param_2, ":town_no"),
      (assign, ":price_factor", 100),
	  (assign, ":encountered_party", "$g_encountered_party"),
	  (assign, "$g_encountered_party", ":town_no"),
	  
      (call_script, "script_get_trade_penalty", ":item_kind_id"),
      (assign, ":trade_penalty", reg0),

      (try_begin),
        (is_between, "$g_encountered_party", centers_begin, centers_end),
        (is_between, ":item_kind_id", trade_goods_begin, trade_goods_end),
        (store_sub, ":item_slot_no", ":item_kind_id", trade_goods_begin),
        (val_add, ":item_slot_no","slot_town_trade_good_prices_begin"),
        (party_get_slot, ":price_factor", ":town_no", ":item_slot_no"),
        (val_mul, ":price_factor", 100), #normalize price factor to range 0..100
        (val_div, ":price_factor", average_price_factor),
      (try_end),
      
      (store_add, ":penalty_factor", 100, ":trade_penalty"),
      
      (val_mul, ":price_factor", ":penalty_factor"),
      (val_div, ":price_factor", 100),

	  (assign, "$g_encountered_party", ":encountered_party"),

      (assign, reg0, ":price_factor"),
      #(set_trigger_result, reg0),
  ]),    
  	
	
#############
##oim_get_guild_master
  ("oim_get_guild_master", 
  [
	(store_script_param, ":unused", 1),
	(assign, reg0, "trp_oim_guild_master"),
  ]), 
  
  ("oim_get_item_base_price", 
  [
	(store_script_param, ":item_no", 1), 
	(store_item_value, ":price", ":item_no"),
	#(item_get_slot, ":price", ":item_no","slot_item_base_price),
	(assign, reg0, ":price"),
  ]), 
	
  ("oim_is_trade_good_availible", 
  [
    (store_script_param, ":town_no", 1),  
	(store_script_param, ":trade_good", 2),  
	
	(party_get_slot, ":merchant", ":town_no","slot_town_merchant"), 
	(store_item_kind_count, ":count", ":trade_good", ":merchant"), 
	(assign, reg0, ":count"),
  ]), 		
	
########################
#oim_change_price_factors
	#arg1 :town_no
	#arg2 :item_no
	#arg3 :count
	#arg4 :flag (1 for selling items, 0 for buying)
	("oim_change_price_factors", 
	[
		(store_script_param, ":town_no", 1),
		(store_script_param, ":trade_item_no", 2),
		(store_script_param, ":count", 3),
		(store_script_param, ":flag", 4),

		(try_for_range, ":unused", 0, ":count"),          
          (store_sub, ":item_slot_no", ":trade_item_no", trade_goods_begin),
          (val_add, ":item_slot_no","slot_town_trade_good_prices_begin"),
          (party_get_slot, ":multiplier", ":town_no", ":item_slot_no"),
		  
		  (try_begin),
		    (eq, ":flag", 0),
            (assign, ":multiplier_change", 10), #effect is 40% at big amounts of buying
          (else_try),
		    (assign, ":multiplier_change", 7), #effect is 30% at big amounts of selling
		  (try_end),

		  (store_item_value, ":item_value", ":trade_item_no"),

		  (try_begin),
		    (ge, ":item_value", 100),
		    (store_sub, ":item_value_sub_100", ":item_value", 100),
		    (store_div, ":item_value_sub_100_div_20", ":item_value_sub_100", 20),
		    (val_add, ":multiplier_change", ":item_value_sub_100_div_20"),
		  (try_end),

		  (try_begin),
		    (eq, ":flag", 0),
            (val_add, ":multiplier", ":multiplier_change"), 
          (else_try),
		    (val_sub, ":multiplier", ":multiplier_change"), 
		  (try_end),

		  (val_clamp, ":multiplier", minimum_price_factor, maximum_price_factor),

          (party_set_slot, ":town_no", ":item_slot_no", ":multiplier"),
        (try_end),


		(try_for_range, ":item_no", trade_goods_begin, trade_goods_end),
			(store_sub, ":offset", ":item_no", trade_goods_begin),
			(val_add, ":offset","slot_town_trade_good_prices_begin"),
			(try_begin), 
				(eq, ":trade_item_no", ":item_no"), 
				(try_begin), 
					(eq, ":count", 100),
					(assign, ":shift", -10),
				(else_try), 
					(eq, ":count", 60),
					(assign, ":shift", -7),
				(else_try), 	
					(assign, ":shift", -5),
				(end_try),
				(try_begin), 
					(eq, ":flag", 1), 
					(val_mul, ":shift", -1),
				(end_try), 			
				(call_script, "script_center_change_trade_good_production", ":town_no", ":trade_item_no", ":shift", 0),
			(end_try), 	
		(try_end),
		(call_script, "script_update_trade_good_prices"),		
	]),
	#script_center_change_trade_good_production  ##this has been removed and is being restored just for this submod
 # INPUT:
 #  param1: center_no
 #  param2: item_id
 #  param3: production_rate (should be between -100 (for net consumption) and 100 (for net production)
 #  param4: randomness (between 0-100)
  ("center_change_trade_good_production",
   [
	  (display_message, "@CHANGING"),
     (store_script_param, ":center_no", 1),
     (store_script_param, ":item_no", 2),
     (store_script_param, ":production_rate", 3),
     (store_script_param, ":randomness", 4),
     (store_random_in_range, ":random_num", 0, ":randomness"),
     (store_random_in_range, ":random_sign", 0, 2),
     (try_begin),
       (eq, ":random_sign", 0),
       (val_add, ":production_rate", ":random_num"),
     (else_try),
       (val_sub, ":production_rate", ":random_num"),
     (try_end),
     (val_sub, ":item_no", trade_goods_begin),
     (val_add, ":item_no", slot_town_trade_good_productions_begin),

     (party_get_slot, ":old_production_rate", ":center_no", ":item_no"),
     (val_add, ":production_rate", ":old_production_rate"),
     (party_set_slot, ":center_no", ":item_no", ":production_rate"),
 ]),

########################################	
	
	
# 	("ms_start_npc_study",
#     [	
# 		(remove_member_from_party, "$g_cur_npc", "p_main_party"),		
# 		(troop_remove_gold, "trp_player", "$g_study_price"),
# 		(troop_set_slot, "$g_cur_npc","slot_troop_is_studing", 24*7),
# 		(troop_set_slot, "$g_cur_npc","slot_troop_occupation", slto_at_univesity),
# 		(troop_set_slot, "$g_cur_npc","slot_troop_studing_profile", "$g_cur_npc_branch"),
# 		(troop_get_slot, ":count", "$g_cur_npc","slot_troop_studing_count"), 
# 		(val_add, ":count", 1), 
# 		(troop_set_slot, "$g_cur_npc","slot_troop_studing_count", ":count"), 
# 		(val_add, "$g_study_count", 1),
# 	]),
	
# 	("ms_check_npc_studing",
#     [	
# 		(try_for_range, ":cur_npc", companions_begin, companions_end),
# 			(troop_slot_ge, ":cur_npc","slot_troop_is_studing", 1),
# 			(troop_get_slot, ":wait_time", ":cur_npc","slot_troop_is_studing"),
# 			(try_begin), 
# 				(eq, debug_mode, 1), 
# 				(assign, reg0, ":wait_time"),
# 				(str_store_troop_name, s2, ":cur_npc"), 
# 				(display_log_message, "@ {s2} stud: {reg0}"), 
# 			(try_end), 	
# 			(try_begin),
# 				(eq, ":wait_time", 1),
# 				(try_begin),
# 					(troop_slot_eq, ":cur_npc","slot_troop_studing_profile", ms_flag_medicine),
					
# 					(troop_raise_skill, ":cur_npc",skl_first_aid,2),
# 					(troop_raise_skill, ":cur_npc",skl_surgery ,2),
# 					(troop_raise_skill, ":cur_npc",skl_wound_treatment ,2),
# 					(troop_raise_skill, ":cur_npc", skl_leadership,2 ),
# 					(troop_raise_skill, ":cur_npc",skl_entertain ,2),
# 					(troop_raise_skill, ":cur_npc",skl_persuasion ,2),
				
# 					(troop_set_slot, ":cur_npc","slot_troop_studing_medicine", 1),
# 				(else_try),
# 					(troop_slot_eq, ":cur_npc","slot_troop_studing_profile", "ms_flag_war_work"),
# 					(troop_raise_skill, ":cur_npc",skl_inventory_management,2),
# 					(troop_raise_skill, ":cur_npc",skl_spotting ,2),
# 					(troop_raise_skill, ":cur_npc",skl_pathfinding ,2),
# 					(troop_raise_skill, ":cur_npc",skl_tactics,2), 
# 					(troop_raise_skill, ":cur_npc",skl_tracking ,2),
# 					(troop_raise_skill, ":cur_npc",skl_trainer ,2),
# 					(troop_raise_skill, ":cur_npc",skl_looting ,2),
# 					(troop_raise_skill, ":cur_npc",skl_engineer ,2),
# 					(troop_set_slot, ":cur_npc","slot_troop_studing_war_work", 1),
# 				(else_try)
# 					(troop_slot_eq, ":cur_npc","slot_troop_studing_profile", "ms_flag_war_prepare"),
# 					(troop_raise_skill, ":cur_npc",skl_foraging ,2),
# 					(troop_raise_skill, ":cur_npc",skl_riding ,2),
# 					(troop_raise_skill, ":cur_npc",skl_athletics ,2),
# 					(troop_raise_skill, ":cur_npc",skl_shield ,2),
# 					(troop_raise_skill, ":cur_npc",skl_weapon_master ,2),
# 					(troop_raise_skill, ":cur_npc",skl_power_draw ,2),
# 					(troop_raise_skill, ":cur_npc",skl_power_throw ,2),
# 					(troop_raise_skill, ":cur_npc",skl_power_strike,2), 
# 					(troop_raise_skill, ":cur_npc",skl_ironflesh,2),
# 					(troop_set_slot, ":cur_npc","slot_troop_studing_war", 1),
# 			   (else_try),
# 					(troop_slot_eq, ":cur_npc","slot_troop_studing_profile", ms_flag_attribute),
# 					(troop_raise_proficiency, ":cur_npc",wpt_one_handed_weapon,100),
# 					(troop_raise_proficiency, ":cur_npc",wpt_two_handed_weapon,100),
# 					(troop_raise_proficiency, ":cur_npc",wpt_archery,100),
# 					(troop_raise_proficiency, ":cur_npc",wpt_throwing,100),
# 					(troop_raise_proficiency, ":cur_npc",wpt_polearm,100),
# 					(troop_raise_attribute, ":cur_npc" , ca_strength,5),
# 					(troop_raise_attribute, ":cur_npc" , ca_agility,5),
# 					(troop_raise_attribute, ":cur_npc" , ca_intelligence,5),
# 					(troop_raise_attribute, ":cur_npc" , ca_charisma,5),
# 					(troop_set_slot, ":cur_npc","slot_troop_studing_attribute", 1),
# 				(try_end),
# 				(troop_set_slot, ":cur_npc","slot_troop_occupation", "slto_player_companion"),
# 				(party_force_add_members, "p_main_party", ":cur_npc", 1),
# 				(str_store_troop_name, s2, ":cur_npc"), 
# 				(display_log_message, "str_member_finished_studying"),
# 			(try_end),
# 			(val_sub, ":wait_time", 1),
# 			(troop_set_slot, ":cur_npc","slot_troop_is_studing", ":wait_time"),
# 		(try_end),	
# 	]),	
 ]
##########trading

simple_triggers = [
(0,
 [
		(try_begin), 
		  (check_quest_active,"qst_oim_deliver_caravan"),
		  (quest_get_slot, ":party_no", "qst_oim_deliver_caravan", "slot_quest_target_party"),  
          (gt, ":party_no", 0), 		  

		  (assign, ":party_is_died", 0),
		  (try_begin),
		    (neg|party_is_active, ":party_no"),
			(assign, ":party_is_died", 1),
			(call_script, "script_cancel_quest", "qst_oim_deliver_caravan"),

			(quest_set_slot, "qst_oim_deliver_caravan", "slot_quest_target_center", -1),  
			(quest_set_slot, "qst_oim_deliver_caravan", "slot_quest_target_item", -1),  
			(quest_set_slot, "qst_oim_deliver_caravan", "slot_quest_target_amount", -1),  
			(quest_set_slot, "qst_oim_deliver_caravan", "slot_quest_target_party", -1),  
			(call_script, "script_add_notification_menu", "mnu_notification_simple_str", "str_oim_caravan_looted", -1),
          (try_end),
		  (eq, ":party_is_died", 0),

          (quest_get_slot, ":target_center_no", "qst_oim_deliver_caravan", "slot_quest_target_center"),  
		  (store_distance_to_party_from_party, ":caravan_distance_to_destination", ":target_center_no", ":party_no"),
		  (assign, reg0, ":caravan_distance_to_destination"),
		  (le, ":caravan_distance_to_destination", 1),
		  (gt, "$oim_count_to_deliver", 0),
          (jump_to_menu, "mnu_oim_caravan_delivered"),
		(end_try), 

      (eq,"$g_player_is_captive",1),
      (gt, "$capturer_party", 0),
      (party_is_active, "$capturer_party"),
      (party_relocate_near_party, "p_main_party", "$capturer_party", 0),
    ]),
]
##########trading
# strings = [  go see end of strings
 ####training
triggers = [
 (0, 0, 1, [], [
						(call_script, "script_ms_check_npc_studing"),
					]),	
 ]