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

divisionSelected = ":sblunt_division%d_selected"
inventorySlot = "slot_agent_sblunt_invslot_%d"

def setDivisionSelectedClear() :
  block = []
  for division in range(9): block += [(assign, divisionSelected % division, 0),]
  return StatementBlock(*block)

def setDivisionSelected() :
  block = []
  for division in range(9):
    block += [
      (try_begin),
        (eq, ":division_no", division),
        (assign, divisionSelected % division, 1),
      (try_end),
    ]
  return StatementBlock(*block)

def memorizeInventory() :
  block = []
  for slot in range(4):
    block += [
      (try_begin),
        (eq, ":item_slot", slot),
        (agent_get_slot, ":item_stored", ":agent_no", inventorySlot % slot),
        (ge, ":item_stored", 0),
        (agent_set_slot, ":agent_no", inventorySlot % slot, ":item_id"),
      (try_end),
    ]
  return StatementBlock(*block)

def resetInventory() :
  block = []
  for slot in range(4):
    block += [(agent_set_slot, ":agent_no", inventorySlot % slot, 0),]
  return StatementBlock(*block)

def updateInventory() :
  block = []
  for slot in range(4):
    block += [
      (try_begin),
        (eq, ":item_slot", slot),
        (agent_get_slot, ":item_id", ":agent_no", inventorySlot % slot),
        (gt, ":item_id", 0),
        (try_begin),
          (eq, ":inventory_action", 1), #Restore
          (agent_equip_item, ":agent_no", ":item_id", ":item_slot"),
        (else_try),
          (eq, ":inventory_action", -1), #Clear
          (agent_unequip_item, ":agent_no", ":item_id", ":item_slot"),
        (try_end),
      (try_end),
    ]
  return StatementBlock(*block)

#For debug only
def updateInventoryDebug() :
  block = []
  for slot in range(4):
    block += [
      (try_begin),
        (eq, ":item_slot", slot),
        (agent_get_slot, ":item_id", ":agent_no", inventorySlot % slot),
        (gt, ":item_id", 0),
        (try_begin),
          (eq, ":inventory_action", 1), #Restore
          (agent_equip_item, ":agent_no", ":item_id", ":item_slot"),
          (str_store_item_name, s1, ":item_id"),
          (display_message, "@[DEBUG] {s0} eqipped {s1}"),
        (else_try),
          (eq, ":inventory_action", -1), #Clear
          (agent_unequip_item, ":agent_no", ":item_id", ":item_slot"),
          (str_store_item_name, s1, ":item_id"),
          (display_message, "@[DEBUG] {s0} uneqipped {s1}"),
        (try_end),
      (try_end),
    ]
  return StatementBlock(*block)

def setWeaponOrderAny() :
  block = []
  for division in range(9):
    block += [
      (try_begin),
        (eq, divisionSelected % division, 1),
        (team_give_order, ":team_id", division, mordr_use_any_weapon),
      (try_end),
    ]
  return StatementBlock(*block)

#Sladki
#Reworked trigger
#Toggling weapons with alternative "blunt" version and back to "default" on respective orders
common_ai_order_toggle = (ti_on_order_issued, 0, 0, [
  (store_trigger_param_1, ":order_no"),
  (this_or_next|eq, ":order_no", mordr_use_blunt_weapons),
  (eq, ":order_no", mordr_use_any_weapon),],

  [
  (store_trigger_param_1, ":order_no"),
  (store_trigger_param_2, ":agent_id"), #Leader
  (agent_get_team, ":team_id", ":agent_id"),

  #Workaround shit to make sure that only divisions who is selected and have troops will be ordered
  setDivisionSelectedClear(),

  (try_for_agents, ":agent_no"),
    (agent_is_active, ":agent_no"),
    (agent_is_human, ":agent_no"),
    (agent_is_non_player, ":agent_no"),
    (agent_is_alive, ":agent_no"),
    (agent_get_team, ":team_no", ":agent_no"),
    (eq, ":team_no", ":team_id"),
    (agent_get_division, ":division_no", ":agent_no"),
    (class_is_listening_order, ":team_id", ":division_no"), #"class" is "division"

    #Mark the troop division as selected
    setDivisionSelected(),

    #Reassign vars
    (assign, ":inventory_action", 0),

    #Search for weapons with alternative mode
    (try_for_range, ":item_slot", ek_item_0, ek_head),
      (agent_get_item_slot, ":item_id", ":agent_no", ":item_slot"),
      (gt, ":item_id", 0),
      (item_get_type, ":item_type", ":item_id"),
      (is_between, ":item_type", itp_type_one_handed_wpn, itp_type_arrows),

      #Memorize current inventory slot to the custom agent inventory slots
      (try_begin),
        (eq, ":order_no", mordr_use_blunt_weapons),
        memorizeInventory(),
      (try_end),

      (try_begin),
        (item_get_slot, ":alternative_weapon", ":item_id", "slot_item_alternate"),
        (gt, ":alternative_weapon", 0),
        (item_get_swing_damage_type, ":damage_type_alt", ":alternative_weapon"),
        (item_get_swing_damage_type, ":damage_type", ":item_id"),

        #Swap weapons
        #Order "Any": blunt to any, order "Blunt": not blunt to blunt (fix stuffs and spears)
        (try_begin),
          (this_or_next|eq, ":order_no", mordr_use_any_weapon),
          (eq, ":damage_type_alt", blunt),
          (this_or_next|eq, ":order_no", mordr_use_any_weapon),
          (neq, ":damage_type", blunt),
          (this_or_next|eq, ":order_no", mordr_use_blunt_weapons),
          (neq, ":damage_type_alt", blunt),
          (this_or_next|eq, ":order_no", mordr_use_blunt_weapons),
          (eq, ":damage_type", blunt),

          #Swap
          (agent_unequip_item, ":agent_no", ":item_id", ":item_slot"),
          (agent_equip_item, ":agent_no", ":alternative_weapon", ":item_slot"),
          (agent_set_wielded_item, ":agent_no", ":alternative_weapon"),

          #Debuging shit
          (try_begin),
            (ge, "$cheat_mode", 1),
            (str_store_agent_name, s0, ":agent_no"),
            (str_store_item_name, s1, ":item_id"),
            (str_store_item_name, s2, ":alternative_weapon"),
            (assign, reg1, ":damage_type"),
            (assign, reg2, ":damage_type_alt"),
            (display_message, "@[DEBUG] {s0} swapped {s1}({reg1}) with {s2}(dmg type:{reg2})"),
          (try_end),

          #Agent has suitable blunt weapon
          #Mark to restore/clear inventory (1, -1), respective agent item slot will be set to -1 to prevent overwriting
          (try_begin),
            (eq, ":order_no", mordr_use_any_weapon),
            (assign, ":inventory_action", 1),
          (else_try),
            (eq, ":order_no", mordr_use_blunt_weapons),
            (assign, ":inventory_action", -1),
            (assign, ":item_id", -1), #Slot will not be overwritten
            memorizeInventory(),
          (try_end),

        (try_end),
      (try_end),
    (try_end),

    #Change inventory
    (try_begin),
      (neq, ":inventory_action", 0),
      (try_for_range, ":item_slot", ek_item_0, ek_head),
        updateInventory(),
      (try_end),
      (eq, ":inventory_action", 1),
      resetInventory(),
    (try_end),

  (try_end),

  #For those who has no blunt weapons and tries to crush skulls with their own fists (make them use any weapon)
  #"Use blunt weapon IF YOU CAN (have to)" instead of "Use blunt even if you have no better option than fists"
  (try_begin),
    (eq, ":order_no", mordr_use_blunt_weapons),
    setWeaponOrderAny(),
  (try_end),

  ]
)

common_wpn_swapping = [common_ai_order_toggle]