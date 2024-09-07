import streamlit as st
import requests
from bs4 import BeautifulSoup

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
    try:
        response = requests.get(episode_link)
        response.raise_for_status()
        
        # Obtener las cookies de la respuesta
        cookies = response.cookies

        soup = BeautifulSoup(response.content, 'html.parser')

        for cookie in cookies:
            print(f"{cookie.name}: {cookie.value}")
        
        id_input = soup.find('input', {'name': 'id'}).get('value')
        fname_input = soup.find('input', {'name': 'fname'}).get('value')
        hash_input = soup.find('input', {'name': 'hash'}).get('value')

        a = 1
        
        if a == 1:
            return f"https://14-ukr-sv.enpantallas.com/v/01/00018/{id_input}_n/n.mp4?t=OUm5m2-1tnd-ZANH8VeNlkYhnL3X16o9qZc6vQvoJOM&s=1725671077&e=43200&f=91557&sp=625&i=177.53"

        referer = "https%3A%2F%2Fenpantallas.com%2Fcategory%2FPedro%2Bel%2Bescamoso%2B2%2BTemporada"
        ## post to https://enpantallas.com/njpexnc5e3yy?op=download1&usr_login=Subiendo&id=njpexnc5e3yy&fname=pedro-el-escamoso-capitulo-1.mp4&referer=https%3A%2F%2Fenpantallas.com%2Fcategory%2FPedro%2Bel%2Bescamoso%2B2%2BTemporada&hash=91483-177-53-1725667877-cb17e183a43ca7f0319ee260796d35f5 but change with values obtained from the html

        url_video_source = f"https://enpantallas.com/{id_input}?op=download1&usr_login=Subiendo&id={id_input}&fname={fname_input}&referer={referer}&hash={hash_input}"

        

    # https://14-ukr-sv.enpantallas.com/v/01/00018/njpexnc5e3yy_n/n.mp4?t=eZCzZ_aR4VaLcbNDVs4mRxRh8v11c2gepOxFJUtpmws&s=1725669207&e=43200&f=91483&sp=625&i=177.53

        ## is POST
        response = requests.post(url_video_source, cookies=cookies)

        soup_source = BeautifulSoup(response.content, 'html.parser')


        ## print in file
        with open('file_source.html', 'w') as file:
            file.write(str(soup_source))

        video_tag = soup_source.find('video', class_='vjs-tech')

        print(video_tag)

        if video_tag:
            return video_tag['src']
        return None
    except Exception as e:
        st.error(f"Error al obtener el video: {e}")
        return None

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
