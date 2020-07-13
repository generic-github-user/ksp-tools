import glob, os
import datetime

read_local_ships = True
read_steam_ships = True

# Buildings ships can be constructed in
buildings = ['SPH', 'VAB']
# Root path of KSP saves
dir = 'C:/Program Files (x86)/Steam/steamapps/common/Kerbal Space Program/'
os.chdir(dir)
savefiles = [name for name in os.listdir('.') if os.path.isdir(name) and name != 'training' and name != 'scenarios']

# List of column headers for table
header = ['Name', 'Description', 'Savefile', 'Building', 'Parts', 'Stages', 'Price', 'Mass', 'Size X', 'Size Y', 'Size Z', 'Created', 'Modified', 'Source']
header = [', '.join(header)]
ship_list = []
# Get property specified by line
def get_prop(string):
	return string.split(' = ')[0]
def get_val(string):
	return string.split(' = ')[1][:-1]
def get_ship_data(file, source):
	# Open file
	f = open(file, 'r')
	lines = f.readlines()
	ship_data = {
		'shipName': '',
		'description': '',
		'partCount': '',
		'stageCount': '',
		'totalCost': '',
		'totalMass': '',
		'shipSize': '',
		'type': '',
		'created': 0,
		'modified': 0
	}
	for line in lines:
		property = get_prop(line)
		if property in ship_data:
			ship_data[property] = get_val(line)
	
	# Record creation and modification time of craftmeta file
	ship_data['created'] = datetime.datetime.fromtimestamp(int(os.path.getctime(file)))
	ship_data['modified'] = datetime.datetime.fromtimestamp(int(os.path.getmtime(file)))
	
	current_ship = [ship_data['shipName'], '', save, ship_data['type'], ship_data['partCount'], ship_data['stageCount'], ship_data['totalCost'], ship_data['totalMass'], *ship_data['shipSize'].split(','), str(ship_data['created']), str(ship_data['modified']), source]
	ship_list.append(', '.join(current_ship))
	f.close()


if read_local_ships:
	# Hop into saves directory to create savefiles list
	os.chdir('saves')
	# Get a list of all directories (saves) except training and scenarios
	savefiles = [name for name in os.listdir('.') if os.path.isdir(name) and name != 'training' and name != 'scenarios']
	# Loop through each saved world
	for save in savefiles:
		# Loop through SPH and VAB
		for building in buildings:
			os.chdir(dir + 'saves/' + save + '/Ships/' + building)
			for file in glob.glob('*.loadmeta'):
				get_ship_data(file, 'Local')
if read_steam_ships:
	# Go back to main KSP directory
	os.chdir('..')
	for building in buildings:
		os.chdir(dir + 'Ships/' + building)
		for file in glob.glob('*.loadmeta'):
				get_ship_data(file, 'Steam')

# Combine data and print to console/output
print('\n'.join(header + ship_list))