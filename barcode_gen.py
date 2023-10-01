import requests
import re
import code128

UCR_CAS_USERNAME = ''
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

code128.image(data[0]['AppBarcodeIdNumber']).save("ucr_gym_barcode.png")
