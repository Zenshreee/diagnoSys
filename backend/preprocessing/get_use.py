import json
import os
import time

def process_documents():

    drug_uses = {}

    files = os.listdir("../data")

    json_files = [f for f in files if f.endswith(".json")]

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
                    brandnames = drugs.get("openfda", {}).get("brand_name", [])
                    drugindication = drugs.get("drugindication", "Drug use not found")
                    if drugindication == "PRODUCT USED FOR UNKNOWN INDICATION":
                        continue 
                    if not brandnames:
                        continue  
                    brandname = brandnames[0]
                    if brandname not in drug_uses:
                        drug_uses[brandname] = {}
                    if drugindication not in drug_uses[brandname]:
                        drug_uses[brandname][drugindication] = 0
                    drug_uses[brandname][drugindication] += 1
    
    threshold = 5
    for brandname, indications in drug_uses.items():
      if len(indications) > 1 and "Drug use not found" in indications:
            del indications["Drug use not found"]
      sorted_indications = sorted(indications.items(), key=lambda x: x[1], reverse=True)[:threshold]
      drug_uses[brandname] = [indication for indication, count in sorted_indications]

    with open("../preprocessing/drug_use.json", "w") as outfile:
        json.dump(drug_uses, outfile)
    
    return drug_uses


if __name__ == "__main__":
    process_documents()


                    
          
            



        

        

