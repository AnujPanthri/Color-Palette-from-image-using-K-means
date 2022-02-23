from flask import *
import json
from PIL import Image
import base64
import io
import numpy as np
from get_colors import get_colors

app=Flask(__name__)


@app.route('/')  # this is a decorator

def hello_world():
    return render_template('home.html')  

@app.route('/test', methods=['GET', 'POST'])
def testfn():
    response=request.get_json()  # base64 string from javascript
    encoded=response['image']
    numofcolors=int(response['numofcolors'])
    
    encoded=encoded.split(',',1)[1]    # to remove padding
    # encoded=encoded[22:]    # to remove padding
    
    de=base64.b64decode(encoded)

    buf=io.BytesIO(de)
    img=Image.open(buf).convert("RGB")
    
    with open("C:/Users/Home/Desktop/Machine Learning/web/static/assets/img4.jpg", "rb") as image2string:
        converted_string = base64.b64encode(image2string.read())
        converted_string=converted_string.decode('utf-8')

    
    # print('img:',img.width,img.height)
    # img.show()
    img=img.resize((100,100))
    # img.show()
    img=np.array(img)
    colors,colors_support=get_colors(img,K=numofcolors)  # use K=5 for old results :( unknown cuz
    # colors,colors_support=get_colors(img,K=6,show=True)  # use K=5 for old results :( unknown cuz
    
    # print(colors)
    # print(colors_support)
    
    dominant_color_idx=np.argmax(colors_support)
    colors=rgb_hex(colors)
    colors_dict={color:int(colors_support[i]) for i,color in enumerate(colors)}  # color:color_support
    out=json.dumps(colors_dict)
    print(out)
    return out

def rgb_hex(colors):
    hex=[]
    for i in range(colors.shape[0]):
        r,g,b=colors[i] 
        hex.append( ('#{:02X}{:02X}{:02X}').format(r, g, b)  )
    return hex
if __name__=='__main__':
    app.run(debug=True)