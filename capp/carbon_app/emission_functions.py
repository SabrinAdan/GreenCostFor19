efco2 = {
    "car": {
        "diesel": 158,
        "petrol": 162,
        "electric": 37,
    },
    "plane": {
        "economy":90, # midpoint of 80–100
        "business": 300, # midpoint of 200–400
    },
    "ferry": {
        "diesel": 200, # midpoint of 180–220
        "lng":  158, # midpoint of 150–165
    },
    "bus": {
        "diesel": 102,
        "electric": 21,
    },
    "train": {
        "diesel": 91,
        "electric": 7,
    },
    "bybane": {
        "electric": 4,
    },
    "motorcycle": {
        "petrol": 111,
        "electric": 23,
    },
    "bicycle": {
        "regular": 9, # midpoint of 5–12
        "electric": 18, # midpoint of 13-22
    },
    "walking": {
        "default": 0,
    },
    "truck": {
        "diesel": 75,
        "biodiesel": 32,
        "electric": 18,
        "hydrogen": 14,
    },
    "van":{
        "diesel": 245,
        "biodiesel": 104,
        "electric": 48,
        "hydrogen": 28,
    },
    "cargo_plane": {
        "dedicated":{
            "jet_fuel": 602,
            "saf": 102,
        },
        "belly": {
            "jet_fuel": 410,
        },
    },
    "rail": {
        "electric": 6,
        "diesel": 28,
    },
    "maritime": {
        "marine_diesel": 13, # midpoint of 10–15
        "lng": 10,
        "biofuel": 6,  # midpoint of 3–8
    },
    "pipeline": {
        "electricity":  9, # midpoint of 7–10
        "fossil_energy": 20, # midpoint of 15–25
    }
}

aircraft_factor = {
    "small": 1.67, # 150 / 90 ≈ economy small relative to base 90
    "medium": 1.06, # 95 / 90
    "big": 0.94,  # 85 / 90
}


def grams_to_kg(co2_grams):
    return round(co2_grams / 1000, 2)


def calculate_basic_emission(kms, factor):
    co2_grams = kms * factor
    return grams_to_kg(co2_grams)


def calculate_plane_emission(kms, base_factor, plane_multiplier):
    co2_grams = kms * base_factor * plane_multiplier
    return grams_to_kg(co2_grams)


def calculate_cargo_emission(kms, factor, weight_kg):
    tons = weight_kg / 1000 if weight_kg else 0
    co2_grams = kms * factor * tons
    return grams_to_kg(co2_grams)


def calculate_pipeline_emission(distance, volume, factor):
    co2_grams = distance * volume * factor
    return grams_to_kg(co2_grams)


def carbon_emission(transport, form_data):
    kms = form_data.get("kms") or 0
    fuel = form_data.get("fuel")
    cargo_weight = form_data.get("cargo_weight") or 0
    load = form_data.get("load") or 0
    volume = form_data.get("volume") or 0
    distance = form_data.get("distance") or 0
    flight_type = form_data.get("flight_type")
    cabin_class = form_data.get("cabin_class")
    aircraft_type = form_data.get("aircraft_type")
    cargo_type = form_data.get("cargo_type")
    ferry_type = form_data.get("ferry_type")
    train_type = form_data.get("train_type")
    bicycle_type = form_data.get("bicycle_type")
    energy_source = form_data.get("energy_source")

    if transport == "car":
        factor = efco2["car"][fuel]
        return calculate_basic_emission(kms, factor)

    elif transport == "plane":
        base_factor = efco2["plane"][cabin_class]
        plane_multiplier = aircraft_factor[aircraft_type]
        return calculate_plane_emission(kms, base_factor, plane_multiplier)

    elif transport == "ferry":
        factor = efco2["ferry"][ferry_type]
        return calculate_basic_emission(kms, factor)

    elif transport == "bus":
        factor = efco2["bus"][fuel]
        return calculate_basic_emission(kms, factor)

    elif transport == "train":
        factor = efco2["train"][train_type]
        return calculate_basic_emission(kms, factor)

    elif transport == "bybane":
        factor = efco2["bybane"][fuel]
        return calculate_basic_emission(kms, factor)

    elif transport == "motorcycle":
        factor = efco2["motorcycle"][fuel]
        return calculate_basic_emission(kms, factor)

    elif transport == "bicycle":
        factor = efco2["bicycle"][bicycle_type]
        return calculate_basic_emission(kms, factor)

    elif transport == "walking":
        factor = efco2["walking"]["default"]
        return calculate_basic_emission(kms, factor)

    elif transport == "truck":
        factor = efco2["truck"][fuel]
        return calculate_cargo_emission(kms, factor, load)
    
    elif transport == "van":
        factor = efco2["van"][fuel]
        return calculate_basic_emission(kms, factor)

    elif transport == "cargo_plane":
        factor = efco2["cargo_plane"][cargo_type][fuel]
        return calculate_cargo_emission(kms, factor, cargo_weight)

    elif transport == "rail":
        factor = efco2["rail"][fuel]
        return calculate_cargo_emission(kms, factor, cargo_weight)

    elif transport == "maritime":
        factor = efco2["maritime"][fuel]
        return calculate_cargo_emission(kms, factor, cargo_weight)

    elif transport == "pipeline":
        factor = efco2["pipeline"][energy_source]
        return calculate_pipeline_emission(distance, volume, factor)

    return None