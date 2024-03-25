import json
import os
import numpy
import math


def process_documents():

    drug_ages = {}

    files = os.listdir("../data")

    json_files = [f for f in files if f.endswith(".json")]

    # get documents.json (../resorces/)
    # with open("../resources/drug_documents.json", "r") as file:
    #     json_doc = json.load(file)

    for documents in json_files:
        with open(f"../data/{documents}", "r") as file:
            data = json.load(file)
        print(f"Processing {documents}")
        count = 1
        for result in data["results"]:
            if count % 1000 == 0:
                print(f"Processing result {count}")
            count += 1
            for drugs in result.get("patient", {}).get("drug", []):
                # brandname = ""
                # brandnames = drugs.get("openfda", {}).get("brand_name", [])
                # if brandnames:
                #     brandname = brandnames[0]
                # if brandname == "":
                #     continue
                brandnames = sorted(drugs.get("openfda", {}).get("brand_name", []))
                if not brandnames:
                    continue
                brandname = brandnames[0]
                if brandname not in drug_ages:
                    drug_ages[brandname] = []
                if "patientonsetage" in result.get("patient", {}):
                    patient_age = result.get("patient", {}).get("patientonsetage")
                    if int(patient_age) > 0 and int(patient_age) < 120:
                        drug_ages[brandname].append(int(patient_age))
                    # print(drug_median_age)

    # drug_ages = {brandname: numpy.median(ages) for brandname, ages in drug_median_age.items() if ages}
    threshold = 10
    drug_median_ages = {}
    for brandname, age in drug_ages.items():
        if len(age) > threshold:
            # drug_median_ages[brandname] = (numpy.median(age), numpy.var(age))
            median = numpy.median(age)
            std_dev = math.sqrt(numpy.var(age))
            drug_median_ages[brandname] = (median, std_dev)

    with open("../resources/drug_median_var_ages.json", "w") as outfile:
        json.dump(drug_median_ages, outfile)

    return drug_median_ages


if __name__ == "__main__":
    process_documents()
