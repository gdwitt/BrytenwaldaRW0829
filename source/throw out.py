(team_give_order, 1, grc_everyone, mordr_stand_ground),(team_give_order, 0, grc_everyone, mordr_stand_ground),

##Trophies calculation: (50% base chance + loot skill * 4) for every 10 enemies
(store_party_size_wo_prisoners, ":enemies_count", ":enemy_party"),
(val_div, ":enemies_count", 10),
(party_get_skill_level, ":player_party_looting", "p_main_party", "skl_looting"),
(val_mul, "player_party_looting", 4),
(assign, ":trophy_chance", 50),
(val_add, ":trophy_chance", ":player_party_looting"),
(try_for_range, ":i_try", 0, ":enemies_count"),
  (store_random_in_range, ":roll", 0, 100),
  (try_begin),
    (gt, ":trophy_chance", ":roll"),
    (val_add, ":num_looted_items", 1),
    (troop_add_item, "trp_temp_troop", "trophy_a"),
  (try_end),
(try_end),
##End trophies calculation


("restore_wagon_troops",
   [   
   
      (party_get_num_companion_stacks, ":num_stacks","p_temp_loot_wagon"),
      (try_for_range, ":stack_no", 0, ":num_stacks"),
         (party_stack_get_troop_id, ":stack_troop","p_temp_loot_wagon",0),
         (party_stack_get_size, ":stack_size","p_temp_loot_wagon",0),
         (party_remove_members,"p_temp_loot_wagon",":stack_troop",":stack_size"),
         (party_add_members, "p_main_party", ":stack_troop", ":stack_size"),         
      (try_end),
      (party_get_num_prisoner_stacks, ":num_stacks","p_temp_loot_wagon"),
      (try_begin),
         (gt,":num_stacks",0),
         (try_for_range, ":stack_no", 0, ":num_stacks"),
            (party_prisoner_stack_get_troop_id, ":stack_troop","p_temp_loot_wagon",0),
            (party_prisoner_stack_get_size, ":stack_size","p_temp_loot_wagon",0),         
            (party_remove_prisoners,"p_temp_loot_wagon",":stack_troop",":stack_size"),
            (party_add_prisoners, "p_main_party", ":stack_troop", ":stack_size"),
         (try_end),
      (try_end),
      (display_message,"@                Supply wagon troops have been reassigned to the main party."),

    ]),