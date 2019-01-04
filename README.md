# DEPRECATED.

## openag_recipe_generator
Python script for generating simple timeseries recipes

## Install
Clone directory
```
cd ~/my_project_folder
git clone https://github.com/OpenAgInitiative/openag_recipe_generator.git
```
Make sure you have python installed
```
python --version
```
Should see something like, if you do not. Go [download python](https://www.python.org/downloads/)
```
Python 2.7.10
```
Edit the parameters in *recipe_generator.py* file for desired recipe output with favorite text editor. [Sublime Text Editor](https://www.sublimetext.com/) is straight forward.
```
### Set parameters #############################################################
recipe_name = 'example_recipe'
recipe_format = 'simple'
cycles = 2 # cycles
day_length = 18 # hours
light_intensity_red = 1 # 1 for on, 0 for off
light_intensity_blue = 1 # 1 for on, 0 for off
light_intensity_white = 1 # 1 for on, 0 for off
night_length = 6 # hours
day_air_temperature = 24 # C
night_air_temperature = 16 # C
air_flush_on_number_per_day = 2 # times / day
air_flush_on_day_length = 60 # minutes
air_flush_on_number_per_night = 0 # times / night
air_flush_on_night_length = 20 # minutes
ph = 6 # pH
nutrient_a_number_per_day = 2 # times / day
nutrient_a_volume = 2.5 # mL
nutrient_b_number_per_day = 1 # times / day
nutrient_b_volume = 5 # mL
################################################################################
```
After you are finished your edits, **SAVE THE FILE**. Once saved, from the same directory that contains *recipe_generator.py*, run
```
cd ~/my_projects_folder/openag_recipe_generator
python recipe_generator.py
```
This will create a new file in the same directory with the same name as the recipe_name. For example, if *recipe_name = 'example_recipe'*, a file called *example_recipe.json* will be created. It will looks something like this. **Note the times are in milliseconds.**
```
{
    "_id": "example_recipe",
    "format": "simple",
    "operations": [
        [
            0,
            "water_potential_hydrogen",
            6
        ],
        [
            0,
            "light_intensity_red",
            1
        ],
        [
            0,
            "light_intensity_blue",
            1
        ],
        [
            0,
            "light_intensity_white",
            1
        ],
        [
            0,
            "air_temperature",
            24
        ],
        [
            0,
            "air_flush_on",
            0
        ],
        [
            0,
            "nutrient_flora_duo_a",
            0
        ],
        [
            0,
            "nutrient_flora_duo_b",
            0
        ],
        [
            10,
            "air_flush_on",
            60
        ],
        [
            10,
            "nutrient_flora_duo_a",
            2.5
        ],
        [
            10,
            "nutrient_flora_duo_b",
            5
        ],
        [
            32400,
            "air_flush_on",
            0
        ],
        [
            32400,
            "nutrient_flora_duo_a",
            0
        ],
        [
            32410,
            "air_flush_on",
            60
        ],
        [
            32410,
            "nutrient_flora_duo_a",
            2.5
        ],
        [
            64800,
            "light_intensity_red",
            0
        ],
        [
            64800,
            "light_intensity_blue",
            0
        ],
        [
            64800,
            "light_intensity_white",
            0
        ],
        [
            64800,
            "air_temperature",
            16
        ],
        [
            86400,
            "light_intensity_red",
            1
        ],
        [
            86400,
            "light_intensity_blue",
            1
        ],
        [
            86400,
            "light_intensity_white",
            1
        ],
        [
            86400,
            "air_temperature",
            24
        ],
        [
            86400,
            "air_flush_on",
            0
        ],
        [
            86400,
            "nutrient_flora_duo_a",
            0
        ],
        [
            86400,
            "nutrient_flora_duo_b",
            0
        ],
        [
            86410,
            "air_flush_on",
            60
        ],
        [
            86410,
            "nutrient_flora_duo_a",
            2.5
        ],
        [
            86410,
            "nutrient_flora_duo_b",
            5
        ],
        [
            118800,
            "air_flush_on",
            0
        ],
        [
            118800,
            "nutrient_flora_duo_a",
            0
        ],
        [
            118810,
            "air_flush_on",
            60
        ],
        [
            118810,
            "nutrient_flora_duo_a",
            2.5
        ],
        [
            151200,
            "light_intensity_red",
            0
        ],
        [
            151200,
            "light_intensity_blue",
            0
        ],
        [
            151200,
            "light_intensity_white",
            0
        ],
        [
            151200,
            "air_temperature",
            16
        ]
    ]
}
```
To upload this to the food computer, copy and paste the json text into create new recipe prompt in the openag ui
