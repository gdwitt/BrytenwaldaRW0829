from source.header_operations import *
from source.header_common import *
from source.header_triggers import ti_on_order_issued, ti_on_item_wielded, \
    gk_toggle_weapon_mode
from source.header_items import itp_type_one_handed_wpn, itp_type_arrows, \
    ek_item_0, ek_head
from source.header_mission_templates import mordr_use_any_weapon, \
    mordr_use_blunt_weapons, mordr_stand_ground
from source.header_items import *
from source.module_constants import *
 
from source.statement import StatementBlock
 
 
inventorySlot = "slot_agent_sblunt_invslot_%d"
 
 
def setWeaponOrderAny() :
  block = [(set_show_messages, 0),]
  for division in range(9):
    block += [
      (try_begin),
        (class_is_listening_order, ":team_id", division),
        (team_give_order, ":team_id", division, mordr_use_any_weapon),
      (try_end),
    ]
  block += [(set_show_messages, 1),]
  return StatementBlock(*block)
 
def isBlunt(itemId) :
  block = [
    (item_get_swing_damage_type, ":damage_type_swing", itemId),
    (item_get_thrust_damage_type, ":damage_type_thrust", itemId),
    (item_get_thrust_damage, ":damage_thrust", itemId),
 
    (str_store_item_name, s0, itemId),
    (assign, reg0, ":damage_type_swing"),
    (assign, reg1, ":damage_thrust"),
    (assign, reg2, ":damage_type_thrust"),
 
    (this_or_next|eq, ":damage_type_thrust", blunt),
    (eq, ":damage_thrust", 0), ##this will include all the axes and picks even if the swing damage is pierces. 
    (eq, ":damage_type_swing", blunt),  ##the traditional check was (item_slot_ge, ":item_no", 'slot_item_swing_damage', 525),
 
    (display_message, "@[DEBUG] {s0} is blunt"),
  ]
  return StatementBlock(*block)
 
def memorizeInventorySlot(slot, itemId) :
  block = []
  for slot_i in range(4):
    block += [
      (try_begin),
        (eq, slot, slot_i),
        (agent_set_slot, ":agent_no", inventorySlot % slot_i, itemId),
      (try_end),
    ]
  return StatementBlock(*block)
 
def resetMemorizedInventory() :
  block = []
  for slot in range(4):
    block += [(agent_set_slot, ":agent_no", inventorySlot % slot, 0),]
  return StatementBlock(*block)
 
def processInventory(inventoryAction) :
  block = []
 
  for slot in range(4):
    if inventoryAction == 1:
      block += [
        (try_begin),
          (agent_get_slot, ":item_id", ":agent_no", inventorySlot % slot),
          (gt, ":item_id", 0),
          (agent_equip_item, ":agent_no", ":item_id", slot),
        (try_end),
      ]
    elif inventoryAction == -1:
      block += [
        (try_begin),
          (agent_get_slot, ":item_id", ":agent_no", inventorySlot % slot),
          (gt, ":item_id", 0),
          (agent_unequip_item, ":agent_no", ":item_id", slot),
        (try_end),
      ]
  return StatementBlock(*block)
 
#For debug only
def processInventoryDebug(inventoryAction) :
  block = []
 
  for slot in range(4):
    if inventoryAction == 1:
      block += [
        (try_begin),
          (agent_get_slot, ":item_id", ":agent_no", inventorySlot % slot),
          (gt, ":item_id", 0),
          (agent_equip_item, ":agent_no", ":item_id", slot),
          (str_store_agent_name, s0, ":agent_no"),
          (str_store_item_name, s1, ":item_id"),
          (display_message, "@[DEBUG] {s0} has equipped {s1}"),
        (try_end),
      ]
    elif inventoryAction == -1:
      block += [
        (try_begin),
          (agent_get_slot, ":item_id", ":agent_no", inventorySlot % slot),
          (gt, ":item_id", 0),
          (agent_unequip_item, ":agent_no", ":item_id", slot),
          (str_store_agent_name, s0, ":agent_no"),
          (str_store_item_name, s1, ":item_id"),
          (display_message, "@[DEBUG] {s0} has unequipped {s1}"),
        (try_end),
      ]
  return StatementBlock(*block)
 
 
#Sladki
#Reworked trigger
#Swap weapons with alternative "blunt" versions and back to "default" on respective orders
common_ai_order_toggle = (ti_on_order_issued, 0, 0, [
  (store_trigger_param_1, ":order_no"),
  (this_or_next|eq, ":order_no", mordr_use_blunt_weapons),
  (eq, ":order_no", mordr_use_any_weapon),],
 
  [
  (store_trigger_param_1, ":order_no"),
  (store_trigger_param_2, ":agent_id"), #Leader
  (agent_get_team, ":team_id", ":agent_id"),
 
  #Process each agent
  (try_for_agents, ":agent_no"),
    (agent_is_active, ":agent_no"),
    (agent_is_human, ":agent_no"),
    (agent_is_non_player, ":agent_no"),
    (agent_is_alive, ":agent_no"),
    (agent_get_team, ":team_no", ":agent_no"),
    (eq, ":team_no", ":team_id"),
    (agent_get_division, ":division_no", ":agent_no"),
    (class_is_listening_order, ":team_id", ":division_no"), #"class" is "division"
 
    #Reassign vars
    (assign, ":blunt_weapons_num", 0),
    (assign, ":total_weapons_num", 0),
 
    #Search for weapons with alternative mode
    (try_for_range, ":item_slot", ek_item_0, ek_head),
      (agent_get_item_slot, ":item_id", ":agent_no", ":item_slot"),
      (gt, ":item_id", 0),
      (item_get_type, ":item_type", ":item_id"),
      (is_between, ":item_type", itp_type_one_handed_wpn, itp_type_arrows),
      (assign, ":is_current_blunt", 0),
      (assign, ":should_be_swapped", 0),
      (val_add, ":total_weapons_num", 1),
 
      #Check is it blunt
      (try_begin),
        isBlunt(":item_id"),
        (val_add, ":blunt_weapons_num", 1),
        (assign, ":is_current_blunt", 1), #Slot containment will not be memorized or restored
      (try_end),
 
      #Try to swap
      (try_begin),
        (item_get_slot, ":alternate_id", ":item_id", "slot_item_alternate"),
        (gt, ":alternate_id", 0),
 
        #Check is it a blunt and should it be swapped
        (try_begin),
          (eq, ":order_no", mordr_use_blunt_weapons),
          isBlunt(":alternate_id"),
          (assign, ":should_be_swapped", 1),
          (try_begin),
            (eq, ":is_current_blunt", 0),
            (val_add, ":blunt_weapons_num", 1),
          (try_end),
        (else_try),
          (eq, ":order_no", mordr_use_any_weapon),
          (eq, ":is_current_blunt", 1),
          (assign, ":should_be_swapped", 1),
        (try_end),
 
        #Swap
        (try_begin),
          (gt, ":should_be_swapped", 0),
          (agent_unequip_item, ":agent_no", ":item_id", ":item_slot"),
          (agent_equip_item, ":agent_no", ":alternate_id", ":item_slot"),
          (agent_set_wielded_item, ":agent_no", ":alternate_id"),
 
          #Debuging shit
          (try_begin),
            (gt, "$cheat_mode", 0),
            (str_store_agent_name, s0, ":agent_no"),
            (str_store_item_name, s1, ":item_id"),
            (str_store_item_name, s2, ":alternate_id"),
            (display_message, "@[DEBUG] {s0} swapped {s1} with {s2}"),
          (try_end),
 
          (assign, ":is_current_blunt", 1), #Slot containment will not be memorized or restored
        (try_end),
      (try_end),
 
      #Memorize slot
      (try_begin),
        (eq, ":order_no", mordr_use_blunt_weapons),
        (neq, ":is_current_blunt", 1),
        memorizeInventorySlot(":item_slot", ":item_id"),
      (try_end),
 
    (try_end),
 
    #"Use any" order - try to restore if there are only blunt weapons are presented in inventory
    (try_begin),
      (eq, ":order_no", mordr_use_any_weapon),
      (eq, ":blunt_weapons_num", ":total_weapons_num"),
          processInventoryDebug(1),
      resetMemorizedInventory(),
    (try_end),
 
    #"Use blunt" order - get rid of lethal weapons if there is at least one of each blunt and lethal weapons in inventory
    (try_begin),
      (eq, ":order_no", mordr_use_blunt_weapons),
 
      (try_begin),
        (gt, "$cheat_mode", 0),
        (str_store_agent_name, s0, ":agent_no"),
        (assign, reg0, ":blunt_weapons_num"),
        (assign, reg1, ":total_weapons_num"),
        (display_message, "@[DEBUG] {s0} has {reg0}/{reg1} blunts"),
      (try_end),
 
      (gt, ":blunt_weapons_num", 0),
      (neq, ":blunt_weapons_num", ":total_weapons_num"),
      processInventoryDebug(-1),
    (try_end),
 
    (display_message, "@[DEBUG]=========================================="),
 
  (try_end),
 
  #For those who has no blunt weapons and tries to crush skulls with their own fists (make them use any weapon)
  #"Use blunt weapon IF YOU CAN (have to)" instead of "Use blunt even if you have no better option than fists"
  (try_begin),
    (eq, ":order_no", mordr_use_blunt_weapons),
    setWeaponOrderAny(),
    (call_script, "script_equip_best_melee_weapon", ":agent_no", 0, 1, 1),
  (try_end),
 ])
###########################from VC
common_ai_order_toggle = [common_ai_order_toggle]
#common_wpn_swapping = [common_ai_order_toggle]
#from equip best need to mke array of blunts then go through it
# (try_for_range, ":item_slot", ek_item_0, ek_head),
#                   (agent_get_item_slot, ":item", ":agent", ":item_slot"),
#                   (gt, ":item", "itm_no_item"),
#                   (item_get_type, ":weapon_type", ":item"),
#                   (eq, ":weapon_type", itp_type_one_handed_wpn),
#                   (item_get_swing_damage, ":swing", ":item"),
#                   (item_get_swing_damage, ":thrust", ":item"),
#                   (val_mul, ":thrust",3),
#                   (val_div, ":thrust",5),
#                   (store_add, ":combdamage",":thrust",":swing"),
#                   (lt, ":cur_score", ":combdamage"),
#                   (assign, ":cur_score", ":combdamage"),
#                   #(gt, ":swing", 19),
#                   (assign, ":weapon", ":item"),
#                 (try_end),