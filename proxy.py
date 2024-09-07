from flask import Flask, request, Response
import requests

app = Flask(__name__)

@app.route('/proxy_video/<path:url>', methods=['GET'])
def proxy_video(url):
    video_url = f"https://{url}"
    
    # Encabezados personalizados
    headers = {
        'Referer': 'https://enpantallas.com/',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'Accept-Encoding': 'identity;q=1, *;q=0',
        'Accept-Language': 'es-419,es;q=0.9',
        'Cookie': 'lang=7; fpestid=G8K_M3Ti_Lz2O0zjV5jNB0zhXJEVql0V6AIzcJibVNWEQsKvlcxyE1TmCSmk49UhO98_iw;',
        'Range': 'bytes=24772608-244185041',
    }

    # Hacer la solicitud al servidor de origen con los encabezados
    response = requests.get(video_url, headers=headers, stream=True)
    
    # Devolver la respuesta del servidor al cliente
    return Response(response.iter_content(chunk_size=1024), content_type=response.headers['Content-Type'])

if __name__ == '__main__':
    app.run(debug=True)