from flask import Flask, request,jsonify,abort,Response
from flask_restful import Api, Resource,reqparse
from sqldb import get_info
from pprint import pprint
import json
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
api = Api(app)

class BallInfo(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('ball', required=False)
    parser.add_argument('time', required=False)
    def get(self):
        arg=self.parser.parse_args()
        try : 
            ball_type = arg['ball']
            time_type = arg['time']
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
                    else: 
                        raise ValueError("There is no tournament information available for this ball type.")
                    
                    print('--------')
                    print(list(infos.values()))
                    datas=list(infos.values())
                    league_list=[]
                    league_dicts=[]
                    for data in datas : 
                        if data['league'] not in league_list :
                            league_list.append(data['league'])
                            league_dicts.append({
                                'id':None,
                                'league':data['league'],
                                'icon':data['league_icon'],
                                'matches':[]
                            })

                    i=0 #計算 datas 指標
                    j=0 #計算 league_dicts 指標

                    while True : 

                        if datas[i]['league'] == league_dicts[j]['league'] : 
                            league_dicts[j]['matches'].append(datas[i])
                        
                        if i >= (len(datas)-1) : 
                            i=0
                            j+=1

                            if j >= len(league_dicts) : 
                                break 
                        
                        else : 
                            i+=1

                    pprint(league_dicts)

                    return jsonify({'meta':{'status':'success', 'message': ''},'data':league_dicts})
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
                            datas=list(infos.values())
                            league_list=[]
                            league_dicts=[]
                            for data in datas : 
                                if data['league'] not in league_list :
                                    league_list.append(data['league'])
                                    league_dicts.append({
                                        'id':None,
                                        'league':data['league'],
                                        'icon':data['league_icon'],
                                        'matches':[]
                                    })

                            i=0 #計算 datas 指標
                            j=0 #計算 league_dicts 指標

                            while True : 

                                if datas[i]['league'] == league_dicts[j]['league'] : 
                                    league_dicts[j]['matches'].append(datas[i])
                                
                                if i >= (len(datas)-1) : 
                                    i=0
                                    j+=1

                                    if j >= len(league_dicts) : 
                                        break 
                                
                                else : 
                                    i+=1

                        else : 
                            league_dicts=None
                            
                        data_dict[ball_type]=league_dicts
                    pprint(data_dict)
                    return jsonify({'meta':{'status':'success', 'message': ''},'data':data_dict})
                    
            else :
                response=jsonify({'meta':{'status':'failed', 'message': 'Please enter the correct parameters.'}})
                response.status_code = 400
                return response
        
        except Exception as err : 
            return jsonify({'meta':{'status':'failed', 'message': str(err) },'data':None})
        # 在這裡進行你的處理邏輯
        



api.add_resource(BallInfo, '/GameMatchInfo/API.ASPX','/GameMatchInfoSQL/API.ASPX')

if __name__ == '__main__':
    app.run('0.0.0.0',debug=True)

