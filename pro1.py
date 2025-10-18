# Name: Joey Yang 
# Student ID: 0316 4367
# Email: joeyy@umich.edu
# Collaborators: Collabrated with Andrew Jacobs, I also used gen AI to help me get started for for calculation ideas for 
# our check points. Also used to create a test case csv just to test the important data for our calculations. More general usage such as fixing bugs and debug, and asking about my errors and what caused it. 



# Joey's fucntions

import csv
import os

def load_csv(file_path):
    """Loads CSV into a list of dictionaries."""
    data = []
    with open(file_path, newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if "" in row:
                del row[""]
            data.append(row)
    return data


def island_species_average(data, species_col="species", body_col="body_mass_g", sex_col="sex"):
    """Calculates average body mass by species and sex."""
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
        total_avg = round(sum(total_list) / len(total_list)) if total_list else 0
        result[sp] = {"average": total_avg, "male": male_avg, "female": female_avg}
    return result


def flipper_length_trend(data, flipper_col="flipper_length_mm", year_col="year", species_col="species"):
    """Finds the average flipper length per year for each species."""
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
    """Writes species averages to a CSV file."""
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Species", "Male", "Female", "Average"])
        for sp, vals in data.items():
            writer.writerow([sp, vals.get("male"), vals.get("female"), vals.get("average")])


def write_flipper_trend(filename, data):
    """Writes flipper trends to a CSV file."""
    with open(filename, "w", newline="") as f:
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


# Andrew’s Functions
def penguin_pullinfo(penguin_csv):
    """Loads penguin data from CSV."""
    rows = []
    file_path = os.path.join(os.getcwd(), penguin_csv)
    with open(file_path, mode="r", newline="", encoding="utf-8") as inFile:
        reader = csv.DictReader(inFile)
        for row in reader:
            rows.append(row)
    return rows


def bill_average_length(rows, species_name, island):
    """Calculates average bill length for a given species and island."""
    total = 0.0
    count = 0
    for row in rows:
        if row["species"] == species_name and row["island"] == island:
            length = row["bill_length_mm"].strip()
            if length != "NA" and length != "":
                total += float(length)
                count += 1
    if count > 0:
        avg = total / count
    else:
        avg = None
    return [{
        "species": species_name,
        "island": island,
        "average_bill_length": avg,
        "count": count
    }]


def bill_average_depth(rows, species_name, island):
    """Calculates average bill depth for a given species and island."""
    total = 0.0
    count = 0
    for row in rows:
        if row["species"] == species_name and row["island"] == island:
            depth = row["bill_depth_mm"].strip()
            if depth != "NA" and depth != "":
                total += float(depth)
                count += 1
    if count > 0:
        avg = total / count
    else:
        avg = None
    return [{
        "species": species_name,
        "island": island,
        "average_bill_depth": avg,
        "count": count
    }]

def save_results_to_file(data, filename):
    """Writes Joey's and Andrew's results to a single .txt file."""
    with open(filename, "w") as file:
        # Joey
        file.write("Island Species Average (Joey's function):\n")
        avg_result = island_species_average(data)
        for species, stats in avg_result.items():
            file.write(f"{species}: {stats}\n")

        file.write("\nFlipper Length Trend (Joey's function):\n")
        trend_result = flipper_length_trend(data)
        for species, years in trend_result.items():
            file.write(f"{species}: {years}\n")

        # Andrew
        penguin_data = penguin_pullinfo("test.csv")

        file.write("\nBill Average Length & Depth (Andrew's functions):\n")
        examples = [
            ("Adelie", "Torgersen"),
            ("Gentoo", "Biscoe"),
            ("Chinstrap", "Dream")
        ]
        results = []

        for species, island in examples:
            length = bill_average_length(penguin_data, species, island)[0]
            depth = bill_average_depth(penguin_data, species, island)[0]
            results.append({
                "species": species,
                "island": island,
                "average_bill_length": length["average_bill_length"],
                "average_bill_depth": depth["average_bill_depth"],
                "count": length["count"]
            })

        file.write(str(results))

if __name__ == "__main__":
    data = load_csv("test.csv")
    save_results_to_file(data, "results.txt")
    penguin_data = penguin_pullinfo("test.csv")
    