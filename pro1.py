import csv

def load_csv(file_path):
    """Load CSV into list of dictionaries."""
    data = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data

def island_species_average(data, species_col="species", body_col="body_mass_g", sex_col="sex"):
    """Average body mass per species and by sex."""
   