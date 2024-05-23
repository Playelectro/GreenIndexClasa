import os, json, glob

import folium
import folium.plugins
import data_manip


from shapely.geometry import Point
from shapely.geometry.polygon import Polygon as Poly

from folium.map import (Marker, LayerControl)
from folium.plugins import (MarkerCluster, Search)
from folium import Polygon
from flask import (Flask, render_template, redirect, request,
                   send_from_directory, )

from jinja2 import Template

app = Flask(__name__)

marker_list = []

area_list = []

rules = []


@app.route('/')
def index():
   return iframe(lang = "ro")
#Make german version
@app.route('/de')
def index_german():
    return iframe(lang = "ger")

@app.route('/fr')
def index_french():
    return iframe(lang = "fr")

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

@app.route('/bio')
def bio_page():
    return species_entry("bio")

@app.route('/rel')
def rel_page():
    return species_entry("rel")

@app.route('/geo')
def geo_page():
    return species_entry("geo")

@app.route('/phil')
def phil_page():
    return species_entry("phil")

@app.route('/histo')
def histo_page():
    return species_entry("histo")
    
# Define LANG continuation
def iframe(lang):
    map.get_root().render()
    header = map.get_root().header.render()
    body_html = map.get_root().html.render()
    
    click_js = """function onClick(e) {
                    $.ajax({
                        url: '',
                        type: 'get',
                        contentType: 'application/json',
                        data: {
                            click_lat: e.latlng.lat,
                            click_lon: e.latlng.lng
                        },
                        success: function(response){
                            update_page(response);
                            showSlides(0);
                        }
                    })
                }
                """
                 
    e = folium.Element(click_js)
    
    map.get_root().script._children[e.get_name()] = e
    
    script = map.get_root().script.render()
    
    args = request.args
    
    intrest_data = ""
    div_marker = "no_class"
    
    if args.get('click_lat') is not None:
    
        click_lat = float(args.get('click_lat'))
        click_lon = float(args.get('click_lon'))

        
        intrest_data = load_marker_info(click_lat, click_lon)
        
        if intrest_data is None:
            intrest_data = load_reser_info(click_lat,click_lon)
            
        if intrest_data is not None:
            div_marker = "item_first"
        print(intrest_data)
        return data_manip.format_data(intrest_data, lang)
                        
    return render_template('index.html', header = header, body_html = body_html, script = script, interest_data = intrest_data)


def load_marker_info(lat, lon):
    for marker in marker_list:
        location = marker['location']
        for i in range(0, len(location)):
            if location[i][0] == lat and location[i][1] == lon:
                return marker
    return None

def load_reser_info(lat, lon):
    for res in area_list:
        poly = Poly(res['area'])
        if poly.contains(Point(lat,lon)):
            return res
    return None


def species_entry(entry):
    
    args = request.args
    
    mrk = None
    
    if args.get('name') is not None:
        
        name = args.get('name')
        
        for marker in marker_list:
            name_mrk = marker['name']
            if name_mrk == name:
                    mrk = marker
                    
        return data_manip.format_data_gallery(mrk)
    
    params = (0, len(marker_list))
    if entry == 'bio':
        params = data_manip.get_bio_params()
    elif entry == 'geo':
        params = data_manip.get_geo_params()
    elif entry == 'rel':
        params = data_manip.get_rel_params()
    elif entry == 'phil':
        params = data_manip.get_phil_params()
    elif entry == 'histo':
        params = data_manip.get_histo_params()
    
    return render_template('species.html', list=marker_list[params[0]:params[1]])

def area_entry():
    
    args = request.args
    
    mrk = None
    
    if args.get('name') is not None:
        
        name = args.get('name')
        
        for marker in area_list:
            name_mrk = marker['name']
            if name_mrk == name:
                    mrk = marker
                    
        return data_manip.format_data_gallery(mrk)

        
    return render_template('nature_reserve.html', list=area_list)


if __name__ == '__main__':
    
    data_manip.load_icons()

    normal_layer = folium.TileLayer(name="Filters", no_wrap=True)
    
    
    map = folium.Map(
        width = "75%",
        height = "600px",
        location = [45.96268191714687, 25.891383244726377],
        zoom_start = 6.5,
        max_bounds = True,    
        tiles=normal_layer
    )
    
    marker_cluster = MarkerCluster().add_to(map)
    
    click_template = """{% macro script(this, kwargs) %}
                        var {{ this.get_name() }} = L.marker(
                            {{ this.location|tojson }},
                            {{ this.options|tojson }}
                            ).addTo({{ this._parent.get_name() }}).on('click', onClick);
                        {% endmacro %}"""

    Marker._template = Template(click_template)

                        
    click_template_p = """{% macro script(this, kwargs) %} 
                          var {{ this.get_name() }} = L.polygon(
                          {{ this.locations|tojson }},
                          {{ this.options|tojson }}
                          ).addTo({{ this._parent.get_name() }}).on('click', onClick);
                          {% endmacro %}"""
    
    folium.Polygon._template = Template(click_template_p)

    
    geography_group = folium.FeatureGroup(name="Puncte Geografice", color='green')
    animal_group = folium.FeatureGroup(name="Specii de Animale", color='brown')
    plant_group = folium.FeatureGroup(name="Specii de Plante", color='plant')
    fish_group = folium.FeatureGroup(name="Specii de Pesti", color='blue')
    battles_group = folium.FeatureGroup(name="Evenimente Istorice", color='red')
    monuments_group = folium.FeatureGroup(name="Monumente Istorice", color='brown')
    reservs_group = folium.FeatureGroup(name="Rezervatii Naturale", color='gray')
    religion_group = folium.FeatureGroup(name="Puncte Religioase", color='yellow')
    philosophy_group = folium.FeatureGroup(name="Puncte Filozofice", color='purple')
    
    
    #Read biology data + rezervations
    data_manip.read_biology_data(marker_list, marker_cluster,  animal_group, fish_group, plant_group, reservs_group)
    
    #Read geography data
    data_manip.read_geography_data(marker_list, marker_cluster,  geography_group)
    
    #Read history data
    data_manip.read_history_data(marker_list, marker_cluster,  monuments_group, battles_group)
    
    #Read religion data
    data_manip.read_religion_data(marker_list, marker_cluster, religion_group)
    
    #Read philosophy data
    data_manip.read_philosophy_data(marker_list, marker_cluster,  philosophy_group)
    
    #Order groups in list
    animal_group.add_to(map)
    plant_group.add_to(map)
    fish_group.add_to(map)
    reservs_group.add_to(map)
    
    geography_group.add_to(map)
    
    monuments_group.add_to(map)
    battles_group.add_to(map)
    
    religion_group.add_to(map)
    
    philosophy_group.add_to(map)
    
    searchnav = Search(
        layer=marker_cluster,
        placeholder="Search a species or location",
        geom_type="Point",
        collapsed=True,
        search_label="name",
        weight=3,
    ).add_to(map)

    
    app.run(host='0.0.0.0')