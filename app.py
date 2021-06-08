from flask import Flask, make_response, jsonify
import secrets
import logging


app = Flask(__name__)

#TODO add folder to mount to the host
fileName = "audit.log"
host="0.0.0.0"
port=8080

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(fileName),
        logging.StreamHandler()
    ]
)

#in-memory data store, for multithreading we can use a redis service. but not enough time in this round
secrets_data = {}

#return_msg will generate returned message and create audit logs
def return_msg(status_code,message={},ctx={"action":'GET',"secret_id":''}): 
    logging.info(" REQUEST: "+ ctx["action"] + " " + ctx["secret_id"] + " RESPONSE: " + str(status_code))
    return make_response(jsonify(message), status_code)

#this funcion will generate unique secrets strings
def rand_secrets_gen():
  return secrets.token_urlsafe(16) 

#generate error handler for garde 
@app.errorhandler(404)
def page_not_found(e):
    return return_msg(404,message={"restult":"Not Found"})

#generate error handler for garde 
@app.errorhandler(500)
def internal_server_error(e):
    return return_msg(500,message={"restult":"System Error"})

#handler for GET secrets
@app.route('/secrets/<secret_id>', methods=['GET'])
def get_secret(secret_id):
  ret_msg = {}
  ret_code = 200
  ctx = {'action':'GET','secret_id':secret_id}
  if secret_id not in secrets_data:
    ret_msg = {"restult":"Not Found"}
    ret_code = 404
  else:
    ret_msg = {'secret': secrets_data[secret_id]}
  return return_msg(200,message=ret_msg,ctx=ctx)

#handler for POST secrets
@app.route('/secrets/<secret_id>', methods=['POST'])
def post_secrets(secret_id):
  ret_msg = {}
  ret_code = 200
  ctx = {'action':'POST','secret_id':secret_id} 
  print('asdf')
  if secret_id in secrets_data:
    ret_code = 400
    ret_msg={"restult":"invalid key"} # will not show key exist explicitly to avoid attack 
  else:
    secrets_data[secret_id] = rand_secrets_gen()
    ret_msg = {'secret': secrets_data[secret_id]}
  return return_msg(200,message=ret_msg,ctx=ctx)

#handler for DELETE secrets
@app.route('/secrets/<secret_id>', methods=['DELETE'])
def delete_secrets(secret_id):
  ret_msg = {}
  ret_code = 200
  ctx = {'action':'DELETE','secret_id':secret_id} 
  if secret_id not in secrets_data:
    ret_code = 404
    ret_msg = {"restult":"invalid key"} # will not show key exist explicitly to avoid attack 
  else:
    del secrets_data[secret_id]
    ret_msg = {"restult":"Done"}
  return return_msg(200,message=ret_msg,ctx=ctx)


if __name__=="__main__":
  app.run(host = host, port = port)

