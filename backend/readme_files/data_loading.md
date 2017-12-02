## Data loading documentation
---------------------------

### Data loading workflow
Each step should be done in sequence as there are some dependencies in each step from the previous step.
- Ingredients loading
- Menu loading
- Phytochemical loading

### Loaded files
We use a `csv` formatted file downloaded from the spreadsheet provided.

### Environment
- Use a virtual environment to run the scripts
- Use python3.5+
- `virtualenv -p path/to/python/distribution venv`
- Activate the virtual env `source venv/bin/activate`

### Ingredients loading
- Go to root app directory
- Run the following command `python -m daily_menu_loader.loader --data-type ingredient --file path/to/ingredient/file.csv --integration-name <integration_name> 

### Menu loading
- Go to root app directory
- Run the following command `python -m daily_menu_loader.loader --data-type menu --meal-type lunch  --file path/to/menu/file.csv --integration-name <integration_name>`
- You can use the `validator.py` to validate your work. `python daily_menu_loader/validator.py`

### Phytochemical loading
- Go to root app directory
- Run the following command `python -m pythochemical_loader.loader --mapping-file optional/path/to/mapping/file.csv --ingredients-file path/to/ingredients/file.csv`
 
`mapping-file` args is optional, if there is no mapping file specified, it will default to searching the database mapping for previously loaded ingredients
