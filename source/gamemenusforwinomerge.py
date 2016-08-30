"Visit the mead hall", #chief sot cambia
       [
           (try_begin),
             (eq,"$all_doors_locked",1),
             (display_message,"str_door_locked",0xFFFFAAAA),
           (else_try),
             (call_script, "script_cf_enter_center_location_bandit_check"),
           (else_try),
             (assign, "$town_entered", 1),
             (set_jump_mission, "mt_town_default"),
             (mission_tpl_entry_set_override_flags, "mt_town_default", 0, af_override_horse),
             (try_begin),
               (eq, "$sneaked_into_town",1),
               (mission_tpl_entry_set_override_flags, "mt_town_default", 0, af_override_all),
             (try_end),
             (party_get_slot, ":cur_scene", "$current_town", slot_town_tavern),
             (jump_to_scene, ":cur_scene"),
             (scene_set_slot, ":cur_scene", slot_scene_visited, 1),

             (assign, "$talk_context", tc_tavern_talk),
             (call_script, "script_initialize_tavern_variables"),

			 (store_random_in_range, ":randomize_attacker_placement", 0, 4),

             (modify_visitors_at_site, ":cur_scene"),
             (reset_visitors),
             
             (assign, ":cur_entry", 17),

			 #this is just a cheat right now
             #(troop_set_slot, "trp_belligerent_drunk", slot_troop_cur_center, "$g_encountered_party"),
			 (try_begin),
				(eq, "$cheat_mode", 1),
				(troop_get_slot, ":drunk_location", "trp_belligerent_drunk", slot_troop_cur_center),
				(try_begin),
					(eq, "$cheat_mode", 0),
				(else_try),
					(is_between, ":drunk_location", centers_begin, centers_end),
					(str_store_party_name, s4, ":drunk_location"),
					(display_message, "str_belligerent_drunk_in_s4"),
			    (else_try),
					(display_message, "str_belligerent_drunk_not_found"),
				(try_end),
				
				(troop_get_slot, ":promoter_location", "trp_fight_promoter", slot_troop_cur_center),
				(try_begin),
					(eq, "$cheat_mode", 0),
				(else_try),
					(is_between, ":promoter_location", centers_begin, centers_end),
					(str_store_party_name, s4, ":promoter_location"),
					(display_message, "str_roughlooking_character_in_s4"),
			    (else_try),
					(display_message, "str_roughlooking_character_not_found"),
				(try_end),				
			 (try_end),
			 
			 #this determines whether or not a lord who dislikes you will commission an assassin
			 (try_begin),
				(store_current_hours, ":hours"),
				(store_sub, ":hours_since_last_attempt", ":hours", "$g_last_assassination_attempt_time"),
				(gt, ":hours_since_last_attempt", 168),
				(try_for_range, ":lord", active_npcs_begin, active_npcs_end),
					(troop_slot_eq, ":lord", slot_lord_reputation_type, lrep_debauched),
					(troop_get_slot, ":led_party", ":lord", slot_troop_leaded_party),
					(party_is_active, ":led_party"),
					(party_get_attached_to, ":led_party_attached", ":led_party"), 
					(eq, ":led_party_attached", "$g_encountered_party"),
					(call_script, "script_troop_get_relation_with_troop", "trp_player", ":lord"),
					(lt, reg0, -20),
					(assign, "$g_last_assassination_attempt_time", ":hours"),
#					(assign, "$g_last_assassination_attempt_location", "$g_encountered_party"),
#					(assign, "$g_last_assassination_attempt_perpetrator", ":lord"),
					
					(troop_set_slot, "trp_hired_assassin", slot_troop_cur_center, "$g_encountered_party"),					
				(try_end),
			 (try_end),	
						
			 (try_begin),
				 (eq, ":randomize_attacker_placement", 0),
				 (call_script, "script_setup_tavern_attacker", ":cur_entry"),

				 (val_add, ":cur_entry", 1),
			 (try_end),
			 
			 (try_begin),
				(eq, 1, 0),
				(troop_slot_eq, "trp_fight_promoter", slot_troop_cur_center, "$current_town"),
                (set_visitor, ":cur_entry", "trp_fight_promoter"),

                (val_add, ":cur_entry", 1),
			 (try_end),
			 
             (party_get_slot, ":mercenary_troop", "$current_town", slot_center_mercenary_troop_type),
             (party_get_slot, ":mercenary_amount", "$current_town", slot_center_mercenary_troop_amount),
             (try_begin),
			   (gt, ":mercenary_troop", 0),
               (gt, ":mercenary_amount", 0),
               (set_visitor, ":cur_entry", ":mercenary_troop"),
               (val_add, ":cur_entry", 1),
             (try_end),

			 (try_begin),
				 (eq, ":randomize_attacker_placement", 1),
				 (call_script, "script_setup_tavern_attacker", ":cur_entry"),

				 (val_add, ":cur_entry", 1),
			 (try_end),
             
             (try_for_range, ":companion_candidate", companions_begin, companions_end),
               (troop_slot_eq, ":companion_candidate", slot_troop_occupation, 0),
               (troop_slot_eq, ":companion_candidate", slot_troop_cur_center, "$current_town"),
			   (neg|troop_slot_ge, ":companion_candidate", slot_troop_prisoner_of_party, centers_begin),
			   
               (set_visitor, ":cur_entry", ":companion_candidate"),

               (val_add, ":cur_entry", 1),
             (try_end),
			 
			 (try_begin),
				 (eq, ":randomize_attacker_placement", 2),
				 (call_script, "script_setup_tavern_attacker", ":cur_entry"),

				 (val_add, ":cur_entry", 1),
			 (try_end),
			 			 
             (try_begin), #this doubles the incidence of ransom brokers and (below) minstrels
               (party_get_slot, ":ransom_broker", "$current_town", slot_center_ransom_broker),
               (gt, ":ransom_broker", 0),
               
               (assign, reg0, ":ransom_broker"),
               (assign, reg1, "$current_town"),
			   
               (set_visitor, ":cur_entry", ":ransom_broker"),
               (val_add, ":cur_entry", 1),
			 (else_try),
			   (is_between, "$g_talk_troop", ransom_brokers_begin, ransom_brokers_end),
			   (store_add, ":alternative_town", "$current_town", 9),
			   
			   (try_begin),
				(ge, ":alternative_town", towns_end),
				(val_sub, ":alternative_town", 22),
			   (try_end),
			   (try_begin),
				(eq, "$cheat_mode", 1),
			    (str_store_party_name, s3, "$current_town"),
			    (str_store_party_name, s4, ":alternative_town"),
			    (display_message, "@{!}DEBUG - Current town is {s3}, but also checking {s4}"),
			   (try_end),	
			   
               (party_get_slot, ":ransom_broker", ":alternative_town", slot_center_ransom_broker),
               (gt, ":ransom_broker", 0),
			   
               (set_visitor, ":cur_entry", ":ransom_broker"),
               (val_add, ":cur_entry", 1),
             (try_end),
			 
             (try_begin),
               (party_get_slot, ":tavern_traveler", "$current_town", slot_center_tavern_traveler),
               (gt, ":tavern_traveler", 0),
               (set_visitor, ":cur_entry", ":tavern_traveler"),
               (val_add, ":cur_entry", 1),
             (try_end),
			 
             (try_begin),
               (party_get_slot, ":tavern_minstrel", "$current_town", slot_center_tavern_minstrel),
               (gt, ":tavern_minstrel", 0),
			   
               (set_visitor, ":cur_entry", ":tavern_minstrel"),
               (val_add, ":cur_entry", 1),
			 (else_try),  
			   (store_add, ":alternative_town", "$current_town", 9),
			   (try_begin),
				(ge, ":alternative_town", towns_end),
				(val_sub, ":alternative_town", 22),
			   (try_end),
 			   ##diplomacy start+ chief
			   #The above code makes assumptions about the number of towns that might not be true on other maps.
			   #Changing it to support variable sizes would not be hard, but I'm not convinced that it is so
			   #desirable in the first place.
			   (is_between, ":alternative_town", centers_begin, centers_end),
			   (party_slot_eq, ":alternative_town", slot_party_type, spt_town),
			   ##diplomacy end+
              (party_get_slot, ":tavern_minstrel", ":alternative_town", slot_center_tavern_minstrel),			   
               (gt, ":tavern_minstrel", 0),
			   
               (set_visitor, ":cur_entry", ":tavern_minstrel"),
               (val_add, ":cur_entry", 1),
             (try_end),

## CC gambling begin chief
             (try_begin),
               (party_get_slot, ":prosperity", "$current_town", slot_town_prosperity),
               (val_mod, ":prosperity", 24),
               (store_time_of_day, ":cur_hour"),
               (store_sub, ":difference", ":prosperity", ":cur_hour"),
               (is_between, ":difference", -1, 2), # -1 0 1, 1/8 probability
               (set_visitor, ":cur_entry", "trp_especial_merchant"),
               (troop_set_name, "trp_especial_merchant", "@Mystic Merchant"),
               (call_script, "script_refresh_mystic_merchant_items", "trp_especial_merchant"),
               (val_add, ":cur_entry", 1),
             (try_end),
## CC gambling end
			 
             (try_begin),
               (party_get_slot, ":tavern_bookseller", "$current_town", slot_center_tavern_bookseller),
               (gt, ":tavern_bookseller", 0),
               (set_visitor, ":cur_entry", ":tavern_bookseller"),
               (val_add, ":cur_entry", 1),
             (try_end),
			 
			 (try_begin),
				 (eq, ":randomize_attacker_placement", 3),
				 (call_script, "script_setup_tavern_attacker", ":cur_entry"),
				 (val_add, ":cur_entry", 1),
			 (try_end),
			 			 
             (try_begin),
               (neg|check_quest_active, "qst_eliminate_bandits_infesting_village"),
               (neg|check_quest_active, "qst_deal_with_bandits_at_lords_village"),
               (assign, ":end_cond", villages_end),
               (try_for_range, ":cur_village", villages_begin, ":end_cond"),
                 (party_slot_eq, ":cur_village", slot_village_bound_center, "$current_town"),
                 (party_slot_ge, ":cur_village", slot_village_infested_by_bandits, 1),
                 (neg|party_slot_eq, ":cur_village", slot_town_lord, "trp_player"),
                 (set_visitor, ":cur_entry", "trp_farmer_from_bandit_village"),
                 (val_add, ":cur_entry", 1),
                 (assign, ":end_cond", 0),
               (try_end),
             (try_end),
             
             (try_begin),
               (eq, "$g_starting_town", "$current_town"),
                              
               (this_or_next|neg|check_quest_finished, "qst_collect_men"),
               (this_or_next|neg|check_quest_finished, "qst_learn_where_merchant_brother_is"),
               (this_or_next|neg|check_quest_finished, "qst_save_relative_of_merchant"),
               (this_or_next|neg|check_quest_finished, "qst_save_town_from_bandits"),
               (eq,  "$g_do_one_more_meeting_with_merchant", 1),
               
			   (assign, ":troop_of_merchant", 0),	
#chief mercaderes
               (try_begin),
                 (eq, "$g_encountered_party_faction", "fac_kingdom_18"),
                 (assign, ":troop_of_merchant", "trp_briton_merchant"),
               (else_try),  
                 (eq, "$g_encountered_party_faction", "fac_kingdom_4"),
                 (assign, ":troop_of_merchant", "trp_saxon_merchant"),
               (else_try),                   
                 (eq, "$g_encountered_party_faction", "fac_kingdom_1"),
                 (assign, ":troop_of_merchant", "trp_pict_merchant"),
               (else_try),  
                 (eq, "$g_encountered_party_faction", "fac_kingdom_23"),
                 (assign, ":troop_of_merchant", "trp_engle_merchant"),
               (else_try),  
                 (eq, "$g_encountered_party_faction", "fac_kingdom_31"),
                 (assign, ":troop_of_merchant", "trp_irish_merchant"),
               (else_try),  
                 (eq, "$g_encountered_party_faction", "fac_kingdom_28"),
                 (assign, ":troop_of_merchant", "trp_centware_merchant"),
               (try_end),
			   (gt, ":troop_of_merchant", 0),	
#chief mercaderes acaba               
               (set_visitor, ":cur_entry", ":troop_of_merchant"),
               (val_add, ":cur_entry", 1),
             (try_end),                         
             
             (change_screen_mission),
           (try_end),
        ],"Door to the tavern."),
                               