#!/usr/bin/python3
#Author: Victor fuentes toledo
import sys
import mysql.connector
from asterisk.agi import AGI

agi = AGI()
agi.verbose("Started callrenovacion")
callerId = agi.env['agi_callerid']
agi.verbose("callerID: "+callerId)
codigo=sys.argv[1]

cnx = mysql.connector.connect(user='victor', password='victor', host='127.0.0.1', database='retem')
cursor = cnx.cursor()

'CONSULTA DE DATOS'
query_codigo = ("SELECT nombre,Apellido,Movil_corporativo,codigo from userscorp where numbercorp=" + callerId)
cursor.execute(query_codigo)
query_result = cursor.fetchall()
if query_result==[]:
    usuario =['0','0','0','0']
else:
    usuario=(list(query_result[0]))

'CONSULTA DE SESSION PREGUNTANDO EL NUMERO DE MOVIL'
query_session = ("SELECT ID,Movil_corporativo,flag_session,timer_session,flag_aviso from usuarios_session where numbercorp=" +callerId)
cursor.execute(query_session)
query_result_session = cursor.fetchall()
if query_result_session==[]:
    usuario_session =['0','0','0','0','0']
else:
    usuario_session=(list(query_result_session[0]))

if usuario[2]==callerId:
    'AUMENTO DE SESSION EN USUARIO'
    if usuario_session[2]=='1':
        sql = "UPDATE usuarios_session SET TIMER_SESSION = '30' WHERE MOVIL_CORPORATIVO = "+str(usuario_session[1])
        #print("sql update: ",sql)
        cursor.execute(sql)
        cnx.commit()
        log='llamada recibida para prorrogar el tiempo para el usuario %s %s'%(usuario[0],usuario[1])
        agi.hangup()