
import json
import folium, glob

rules = json.load(open("data/biology/recommendations/recomendations.json", encoding="utf8"))

bio_beign=0
bio_end=0

geo_begin=0
geo_end=0

histo_begin=0
histo_end=0

philo_begin=0
philo_end=0

rel_begin=0
rel_end=0

#Icon Dictionary
icons = {}

def load_icons():
    icons["bio"] = "green"
    icons["rel"] = "purple"
    icons["philo"] = "yellow"
    icons["geo"] = "beige"
    icons["histo"] = "gray" 


def get_icon(icon):
    return folium.Icon(color=icons[icon])

def format_data(data, lang):
    
    name = data['name']
    description = data['description']
    
    if lang == "fr":
        name = data['french_name']
        description = data['french_description']
        
    if lang == "ger":
        name = data['german_name']
        description = data['german_description']
    
    title = f"<h1><p align = right> {name}</p></h1>"
  #  if data.get('status') is None or len(data['status']) == 0  or data['status'].find("default") != -1:
  #      title = f"<h1>{data['name']}</h1>"
  #   else:
  #      title = f"<h1>{data['name']} - {data['status']}</h1>"
  
    suggestions = ""        
    
    #if data.get('type') is not None:
    #    if data['type'] == "Fish":
    #        suggestions = rules['fish']
    #   elif data['type'] == "Plants":
    #        suggestions = rules['plants']
    #    else:
    #        suggestions = rules['animals']

    risc = get_status(data)
    
    if len(risc) > 0:
        risc = f"<img style = \"width:100px; height:100px; \" src = \"{risc}\">" 
    
    
    if len(suggestions) > 0:
        suggestions = f"""
            <br>
            <p align=center style = "font-size:30px;">Sugestii</p>
            <ul>
                <li><p>{suggestions[0]}</p></li>
                <li><p>{suggestions[1]}</p></li>
                <li><p>{suggestions[2]}</p></li>
            </ul>
            <br>
        """
    
    
    html = f'''  
    <div class = "item_second" id = "info">
         <div class="wrapper">
            <div align = right class= "item_first">
                {title}
                {risc}
            </div>
            
            <div class = "item_second">
                 <a href="javascript:void(0)" class="infocbtn prevent-select" onclick="closeInfo()">&times;</a>
            </div>
        </div>

        <p align = left style = "width: 70%">
        {description}
        
        </p>
        
        
        {suggestions}
        
        <div class="slideshow-container">
    
            <div class="mapSlides" width = 50%>
                <img src="{data['images']}" class = "resize">
            </div>
        </div>
        <br>    
    </div>
    </div>
    </div>

    '''
    return html

#
#
#
#
#
#

# BIOLOGY
def read_biology_data(marker_list, cluster, animal_group, fish_group, plant_group, reservs_group):
    leng = 0
    global bio_beign, bio_end
    bio_beign = len(marker_list)
    for j_file in glob.glob("data/biology/protected_species/*.json"):
        if j_file.rfind('template') == -1:
            f = open(j_file, encoding = "utf8")
            js = json.load(f)
          #  f.close()
            
            #f = open(j_file.replace("data/", "data/lang/french/"), encoding="utf8")
            
           # jst = json.load(f)
            
           # js['french_name'] = jst["name"] 
           # js['french_description'] = jst["description"]
           # f.close()
            
          #  f = open(j_file.replace("data/", "data/lang/german/"), encoding="utf8")
          #  jst = json.load(f)
            
         #   js['german_name'] = jst["name"]
           # js['german_description'] = jst["description"]
            
            i = 0
            
            spec = None
            #change to be just biology group
            while i < len(js['location']):
                if js['type'] == 'Animal':
                    spec = folium.Marker(location = js['location'][i], tooltip = js['name'], name = js['name'],icon = get_icon("bio"))
                    animal_group.add_child(spec)
                elif js['type'] == 'Fish':
                    spec = folium.Marker(location = js['location'][i], tooltip = js['name'], name = js['name'],icon = get_icon("bio"))
                    fish_group.add_child(spec)
                elif js['type'] == 'Plant':
                    spec = folium.Marker(location = js['location'][i], tooltip = js['name'], name = js['name'],icon = get_icon("bio"))
                    plant_group.add_child(spec)
                i+=1
                spec.add_to(cluster)
            marker_list.append(js)

            leng+=1            
            f.close()

    for j_file in glob.glob("data/biology/reservations/*.json"):
        if j_file.rfind('template') == -1:
            f = open(j_file, encoding="utf8")
            js = json.load(f)
            f.close()
            
          #  f = open(j_file.replace("data/", "data/lang/french/"), encoding="utf8")
          #  jst = json.load(f)
            
         #   js['french_name'] = jst["name"] 
         #   js['french_description'] = jst["description"]
         #   f.close()
            
         #   f = open(j_file.replace("data/", "data/lang/german/"), encoding="utf8")
        #    jst = json.load(f)
            
          #  js['german_name'] = jst["name"]
          #  js['german_description'] = jst["description"]
            
            poly = folium.Marker(location= js['location'][0], tooltip=js['name'], name=js['name'],icon = get_icon("bio"))
            reservs_group.add_child(poly)
            marker_list.append(js)
            poly.add_to(cluster)
            
            leng+=1
            f.close()
    bio_end = bio_beign + leng

# HISTORY   
def read_history_data(marker_list, cluster, monument_group, battles_group):
    length = 0
    global histo_begin, histo_end
    histo_begin = len(marker_list)
    for j_file in glob.glob("data/history/events/*.json"):
        if j_file.rfind('template') == -1:
            f = open(j_file, encoding = "utf8")
            js = json.load(f)
            i = 0
            
            spec = None
            
            while i < len(js['location']):
                spec = folium.Marker(location = js['location'][i], tooltip = js['name'], name = js['name'],icon = get_icon("histo"))
                battles_group.add_child(spec)
                spec.add_to(cluster)
                i+=1
            
            
            marker_list.append(js)
            length += 1
            f.close()
            
    for j_file in glob.glob("data/history/monuments/*.json"):
        if j_file.rfind('template') == -1:
            f = open(j_file, encoding = "utf8")
            js = json.load(f)
            i = 0
            
            spec = None
            
            while i < len(js['location']):
                spec = folium.Marker(location = js['location'][i], tooltip = js['name'], name = js['name'],icon = get_icon("histo"))
                monument_group.add_child(spec)
                spec.add_to(cluster)
                i+=1
            
            
            marker_list.append(js)
            length += 1
            f.close()
    histo_end = histo_begin + length

# RELIGION
def read_religion_data(marker_list, cluster, religion_group):
    length = 0
    global rel_begin, rel_end
    rel_begin = len(marker_list)
    
    for j_file in glob.glob("data/religion/*.json"):
        if j_file.rfind('template') == -1:
            f = open(j_file, encoding = "utf8")
            js = json.load(f)
            i = 0
            
            spec = None
            
            while i < len(js['location']):
                spec = folium.Marker(location = js['location'][i], tooltip = js['name'], name = js['name'],icon = get_icon("rel"))
                religion_group.add_child(spec)
                spec.add_to(cluster)
                i+=1
                marker_list.append(js)
            length +=1
            f.close()
    rel_end = rel_begin + length


# PHILOSOPHY
def read_philosophy_data(marker_list, cluster, philosophy_group):
    length = 0
    global philo_begin, philo_end
    philo_begin = len(marker_list)
    
    for j_file in glob.glob("data/philosophy/*.json"):
        if j_file.rfind('template') == -1:
            f = open(j_file, encoding = "utf8")
            js = json.load(f)
            i = 0
            
            spec = None
            
            while i < len(js['location']):
                spec = folium.Marker(location = js['location'][i], tooltip = js['name'], name = js['name'],icon = get_icon("philo"))
                philosophy_group.add_child(spec)
                spec.add_to(cluster)
                i+=1
            
            
            marker_list.append(js)
            length+=1
            f.close()
    philo_end = philo_begin + length

# GEOGRAPHY
def read_geography_data(marker_list, cluster, geography_group):
    length = 0
    global geo_begin, geo_end
    geo_begin = len(marker_list)
    
    for j_file in glob.glob("data/geography/*.json"):
        if j_file.rfind('template') == -1:
            f = open(j_file, encoding = "utf8")
            js = json.load(f)
            i = 0
            
            spec = None
            
            while i < len(js['location']):
                spec = folium.Marker(location = js['location'][i], tooltip = js['name'], name = js['name'],icon = get_icon("geo"))
                geography_group.add_child(spec)
                spec.add_to(cluster)
                i+=1
            
            
            marker_list.append(js)
            length +=1
            f.close()
    geo_end = geo_begin + length

def format_data_gallery(data):
    
    title = f"<h1>{data['name']}</h1>"


    risc = get_status(data)
   
    
    if len(risc) > 0:
        risc = f"<img style = \"width:100px; height:100px; \" src = \"{risc}\">" 
    
    
    html = f'''  
    <div class = "item_second" id = "info">
         <div class="wrapper">
            <div align = right class= "item_first">
                {title}
                {risc}
            </div>
            
            <div class = "item_second">
                 <a href="javascript:void(0)" class="infocbtn prevent-select" onclick="closeInfo()">&times;</a>
            </div>
        </div>

        <p align = left style = "width: 70%">
        {data['description']}
        
        </p>
        
        <div align=center style = "width: 35%">

            <img src="{data['images']}" style="width:100%; height:300px;">
            
        </div>
        <br>
        
    </div>
        
    </div>
    </div>
    </div>

    '''
    return html


def get_status(data):
    if data.get('status') is not None:
        if data['status'] == "Risc Scazut":
            return "/static/images/Lc.jpg"
        elif data['status'] == "Aproape de pericol":
            return "/static/images/Nt.jpg"
        elif data['status'] == "Vulnerabil":
            return "/static/images/Vu.jpg"
        elif data['status'] == "In pericol":
            return "/static/images/En.jpg"
        elif data['status'] == "Critic":
            return "/static/images/Cr.jpg"
        elif data['status'] == "Extinct in salbaticie":
            return "/static/images/Ew.jpg"
        elif data['status'] == "Extint":
            return "/static/images/Ex.jpg"
    return ""

def get_bio_params():
    return (bio_beign, bio_end)

def get_rel_params():
    return (rel_begin, rel_end)

def get_geo_params():
    return (geo_begin, geo_end)

def get_histo_params():
    return (histo_begin, histo_end)

def get_phil_params():
    return (philo_begin, philo_end)