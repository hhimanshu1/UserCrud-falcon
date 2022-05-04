
import json
import falcon
import datetime
import decimal

#middleware classes for processing

#this will read the stream from the request then it will decode this data into json format
#If it cannot decode, it will return an TypeError

def json_serializer(obj):
        if isinstance(obj, datetime.datetime):
            return obj
        elif isinstance(obj, decimal.Decimal):
            return str(obj)

        raise TypeError('Cannot srrialize {!r} (type {})'.format(obj,type(obj)))


class JSONtranslator:
    def process_request(self,req,resp):
        if req.content_length in (None,0):
            return
        body= req.stream.read()

        if not body:
            raise falcon.HTTPBadRequest('Empty body request.A valid JSon document is required')

        try:
            #You can access the request data using req.context['request']
            req.context['request']=json.loads(body.decode('utf-8'))
        except (ValueError, UnicodeDecodeError):
            raise falcon.HTTPError(falcon.HTTP_753,
            'Malformed JSON . could not decode the request body.'
            'Ths JSon was incorrect or not encoded as UTF-8')


    


    def process_response(self,req,resp,resource,req_succeeded):
        if 'response' not  in resp.context:
            return
        resp.body=json.dumps(
            resp.context['response'],
            default=json_serializer
        )

    # def json_serializer(obj):
    #     if isinstance(obj, datetime.datetime):
    #         return obj
    #     elif isinstance(obj, decimal.Decimal):
    #         return str(obj)

    #     raise TypeError('Cannot srrialize {!r} (type {})'.format(obj,type(obj)))


class RequireJSON(object):
    def process_request(self,req,resp):
        if not req.client_accepts_json:
            raise falcon.HTTPNotAcceptable('This Api only support responses encoded as json',href='http://docs.examples.com/api/json')

        if req.method in ('POST','PUT'):
            if 'application/json' not in req.content_type:
                raise falcon.HTTPUnsupportedMediaType('This Api only support request encoded as json,',href='http://docs.examples.com/api/json')
