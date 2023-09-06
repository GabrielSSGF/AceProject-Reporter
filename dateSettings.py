import apiData
import datetime
import datetime as dt
from datetime import time, timedelta, datetime

class DateSettings:
    def __init__(self):
        self.DIA_ATUAL, self.MES_ATUAL, self.ANO_ATUAL = self._getDataAtual()
        self.DATA_SEGUNDA_ATUAL = self._getDataSegundaSemanaAtualPreFimMes()
        self.DATA_SEGUNDA_PASSADA = self._getDataSegundaFeiraPassada()
        self.DATA_PRIMEIRO_DIA_MES = self._getPrimeiroDiaMes()
        self.PERIODO_DIA_FOR_TEMPLATE_COLABORADOR, self.DEMORA_FOR_TEMPLATE_COLABORADOR = self._getPeriodoDia("Bom dia", " ", "Boa tarde", " ainda ")
        self.PERIODO_DIA_FOR_TEMPLATE_HR, self.DEMORA_FOR_TEMPLATE_HR = self._getPeriodoDia(" ", " antes ", " novamente ", " depois ")
        
    def defineDataIncio(self, tipoRelatorio):
        if self._hojeForPrimeiroDiaUtilMes() and tipoRelatorio == "Mensal":
            dataAtual = datetime.now()
            dataInicio = dataAtual.replace(day=1)
            dataInicio = dataInicio.strftime("%Y-%m-%d")
        elif self._hojeForPrimeiroDiaUtilMes() and tipoRelatorio == "Semanal": 
            dataInicio = self.DATA_SEGUNDA_ATUAL
        else: 
            dataInicio = self.DATA_SEGUNDA_PASSADA
        return dataInicio
    
    def _getDataAtual(self):
        dataAtual = dt.datetime.now()
        diaAtual = dataAtual.strftime('%d')
        mesAtual = dataAtual.strftime("%m")
        anoAtual = dataAtual.year
        return diaAtual, mesAtual, anoAtual
    
    def _getDataSegundaSemanaAtualPreFimMes(self):
        today = datetime.today()
        dataAtual = datetime.now()
        diasDesdeSegunda = today.weekday()
        
        if diasDesdeSegunda == 0:
            diferenca_dias = dataAtual.weekday() + 7
            dataSegunda = dataAtual - timedelta(days=diferenca_dias)
        else:
            dataSegunda = today - timedelta(days=diasDesdeSegunda)
        return dataSegunda.strftime("%Y-%m-%d")

    def _getDataSegundaFeiraPassada(self):
        dataAtual = datetime.now()
        diferencaDias = dataAtual.weekday() + 7
        dataUltimaSegunda = dataAtual - timedelta(days=diferencaDias)
        return dataUltimaSegunda.strftime("%Y-%m-%d")

    def getDatasInicioFim(self, timeSheets):
        today = datetime.today()
        for i in timeSheets['results']:
            dataInicio = datetime.strptime(i['DATE_WEEK_START'], "%Y-%m-%dT%H:%M:%S")
            dataFim = dataInicio + timedelta(days=6)
            dataInicioFormatada = dataInicio.strftime("%d/%m/%Y")
            dataFimFormatada = dataFim.strftime("%d/%m/%Y")
            break
        
        if (today.day - 7) < 0:
            dataInicioFormatada = self._getPrimeiroDiaMes()  
        
        elif self._hojeForDiaPrimeiro():
            yesterday = datetime.now() - timedelta(days=1)
            dataFimFormatada = yesterday.strftime("%d/%m/%Y")
        
        return dataInicioFormatada, dataFimFormatada
        
    def _getPrimeiroDiaMes(self):
        dataAtual = datetime.now()
        primeiroDiaMes = dataAtual.replace(day=1)
        return primeiroDiaMes.strftime("%d/%m/%Y")

    def _getPeriodoDia(self, quantidadePreMeioDia, demoraPreMeioDia, quantidadePosMeioDia, demoraPosMeioDia):
        horaAtual = datetime.now().time()
        meioDia = time(12, 0)
        
        if horaAtual >= meioDia:
            quantidade = quantidadePosMeioDia
            demora = demoraPosMeioDia
        else: 
            quantidade = quantidadePreMeioDia
            demora = demoraPreMeioDia
        
        return quantidade, demora

    def _getDataOntem(self):
        dataHoje = datetime.today()
        dataOntem = dataHoje - timedelta(days=1)
        return dataOntem.strftime("%Y-%m-%d")
    
    def _hojeForDiaPrimeiro(self):
        today = datetime.today()
        if today.day == 4:
            return True
        return False
        
    def _hojeForPrimeiroDiaUtilMes(self):
        today = datetime.today()
        primeiroDiaMes = today.replace(day=1)
        if today.weekday() < 5 and today == primeiroDiaMes:
            return True
        return False