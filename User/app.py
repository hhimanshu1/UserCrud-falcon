from hashlib import sha1
import json
from wsgiref.simple_server import make_server
import falcon
from middleware import JSONtranslator, RequireJSON
from model import User,PeeweeConnectionMiddleware
from werkzeug.security import generate_password_hash as gph


class UserResource():
    def on_get(self,req,resp):
        try:
            users=User.select()
            user_list=[]
            for user in users:
                user_list.append(user)
            resp.body=json.dumps({
                'status':'Success',
                'result':user_list
            })
            resp.status=falcon.HTTP_200
        except Exception as e:
            resp.status=falcon.HTTP_404
            resp.body=json.dumps({
                'status':'Failed',
                'message':str(e)
            })

    def on_post(self,req,resp):
        try:
            _info=json.loads(req.stream.read())
            print(_info['username'])
            print(_info['age'])
            if User.select().where(User.username==_info['username']).exists():
                resp.body=json.dumps({
                    'status':'Failed',
                    'message':'User Already Exists'
                })
            else:
                user=User.create(
                    username=_info['username'],
                    firstName=_info['firstName'],
                    lastName=_info['lastName'],
                    age=_info['age'],
                    password=gph(_info['password'],method=sha1)
                    )
                resp.body=json.dumps({
                    'status':'Success',
                    'message':'User Created'
                })
                user.save()
                resp.status=falcon.HTTP_200
        except Exception as e:
            resp.status=falcon.HTTP_500
            resp.body=json.dumps({
                'status':'Failed',
                'message':str(e)
            })

app=falcon.API(middleware=[PeeweeConnectionMiddleware(),RequireJSON(),JSONtranslator()])
user=UserResource()

app.add_route('/user',user)
app.add_route('/user/{id}',user)
app.add_route('/user/delete/{id}',user)
app.add_route('/user/update/{id}',user)

if __name__=='__main__':
    with make_server('', 8000, app) as httpd:
        print('Serving on port 8000...')
        httpd.serve_forever()