
"""

@author:  Omar Guerrero
Programa que aborta cualquier codigo, recibiendo como parametro un mesaje perzonalizado
"""
#-*- coding: utf-8 -*-

import sys
import conexion.connPost as pg

def abort_post(engine,mensaje):
   pg.CierraConn(engine)
   print ('**************************************************************************************************')
   print ('****' + mensaje +'****')
   print ('**************************************************************************************************')
   sys.exit(1)

def abort_no_sql(mensaje):
   print ('**************************************************************************************************')
   print ('****' + mensaje +'****')
   print ('**************************************************************************************************')
   sys.exit(1)