# Dict

efco2 = {
    # --------- Individual ------------
    "car": {
        "diesel": 229,
        "petrol": 198,
        "electric": 59
    },
    "plane": {
        "domestic": {
            "economy": 186,
            "business": 284,
        },
        "international": {
            "economy": 186,
            "business": 284,
        },
    },
    "ferry": {
        "passenger": 186,
        "car_ferry": 23
    },
    "bus": {
        "diesel": 30,
        "electric": 13,
    },
    "train": {
        "diesel": 91,
        "electric": 7,
    },
    "bybane": {
        "default": 1.5
    },
    "motorcycle": {
        "petrol": 95,
        "electric": 20
    },
    "bicycle": {
        "regular": 0,
        "electric": 5
    },
    "walking": {
        "default": 0
    },

    # ------ Business ------
    "truck": {
        "diesel": 120,
        "biodiesel": 100,
        "electric": 40,
        "hydrogen": 30
    },
    "cargo_plane": {
        "jet_fuel": 500,
        "saf": 300
    },
    "rail": {
        "electric": 15,
        "diesel": 40
    },
    "maritime": {
        "marine_diesel": 80,
        "lng": 60,
        "biofuel": 40
    },
    "pipeline": {
        "electricity": 5,
        "fossil_energy": 20
    }
}

aircraft_factor = {
    "small": 1.1,
    "medium": 1.0,
    "big": 0.9
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
    ferry_type = form_data.get("ferry_type")
    train_type = form_data.get("train_type")
    bicycle_type = form_data.get("bicycle_type")
    energy_source = form_data.get("energy_source")

    if transport == "car":
        factor = efco2["car"][fuel]
        return calculate_basic_emission(kms, factor)

    elif transport == "plane":
        base_factor = efco2["plane"][flight_type][cabin_class]
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
        factor = efco2["bybane"]["default"]
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

    elif transport == "cargo_plane":
        factor = efco2["cargo_plane"][fuel]
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