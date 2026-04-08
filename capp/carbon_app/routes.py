from flask import Flask, render_template, Blueprint, request

carbon_app = Blueprint('carbon_app', __name__)

efco2 = {
    # --------- Individual ------------
    "car":{
        "diesel": 229, 
        "petrol": 198,
        "electric": 59
    },
     "plane":{
        "domestic": {
            "economy": 186, 
            "business": 284, 
        },
        "international":{
            "economy": 186, 
            "business": 284, 
        },  
    },
     "ferry": {
        "passenger": 186,
        "car_ferry": 23
    },
     "bus":{
        "diesel": 30, 
        "electric": 13, 
    }, 
     "train":{
         "diesel": 91, 
         "electric":7,  
         
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
         
 

@carbon_app.route('/carbon_app')
def carbon_app_home():
    return render_template('carbonCalculator/carbon_app.html', title='carbon_app')


@carbon_app.route('/entry', methods=['GET', 'POST'])
def entry_home():
    user_type = request.args.get("user_type")
    transport = request.args.get("transport")
    results = None
   
    
    #Get the data 
    
    if request.method == "POST": 
        kms = request.form.get("kms",type=float)
        fuel = request.form.get("fuel")
        cargo_weight = request.form.get("cargo_weight", type=float)
        load = request.form.get("load", type=float)
        volume = request.form.get("volume", type=float)
        distance = request.form.get("distance", type=float)
        flight_type = request.form.get("flight_type")
        cabin_class = request.form.get("cabin_class")
        aircraft_type = request.form.get("aircraft_type")
        ferry_type = request.form.get("ferry_type")
        train_type = request.form.get("train_type")
        bicycle_type = request.form.get("bicycle_type")
        energy_source = request.form.get("energy_source")
        
        if transport == "car": 
            factor = efco2[transport][fuel]
            co2_grams = kms * factor
            co2_kg = co2_grams / 1000 
            results = round(co2_kg, 2)  
            
        elif transport == "plane":
            base_factor = efco2[transport][flight_type][cabin_class]
            plane_multiplier = aircraft_factor[aircraft_type]

            co2_grams = kms * base_factor * plane_multiplier
            co2_kg = co2_grams / 1000
            results = round(co2_kg, 2)
            
        elif transport == "ferry": 
            factor = efco2[transport][ferry_type]
            co2_grams = kms * factor
            co2_kg = co2_grams / 1000
            results = round(co2_kg, 2)
        
        elif transport == "bus":
            factor = efco2[transport][fuel]
            co2_grams = kms *factor
            co2_kg = co2_grams /1000
            results = round(co2_kg, 2)
            
        elif transport == "train":
            factor = efco2[transport][train_type]
            co2_grams = kms *factor
            co2_kg = co2_grams /1000
            results = round(co2_kg, 2)
            
        elif transport == "bybane": 
            factor = efco2[transport]["default"]
            co2_grams = kms *factor
            co2_kg = co2_grams /1000
            results = round(co2_kg, 2)
            
        elif transport == "motorcycle": 
            factor = efco2[transport][fuel]
            co2_grams = kms *factor
            co2_kg = co2_grams /1000
            results = round(co2_kg, 2)
            
        elif transport == "bicycle": 
            factor = efco2[transport][bicycle_type]
            co2_grams = kms *factor
            co2_kg = co2_grams /1000
            results = round(co2_kg, 2) 
            
        elif transport == "walking":
            factor = efco2[transport]["default"]
            co2_grams = kms * factor
            co2_kg = co2_grams / 1000
            results = round(co2_kg, 2)
            
        # ------- Business -------
        
        elif transport == "truck": 
            factor = efco2[transport][fuel]
            load_tons = float(load) / 1000 if load else 0
            co2_grams = kms * factor * load_tons
            co2_kg = co2_grams / 1000
            results = round(co2_kg, 2)
            
            
        elif transport == "cargo_plane":
            factor = efco2[transport][fuel]
            cargo_tons = float(cargo_weight) / 1000 if cargo_weight else 0
            co2_grams = kms * factor * cargo_tons
            co2_kg = co2_grams / 1000
            results = round(co2_kg, 2)
            
        elif transport == "rail":
            factor = efco2[transport][fuel]
            cargo_tons = float(cargo_weight) / 1000 if cargo_weight else 0
            co2_grams = kms * factor * cargo_tons
            co2_kg = co2_grams / 1000
            results = round(co2_kg, 2)
            
        elif transport == "maritime":
            factor = efco2[transport][fuel]
            cargo_tons = float(cargo_weight) / 1000 if cargo_weight else 0
            co2_grams = kms * factor * cargo_tons
            co2_kg = co2_grams / 1000
            results = round(co2_kg, 2)
            
        elif transport == "pipeline":
            factor = efco2[transport][energy_source]
            co2_grams = distance * volume * factor
            co2_kg = co2_grams / 1000
            results = round(co2_kg, 2)
            
               
        
    return render_template('carbonCalculator/entry.html',user_type=user_type, transport=transport, results=results,title='entry')