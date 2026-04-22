from flask import Flask, flash, redirect, render_template, Blueprint, request, url_for
from capp.models import Transport
from flask_login import current_user, login_required
from capp import db
import csv
from flask import Response
from io import StringIO

from capp.carbon_app.emission_functions import carbon_emission, efco2
from capp.carbon_app.table_functions import get_entries,format_entries_for_table, get_latest_entry, get_emissions_by_transport, get_kms_by_transport, get_emissions_by_date,get_kms_by_date
from capp.carbon_app.chart_functions import get_categories_for_user_type,build_chart_values,format_date_chart,get_alternatives, alternatives_map


carbon_app = Blueprint('carbon_app', __name__)


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
        form_data = {
            "kms": request.form.get("kms", type=float),
            "fuel": request.form.get("fuel"),
            "cargo_weight": request.form.get("cargo_weight", type=float),
            "load": request.form.get("load", type=float),
            "volume": request.form.get("volume", type=float),
            "distance": request.form.get("distance", type=float),
            "flight_type": request.form.get("flight_type"),
            "cabin_class": request.form.get("cabin_class"),
            "aircraft_type": request.form.get("aircraft_type"),
            "ferry_type": request.form.get("ferry_type"),
            "train_type": request.form.get("train_type"),
            "bicycle_type": request.form.get("bicycle_type"),
            "energy_source": request.form.get("energy_source"),
        }
        
        
        results = carbon_emission(transport, form_data)
        if results is not None:
            entry = Transport(
                user_id=current_user.id,
                user_type=user_type,
                transport=transport,
                kms=form_data["kms"],
                fuel=form_data["fuel"],
                flight_type=form_data["flight_type"],
                cabin_class=form_data["cabin_class"],
                aircraft_type=form_data["aircraft_type"],
                ferry_type=form_data["ferry_type"],
                train_type=form_data["train_type"],
                bicycle_type=form_data["bicycle_type"],
                load=form_data["load"],
                cargo_weight=form_data["cargo_weight"],
                volume=form_data["volume"],
                distance=form_data["distance"],
                energy_source=form_data["energy_source"],
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
    
    entries = get_entries(current_user.id, user_type)
    formatted_entries = format_entries_for_table(entries)
    
    latest_entry = get_latest_entry(current_user.id, user_type)
    
    latest_result = latest_entry.co2 if latest_entry else 0
    latest_transport = latest_entry.transport if latest_entry else "-"
    
    emissions_by_transport = get_emissions_by_transport(current_user.id, user_type)
    kms_by_transport = get_kms_by_transport(current_user.id, user_type)
    emissions_by_date = get_emissions_by_date(current_user.id, user_type)
    kms_by_date = get_kms_by_date(current_user.id, user_type)

    categories = get_categories_for_user_type(user_type)
    emission_transport = build_chart_values(emissions_by_transport, categories)
    kms_transport = build_chart_values(kms_by_transport, categories)

    dates_label, over_time_emissions = format_date_chart(emissions_by_date)
    kms_dates_label, over_time_kms = format_date_chart(kms_by_date)
    
    
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

