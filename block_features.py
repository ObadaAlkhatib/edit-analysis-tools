import aiatools as aia
from aiatools.block_types import *
from aiatools.component_types import *

block_features = ['Ball.SetVisible', 'and', 'or', 'equal', 'Ball.CollidedWith', 'Button.SetVisible', 'BarcodeScanner.DoScan', 'Canvas.Flung',
			'Clock.FormatDate', 'Clock.Timer', 'close screen', 'CloudDB.AppendItemToList', 'CloudDB.DataChanged', 'CloudDB.GotValue',
			'CloudDB.RetrieveValue', 'CloudDB.StoreValue', 'get start value', 'if/then', 'ImageSprite.CollidedWith', 'initialize global', 
			'is in list?', 'make a list', 'Map.DoubleTapAtPoint', 'Notifier.AfterChoosing', 'open screen', 'open screen with start value', 
			'procedure call', 'procedure definition', 'Screen.Initialize', 'select list item', 'set variable to', 'when Back.Click']


def has_feature_block(block, feature):

	if feature[-11:] == 'SetLocation':
		if block.mutation != None:
			if 'method_name' in block.mutation:
				if block.mutation['method_name'] == 'SetLocation':
					if block.mutation['component_type'] == feature[:-12]:
						return True

	if feature[-10:] == 'SetVisible':
		if block.type == 'component_set_get':
			if block.mutation != None:
				if block.mutation['component_type'] == feature[:-11] and block.mutation['set_or_get'] == 'set' and block.mutation['property_name'] == 'Visible':
					return True

	if feature == 'and' or feature == 'or':
		if block.type == 'logic_operation':
			if 'OP' in block.fields:
				if block.fields['OP'] == feature.upper():
					return True

	if feature == 'equal':
		if block.type == 'logic_operation':
			if 'OP' in block.fields:
				if block.fields['OP'] == 'EQ':
					return True

	if feature[-12:] == 'CollidedWith':
		if block.mutation != None:
			if 'event_name' in block.mutation:
				if block.mutation['event_name'] == 'CollidedWith':
					if block.mutation['component_type'] == feature[:-13]:
						return True

	if feature[-6:] == 'DoScan':
		if block.type == 'component_method':
			if block.mutation['method_name'] == 'DoScan':
				if block.mutation['component_type'] == feature[:-7]:
					return True

	if feature[-5:] == 'Flung':
		if block.type == 'component_event':
			if block.mutation['event_name'] == 'Flung':
				if block.mutation['component_type'] == feature[:-6]:
					return True

	if feature[-10:] == 'FormatDate':
		if block.type == 'component_method':
			if block.mutation != None:
				if block.mutation['component_type'] == feature[:-11]:
					if block.mutation['method_name'] == 'FormatDate':
						return True

	if feature[-5:] == 'Timer':
		if block.type == 'component_event':
			if block.mutation != None:
				if block.mutation['component_type'] == feature[:-6]:
					if block.mutation['event_name'] == 'Timer':
						return True

	if feature == 'close screen':
		if block.type == 'controls_closeScreen':
			return True

	if feature[-16:] == 'AppendItemToList':
		if block.type == 'component_method':
			if block.mutation != None:
				if block.mutation['component_type'] == feature[:-17] and block.mutation['method_name'] == 'AppendValueToList':
					return True

	if feature[-11:] == 'DataChanged':
		if block.type == 'component_event':
			if block.mutation != None:
				if block.mutation['component_type'] == feature[:-12] and block.mutation['event_name'] == 'DataChanged':
					return True

	if feature[-8:] == 'GotValue':
		if block.type == 'component_event':
			if block.mutation != None:
				if block.mutation['component_type'] == feature[:-9] and block.mutation['event_name'] == 'GotValue':
					return True

	if feature[-13:] == 'RetrieveValue':
		if block.type == 'component_method':
			if block.mutation != None:
				if block.mutation['component_type'] == feature[:-14] and block.mutation['method_name'] == 'GetValue':
					return True

	if feature[-10:] == 'StoreValue':
		if block.type == 'component_method':
			if block.mutation != None:
				if block.mutation['component_type'] == feature[:-11] and block.mutation['method_name'] == 'StoreValue':
					return True

	if feature == 'get start value':
		if block.type == 'controls_getStartValue':
			return True


	if feature == 'if/then':
		if block.type == 'controls_if':
			return True

	if feature == 'initialize global':
		if block.type == 'global_delaration':
			return True

	if feature == 'is in list?':
		if block.type == 'lists_is_in':
			return True

	if feature == 'make a list':
		if block.type == 'lists_create_with':
			return  True

	if feature[-16:] == 'DoubleTapAtPoint':
		if block.type == 'component_event':
			if block.mutation != None:
				if block.mutation['component_type'] == feature[:-17] and block.mutation['event_name'] == 'DoubleTapAtPoint':
					return True

	if feature[-13:] == 'AfterChoosing':
		if block.type == 'component_event':
			if block.mutation != None:
				if block.mutation['component_type'] == feature[:-14] and block.mutation['event_name'] == 'AfterChoosing':
					return True

	if feature == 'open screen':
		if block.type == 'controls_openAnotherScreen':
			return True

	if feature == 'open screen with start value':
		if block.type == 'controls_openAnotherScreenWithStartValue':
			return True

	if feature == 'procedure call':
		if block.type == 'procedures_callnoreturn' or block.type == 'procedures_callreturn':
			return True

	if feature == 'procedure definition':
		if block.type == 'procedure_defreturn' or block.type == 'procedure_defnoreturn':
			return True

	if feature == 'Screen.Initialize':
		if block.type == 'component_event':
			if block.mutation != None:
				if block.mutation['component_type'] == 'Form':
					if block.mutation['event_name'] == 'Initialize':
						return True

	if feature == 'select list item':
		if block.type == 'lists_select_item':
			return True

	if feature[0:3] == 'set' and feature[-2:] == 'to':
		if block.type == 'lexical_variable_set':
			if block.fields != {}:
				if block.fields['VAR'] == feature[4:-3]:
					return True

	if feature == 'when Back.Click':
		if block.type == 'component_event':
			if block.mutation != None:
				if block.mutation['component_type'] == 'Form' and block.mutation['event_name'] == 'BackPressed':
					return True

	return False



def identify_block_features(project, block_features):

	dict_of_features = {}

	for snap in project.snapshots:
		for block in snap.screen.blocks:
			for feature in block_features:

				if has_feature_block(block, feature) and feature not in dict_of_features:
					dict_of_features[feature] = snap

	return dict_of_features


def count_block_features(project, block_features):

	dict_of_total_features = {}

	for snap in project.snapshots:
		for block in snap.screen.blocks:
			for feature in block_features:

				if has_feature_block(block, feature):
					if feature in dict_of_total_features:
						if block.id not in dict_of_total_features[feature]:
							dict_of_total_features[feature][block.id] = snap
							dict_of_total_features[feature]['count'] += 1
					else:
						dict_of_total_features[feature] = {block.id: snap, 'count':  1}

	return dict_of_total_features





