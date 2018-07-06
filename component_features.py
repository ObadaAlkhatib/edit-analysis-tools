
import aiatools as aia
from aiatools.block_types import *
from aiatools.component_types import *

component_features = ['BarcodeScanner', 'BluetoothClient', 'BluetoothServer', 'BluetoothLE', 'Camera', 'Canvas',
					  'Clock', 'CloudDB', 'LocationSensor', 'Map', 'Notifier', 'QR_Code', 'Sound', 'TextToSpeech', 
					  'TinyDB', 'Web']

def has_feature_component(component, feature):

	if component.type.name == feature:
		return True
	return False


def identify_component_features(project, features):

	dict_of_features = {}

	for snap in project.snapshots:
		for component in snap.screen.components:
			for feature in features:

				if has_feature_component(component, feature) and feature not in dict_of_features:
					dict_of_features[feature] = snap

	return dict_of_features


def count_component_features(project, features):

	dict_of_total_features = {}

	for snap in project.snapshots:
		for component in snap.screen.components:
			for feature in features:

				if has_feature_component(component, feature):
					if feature in dict_of_total_features:
						if component.id not in dict_of_total_features[feature]:
							dict_of_total_features[feature][component.id] = snap
							dict_of_total_features[feature]['count'] += 1
					else:
						dict_of_total_features[feature] = {component.id: snap, 'count':  1}
						
	return dict_of_total_features


