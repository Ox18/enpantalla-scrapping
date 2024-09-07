import requests
import re
from bs4 import BeautifulSoup

# URL del primer GET
url_get = "https://enpantallas.com/njpexnc5e3yy"
headers_get = {
    'Referer': 'https://enpantallas.com/njpexnc5e3yy',
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
    'Referer': 'https://enpantallas.com/njpexnc5e3yy',
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

print(script_tag)

## we need to remove the first and last character
### script tag is equal to
# (function(p,a,c,k,e,d){while(c--)if(k[c])p=p.replace(new RegExp('\\b'+c.toString(a)+'\\b','g'),k[c]);return p}('b 6=1n(\'1m\',{50:[{1g:"r://14-26-23.q.p/v/22/21/4z/n.27?t=4y-4x&s=1q&e=4w&f=1t&4v=4u&i=1s.1r",4t:"4s/27",4r:"4q",4p:"4o 4n 4m"}],4l:"r://14-26-23.q.p/i/22/21/4k.4j",4i:{4h:[\'4g\',\'4f\',\'4e\',\'4d\',\'4c\',\'4b\',\'4a\',\'49\',\'48\',\'47\',\'46\',\'45\',\'44\',\'43\',\'42\',\'41\']},40:{20:{},3z:{}},3y:[\'20\',\'3x\'],3w:[1,1.25,1.5,2]});6.3v(8(){1b.3u({3t:0.1,3s:5,3r:3q});$(".m-3p-1z > l").k($(\'<j>\',{h:\'#17\',a:\'#17\'})).g(\'#17\');$(".m-a-1x > l").k($(\'<j>\',{h:\'1\',a:\'w%\'})).g(\'1\');$(".m-1y-1z > l").k($(\'<j>\',{h:\'#16\',a:\'#16\'})).g(\'#16\');$(".m-1y-1x > l").k($(\'<j>\',{h:\'0.3\',a:\'30%\'})).g(\'0.3\');$(".m-3o-3n > l").k($(\'<j>\',{h:\'1\',a:\'w%\'})).g(\'1\')});b 12,13;b 3m=0,3l=0,3k=0,9=0;$.3j({3i:{\'3h-3g\':\'1c-3f\'}});6.15(\'19\',8(){1w()});6.15(\'3e\',8(){$(\'x.1v\').3d();11.1a(\'z\')});6.15(\'3c\',8(){d(5>0&&6.c()>=5&&13!=1){13=1;$(\'x.3b\').3a(\'39\')}d(6.c()>=9+5||6.c()<9){9=6.c();11.38(\'z\',37.36(9),{35:u*u*24*7})}});8 1w(){$(\'x.1v\').1u();$(\'#34\').1u();d(12)33;12=1;y=0;d(32.31===2z){y=1}$.1o(\'r://q.p/2y?1f=2x&1e=1d&2w=1t-1s-1r-1q-2v&2u=&y=\'+y,8(1p){$(\'#2t\').2s(1p)});b 9=11.1o(\'z\');d(9>0){6.c(9)}}8 2r(){1n(\'1m\').2q();b $o=$("<x />").1l({2p:"2o",1k:"w%",1j:"w%",2n:0,1h:0,1i:2m,2l:"2k(10%, 10%, 10%, 0.4)","a-2j":"2i"});$("<2h />").1l({1k:"u%",1j:"u%",1i:2g,"2f-1h":"2e"}).2d({\'1g\':\'r://q.p/?1f=2c&1e=1d\',\'2b\':\'0\',\'2a\':\'1c\'}).18($o);$o.29(8(){$(1b).1a();6.19()});$o.18($(\'#28\'))}',36,181,'||||||player||function|lastt|text|var|currentTime|if|||val|value||option|append|select|vjs||dd|com|enpantallas|https|||60||100|div|adb|ttnjpexnc5e3yy||ls|vvplay|vvad||on|303030|FFFFFF|appendTo|play|remove|this|no|njpexnc5e3yy|file_code|op|src|top|zIndex|height|width|css|vjsplayer|videojs|get|data|1725673799|53|177|91483|hide|video_ad|doPlay|opacity|bg|color|chromecast|00018|01|sv|||ukr|mp4|vplayer|click|scrolling|frameborder|upload_srt|prop|50px|margin|1000001|iframe|center|align|rgba|background|1000000|left|absolute|position|pause|showCCform|html|fviews|embed|388ff7ba7aee8c71585b7c5c4b409c52|hash|view|dl|undefined||cRAds|window|return|over_player_msg|ttl|round|Math|set|slow|fadeIn|video_ad_fadein|timeupdate|show|ended|cache|Cache|Content|headers|ajaxSetup|v2done|tott|prevt|percent|font|fg|true|enableVolumeScroll|seekStep|volumeStep|hotkeys|ready|playbackRates|html5|techOrder|airPlay|plugins|fullscreenToggle|qualitySelector|pictureInPictureToggle|audioTrackButton|subsCapsButton|descriptionsButton|chaptersButton|playbackRateMenuButton|customControlSpacer|durationDisplay|seekToLive|liveDisplay|progressControl|currentTimeDisplay|volumePanel|playToggle|children|controlBar|jpg|njpexnc5e3yy_xt|poster|kbps|574|1024x576|label|576|res|video|type|625|sp|43200|UI4W4rVyXotjUBDdRQbXU3IlGp135gjTAqLoE|7Q6Bt|njpexnc5e3yy_n|sources'.split('|')))

### lughourbdidn is from url uri

n_video = "njpexnc5e3yy" + "_n"

t = script_tag

## split with | en get the last 3th

t = t.split('|')[-4]

print(t)
