#!/usr/bin/python
# coding: utf-8
from flask import Flask, render_template, request
import pandas as pd
import requestdata
from sqlalchemy import create_engine

from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
import requests
import json

import base64



application = Flask(__name__)


list1=[]





@application.route('/', methods=['GET','POST'])
def entry_point2():
    try:
        list1=[]
        if request.method=='POST':
            
            engine=create_engine('mysql+pymysql://admin:12345678@database-1.cod1kdbr9qur.us-east-2.rds.amazonaws.com/Finaldb',echo=False)
            
            df1=pd.read_sql_table('GLOBALCURRENT',engine)
            #print(df1)
            
            
            
        
            
            
            if len(request.form)==1:
                song_url1=request.form['url']
            elif len(request.form)==2:
                if request.form['url']=='':    
                    song_url1=request.form['url1']
                else:
                    song_url1=request.form['url']
                    
                
                
            
            x=song_url1.split('/')
            if x[-2]=='album':
                song_url=x[-1]
                y=song_url.split('?')
                song_url2=y[0]
                r=requestdata.pora_idalbum(song_url2)
                df=pd.DataFrame(r)
                #print(df)
            elif x[-2]=='playlist':
                song_url=x[-1]
                y=song_url.split('?')
                song_url4=y[0]
                p=requestdata.pora_idplaylist(song_url4)
                df=pd.DataFrame(p)
                #print(df)
            newdf=df1[['acousticness','danceability','duration_ms','energy','instrumentalness','liveness','loudness','speechiness','tempo','valence']]
            combined_df=newdf.append(df,ignore_index = True)
            scaler = MinMaxScaler()
            floats_scaled = pd.DataFrame(scaler.fit_transform(combined_df), columns = combined_df.columns) * 0.2
            sd=pd.DataFrame(cosine_similarity(floats_scaled))
            nice_df=df1.join(pd.Series(sd[50][:-1],name='Similarity'))
            recommendations=nice_df.nlargest(5, ['Similarity'])
            recommendations.reset_index(inplace=True)
            recommendations=recommendations['id']
            #print(recommendations)
            def base64_encode(client_id,client_secret):
                encodedData = base64.b64encode(bytes(f"{client_id}:{client_secret}", "ISO-8859-1")).decode("ascii")
                authorization_header_string = f"{encodedData}"
                return(authorization_header_string)
            
            
            for i in range(len(recommendations)):
                list2=[]
                
                header_string= base64_encode('c0ab671cf54e43ce914a8aa5b116f8d6','392dbc90b09046339e0a3816d79433cd')
                headers = {
                    'Authorization': 'Basic '+header_string,
                }
                
                data = {
                    'grant_type': 'client_credentials'
                }
                
                response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
                access_token = json.loads(response.text)
                access_token = access_token['access_token']
                headers = {
                        'Authorization': 'Bearer '+access_token,
                    }
                track_response = requests.get('https://api.spotify.com/v1/tracks/'+recommendations[i], headers=headers)
                r = json.loads(track_response.text)
                
                
                list2.append(r['external_urls']['spotify'])
                list2.append(r['name'])
                
                
                list2.append(r['album']['images'][2]['url'])
                
                
                list1.append(list2)
                
        return render_template('index.html',  list1=list1)
    
        
    except:
        print("1")
        return render_template('trends.html')


@application.route('/about')
def entry_point():
    
    
    return render_template('trends.html')



if __name__ == '__main__':
    application.run(debug=True)

 
