import apiData
from datetime import datetime

class UserGroups:
    def __init__(self, dadosAPI, timeSheets):
        global DATA_API, DATA_TIMESHEETS
        DATA_API = dadosAPI
        DATA_TIMESHEETS = timeSheets
        userNames = dadosAPI.LOWERCASE_USERNAMES
        self.SUBMITTED_USERS = self._getSubmittedUsers(userNames)
        self.SUBMITTED_AND_APPROVED_USERS = self._getSubmittedAndApprovedUsers(userNames)
        self.UNSUBMITTED_USERS = self._getUnsubmittedUsers(userNames, self.SUBMITTED_AND_APPROVED_USERS)
        self.LISTA_COLABORADORES_APROVACAO_FORMATADA, self.LISTA_COLABORADORES_SEM_SUBMISSAO_FORMATADA = self._formatarListaStatusColaboradores(self._createListaStatusColaboradores(self.UNSUBMITTED_USERS, self.SUBMITTED_USERS))
    
    def _getSubmittedUsers(self, userNames):
        submittedUsers = []
        for timeSheet in DATA_TIMESHEETS["results"]:
            usernameIntimeSheet = timeSheet["USERNAME"]
            if timeSheet["TIME_STATUS_NAME"] == "Submitted" and usernameIntimeSheet in userNames:
                submittedUsers.append(usernameIntimeSheet)
        return submittedUsers
    
    def _getSubmittedAndApprovedUsers(self, userNames):
        submittedAndApprovedUsers = []
        for timeSheet in DATA_TIMESHEETS["results"]:
            userIntimeSheet = timeSheet["USERNAME"]
            if (timeSheet["TIME_STATUS_NAME"] == "Submitted" or timeSheet["TIME_STATUS_NAME"] == "Approved") and userIntimeSheet in userNames:
                submittedAndApprovedUsers.append(userIntimeSheet)
        return submittedAndApprovedUsers
    
    def _getUnsubmittedUsers(self, userNames, submittedAndApprovedUsers):
        unsubmittedUsers = list(set(userNames) - set(submittedAndApprovedUsers))
        today = datetime.today()
        if (today.day - 7) < 0:
            diaPrimeiroMes = (today.day - 7)*-1 + 2
            self._getFirstWeekTimesheet(diaPrimeiroMes, unsubmittedUsers)
        return unsubmittedUsers
    
    def _getFirstWeekTimesheet(self, diaPrimeiroMes, unsubmittedUsers):
        i = diaPrimeiroMes
        quantidadeHorasEnviadasPrimeiraSemana = 0
        for timeSheet in DATA_TIMESHEETS["results"]:
            while i < 7:
                if timeSheet[f'TOTAL{i}'] != 0 and i < 6:
                    quantidadeHorasEnviadasPrimeiraSemana += 1
                i += 1
            if quantidadeHorasEnviadasPrimeiraSemana == 0:
                unsubmittedUsers.append(timeSheet['USERNAME'])
    
    def _createListaStatusColaboradores(self, unsubmittedUsers, submittedUsers):
        listaStatusColaboradores = []
        
        upperCaseUnsubmittedUsers = self._getUpperCaseUserNames(unsubmittedUsers, DATA_API.FULLDISPLAY_USERNAMES)
        upperCaseSubmittedUsers = self._getUpperCaseUserNames(submittedUsers, DATA_API.FULLDISPLAY_USERNAMES)
        
        for user in upperCaseSubmittedUsers:
            listaStatusColaboradores.append(user + "Aprovação pendente")
        
        for user in upperCaseUnsubmittedUsers:
            listaStatusColaboradores.append(user + "Submissão pendente")
        
        return listaStatusColaboradores

    def _getUpperCaseUserNames(self, userGroup, fullDisplayUserNames):
        nameMapping = {}

        for item in fullDisplayUserNames:
            parts = item.split(" (")
            nameMapping[parts[0].lower()] = parts[1][:-1]

        upperCaseNames = [nameMapping[name.lower()] for name in userGroup]
        
        return upperCaseNames

    def _formatarListaStatusColaboradores(self, lista):
        colaboradoresSet = set()
        colaboradoresUnicos = []

        for colaborador in lista:
            if colaborador not in colaboradoresSet:
                colaboradoresUnicos.append(colaborador)
                colaboradoresSet.add(colaborador)
                
        colaboradoresAprovacao = []
        colaboradoresSubmissao = []
        
        colaboradoresSet.clear()
        
        for colaborador in colaboradoresUnicos:
            if colaborador not in colaboradoresSet:
                colaboradoresSet.add(colaborador)
                if "Aprovação pendente" in colaborador:
                    colaboradoresAprovacao.append(colaborador)
                elif "Submissão pendente" in colaborador:
                    colaboradoresSubmissao.append(colaborador)
        
        listaAprovacaoFormatada = "\n".join([f"\t• {item.replace('Aprovação pendente', '')}" for item in colaboradoresAprovacao])
        listaSemSubmissaoFormatada = "\n".join([f"\t• {item.replace('Submissão pendente', '')}" for item in colaboradoresSubmissao])
        return listaAprovacaoFormatada, listaSemSubmissaoFormatada
