# Name: Joey Yang 
# Student ID: 0316 4367
# Email: joeyy@umich.edu
# Collaborators: Collabrated with Andrew Jacobs, I also used gen AI to help me get started for for calculation ideas for 
# our check points. Also used to create a test case csv just to test the important data for our calculations. More general usage such as fixing bugs and debug, and asking about my errors and what caused it. 

import csv

def load_csv(file_path):
    data = []
    csvfile = open(file_path, newline='')
    reader = csv.DictReader(csvfile)
    for row in reader:
        data.append(row)
    csvfile.close()
    return data

def island_species_average(data, species_col="species", body_col="body_mass_g", sex_col="sex"):
    species_dict = {}
    for row in data:
        sp = row[species_col]
        sex = row[sex_col].lower()
        value = row[body_col].strip()
        
        if value != "" and value.replace(".", "", 1).isdigit():
            mass = float(value)
        else:
            continue

        if sp not in species_dict:
            species_dict[sp] = {"male": [], "female": []}
        species_dict[sp][sex].append(mass)

    result = {}
    for sp, sex_dict in species_dict.items():
        male_avg = round(sum(sex_dict["male"]) / len(sex_dict["male"])) if sex_dict["male"] else 0
        female_avg = round(sum(sex_dict["female"]) / len(sex_dict["female"])) if sex_dict["female"] else 0
        total_list = sex_dict["male"] + sex_dict["female"]
        total_avg = round(sum(total_list) / len(total_list)) if total_list else 0 #changed None to 0 
        result[sp] = {"average": total_avg, "male": male_avg, "female": female_avg}
    return result

def flipper_length_trend(data, flipper_col="flipper_length_mm", year_col="year", species_col="species"):
    """Average flipper length per species per year."""
    trend_dict = {}
    species_set = set()

    for row in data:
        sp = row[species_col]
        species_set.add(sp)
        year = row[year_col]
        value = row[flipper_col].strip()

        if value != "" and value.replace(".", "", 1).isdigit():
            flipper = float(value)
        else:
            continue

        if sp not in trend_dict:
            trend_dict[sp] = {}
        if year not in trend_dict[sp]:
            trend_dict[sp][year] = []
        trend_dict[sp][year].append(flipper)

    result = {}
    for sp in species_set:  
        result[sp] = {}
        if sp in trend_dict:
            for yr, lengths in trend_dict[sp].items():
                if lengths:
                    result[sp][int(yr)] = round(sum(lengths) / len(lengths), 1)
    return result

def write_species_average(filename, data):
    f = open(filename, "w", newline="")
    writer = csv.writer(f)
    writer.writerow(["Species", "Male", "Female", "Average"])
    for sp, vals in data.items():
        writer.writerow([sp, vals.get("male"), vals.get("female"), vals.get("average")])
    f.close()

def write_flipper_trend(filename, data):
    f = open(filename, "w", newline="")
    writer = csv.writer(f)
    years = set()
    for sp_vals in data.values():
        years.update(sp_vals.keys())
    years = sorted(list(years))
    writer.writerow(["Species"] + years)
    
    for sp, vals in data.items():
        row = [sp]
        for yr in years:
            row.append(vals.get(yr, ""))
        writer.writerow(row)
    f.close()

if __name__ == "__main__":
    data = load_csv("penguins.csv")  
    species_avg = island_species_average(data)
    flipper_trend = flipper_length_trend(data)
    