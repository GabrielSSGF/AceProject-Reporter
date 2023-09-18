from datetime import datetime, timedelta, time
import datetime as dt
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import smtplib

def enviarEmail(dadosUserGroups, dadosAPIData, dadosData, dadosTimeSheets, tipoPeriodo):
    global USER_CLASS, API_CLASS, DATE_CLASS, TIMESHEETS, PERIODO_TEMPO
    TIMESHEETS = dadosTimeSheets
    DATE_CLASS = dadosData
    API_CLASS = dadosAPIData
    USER_CLASS = dadosUserGroups
    if tipoPeriodo == "Mensal":
        PERIODO_TEMPO = " neste mês"
    PERIODO_TEMPO = " nesta semana"
    verificaHorario(tipoPeriodo)
    
def verificaHorario(tipoPeriodo):
    agora = dt.datetime.now()
    horaAtual = agora.hour
    if horaAtual == 9: verificaUnsubmittedUsers()
    elif horaAtual == 12: 
        verificaUnsubmittedUsers()
        enviarEmailTipo("Relatório RH", "")
    elif horaAtual == 17 and tipoPeriodo == 'Mensal':
        enviarEmailTipo("Relatório RH", "")
    else:
        enviarEmailTipo("Relatório RH", "")
        enviarEmailTipo("Aprovação", "")

def verificaUnsubmittedUsers():
    unsubmittedUsers = USER_CLASS.UNSUBMITTED_USERS
    if unsubmittedUsers:
        for user in unsubmittedUsers:
            enviarEmailTipo("Cobrança", user)

def enviarEmailTipo(tipoEmail, colaborador): 
    remetente, destinatarios = setRemetenteDestinatario(tipoEmail, colaborador)
    assunto = setAssuntoEmail(tipoEmail)
    estruturaEmail = setEmailStructure(remetente, destinatarios, assunto)
    setSMTPServer(remetente, estruturaEmail)
    
def setAssuntoEmail(tipoEmail):
    if tipoEmail == "Cobrança": assunto = "Time Card"
    elif tipoEmail == "Aprovação": assunto = "Aprovação do Time Card_Equipe"
    else: assunto = f"Relatórios TimeCard AceProject - {DATE_CLASS.DIA_ATUAL}/{DATE_CLASS.MES_ATUAL}/{DATE_CLASS.ANO_ATUAL}"
    return assunto 

def setRemetenteDestinatario(tipoEmail, colaborador):
    remetente = API_CLASS.DADOS_FROM_JSON['Email']
    if tipoEmail == "Cobrança":
        destinatarios = colaborador
    else: destinatarios = API_CLASS.DADOS_FROM_JSON['EmailManagers']
    return remetente, destinatarios
    
def setEmailStructure(remetente, destinatarios, assunto):
    email = MIMEMultipart()
    email['From'] = remetente
    email['Subject'] = assunto

    if assunto == "Time Card":
        corpo = templateCobrancaColaborador(destinatarios)
        email['To'] = ''.join(destinatarios + f'@{API_CLASS.DADOS_FROM_JSON["CompanyEmail"]}.com')
        email['Cc'] = API_CLASS.DADOS_FROM_JSON['HREmail']
    elif assunto == "Aprovação do Time Card_Equipe":
        corpo = templateAprovacaoGestor()
        email['To'] = ', '.join(destinatarios)
        email['Cc'] = API_CLASS.DADOS_FROM_JSON['HREmail']
    else:
        corpo = templateRelatoriosRH()
        email['To'] = API_CLASS.DADOS_FROM_JSON['HREmail']
        email.attach(MIMEText(corpo, 'plain'))
        with open(API_CLASS.DADOS_FROM_JSON['PathToReport'], 'rb') as anexo:
            part = MIMEApplication(anexo.read(), Name='RelatórioAce.xlsx')
            part['Content-Disposition'] = 'attachment; filename="RelatórioAce.xlsx"'
            email.attach(part)
        return email

    email.attach(MIMEText(corpo, 'plain'))
    return email

def templateCobrancaColaborador(colaborador):
    colaborador = getUpperCaseUserName(colaborador)
    dataInicioFormatada, dataFimFormatada = DATE_CLASS.getDatasInicioFim(TIMESHEETS)
    periodoDia, demora = DATE_CLASS.PERIODO_DIA_FOR_TEMPLATE_COLABORADOR, DATE_CLASS.DEMORA_FOR_TEMPLATE_COLABORADOR
    
    corpo = f"""
    {periodoDia}, {colaborador}!

    Observamos que o seu time card de {dataInicioFormatada} à {dataFimFormatada}{demora}não foi submetido, por favor regularize o mais breve possível.
    Caso não tenha trabalhado durante o período descrito acima, desconsidere este e-mail.

    Gerado por automação. NÃO RESPONDA ESTE EMAIL - EM CASO DE DÚVIDAS, CONTATAR O RH OU SEU(SUA) GESTOR(A).

    Att,
    
    RH
    
    
    """
    
    
    print(corpo)
    
    return corpo

def getUpperCaseUserName(lowerCaseUserName):
    fullDisplayUserNames = API_CLASS.FULLDISPLAY_USERNAMES
    name_mapping = {}

    for item in fullDisplayUserNames:
        parts = item.split(" (")
        name_mapping[parts[0]] = parts[1][:-1]

    if lowerCaseUserName in name_mapping:
        upperCaseUserName = name_mapping[lowerCaseUserName]
    
    return upperCaseUserName

def templateAprovacaoGestor():    
    dataInicioFormatada, dataFimFormatada = DATE_CLASS.getDatasInicioFim(TIMESHEETS)
    listaColaboradoresAprovacao, listaColaboradoresSemSubmissao = USER_CLASS.LISTA_COLABORADORES_APROVACAO_FORMATADA, USER_CLASS.LISTA_COLABORADORES_SEM_SUBMISSAO_FORMATADA
    
    corpo = f"""
    Boa tarde Gestores!

    O time card no período de {dataInicioFormatada} à {dataFimFormatada} dos colaboradores abaixo não foram aprovados, por favor, regularize o mais breve possível.

    Lista de colaboradores esperando aprovação:
    {listaColaboradoresAprovacao}

    Lista de colaboradores que não submeteram:
    {listaColaboradoresSemSubmissao}

    Gerado por automação. NÃO RESPONDA ESTE EMAIL - EM CASO DE DÚVIDAS, CONTATAR O RH.

    Att,
    
    RH
    
    """
    
    print(corpo)
    
    return corpo

def templateRelatoriosRH():
    
    listaColaboradoresSemSubmissao = USER_CLASS.LISTA_COLABORADORES_SEM_SUBMISSAO_FORMATADA
    quantidade, demora = DATE_CLASS.PERIODO_DIA_FOR_TEMPLATE_HR, DATE_CLASS.DEMORA_FOR_TEMPLATE_HR
    
    corpo = f"""
    Boa tarde, RH!

    Segue{quantidade}em anexo o arquivo contendo as planilhas do 1° e 2° relatório{PERIODO_TEMPO}.
    
    Aqui está a lista de colaboradores que não submeteram suas horas{demora}do meio dia:
    {listaColaboradoresSemSubmissao}

    Gerado por automação. NÃO RESPONDA ESTE EMAIL - EM CASO DE DÚVIDAS, CONTATAR cloud@{API_CLASS.DADOS_FROM_JSON["CompanyEmail"]}.com

    Att,
    
    Cloud Admin
    
    """
    
    print(corpo)
    
    return corpo

def setSMTPServer(remetente, estruturaEmail):
    servidor = smtplib.SMTP('smtp.office365.com', 587)
    servidor.starttls()
    servidor.login(remetente, API_CLASS.DADOS_FROM_JSON['EmailPassword'])
    texto = estruturaEmail.as_string()
    servidor.sendmail(remetente, estruturaEmail['To'], texto)
    servidor.quit()
