import jwt
from datetime import datetime, timedelta

class Auth():
	def __init__(self):
		# todo criar hash de verdade
		self.hashjwt = "7263723672sdsd9"

	def generate_auth_token(self, data, exp=30, time_exp=False):
	    if time_exp == True:
	        date_time = data['exp']
	    else:
	        date_time = datetime.utcnow() + timedelta(minutes=exp)
	    
	    dict_jwt = {
	        'username': data['username'],
	        'senha': data['senha'],
	        'exp': date_time
	    }
	    
	    access_token = jwt.encode(dict_jwt, self.hashjwt, algorithm="HS256")
	    
	    return access_token

	def verify_auth_token(self, token):
	    status = 401
	    try:
	        jwt.decode(token, self.hashjwt, algorithm="HS256")
	        message = "Token Válido"
	        status = 200
	    except jwt.ExpiredSignatureError:
	        message = "Token expirado, realize um novo login"
	    except:
	        message = "Token Inválido"
	    return {
	        'message': message,
	        'status': status
	    }