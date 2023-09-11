import datetime
from datetime import datetime, timedelta
import requests
import dateSettings
import json

class APIData:
    def __init__(self):
        global DATE_CLASS
        DATE_CLASS = dateSettings.DateSettings()
        self.DADOS_FROM_JSON = self._getDataFromFile()
        self.GUID = self._getGuid(self.DADOS_FROM_JSON)
        self.FULLDISPLAY_USERNAMES = self._getUserNames(self.GUID, self.DADOS_FROM_JSON)
        self.LOWERCASE_USERNAMES = self._getLowerCaseUserNames(self.FULLDISPLAY_USERNAMES)

    def _getDataFromFile(self):
        with open('configData.json', 'r') as arquivoJson:
            dados = json.load(arquivoJson)
        return dados

    def _getGuid(self, DADOS_FROM_JSON):
        dadosFromAPI = self._requestAPI(f"https://api.aceproject.com/?fct=login&accountid={DADOS_FROM_JSON['AccountId']}&username={DADOS_FROM_JSON['UserName']}&password={DADOS_FROM_JSON['Password']}&format=json")
        guid = dadosFromAPI['results'][0]['GUID']
        return guid
        
    def _requestAPI(self, url):
        headers = {
            'Accept': 'application/json'
        }
        response = requests.get(url, headers=headers)
        dadosFromAPI = response.json()
        return dadosFromAPI

    def _getTimeSheets(self, guid, dataInicio):
        dadosFromAPI = self._requestAPI(f"https://api.aceproject.com/?fct=gettimeSheetstoapprove&guid={guid}&projectid=NULL&filtertimeSheetperiodid=NULL&filtertimeSheetlineid=NULL&filterdatefrom={dataInicio}&filterdateto=NULL&filtertimestatus=NULL&filterprojectstatus=NULL&filterprojecttypeid=NULL&filterusergroupid=NULL&filterclientid=NULL&filteruserid=NULL&filtertimetypeid=NULL&weekview=False&sortorder=NULL&pagenumber=NULL&rowsperpage=NULL&format=json")
        return dadosFromAPI

    def _getUserNames(self, guid, DADOS_FROM_JSON):
        userNames = self._getAllUserNames(guid, DADOS_FROM_JSON)
        return userNames

    def _getAllUserNames(self, guid, DADOS_FROM_JSON):
        dadosFromAPI = self._requestAPI(f"https://api.aceproject.com/?fct=getusersstats&guid={guid}&filteractive=True&format=json")
        allUsersFullDisplayName = [entry["DISPLAYED_NAME"] for entry in dadosFromAPI["results"]]
        userFullDisplayName = self._removeManagerUserNames(allUsersFullDisplayName, DADOS_FROM_JSON)
        return userFullDisplayName
    
    def _removeManagerUserNames(self, userFullDisplayName, DADOS_FROM_JSON):
        managersUserNames = DADOS_FROM_JSON["ManagersToRemoveFromBilling"]
        print(managersUserNames)
        for i in managersUserNames:
            if i in userFullDisplayName:
                userFullDisplayName.remove(i)
        return userFullDisplayName
    
    def _getLowerCaseUserNames(self, userNames):
        lowerCaseUserNames = [name.split()[0] for name in userNames]
        return lowerCaseUserNames
