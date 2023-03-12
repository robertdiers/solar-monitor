#!/usr/bin/env python

import json
import requests
import FlatJson

# _LoginURL = "https://eu.semsportal.com/api/v2/Common/CrossLogin"
_LoginURL = "https://www.semsportal.com/api/v2/Common/CrossLogin"
_PowerStationURLPart = "/v2/PowerStation/GetMonitorDetailByPowerstationId"
_RequestTimeout = 30  # seconds

_DefaultHeaders = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "token": '{"version":"","client":"ios","language":"en"}',
}

class SemsApi:
    """Interface to the SEMS API."""

    def __init__(self, username, password):
        """Init dummy hub."""
        self._username = username
        self._password = password
        self._token = None

    def test_authentication(self) -> bool:
        """Test if we can authenticate with the host."""
        try:
            self._token = self.getLoginToken(self._username, self._password)
            return self._token is not None
        except Exception as exception:
            print ("ERROR Goodwe: ", exception)
            return False

    def getLoginToken(self, userName, password):
        """Get the login token for the SEMS API"""
        try:

            # Prepare Login Data to retrieve Authentication Token
            # Dict won't work here somehow, so this magic string creation must do.
            login_data = '{"account":"' + userName + '","pwd":"' + password + '"}'
            # login_data = {"account": userName, "pwd": password}

            # Make POST request to retrieve Authentication Token from SEMS API
            login_response = requests.post(
                _LoginURL,
                headers=_DefaultHeaders,
                data=login_data,
                timeout=_RequestTimeout,
            )

            login_response.raise_for_status()

            # Process response as JSON
            jsonResponse = login_response.json()  # json.loads(login_response.text)

            # Get all the details from our response, needed to make the next POST request (the one that really fetches the data)
            # Also store the api url send with the authentication request for later use
            tokenDict = jsonResponse["data"]
            tokenDict["api"] = jsonResponse["api"]

            return tokenDict
        except Exception as exception:
            print ("ERROR Goodwe: ", exception)
            return None

    def getData(self, powerStationId, renewToken=False, maxTokenRetries=2):
        """Get the latest data from the SEMS API and updates the state."""
        try:
            # Get the status of our SEMS Power Station
            if maxTokenRetries <= 0:
                raise OutOfRetries
            if self._token is None or renewToken:
                self._token = self.getLoginToken(self._username, self._password)

            # Prepare Power Station status Headers
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "token": json.dumps(self._token),
            }

            powerStationURL = self._token["api"] + _PowerStationURLPart

            data = '{"powerStationId":"' + powerStationId + '"}'

            response = requests.post(
                powerStationURL, headers=headers, data=data, timeout=_RequestTimeout
            )
            jsonResponse = response.json()
            # try again and renew token is unsuccessful
            if jsonResponse["msg"] != "success" or jsonResponse["data"] is None:
                return self.getData(
                    powerStationId, True, maxTokenRetries=maxTokenRetries - 1
                )

            return jsonResponse["data"]
        except Exception as exception:
            print ("ERROR Goodwe: ", exception)

def read(sems_user, sems_password, sems_stationid):
    try:
        goodwe = SemsApi(sems_user,sems_password)
        data = goodwe.getData(sems_stationid)
        #print(data['inverter'])
        #print(data['inverter'][0])
        #print(data['inverter'][0]['dict']['left'])

        result = {}
        for tmp in data['inverter'][0]:
            #print(tmp)
            if tmp not in ['dict', 'next_device', 'd', 'prev_device', 'invert_full', 'points']:
                result[tmp] = data['inverter'][0][tmp]
        #for d in data['inverter'][0]['dict']['left']:
            #print(d)
            #result[d['key']] = d['value']
        #for d in data['inverter'][0]['dict']['right']:
            #print(d)
            #result[d['key']] = d['value']

        return result
    except Exception as exception:
        print ("ERROR Goodwe: ", exception)
