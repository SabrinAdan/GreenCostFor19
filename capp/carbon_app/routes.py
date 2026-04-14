from flask import Flask, flash, redirect, render_template, Blueprint, request, url_for
from capp.models import Transport
from flask_login import current_user, login_required
from capp import db
from capp.carbon_app.carbon_methods import carbon_emission
from datetime import timedelta, datetime
from sqlalchemy import func

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


############

individual_transports = ["car", "plane", "ferry", "bus","train", "bybane", "motorcycle","bicycle", "walking" ]
business_transports = ["truck", "cargo_plane", "rail", "maritime", "pipeline"]




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
         
 
 #####################
 
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
    "cargo_plane": ["rail", "maritime"],
    "rail": ["truck", "maritime"],
    "maritime": ["rail", "truck"],
    "pipeline": ["rail"]
}
def get_alternatives(transport, user_type):
    possible = alternatives_map.get(transport, [])

    if user_type == "business":
        return [t for t in possible if t in business_transports]
    else:
        return [t for t in possible if t in individual_transports]

@carbon_app.route('/carbon_app')
def carbon_app_home():
    return render_template('carbonCalculator/carbon_app.html', title='carbon_app')


@carbon_app.route('/entry', methods=['GET', 'POST'])
@login_required
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
            co2_grams = float(kms * factor)
            co2_kg = float(co2_grams / 1000)
            results = round(co2_kg, 2)  
            
        elif transport == "plane":
            base_factor = efco2[transport][flight_type][cabin_class]
            plane_multiplier = aircraft_factor[aircraft_type]

            co2_grams = float(kms * base_factor * plane_multiplier)
            co2_kg = float(co2_grams / 1000)
            results = round(co2_kg, 2)
            
        elif transport == "ferry": 
            factor = efco2[transport][ferry_type]
            co2_grams = float(kms * factor)
            co2_kg = float(co2_grams / 1000)
            results = round(co2_kg, 2)
        
        elif transport == "bus":
            factor = efco2[transport][fuel]
            co2_grams = float(kms *factor)
            co2_kg = float(co2_grams /1000)
            results = round(co2_kg, 2)
            
        elif transport == "train":
            factor = efco2[transport][train_type]
            co2_grams = float(kms *factor)
            co2_kg = float(co2_grams /1000)
            results = round(co2_kg, 2)
            
        elif transport == "bybane": 
            factor = efco2[transport]["default"]
            co2_grams = float(kms *factor)
            co2_kg =float( co2_grams /1000)
            results = round(co2_kg, 2)
            
        elif transport == "motorcycle": 
            factor = efco2[transport][fuel]
            co2_grams = float(kms *factor)
            co2_kg = float(co2_grams /1000)
            results = round(co2_kg, 2)
            
        elif transport == "bicycle": 
            factor = efco2[transport][bicycle_type]
            co2_grams = float(kms *factor)
            co2_kg = float(co2_grams /1000)
            results = round(co2_kg, 2) 
            
        elif transport == "walking":
            factor = efco2[transport]["default"]
            co2_grams = float(kms * factor)
            co2_kg = float(co2_grams / 1000)
            results = round(co2_kg, 2)
            
        # ------- Business -------
        
        elif transport == "truck": 
            factor = efco2[transport][fuel]
            load_tons = float(load) / 1000 if load else 0
            co2_grams = float(kms * factor * load_tons)
            co2_kg = co2_grams / 1000
            results = round(co2_kg, 2)
            
            
        elif transport == "cargo_plane":
            factor = efco2[transport][fuel]
            cargo_tons = float(cargo_weight) / 1000 if cargo_weight else 0
            co2_grams = float(kms * factor * cargo_tons)
            co2_kg = float(co2_grams / 1000)
            results = round(co2_kg, 2)
            
        elif transport == "rail":
            factor = efco2[transport][fuel]
            cargo_tons = float(cargo_weight) / 1000 if cargo_weight else 0
            co2_grams = float(kms * factor * cargo_tons)
            co2_kg = float(co2_grams / 1000)
            results = round(co2_kg, 2)
            
        elif transport == "maritime":
            factor = efco2[transport][fuel]
            cargo_tons = float(cargo_weight) / 1000 if cargo_weight else 0
            co2_grams = float(kms * factor * cargo_tons)
            co2_kg = float(co2_grams / 1000)
            results = round(co2_kg, 2)
            
        elif transport == "pipeline":
            factor = efco2[transport][energy_source]
            co2_grams = float(distance * volume * factor)
            co2_kg =float( co2_grams / 1000)
            results = round(co2_kg, 2)
            
            
        if results is not None:
            entry = Transport(
                user_id=current_user.id,
                user_type=user_type,
                transport=transport,
                kms=kms,
                fuel=fuel,
                flight_type=flight_type,
                cabin_class=cabin_class,
                aircraft_type=aircraft_type,
                ferry_type=ferry_type,
                train_type=train_type,
                bicycle_type=bicycle_type,
                load=load,
                cargo_weight=cargo_weight,
                volume=volume,
                distance=distance,
                energy_source=energy_source,
                co2=results
            )

            db.session.add(entry)
            db.session.commit()
            flash("Emission entry saved successfully.", "success")
            return redirect(url_for('carbon_app.results_home',results=results,transport=transport,user_type=user_type))
            
               
        
    return render_template('carbonCalculator/entry.html',user_type=user_type, transport=transport, results=results,title='entry')


@carbon_app.route('/results')
@login_required
def results_home():
    user_type = request.args.get("user_type", "individual")
    start_date = datetime.now() - timedelta(days=5)

    entries = (
        Transport.query
        .filter_by(user_id=current_user.id, user_type=user_type)
        .filter(Transport.created_at > start_date)
        .order_by(Transport.created_at.desc())
        .order_by(Transport.transport.asc())
        .all()
    )

    latest_entry = (
        Transport.query
        .filter_by(user_id=current_user.id, user_type=user_type)
        .order_by(Transport.created_at.desc())
        .first()
    )

    latest_result = latest_entry.co2 if latest_entry else 0
    latest_transport = latest_entry.transport if latest_entry else "-"

    emissions_by_transport = (
        db.session.query(func.sum(Transport.co2), Transport.transport)
        .filter(Transport.user_id == current_user.id)
        .filter(Transport.user_type == user_type)
        .filter(Transport.created_at > start_date)
        .group_by(Transport.transport)
        .order_by(Transport.transport.asc())
        .all()
    )

    kms_by_transport = (
        db.session.query(func.sum(Transport.kms), Transport.transport)
        .filter(Transport.user_id == current_user.id)
        .filter(Transport.user_type == user_type)
        .filter(Transport.created_at > start_date)
        .group_by(Transport.transport)
        .order_by(Transport.transport.asc())
        .all()
    )

    emissions_by_date = (
        db.session.query(func.sum(Transport.co2), func.date(Transport.created_at))
        .filter(Transport.user_id == current_user.id)
        .filter(Transport.user_type == user_type)
        .filter(Transport.created_at > start_date)
        .group_by(func.date(Transport.created_at))
        .order_by(func.date(Transport.created_at).asc())
        .all()
    )

    kms_by_date = (
        db.session.query(func.sum(Transport.kms), func.date(Transport.created_at))
        .filter(Transport.user_id == current_user.id)
        .filter(Transport.user_type == user_type)
        .filter(Transport.created_at > start_date)
        .group_by(func.date(Transport.created_at))
        .order_by(func.date(Transport.created_at).asc())
        .all()
    )

    categories = get_categories_for_user_type(user_type)
    emission_transport = build_chart_values(emissions_by_transport, categories)
    kms_transport = build_chart_values(kms_by_transport, categories)

    dates_label = [str(date_value) for total, date_value in emissions_by_date]
    over_time_emissions = [float(total or 0) for total, date_value in emissions_by_date]

    kms_dates_label = [str(date_value) for total, date_value in kms_by_date]
    over_time_kms = [float(total or 0) for total, date_value in kms_by_date]
    
    #Alternatives 
    
    alternative_data = []
    
    if latest_entry: 
        alternatives = get_alternatives(latest_transport, user_type)
        
        for alt in alternatives: 
            if alt in efco2 and latest_entry.kms: 
                factor_data = efco2[alt]
                
                if isinstance(factor_data, dict): 
                    factor = list(factor_data.values())[0]
                else: 
                    factor = factor_data
                    
                alt_co2= (float(latest_entry.kms) *factor)/1000
                savings = max(0, latest_entry.co2 - alt_co2)
                
                alternative_data.append({"transport": alt, "co2": round(alt_co2,2), "savings": round(savings,2)})

    alternative_data = sorted(alternative_data, key=lambda x: x["co2"])
    
    return render_template(
        'carbonCalculator/results.html',
        results=latest_result,
        transport=latest_transport,
        user_type=user_type,
        entries=entries,
        categories=categories,
        emission_transport=emission_transport,
        kms_transport=kms_transport,
        dates_label=dates_label,
        over_time_emissions=over_time_emissions,
        kms_dates_label=kms_dates_label,
        over_time_kms=over_time_kms, 
        alternative_data=alternative_data
    )
    
    
#Delete emission
@carbon_app.route('/delete-emission/<int:entry_id>', methods=['POST'])
def delete_emission(entry_id):
    entry = Transport.query.get_or_404(int(entry_id))
    db.session.delete(entry)
    db.session.commit()
    flash("Entry deleted", "success")
    return redirect(url_for('carbon_app.results_home', user_type=entry.user_type))