import logging
import io

import azure.functions as func
from PIL import Image, ImageDraw
from random import randint
import requests
from lxml import html
import code128

def main(req: func.HttpRequest) -> func.HttpResponse:
    UCR_CAS_USERNAME = '' # or get from request body
    UCR_CAS_PASSWORD = ''

    s = requests.Session()

    s.get("https://innosoftfusiongo.com/sso/login/login-start.php?id=124")

    cas_url = 'https://auth.ucr.edu/cas/login?service=https%3A%2F%2Finnosoftfusiongo.com%2Fsso%2Flogin%2Flogin-process-cas.php'
    resp = s.get(cas_url)
    auth = re.search(r'<input\s+type="hidden"\s+name="execution"\s+value="([^"]+)"', resp.text).group(1)
    login_data = {
        'username': UCR_CAS_USERNAME,
        'password': UCR_CAS_PASSWORD,
        'execution': auth,
        '_eventId': 'submit',
        'geolocation': None
    }
    s.post(cas_url, login_data)

    auth_token = s.get("https://innosoftfusiongo.com/sso/login/login-finish.php").headers['Fusion-Token']

    data = s.get("https://innosoftfusiongo.com/sso/api/barcode.php?id=124", headers={ "Authorization": f"Bearer {auth_token}" }).json()

    img = code128.image(data[0]['AppBarcodeIdNumber'])

    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return func.HttpResponse(img_bytes.read(), headers={"Content-Type": "image/png"})
