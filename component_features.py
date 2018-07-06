
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

	list_of_total_features = []

	for snap in project.snapshots:
		for component in snap.screen.components:
			for feature in features:

				if has_feature_component(component, feature) and feature not in list_of_total_features:
					list_of_total_features.append(feature)

	return list_of_total_features


def count_component_features(project, features):

	dict_of_total_features = {}

	for snap in project.snapshots:
		for component in snap.screen.components:
			for feature in features:

				if has_feature_component(component, feature):
					if feature in dict_of_total_features:
						if component.id not in dict_of_total_features[feature][0]:
							dict_of_total_features[feature][0].append(component.id)
							dict_of_total_features[feature][1] += 1
					else:
						dict_of_total_features[feature] = [[component.id], 1]

	return dict_of_total_features


