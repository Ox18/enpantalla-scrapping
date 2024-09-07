import streamlit as st
import requests
from bs4 import BeautifulSoup
import re


# Función para obtener las series
def scrape_series(name):
    try:
        url = f"https://enpantallas.com/?op=categories_all&name={name}"
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        series = []
        for item in soup.find_all('div', class_='vid_block'):
            title_div = item.find('div', class_='vb_title_center')
            title = title_div.find('b').text if title_div and title_div.find('b') else 'Sin título'
            image_style = item.find('a', class_='morevids')['style']
            image_url = image_style.split('url(')[-1].strip(');')
            link = item.find('a', class_='morevids')['href']
            series.append({'title': title, 'image_url': image_url, 'link': link})
        return series
    except Exception as e:
        st.error(f"Error al obtener series: {e}")
        return []

# Función para obtener capítulos de una serie
def scrape_serie_details(serie_url):
    try:
        response = requests.get(serie_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        episodes = []
        for item in soup.find_all('div', class_='videobox'):
            episode_title = item.find('a', class_='title').text
            episode_link = item.find('a', class_='title')['href']
            image_style = item.find('span', class_='video200')['style']
            image_url = image_style.split('url(')[-1].strip(');')
            episodes.append({'title': episode_title, 'link': episode_link, 'image_url': image_url})
        return episodes
    except Exception as e:
        st.error(f"Error al obtener capítulos: {e}")
        return []

# Función para obtener la URL del video MP4
def get_video_url(episode_link):
    print({episode_link})
    ID_VIDEO = episode_link.split('/')[-1]
    url_get = episode_link
    headers_get = {
        'Referer': episode_link,
        'User-Agent': 'Mozilla/5.0'
    }

    # Hacer la solicitud GET
    response_get = requests.get(url_get, headers=headers_get)

    # Parsear el HTML con BeautifulSoup
    soup = BeautifulSoup(response_get.text, 'html.parser')

    # Extraer los campos ocultos (input hidden) del formulario
    form_data = {}
    for input_tag in soup.find_all('input', type='hidden'):
        form_data[input_tag.get('name')] = input_tag.get('value')

    # Extraer el campo 'imhuman'
    form_data['imhuman'] = '✔️ CLICK HERE TO WATCH VIDEO'

    # URL de acción del formulario POST
    form_action = soup.find('form').get('action')
    url_post = f"{url_get}"

    # Encabezados para la solicitud POST
    headers_post = {
        'Referer': episode_link,
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0'
    }

    # Hacer la solicitud POST con los datos extraídos
    response_post = requests.post(url_post, headers=headers_post, data=form_data)

    ## from response_post.text extract the URL of the video in based from url part .enpantallas.com/i and acpture the first URL

    ## hazl ocon regeex
    fragmento = response_post.text
    url_img = re.search(r'\[IMG\](.*?)\[/IMG\]', fragmento).group(1)

    ## ok url is captured https://14-ukr-sv.enpantallas.com/i/01/00018/njpexnc5e3yy_t.jpg but we nee https://14-ukr-sv.enpantallas.com/i/01/00018

    url_img = url_img[:-7]
    ## url_img is now https://14-ukr-sv.enpantallas.com/i/01/00018/njpexnc5e3y but we need https://14-ukr-sv.enpantallas.com/i/01/00018
    # not work

    ## split with / and join the first 6 elements
    url_img = '/'.join(url_img.split('/')[:6]) ## CAPTURED https://14-ukr-sv.enpantallas.com/i/01/

    ## replace /i/ with /v/
    url_video = url_img.replace('/i/', '/v/')

    script_tag = re.search(r'<script type=\'text/javascript\'>eval(.*?)</script>', response_post.text, re.DOTALL).group(1)

    ## we need to remove the eval function
    script_tag = re.sub(r'eval\(.*?\)', '', script_tag)

    n_video = ID_VIDEO + "_n"

    t = script_tag.split(n_video)[0].split("|")[-2]

    s = script_tag.split("vjsplayer")[1].split("|")[4]

    e = script_tag.split("res|video")[1].split("|")[4]

    f = script_tag.split("vjsplayer")[1].split("|")[7]

    sp = script_tag.split("res|video")[1].split("|")[2]

    i = 177.53

    final_url = f"{url_video}/{n_video}/n.mp4?t={t}&s={s}&e={e}&f={f}&sp={sp}&i={i}"

    return final_url

# Aplicación con Streamlit
st.title('Scraping Dinámico de Series')

# Input para ingresar el valor de "name"
name_input = st.text_input("Introduce el valor de 'name' para buscar series:")

# Reproductor de video inicial sin contenido, se actualizará dinámicamente
video_container = st.empty()  # Creamos un espacio para el video

if name_input:
    st.write(f"Buscando series para: {name_input}")
    series_list = scrape_series(name_input)

    if series_list:
        series_titles = [series['title'] for series in series_list]
        selected_title = st.selectbox("Selecciona una serie", series_titles)
        selected_series = next(series for series in series_list if series['title'] == selected_title)

        st.image(selected_series['image_url'], width=300)
        st.markdown(f"### {selected_series['title']}")

        if st.button("Mostrar capítulos"):
            serie_url = f"{selected_series['link']}"
            episodes = scrape_serie_details(serie_url)

            if episodes:
                selected_episode_title = st.selectbox("Selecciona un capítulo", [ep['title'] for ep in episodes])
                selected_episode = next(ep for ep in episodes if ep['title'] == selected_episode_title)

                st.image(selected_episode['image_url'], width=200)
                st.write(f"Reproduciendo: {selected_episode['title']}")

                # Obtener la URL del video al seleccionar el capítulo
                video_link = f"{selected_episode['link']}"
                actual_video_url = get_video_url(video_link)

                # Actualizamos el reproductor con la URL del nuevo video
                if actual_video_url:
                    video_container.video(actual_video_url)
                else:
                    st.write("No se pudo obtener el video.")
            else:
                st.write("No se encontraron capítulos.")
    else:
        st.write("No se encontraron series.")
