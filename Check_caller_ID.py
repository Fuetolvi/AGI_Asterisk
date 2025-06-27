#!/usr/bin/python3
#Author: Victor fuentes toledo
import sys
import mysql.connector
from asterisk.agi import AGI

agi = AGI()
agi.verbose("Started rutinacall")
callerId = agi.env['agi_callerid']
agi.verbose("callerID: "+callerId)
codigo=sys.argv[1]


cnx = mysql.connector.connect(user='victor', password='victor', host='127.0.0.1', database='usersNumber')
cursor = cnx.cursor()

'CONSULTA DE DATOS'
query_codigo = ("SELECT nombre,Apellido,Movil_corporativo,codigo from users where numberCop=" + callerId)
cursor.execute(query_codigo)
query_result = cursor.fetchall()
if query_result==[]:
    usuario =['0','0','0','0']
else:
    usuario=(list(query_result[0]))

'CONSULTA DE SESSION PREGUNTANDO EL NUMERO DE MOVIL'
query_session = ("SELECT ID,Movil_corporativo,flag_session,timer_session,flag_aviso from users_sesions where numberCop=" +callerId)
cursor.execute(query_session)
query_result_session = cursor.fetchall()
if query_result_session==[]:
    usuario_session =['0','0','0','0','0']
else:
    usuario_session=(list(query_result_session[0]))

if usuario[2]==callerId:
    if usuario_session[2]=='0':
        'PREGUNTA CODIGO'
        'CODIGO INCORRECTO'
        if usuario[3]!=codigo:
            log='token ingresado inválido por el usuario %s %s'%(usuario[0],usuario[1])
            agi.appexec('Playback','auth-incorrect')
            agi.hangup()
        else:
            '-- CODIGO CORRECTO --'
            'COMPRUEBA LAS SESIONES ACTIVAS'
            query_check_session = ("SELECT ID from usuarios_session")
            cursor.execute(query_check_session)
            query_result_check_session = cursor.fetchall()
            'SI NO HAY SESIONES , REGISTRO EN ID 1'
            if query_result_check_session == []:
                sql = "INSERT INTO usuarios_session (ID, MOVIL_CORPORATIVO,FLAG_SESSION,TIMER_SESSION,FLAG_AVISO) VALUES (%s, %s, %s, %s, %s)"
                val = ("1",str(callerId),"1","30",'0')
                cursor.execute(sql,val)
                cnx.commit()
                log='Acceso habilitado para el usuario %s %s'%(usuario[0],usuario[1])

                'SCRIPT DE CONEXION'
                'LOG DE REGISTRO NOMBRE, APELLIDOS,ACCESO ACTIVO'
                agi.appexec('Playback','auth-thankyou')
                agi.hangup()
            else:
                'SI HAY SESIONES COMPROBAR SI HAY ALGUNA VACIA'
                ID_SESSIONS_BBDD=[]
                ID_SESSIONS=[1,2,3,4]
                for idd in range(len(query_result_check_session)):
                    #print(list(query_result_check_session[idd])[0])
                    ID_SESSIONS_BBDD.append(list(query_result_check_session[idd])[0])
                s = set(ID_SESSIONS_BBDD)
                rows_libre = [x for x in ID_SESSIONS if x not in s]
                if rows_libre ==[]:
                    rows_libre=[]
                    log = 'Todas las sesiones estan ocupadas'
                    print(log)

                    agi.appexec('Playback','please-try-call-later')
                    agi.hangup()
                else:
                    sql = "INSERT INTO usuarios_session (ID, MOVIL_CORPORATIVO,FLAG_SESSION,TIMER_SESSION,FLAG_AVISO) VALUES (%s, %s, %s, %s, %s)"
                    val = (str(rows_libre[0]), str(callerId), '1', '30','0')
                    cursor.execute(sql, val)
                    cnx.commit()
                    print("Escribiendo en ID: ", rows_libre[0])
                    log = 'Acceso habilitado para el usuario %s %s' % (usuario[0], usuario[1])
                    print(log)
                    'SCRIPT DE CONEXION'
                    'LOG DE REGISTRO NOMBRE, APELLIDOS,ACCESO ACTIVO'
                    agi.appexec('Playback','auth-thankyou')
                    agi.hangup()