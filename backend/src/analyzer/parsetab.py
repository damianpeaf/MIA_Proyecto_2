
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'ARROW COMMAND PARAM VALUEinit : COMMAND parameters \n            | COMMAND\n            | VALUE parameters\n            | VALUEparameters : parameters parameter \n                | parameterparameter : PARAM ARROW VALUE'
    
_lr_action_items = {'COMMAND':([0,],[2,]),'VALUE':([0,9,],[3,10,]),'$end':([1,2,3,4,5,7,8,10,],[0,-2,-4,-1,-6,-3,-5,-7,]),'PARAM':([2,3,4,5,7,8,10,],[6,6,6,-6,6,-5,-7,]),'ARROW':([6,],[9,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'init':([0,],[1,]),'parameters':([2,3,],[4,7,]),'parameter':([2,3,4,7,],[5,5,8,8,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> init","S'",1,None,None,None),
  ('init -> COMMAND parameters','init',2,'p_init','parser.py',15),
  ('init -> COMMAND','init',1,'p_init','parser.py',16),
  ('init -> VALUE parameters','init',2,'p_init','parser.py',17),
  ('init -> VALUE','init',1,'p_init','parser.py',18),
  ('parameters -> parameters parameter','parameters',2,'p_parameters','parser.py',28),
  ('parameters -> parameter','parameters',1,'p_parameters','parser.py',29),
  ('parameter -> PARAM ARROW VALUE','parameter',3,'p_parameter','parser.py',37),
]
