import requests
import re
from bs4 import BeautifulSoup


ID_VIDEO = "h57nteb2oc29"

# URL del primer GET
url_get = f"https://enpantallas.com/{ID_VIDEO}"
headers_get = {
    'Referer': f'https://enpantallas.com/{ID_VIDEO}',
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
    'Referer': f'https://enpantallas.com/{ID_VIDEO}',
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

print(script_tag)

s = script_tag.split("vjsplayer")[1].split("|")[4]

e = script_tag.split("res|video")[1].split("|")[4]

f = script_tag.split("vjsplayer")[1].split("|")[7]

sp = script_tag.split("res|video")[1].split("|")[2]

i = 177.53

final_url = f"{url_video}/{n_video}/n.mp4?t={t}&s={s}&e={e}&f={f}&sp={f}&i={i}"

print(final_url)