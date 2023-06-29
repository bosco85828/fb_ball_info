from flask import Flask, request,jsonify
from flask_restful import Api, Resource
from sqldb import get_info
from pprint import pprint
import json
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
api = Api(app)

class BallInfo(Resource):
    def get(self):
        ball_type = request.args.get('ball')
        print(ball_type)
        time_type = request.args.get('time')
        if not time_type: 
            time_type = "live"

        if ball_type: 
            if ball_type != 'all':
                temp=get_info(ball_type,time_type)
                infos={}
                if temp : 
                    for info in temp : 
                        data=json.loads(info[1])
                        infos[data['id']]=data
                print('--------')
                print(list(infos.values()))
                data=list(infos.values())

                return jsonify({'meta':{'status':'success', 'message': ''},'data':data})
            else : 
                ball_types={
                    '1':'soccer',
                    '3':'basketball',
                    '7':'baseball',
                    '5':'tennis',
                    '13':'volleyball',
                    '47':'badminton',
                    '4':'football',
                    '15':'table_tennis'
                }
                data_dict={
                    'soccer':None,
                    'basketball':None,
                    'baseball':None,
                    'tennis':None,
                    'volleyball':None,
                    'badminton':None,
                    'football':None,
                    'table_tennis':None
                }
                for ball_type in ball_types.values():
                    temp=get_info(ball_type,time_type)
                    infos={}

                    if temp : 
                        for info in temp : 
                            data=json.loads(info[1])
                            infos[data['id']]=data
                            
                    if infos : 
                        data=list(infos.values())
                        data_dict[ball_type]=data
                # pprint(data_dict)
                return jsonify({'meta':{'status':'success', 'message': ''},'data':data_dict})
                
        else : 
            return jsonify({'meta':{'status':'failed', 'message': 'Please enter the correct parameters.'}}),400
        
        # 在這裡進行你的處理邏輯
        
        return jsonify({'meta':{'status':'success', 'message': '123'}})

api.add_resource(BallInfo, '/GameMatchInfo')

if __name__ == '__main__':
    app.run('0.0.0.0',debug=True)

