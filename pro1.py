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
    species_dict = {}
    for row in data:
        sp = row[species_col]
        sex = row[sex_col].lower()
        try:
            mass = float(row[body_col])
        except:
            continue 
        if sp not in species_dict:
            species_dict[sp] = {"male": [], "female": []}
        species_dict[sp][sex].append(mass)

    result = {}
    for sp, sex_dict in species_dict.items():
        male_avg = round(sum(sex_dict["male"]) / len(sex_dict["male"])) if sex_dict["male"] else 0
        female_avg = round(sum(sex_dict["female"]) / len(sex_dict["female"])) if sex_dict["female"] else 0
        total_list = sex_dict["male"] + sex_dict["female"]
        total_avg = round(sum(total_list) / len(total_list)) if total_list else 0
        result[sp] = {"average": total_avg, "male": male_avg, "female": female_avg}
    return result