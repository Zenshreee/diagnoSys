import json

def load_drugs():
    with open('brand_to_generic.json', 'r') as file:
        return json.load(file)


def edit_matrix(query, message, ins_cost_func, del_cost_func, sub_cost_func):
    """Calculates the edit matrix

    Arguments
    =========

    query: query string,

    message: message string,

    ins_cost_func: function that returns the cost of inserting a letter,

    del_cost_func: function that returns the cost of deleting a letter,

    sub_cost_func: function that returns the cost of substituting a letter,

    Returns:
        edit matrix {(i,j): int}
    """

    m = len(query) + 1
    n = len(message) + 1

    chart = {(0, 0): 0}
    for i in range(1, m):
        chart[i, 0] = chart[i - 1, 0] + del_cost_func(query, i)
    for j in range(1, n):
        chart[0, j] = chart[0, j - 1] + ins_cost_func(message, j)
    for i in range(1, m):
        for j in range(1, n):
            chart[i, j] = min(
                chart[i - 1, j] + del_cost_func(query, i),
                chart[i, j - 1] + ins_cost_func(message, j),
                chart[i - 1, j - 1] + sub_cost_func(query, message, i, j),
            )
    return chart

# def edit_distance(query, drug_name):
#   query = query.lower()
#   drug_name = drug_name.lower()

#   matrix = edit_matrix(query, drug_name, 1, 1, 2)

#   return matrix[(len(query), len(drug_name))]


def edit_distance(query, drug_name, ins_cost=1, del_cost=1, sub_cost=2):
    query = query.lower()
    drug_name = drug_name.lower()

    def ins_cost_func(s, pos):
        return ins_cost

    def del_cost_func(s, pos):
        return del_cost

    def sub_cost_func(s1, s2, pos1, pos2):
        return sub_cost if s1[pos1-1] != s2[pos2-1] else 0

    matrix = edit_matrix(query, drug_name, ins_cost_func, del_cost_func, sub_cost_func)

    return matrix[(len(query), len(drug_name))]


def edit_distance_search(query):
    drugs = load_drugs()
    results = []

    for drug_name in drugs.keys():
        score = edit_distance(query, drug_name)
        results.append((score, drug_name)) 

    results.sort(key=lambda x: x[0])
    return results[0]

# testing
closest_match = edit_distance_search("FIBERCOR")
print("Closest match:", closest_match)


