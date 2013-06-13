#!/usr/bin/python
# -*- coding: latin-1 -*-
#
#  test2.py - Test mit MySQL
#  
#  Copyright 2013 Mechtilde Stehmann <mechtilde@stephan>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

import os, sys

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, select

from sqlalchemy.dialects.mysql import pymysql

class test(object):
	def __init__(self):
		pass
		
	def connect_mysql(self,User,Password,Host,Database):
		filename = 'mysql+mysqldb://' + User + ':' + Password + '@' + Host + '/' + Database
		self.engine = create_engine(filename + '?charset=latin1')
		self.metadata = MetaData()
		self.metadata.bind = self.engine
		
	def create_tbl_adr(self):
		self.tab = Table('Adresse2', self.metadata,
			Column('id', Integer, primary_key = True),
			Column('Name', String(30)),
			Column('Vorname', String(30)),
			Column('StrasseNr', String(40)),
			Column('PLZ', String(10)),
			Column('Ort', String(10)),
			Column('Land', String(30)))
		self.metadata.create_all()

	def insert_adress(self, Name, Vorname, StrasseNr, PLZ, Ort, Land):
		conn = self.engine.connect()
		conn.execute(Table('Adresse2',self.metadata, autoload=True).insert(), [
			{'Name': Name, 'Vorname': Vorname, 'StrasseNr': StrasseNr, 'PLZ': PLZ, 'Ort': Ort, 'Land': Land}])

	def get_Table(self, tablename):
		tabc = Table(tablename, self.metadata, autoload=True).c
		if tablename == 'Adresse2':
			query = select([tabc.Name, tabc.Vorname, tabc.StrasseNr, tabc.PLZ, tabc.Ort, tabc.Land])
			return self.engine.execute(query)
		else:
			print("Tabelle existiert nicht")

def main():
	root = test()
	root.connect_mysql('test','test','localhost','test')
	root.create_tbl_adr()
	root.insert_adress('Schmidt','Hans', 'Löhnstr.', '12345', 'Stadt', 'Land')
	daten = root.get_Table('Adresse2')
	
	for element in daten:
		print(element['Name'])

	return 0
	
if __name__ == '__main__':
	main() 
