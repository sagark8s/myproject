import folium
import os
from utils.utils import console
try:
    os.mkdir('temp_html')
except:
    pass
def generate_map(data,name):
    console.log(data.columns)
    console.log(data.head(1))
    #stb_vector_data_store.{field},"productId","productName","boundary","productImage","productDescription"
    coords_list = data[3].tolist()
    title_list = data[2].tolist()
    image_list = data[4].tolist()
    product_links = data[1].tolist()
    product_desc_list = data[5].tolist()
    html_file= f"temp_html/{name}.html"
    if os.path.exists(html_file):
        return html_file
    lat,longt = "-4.58333333,55.66666666".split(',')
    lat,longt = float(lat),float(longt)
    m = folium.Map(location=(lat,longt),zoom_start=10)
    
    for coords,title,image,desc,link in zip(coords_list,title_list,image_list,product_desc_list,product_links):
        try:
            image_url = f"<img src={image}>"
            lat,longt = coords.split(',')
            lat,longt = float(lat),float(longt)
            console.log(lat,longt)
            product_link = f"""<a href="{link.replace('url: ','')}">{title}</a>"""
            desc = '\n'.join([f"""<li>{i}</li>""" for i in desc.split('.')])
            desc = f"<ul>{desc}</ul>"

            html = f"""
            <h1>{title}</h1>
            <br>
            {image_url}
            <br>
            {product_link}
            <br>
            {desc}
            """
            console.log(html)
            iframe = folium.IFrame(html=html, width=600, height=600)
            popup = folium.Popup(iframe, max_width=2650)
            folium.Marker(
            location=[lat, longt],
            popup=popup,
            ).add_to(m)
        except Exception as e:
            console.log(e)
    m.save(html_file)
    return html_file



