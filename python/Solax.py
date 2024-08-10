#!/usr/bin/python3

import requests
import FlatJson

#https://global.solaxcloud.com/proxyApp/proxy/api/getRealtimeInfo.do?tokenId=MYTOKEN&sn=REGISTRATIONNO

def read(solax_tokenid, solax_inverter):  
    try:

        #connection Solax API
        res = requests.get('https://global.solaxcloud.com/proxyApp/proxy/api/getRealtimeInfo.do?tokenId='+solax_tokenid+'&sn='+solax_inverter)
        
        result = {}
        result["status_code"] = res.status_code

        json_object = FlatJson.flatten(res.content)
        #print(json_object)
        #result["inverterSN"] = json_object['result_inverterSN']
        result["sn"] = json_object['result_sn']
        result["acpower"] = json_object['result_acpower'] #W
        result["yieldtoday"] = json_object['result_yieldtoday'] #KWh
        result["feedinpower"] = json_object['result_feedinpower'] #W
        result["feedinenergy"] = json_object['result_feedinenergy'] #KWh
        result["inverterStatus"] = json_object['result_inverterStatus']

        return result      
    except Exception as ex:
        print ("ERROR Solax: ", ex) 
