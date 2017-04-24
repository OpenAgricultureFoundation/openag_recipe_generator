import json
import operator

### Set parameters #############################################################
recipe_name = 'nutrient_doser_fail_test_7d'
recipe_format = 'simple'
cycles = 84 # cycles
day_length = 1 # hours
light_intensity_red = 1 # 1 for on, 0 for off
light_intensity_blue = 1 # 1 for on, 0 for off
light_intensity_white = 1 # 1 for on, 0 for off
night_length = 1 # hours
day_air_temperature = None # C
night_air_temperature = None # C
air_flush_on_number_per_day = 0 # times / day
air_flush_on_day_length = 60 # minutes
air_flush_on_number_per_night = 0 # times / night
air_flush_on_night_length = 20 # minutes
ph = None # pH
nutrient_a_number_per_day = 1 # times / day
nutrient_a_volume = 5 # mL
nutrient_b_number_per_day = 1 # times / day
nutrient_b_volume = 5 # mL
################################################################################

# Generate recipe
recipe = {}
recipe['_id'] = recipe_name
recipe['format'] = recipe_format
recipe['operations'] = []
if ph is not None:
    recipe['operations'].append([0, 'water_potential_hydrogen', ph])

for i in range(cycles):
    # Set day & night start times
    day_start_time = (day_length + night_length) * 3600 * i
    night_start_time = day_start_time + day_length * 3600
    # Set day parameters
    recipe['operations'].append([day_start_time, 'light_intensity_red', light_intensity_red])
    recipe['operations'].append([day_start_time, 'light_intensity_blue', light_intensity_blue])
    recipe['operations'].append([day_start_time, 'light_intensity_white', light_intensity_white])
    if day_air_temperature != None:
        recipe['operations'].append([day_start_time, 'air_temperature', day_air_temperature])
    # Set air flush
    for i in range(air_flush_on_number_per_day):
        time = day_start_time + day_length * 3600 / air_flush_on_number_per_day * i
        recipe['operations'].append([time, 'air_flush_on', 0]) # Air flush firmware only turns on for new value duation if new value is different than prev
        recipe['operations'].append([time + 10, 'air_flush_on', air_flush_on_day_length]) # Send real value after setting flush to 0 for 10 sec
    # Set nutrient a
    for i in range(nutrient_a_number_per_day):
        time = day_start_time + day_length * 3600 / nutrient_a_number_per_day * i
        recipe['operations'].append([time, 'nutrient_flora_duo_a', 0]) # Pump firmware only doses volume if new value is different than prev
        recipe['operations'].append([time + 10, 'nutrient_flora_duo_a', nutrient_a_volume]) # Send real value after setting volume to 0 for 10 sec
    # Set nutrient b
    for i in range(nutrient_b_number_per_day):
        time = day_start_time + day_length * 3600 / nutrient_b_number_per_day * i
        recipe['operations'].append([time, 'nutrient_flora_duo_b', 0]) # Pump firmware only doses volume if new value is different than prev
        recipe['operations'].append([time + 10, 'nutrient_flora_duo_b', nutrient_b_volume]) # Send real value after setting volume to 0 for 10 sec

    # Set night parameters
    recipe['operations'].append([night_start_time, 'light_intensity_red', 0])
    recipe['operations'].append([night_start_time, 'light_intensity_blue', 0])
    recipe['operations'].append([night_start_time, 'light_intensity_white', 0])
    if night_air_temperature is not None:
        recipe['operations'].append([night_start_time, 'air_temperature', night_air_temperature])

    for i in range(air_flush_on_number_per_night):
        time = night_start_time + night_length * 3600 / air_flush_on_number_per_night * i
        recipe['operations'].append([time, 'air_flush_on', 0]) # Air flush only sets new value if different than prev
        recipe['operations'].append([time + 10, 'air_flush_on', air_flush_on_night_length]) # Send real value after setting flush to 0 for 10 sec

# Sort recipe so timeseries is linear
recipe['operations'] = sorted(recipe['operations'], key=operator.itemgetter(0))

# Write recipe to file
f = open('{}.json'.format(recipe_name), 'w')
f.write(json.dumps(recipe, indent=4, sort_keys=True))
f.close()
