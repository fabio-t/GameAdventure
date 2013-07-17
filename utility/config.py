'''
Created on 19/ago/2011

@author: koteko
'''

import os
from xml.dom import minidom

def parseConfigXML(level):
	fullname = os.path.join('data', level, 'config.xml')
		
	playerConf = {}
	hotConf = []
	zoneConf = {}
	
	xmlFile = minidom.parse(fullname)
	
	playerXML = xmlFile.getElementsByTagName('player')[0]
	
	playerConf['start_position'] = (playerXML.getElementsByTagName('start_position')[0].getElementsByTagName('x')[0].firstChild.data, 
					playerXML.getElementsByTagName('start_position')[0].getElementsByTagName('y')[0].firstChild.data)
	
	playerConf['ratio'] = playerXML.getElementsByTagName('ratio')[0].firstChild.data
	playerConf['side'] = playerXML.getElementsByTagName('side')[0].firstChild.data
	
	hotspotsXML = xmlFile.getElementsByTagName('hotspot')[0].getElementsByTagName('coord')
	
	for coord in hotspotsXML:
		hotConf.append([coord.getElementsByTagName('x')[0].firstChild.data, coord.getElementsByTagName('y')[0].firstChild.data,
				coord.getElementsByTagName('width')[0].firstChild.data, coord.getElementsByTagName('height')[0].firstChild.data,
				coord.getElementsByTagName('toGo')[0].firstChild.data])
	
	zoneXML = xmlFile.getElementsByTagName('zone')[0]
	
	zoneConf['type'] = zoneXML.getElementsByTagName('type')[0].firstChild.data
	
	return playerConf, hotConf, zoneConf

def parseConfigFile(level):
	fullname = os.path.join('data', level, 'config')
		
	confFile = open(fullname, 'r')
	
	player = {}
	hotspots = []
		
	while confFile:
		l = confFile.readline().strip().lower()
		
		if len(l) == 0:
			continue
		
		if "[player]" in l:
			words = l.split(" ")
			
			if words[0] == "start_position":
				player["start_position"] = (words[1], words[2])
			elif words[0] == "ratio":
				player["ratio"] = words[1]
			elif words[0] == "side":
				player["side"] = words[1]
				
		elif "[hotspots]" in l:
			while confFile:
				words = confFile.readline().strip().lower().split(" ")
				
				if len(words) != 4:
					continue
				
				hotspots.append((words[0], words[1], words[2], words[3]))
				
	confFile.close()
	
	return (player, hotspots)	
			
				