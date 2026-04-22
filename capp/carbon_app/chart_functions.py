individual_transports = ["car", "plane", "ferry", "bus","train", "bybane", "motorcycle","bicycle", "walking" ]
business_transports = ["truck", "van" ,"cargo_plane", "rail", "maritime", "pipeline"]

alternatives_map = {
     # Individual
    "car": ["bus", "train", "bicycle", "walking", "bybane"],
    "plane": ["train"],
    "motorcycle": ["bus", "train", "bybane"],
    "ferry": ["train", "bus"],
    "bus": ["train", "bybane", "bicycle"],
    "train": ["bus", "bybane", "bicycle"],
    "bybane": ["bus", "train", "bicycle", "walking"],
    "bicycle": ["walking", "bybane"],
    "walking": ["bicycle", "bybane", "bus"],

    # Business
    "truck": ["rail", "maritime"],
    "van": ["truck", "rail"],
    "cargo_plane": ["rail", "maritime"],
    "rail": ["truck", "maritime"],
    "maritime": ["rail", "truck"],
    "pipeline": ["rail"],
}


def get_categories_for_user_type(user_type):
    if user_type == "business":
        return business_transports
    return individual_transports


def build_chart_values(query_result, ordered_categories):
    values_by_category = {category: 0 for category in ordered_categories}

    for total, category in query_result:
        if category in values_by_category:
            values_by_category[category] = float(total or 0)

    return [values_by_category[category] for category in ordered_categories]


def format_date_chart(query_result):
    labels = [str(date_value) for total, date_value in query_result]
    values = [float(total or 0) for total, date_value in query_result]
    return labels, values

def get_alternatives(transport, user_type):
    possible = alternatives_map.get(transport, [])

    if user_type == "business":
        return [t for t in possible if t in business_transports]
    else:
        return [t for t in possible if t in individual_transports]
