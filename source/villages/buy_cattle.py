from source.header_operations import *
from source.header_common import *


menus = [

    ("buy_cattle", 0, "I want to buy some cattle.", "none", [
        (party_slot_eq, "$current_town", "slot_village_state", 0),
        (neg|party_slot_ge, "$current_town", "slot_village_infested_by_bandits", 1),

        # don't allow buying cattle when cattle quest is active.
        (assign, ":quest_village", 0),
        (try_begin),
            (check_quest_active, "qst_deliver_cattle"),
            (quest_slot_eq, "qst_deliver_cattle", "slot_quest_target_center", "$current_town"),
            (assign, ":quest_village", 1),
        (try_end),
        (eq, ":quest_village", 0),
        ], [
            ("continue", [], "Continue",
                [(jump_to_menu, "mnu_buy_cattle2")
        ]),
    ]),

    ("buy_cattle2", 0,
     "There are {reg7} heads of cattle, each for {reg6} scillingas. How many do "
     "you want to buy?", "none", [
        (set_background_mesh, "mesh_pic_cattle"),

        (party_get_slot, reg5, "$g_encountered_party", "slot_village_number_of_cattle"),
        (party_get_slot, reg7, "$g_encountered_party", "slot_center_head_cattle"),
       (display_message, "@{!}DEBUG cattle in village menu at number {reg5} & headcattle at {reg7}"),
        (gt, reg7, 0),
        (store_item_value, ":cattle_cost", "itm_cattle_meat"),
        (val_add, ":cattle_cost", "itm_cattle_meat"),##gdw new to make cows more rep of slaughter value
        (val_add, ":cattle_cost", "itm_raw_leather"),
        (val_add, ":cattle_cost", "itm_raw_leather"),
        (call_script, "script_game_get_item_buy_price_factor", "itm_cattle_meat"),
        (val_mul, ":cattle_cost", reg0),
        (val_div, ":cattle_cost", 50),  # Multiplied by 2 and divided by 100
        (assign, "$temp", ":cattle_cost"),
        (assign, reg6, ":cattle_cost"),
     ], [

        ("cattle_ok", [
            #(party_get_slot, ":num_cattle",  "$g_encountered_party", "slot_village_number_of_cattle"),
            (party_get_slot, reg6, "$g_encountered_party", "slot_center_head_cattle"),
            (ge, reg6, 1),
            #(assign, reg6, ":num_cattle"),
            (display_message, "@{!}DEBUG cattle prepurchase no. is {reg6}"),
            (store_troop_gold, ":gold", "trp_player"),
            (ge, ":gold", "$temp"),
          
        ], "One.", [
            (call_script, "script_buy_cattle_from_village", "$g_encountered_party", 1, "$temp"),
        ]),

        ("cattle_ok2", [
            # (party_get_slot, ":num_cattle", "$g_encountered_party", "slot_village_number_of_cattle"),
            # (ge, ":num_cattle", 5),
             (party_get_slot, reg7, "$g_encountered_party", "slot_center_head_cattle"),
            (ge, reg7, 5),
            (store_troop_gold, ":gold", "trp_player"),
            (store_mul, ":cost", "$temp", 5),
            (ge, ":gold", ":cost"),
        ], "Five", [
            (call_script, "script_buy_cattle_from_village", "$g_encountered_party", 5, "$temp"),
            (display_message, "@{!}DEBUG cattle big purchase no. is {reg7}"),
        ]),

        ("cattle_ok3", [], "Forget it.", [
            (jump_to_menu,"mnu_village")
        ]),
    ]),
]
