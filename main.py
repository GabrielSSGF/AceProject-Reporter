import apiData
import dateSettings
import emailSending
import excelCreation
import userGroups

def main():
    dateClass = dateSettings.DateSettings()
    if dateClass._hojeForPrimeiroDiaUtilMes():
        geraRelatorio('Mensal', dateClass)
        geraRelatorio('Semanal', dateClass)
    else: geraRelatorio('Semanal', dateClass)

def geraRelatorio(periodo, dateClass):
    apiClass = apiData.APIData() 
    timeSheets = apiClass._getTimeSheets(apiClass.GUID, dateClass.defineDataIncio(periodo))
    excelCreation.createExcelSheets(timeSheets, apiClass)
    userClass = userGroups.UserGroups(apiClass, timeSheets)
    emailSending.enviarEmail(userClass, apiClass, dateClass, timeSheets, periodo)
    
if __name__ == '__main__':
    main()