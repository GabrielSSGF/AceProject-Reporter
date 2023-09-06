from datetime import datetime, timedelta
import pandas as pd

def createExcelSheets(timeSheets, apiClass):
    dadosPrimeiraSheet = []
    dadosSegundaSheet = []
    
    modifyList(timeSheets, dadosPrimeiraSheet, "First")
    modifyList(timeSheets, dadosSegundaSheet, "Second")
    
    dataFramePrimeiraSheet = pd.DataFrame(dadosPrimeiraSheet, columns=["Date", "TimeStatus", "User"])
    dataFrameSegundaSheet = pd.DataFrame(dadosSegundaSheet, columns=["Date", "TimeStatus", "User", "ProjectName", "TaskResume", "Total", "Comments"])
    
    dataFramePrimeiraSheet = dataFramePrimeiraSheet.set_index("Date").sort_values(by=["User", "Date"])
    dataFrameSegundaSheet = dataFrameSegundaSheet.set_index("Date").sort_values(by=["User", "Date"])
    
    excelWriter = pd.ExcelWriter(apiClass.DADOS_FROM_JSON['PathToReport'], engine="xlsxwriter")

    dataFrameToExcel(dataFramePrimeiraSheet, "1° Relatório", excelWriter)
    dataFrameToExcel(dataFrameSegundaSheet, "2° Relatório", excelWriter)
    
    excelWriter._save()

def modifyList(timeSheets, listaDados, listType):
    for timeSheet in timeSheets["results"]:
        timeSheetStatus_Is_SubmittedOrApproved = (timeSheet['TIME_STATUS_NAME'] == "Submitted" or timeSheet['TIME_STATUS_NAME'] == "Approved")
        if timeSheetStatus_Is_SubmittedOrApproved and listType == "First": checkWorkDayFirstSheet(listaDados, timeSheet)
        elif timeSheetStatus_Is_SubmittedOrApproved and listType == "Second": checkWorkDaySecondSheet(listaDados, timeSheet)

def checkWorkDayFirstSheet(listaDados, timeSheet):
    i = 1
    while i < 8:
        if timeSheet[f'TOTAL{i}'] > 0:
            date = getTimeSheetDate(i, timeSheet)
            timeStatus = timeSheet['TIME_STATUS_NAME']
            user = timeSheet['USERNAME']
            row = [date, timeStatus, user]
            listaDados.append(row)
        i += 1

def getTimeSheetDate(i, timeSheet):
    parsedDate = datetime.strptime(timeSheet['DATE_WEEK_START'], "%Y-%m-%dT%H:%M:%S")
    updatedDate = parsedDate + timedelta(days=i-1)
    formattedDate = updatedDate.strftime("%d/%m/%Y")
    return formattedDate

def checkWorkDaySecondSheet(listaDados, timeSheet):
    i = 1
    while i < 8:
        if timeSheet[f'TOTAL{i}'] > 0:
            date = getTimeSheetDate(i, timeSheet)
            timeStatus = timeSheet['TIME_STATUS_NAME']
            user = timeSheet['USERNAME']
            projectName = timeSheet['PROJECT_NAME']
            taskResume = timeSheet['TASK_RESUME']
            total = timeSheet[f'TOTAL{i}']
            comments = timeSheet['COMMENT']

            row = [date, timeStatus, user, projectName, taskResume, total, comments]
            listaDados.append(row)
        i += 1

def dataFrameToExcel(dataFrame, sheetName, excelWriter):
    dataFrame.to_excel(excelWriter, sheet_name=sheetName, index=True)
    worksheet = excelWriter.sheets[sheetName]
    
    if sheetName == "1° Relatório":
        worksheet.set_column("A:B", 15)
        worksheet.set_column("C:C", 25)
    else:
        worksheet.set_column("A:F", 15)
        worksheet.set_column("C:C", 23)
        worksheet.set_column("D:D", 43)
        worksheet.set_column("E:E", 74)