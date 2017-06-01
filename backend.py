import json, re

'''
Suponiendo que la DB es un archivo físico "db.json"
[{
  "id":1,
  "username":"Claudio Yacarini"
},
{
  "id":2,
  "username":"Scarlett Johansson"
},{
  "id":3,
  "username":"Ursa Warrior"
}]
'''

# Globals
DB_NAME = "db.json"


# Open the database
def read_db(db_name):
  data = None
  try:
    with open(db_name, "r") as f:
      data = f.read()
  except Exception as e:
    print ("*** Error de lectura de la DB {0}".format(e))
    return {}
  try:
     return json.loads(data)
  except Exception as e:
    print ("*** Error parseo de la DB {0}".format(e))
    return {}


# Objetos utiles para el rest
class Request:
  def __init__(self, params):
    self.params = params

class Response:
  def __init__(self, body, status):
    self.body = body
    self.status = status    


# Método get del servicio rest para consultar una colección
class Collection:
  @classmethod
  def on_get(self, req, resp):
    data_dict = read_db(DB_NAME)
    resp.body = data_dict
    resp.status = 200


# Método get del servicio rest para consultar por un recurso
class Single:
  @classmethod
  def on_get(self, req, resp, resource_id):
    data_dict = read_db(DB_NAME)
    try:
      res_index = next( index for (index, d) in enumerate(data_dict) 
                        if d["id"] == resource_id)
    except Exception as e:
      res_index = -1
  #  if resource_id in data_dict:
  #    response = data_dict.get(resource_id, None)
  #    status = 200
    if res_index > -1:
      response = data_dict[res_index]
      status = 200
    else:
      response = "*** Error 404 - {0} not found".format(resource_id)
      status = 404
    resp.body = response
    resp.status = status


# Simular las urls rest
def get_rest_collection():
  _req = Request(None)
  _resp = Response(None, None)
  Collection.on_get(_req, _resp)
  return _resp.status, _resp.body


def get_rest_resource(resource_id):
  _req = Request(None)
  _resp = Response(None, None)
  Single.on_get(_req, _resp, resource_id)
  return _resp.status, _resp.body


# Simular el render de un html
def render(html, data):
  print ("="*30)
  if html == "single":
    show_user(data)
  elif html == "collection":
    print ("---- LISTA DE USUARIOS ----")
    for user in data:
      print ("-"*27)
      show_user(user)
  else:
    print ("NO EXISTEN DATOS")
    print data
  print ("="*30)

def show_user(u_data):
  try:
    print ("ID       : [{}]".format(u_data.get("id", None)))
    print ("USERNAME : [{}]".format(u_data.get("username", None)))
  except:
    print ("*** Data inconsistente. Se espera 'dict', se recibe {0}"
                .format(type(u_data)))


# Vistas django
def view_load_userdata(user_id):
  status_code, user_data = get_rest_resource(user_id)
  if status_code == 200:
    return render("single", user_data)
  else:
    return render("404", user_data)

def view_users_list():
  status_code, list_users = get_rest_collection()
  if status_code == 200:
    return render("collection", list_users)
  else:
    return render("404", list_users)
  

if __name__ == "__main__":
  view_load_userdata(1) # Find a user
  view_load_userdata(4) # User does not exists
  view_users_list()     # Global list of users
  DB_NAME = "no_existe" # Changing failed DB
  view_users_list() 

