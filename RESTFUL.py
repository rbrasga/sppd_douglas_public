###After we upload the top 1000 teams, enable refreshing the teams that top 1000 players are on!
###If the team member was updated within the last 12 hours, don't query again.

import datetime, time, sys
import random
import requests
import json
from api import SPPD_API
import HELPER_DB
import traceback
import DATABASE

EndpointTarget = "http://localhost:5002"
SPPD_API.setUsernamePassword("<email address>","<password>")

def doCleanup():
	HOST=f'{EndpointTarget}/cleanup'
	r = requests.get(HOST)
	response_body=r.text
	print("doCleanup: " + response_body.strip("\n"))
	
def getAllEvents():
	result = SPPD_API.getAllEvents()
	print(result)
	events=processAllEvents(result)
	if len(events) > 0:
		uploadEvents(events)
	return len(events) > 0
		
def getAllEvents_two():
	result = SPPD_API.getAllEvents()
	print(result)
	events=processAllEvents_two(result)
	if len(events) > 0:
		uploadEvents_two(events)
	return len(events) > 0
		
def uploadEvents(events):
	HOST=f'{EndpointTarget}/insert_events'
	payload = {}
	# EVENTID : [NAME,TYPE,TEAM,start,end]
	payload["EVENTS"]=events
	payload_str=json.dumps(payload)
	r = requests.post(HOST, data=payload_str)
	response_body=r.text
	print("uploadEvents: " + response_body.strip("\n"))
	
def uploadEvents_two(events):
	HOST=f'{EndpointTarget}/insert_events_two'
	payload = {}
	# EVENTID : [NAME,TYPE,TEAM,start,end]
	payload["EVENTS"]=events
	payload_str=json.dumps(payload)
	r = requests.post(HOST, data=payload_str)
	response_body=r.text
	print("uploadEvents_two: " + response_body.strip("\n"))
	

def processAllEvents(json_string):
	#print(json_string)
	event_list={}
	result={}
	try:
		result = json.loads(json_string)
	except Exception as e:
		print(str(e))
	if type(result) != dict: return event_list
	if "events" not in result.keys(): return event_list
	result=result["events"]
	if type(result) != list: return event_list
	if len(result) < 1: return event_list
	for event in result:
		if type(event) == dict and \
			"event_id" in event.keys() and \
			"event_name" in event.keys() and \
			"event_type_id" in event.keys() and \
			"start_time" in event.keys() and \
			"end_time" in event.keys() and \
			"tiered_rewards" in event.keys():
			#EVENTID : [NAME,TYPE,TEAM,start,end]
			event_id=event["event_id"]
			event_name=event["event_name"]
			event_type_id=event["event_type_id"]
			TEAM=0
			if "team_tiered_rewards" in event.keys():
				TEAM=1
			PACK_DATA=[]
			tiered_rewards=event["tiered_rewards"]
			for elem in tiered_rewards:
				if "score" in elem:
					PACK_DATA.append(elem["score"])
			start_time=event["start_time"]
			end_time=event["end_time"]
			event_list[event_id]=[event_name,event_type_id,TEAM,start_time,end_time,PACK_DATA]
	return event_list
	
def getOnePack(elem,pack_num,is_team):
	'''
	one_pack = [
		team_pack,pack_num,score,
		CARDS0,CARDSP0, #common
		CARDS1,CARDSP1, #rare
		CARDS2,CARDSP2, #epic
		CARDS3,CARDSP3, #legendary
		CUR1,CUR2,CUR3, #Coins, Cash, PVP, POOF
		UPS0,UPSP0, #bronze
		UPS1,UPSP1, #silver
		UPS2,UPSP2, #gold
		reward_pack
	]
	'''
	one_pack = [
		is_team,pack_num,0,
		0,0,
		0,0,
		0,0,
		0,0,
		0,0,0,0,
		0,0,
		0,0,
		0,0,
		[]
	]
	if "score" in elem:
		one_pack[2] = elem["score"]
	if "gacha_data" in elem:
		if "cards" in elem["gacha_data"]:
			op_index=3
			for x in ["0","1","2","3"]:
				if x in elem["gacha_data"]["cards"]:
					if "min" in elem["gacha_data"]["cards"][x]:
						one_pack[op_index]=elem["gacha_data"]["cards"][x]["min"]
					if "p" in elem["gacha_data"]["cards"][x]:
						one_pack[op_index+1]=100*elem["gacha_data"]["cards"][x]["p"]
				op_index+=2
		if "currency" in elem["gacha_data"]:
			op_index=11
			for x in ["213","214","253", "264"]:
				if x in elem["gacha_data"]["currency"]:
					if "min" in elem["gacha_data"]["currency"][x]:
						one_pack[op_index]=elem["gacha_data"]["currency"][x]["min"]
				op_index+=1
		if "upgrades" in elem["gacha_data"]:
			op_index=15
			for x in ["0","1","2"]:
				if x in elem["gacha_data"]["upgrades"]:
					if "min" in elem["gacha_data"]["upgrades"][x]:
						one_pack[op_index]=elem["gacha_data"]["upgrades"][x]["min"]
					if "p" in elem["gacha_data"]["upgrades"][x]:
						one_pack[op_index+1]=100*elem["gacha_data"]["upgrades"][x]["p"]
				op_index+=2
	if "contents" in elem:
		reward_pack = []
		if "cards" in elem["contents"] and len(elem["contents"]["cards"]) > 0:
			for card in elem["contents"]["cards"]:
				if "id" in card and "quantity" in card:
					reward_pack.append({card["id"] : card["quantity"]})
		if "balance" in elem["contents"] and len(elem["contents"]["balance"]) > 0:
			for balance in elem["contents"]["balance"]:
				if "code" in balance and "value" in balance:
					reward_pack.append({balance["code"] : balance["value"]})
		if "items" in elem["contents"] and len(elem["contents"]["items"]) > 0:
			index = 0
			while index < len(elem["contents"]["items"]):
				if index+1 < len(elem["contents"]["items"]):
					item_id = elem["contents"]["items"][index]
					quantity = elem["contents"]["items"][index+1]
					reward_pack.append({item_id : quantity})
				index+=2
		if "gear" in elem["contents"] and len(elem["contents"]["gear"]) > 0:
			reward_pack.append({10000 : len(elem["contents"]["gear"])})
		one_pack[-1] = reward_pack
	return one_pack
	
def processAllEvents_two(json_string):
	event_list={}
	result={}
	try:
		result = json.loads(json_string)
	except Exception as e:
		print(str(e))
	if type(result) != dict: return event_list
	if "events" not in result.keys(): return event_list
	result=result["events"]
	if type(result) != list: return event_list
	if len(result) < 1: return event_list
	for event in result:
		if type(event) == dict and \
			"event_id" in event.keys() and \
			"event_type_id" in event.keys() and \
			"start_time" in event.keys() and \
			"end_time" in event.keys() and \
			"tiered_rewards" in event.keys():
			#EVENTID : [NAME,TYPE,TEAM,start,end]
			event_id=event["event_id"]
			event_name="Unknown"
			if "desc" in event and "title" in event["desc"]:
				event_name=event["desc"]["title"]
			elif "event_name" in event:
				event_name=event["event_name"]
			event_type_id=event["event_type_id"]
			PACK_DATA=[]
			TEAM=0
			if "team_tiered_rewards" in event.keys():
				pack_num=1
				for elem in event["team_tiered_rewards"]:
					PACK_DATA.append(getOnePack(elem,pack_num,1))
					pack_num+=1
			pack_num=1
			for elem in event["tiered_rewards"]:
				PACK_DATA.append(getOnePack(elem,pack_num,0))
				pack_num+=1
			start_time=event["start_time"]
			end_time=event["end_time"]
			event_list[event_id]=[event_name,event_type_id,TEAM,start_time,end_time,PACK_DATA]
	return event_list
	
#BINDS
def bindWord(dServer,dWord,dType,dContent,author=None,command_id=None):
	HOST=f'{EndpointTarget}/bind_word'
	payload = {}
	payload["DSERVER"]=dServer
	payload["DWORD"]=dWord
	payload["DTYPE"]=dType
	payload["DCONTENT"]=dContent
	payload["CREATOR"]=author
	if command_id != None:
		payload["DISCORDID"]=command_id
	payload_str=json.dumps(payload)
	r = requests.post(HOST, data=payload_str)
	response_body=r.text
	print("bindWord: " + response_body.strip("\n"))
	try:
		return int(response_body) > 0
	except:
		pass
	return False
	
def unbindWord(dServer,dWord):
	HOST=f'{EndpointTarget}/unbind_word'
	payload = {}
	payload["DSERVER"]=dServer
	payload["DWORD"]=dWord
	payload_str=json.dumps(payload)
	r = requests.post(HOST, data=payload_str)
	response_body=r.text
	print("unbindWord: " + response_body.strip("\n"))
	try:
		return int(response_body) > 0
	except:
		pass
	return False
	
#USERS
def updatePastNames():
	HOST=f'{EndpointTarget}/update_past_names'
	payload = {}
	payload_str=json.dumps(payload)
	r = requests.post(HOST, data=payload_str)
	response_body=r.text
	print("updatePastNames: " + response_body.strip("\n"))

def deleteAccount(index,okta_id):
	HOST=f'{EndpointTarget}/delete_account'
	payload = {}
	payload["INDEX"]=index
	payload["OKTAID"]=okta_id
	payload_str=json.dumps(payload)
	r = requests.post(HOST, data=payload_str)
	response_body=r.text
	print("deleteAccount: " + response_body.strip("\n"))

def optoutAccount(index,okta_id):
	HOST=f'{EndpointTarget}/optout_account'
	payload = {}
	payload["INDEX"]=index
	payload["OKTAID"]=okta_id
	payload_str=json.dumps(payload)
	r = requests.post(HOST, data=payload_str)
	response_body=r.text
	print("optoutAccount: " + response_body.strip("\n"))

def setPrimaryAccount(index,okta_id):
	HOST=f'{EndpointTarget}/primary_account'
	payload = {}
	payload["INDEX"]=index
	payload["OKTAID"]=okta_id
	payload_str=json.dumps(payload)
	r = requests.post(HOST, data=payload_str)
	response_body=r.text
	print("setPrimaryAccount: " + response_body.strip("\n"))
	
def uploadAccount(user_id, okta_id):
	HOST=f'{EndpointTarget}/login_users'
	payload = {}
	payload["USERID"]=user_id
	payload["OKTAID"]=okta_id
	payload_str=json.dumps(payload)
	r = requests.post(HOST, data=payload_str)
	response_body=r.text
	print("uploadAccount: " + response_body.strip("\n"))
	return response_body
	
def uploadUser(user_ids_to_names, hint=None):
	HOST=f'{EndpointTarget}/users'
	payload = {}
	payload["USERIDS"]=user_ids_to_names
	payload["HINT"]=hint
	payload_str=json.dumps(payload)
	r = requests.post(HOST, data=payload_str)
	response_body=r.text
	print("uploadUser: " + response_body.strip("\n"))
	
def uploadUserPlatform(user_ids_to_names, hint=None):
	HOST=f'{EndpointTarget}/users_platform'
	payload = {}
	payload["USERIDS"]=user_ids_to_names
	payload["HINT"]=hint
	payload_str=json.dumps(payload)
	r = requests.post(HOST, data=payload_str)
	response_body=r.text
	print("uploadUserPlatform: " + response_body.strip("\n"))
	
def uploadUserDetails(key, team_id, user_details, deck):
	HOST=f'{EndpointTarget}/user_details'
	payload = {}
	payload["USERID"]=key
	payload["TEAMID"]=team_id
	payload["USER_DETAILS"]=user_details
	payload["DECK"]=deck
	payload_str=json.dumps(payload)
	r = requests.post(HOST, data=payload_str)
	response_body=r.text
	print("uploadUserDetails: " + response_body.strip("\n"))
	
#COLLECTIONS
def processUpgrades(level, upgrades):
	if upgrades == None or "/" not in upgrades: return 0
	split_str=upgrades.split("/")
	min_upgrades = int(split_str[0])
	max_upgrades = int(split_str[1])
	wal_map=DATABASE.WAL_MAP[level]
	if wal_map[1] != max_upgrades: return 0
	cur_upgrades=min_upgrades-wal_map[0]
	if cur_upgrades < 0: cur_upgrades=0
	if cur_upgrades > max_upgrades - wal_map[0]: cur_upgrades = max_upgrades - wal_map[0]
	return cur_upgrades
		
def processCollectionsData(user_id, data, cur_collection):
	cards_to_update={} #card_id : {'l': level, 'u': upgrades}, ...
	for elem in data:
		#Example: { 'id': 'Dogpoo', 'Cost': 3, 'Level': 0, 'Upgrades': '0/0' }
		card_name=elem['id'].lower()
		level=elem['Level']
		if level != None:
			old_level=0
			old_upgrades=0
			if card_name in cur_collection:
				#Need to check if it's already in the list
				old_level,old_upgrades=cur_collection[card_name]
			#Need to get the raw number of upgrades
			upgrades=processUpgrades(level,elem['Upgrades'])
			if level != old_level or old_upgrades != upgrades:
				card_id=DATABASE.LOWER_NAME_TO_ID[card_name]
				if "spell" in DATABASE.DECK_MAP[card_id]: upgrades=0
				cards_to_update[card_id]={'l': level, 'u': upgrades}
	if len(cards_to_update) > 0:
		uploadCollection(user_id, cards_to_update)
	
def uploadCollection(user_id, cards):
	HOST=f'{EndpointTarget}/collections'
	payload = {}
	payload["USERID"]=user_id
	payload["CARDS"]=cards
	payload_str=json.dumps(payload)
	r = requests.post(HOST, data=payload_str)
	response_body=r.text
	print("uploadCollection: " + response_body.strip("\n"))
	
def uploadCardComparisonData(team_id, cards):
	HOST=f'{EndpointTarget}/card_comparison_data'
	payload = {}
	payload["TEAMID"]=team_id
	payload["CARDS"]=cards
	payload_str=json.dumps(payload)
	r = requests.post(HOST, data=payload_str)
	response_body=r.text
	print("uploadCardComparisonData: " + response_body.strip("\n"))
	
def uploadBracketSubscription(email, teams):
	HOST=f'{EndpointTarget}/bracket_subscriptions'
	payload = {}
	payload["TEAMS"]=teams
	payload["EMAIL"]=email
	payload_str=json.dumps(payload)
	r = requests.post(HOST, data=payload_str)
	response_body=r.text
	print("uploadBracketSubscription: " + response_body.strip("\n"))
	
def uploadTeamApplicationData(team_id, players):
	HOST=f'{EndpointTarget}/insert_team_applications'
	payload = {}
	payload["TEAMID"]=team_id
	payload["USERS"]=players
	payload_str=json.dumps(payload)
	r = requests.post(HOST, data=payload_str)
	response_body=r.text
	print("uploadTeamApplicationData: " + response_body.strip("\n"))
	
#TEAMS
def updatePastTeams():
	HOST=f'{EndpointTarget}/update_past_teams'
	payload = {}
	payload_str=json.dumps(payload)
	r = requests.post(HOST, data=payload_str)
	response_body=r.text
	print("updatePastTeams: " + response_body.strip("\n"))
	
def uploadTeamMembers(team_id,member_list):
	HOST=f'{EndpointTarget}/team_members'
	payload = {}
	payload["TEAMID"]=team_id
	payload["USERIDS"]=member_list # { userid1 : {ROLE: ROLE, NKLEVEL: NKLEVEL, ...}, ... }
	
	payload_str=json.dumps(payload)
	r = requests.post(HOST, data=payload_str)
	response_body=r.text
	print("uploadTeamMembers: " + response_body.strip("\n"))
	
def uploadTeam(team_id, name):
	HOST=f'{EndpointTarget}/teams'
	payload = {}
	payload["TEAMID"]=team_id
	payload["NAME"]=name
	
	payload_str=json.dumps(payload)
	r = requests.post(HOST, data=payload_str)
	response_body=r.text
	print("uploadTeam: " + response_body.strip("\n"))

def uploadTVTMeta(team_id, rank_details, team_details):
	HOST=f'{EndpointTarget}/teams_report'
	payload = {}
	
	payload["TEAMID"]=int(team_id)
	payload["RANK"]=None
	if rank_details != None: payload["RANK"]=rank_details[team_id]["RANK"]
	payload["TROPHIES"]=team_details["TROPHIES"]
	payload["MEMBERS"]=team_details["MEMBERS"]
	payload["NKLEVEL"]=team_details["NKLEVEL"]
	payload["COUNTRY"]=team_details["COUNTRY"]
	payload["STATUS"]=team_details["STATUS"]
	payload["DESCRIPTION"]=team_details["DESCRIPTION"]
	
	payload_str=json.dumps(payload)
	r = requests.post(HOST, data=payload_str)
	response_body=r.text
	print("uploadTVTMeta: " + response_body.strip("\n"))

#EVENTS
def uploadEvents(events):
	HOST=f'{EndpointTarget}/insert_events'
	payload = {}
	# EVENTID : [NAME,TYPE,TEAM,start,end]
	payload["EVENTS"]=events
	payload_str=json.dumps(payload)
	r = requests.post(HOST, data=payload_str)
	response_body=r.text
	print("uploadEvents: " + response_body.strip("\n"))
	
def uploadDouglasSubscriptions(teamname,channel_id,wsid=None,wstoken=None,delete=False):
	HOST=f'{EndpointTarget}/douglas_subscriptions'
	payload = {}
	# EVENTID : [NAME,TYPE,TEAM,start,end]
	payload["TEAM"]=teamname
	payload["CHANNELID"]=channel_id
	payload["DELETE"]=delete
	if wsid != None:
		payload["WSID"]=wsid
	if wstoken != None:
		payload["WSTOKEN"]=wstoken
	payload_str=json.dumps(payload)
	r = requests.post(HOST, data=payload_str)
	response_body=r.text
	print("uploadDouglasSubscriptions: " + response_body.strip("\n"))
	return response_body.strip("\n")
	
def uploadChatSupport(teamid,channel_id,wsid=None,wstoken=None,email=None,delete=False):
	HOST=f'{EndpointTarget}/chat_support_two'
	payload = {}
	if delete:
		payload["ACTION"]="REM"
	else:
		payload["ACTION"]="ADD"
		payload["TEAM"]=teamid
		payload["WSID"]=wsid
		payload["WSTOKEN"]=wstoken
		if email != None:
			payload["EMAIL"]=email
	payload["CHANNEL"]=channel_id
	payload_str=json.dumps(payload)
	r = requests.post(HOST, data=payload_str)
	response_body=r.text
	print("uploadChatSupport: " + response_body.strip("\n"))
	return response_body.strip("\n")
	
def uploadChatSupportTVT(channel_id,tvt_channel_id=None,wsid=None,wstoken=None,delete=False):
	HOST=f'{EndpointTarget}/chat_support_two'
	payload = {}
	if delete:
		payload["ACTION"]="TVTREM"
	else:
		payload["ACTION"]="TVTADD"
		payload["TVTCHANNEL"]=tvt_channel_id
		payload["WSID"]=wsid
		payload["WSTOKEN"]=wstoken
	payload["CHANNEL"]=channel_id
	payload_str=json.dumps(payload)
	r = requests.post(HOST, data=payload_str)
	response_body=r.text
	print("uploadChatSupportTVT: " + response_body.strip("\n"))
	return response_body.strip("\n")
	
def updateChatSupport(teamid,wsid,wstoken):
	HOST=f'{EndpointTarget}/chat_support_two'
	payload = {}
	payload["ACTION"]="UPDATE"
	payload["TEAM"]=teamid
	payload["WSID"]=wsid
	payload["WSTOKEN"]=wstoken
	payload_str=json.dumps(payload)
	r = requests.post(HOST, data=payload_str)
	response_body=r.text
	print("updateChatSupport: " + response_body.strip("\n"))
	return response_body.strip("\n")
	
def uploadChatSupportConf(channel_id,enable=False):
	HOST=f'{EndpointTarget}/chat_support_two'
	payload = {}
	payload["ACTION"]="CONF"
	payload["ENABLE"]=enable
	payload["CHANNEL"]=channel_id
	payload_str=json.dumps(payload)
	r = requests.post(HOST, data=payload_str)
	response_body=r.text
	print("uploadChatSupportConf: " + response_body.strip("\n"))
	return response_body.strip("\n")

def processAllEvents(json_string):
	#print(json_string)
	event_list={}
	result={}
	try:
		result = json.loads(json_string)
	except Exception as e:
		print(str(e))
	if type(result) != dict: return event_list
	if "events" not in result.keys(): return event_list
	result=result["events"]
	if type(result) != list: return event_list
	if len(result) < 1: return event_list
	for event in result:
		if type(event) == dict and \
			"event_id" in event.keys() and \
			"event_name" in event.keys() and \
			"event_type_id" in event.keys() and \
			"start_time" in event.keys() and \
			"end_time" in event.keys() and \
			"tiered_rewards" in event.keys():
			#EVENTID : [NAME,TYPE,TEAM,start,end]
			event_id=event["event_id"]
			event_name=event["event_name"]
			event_type_id=event["event_type_id"]
			TEAM=0
			if "team_tiered_rewards" in event.keys():
				TEAM=1
			PACK_DATA=[]
			tiered_rewards=event["tiered_rewards"]
			for elem in tiered_rewards:
				if "score" in elem:
					PACK_DATA.append(elem["score"])
			start_time=event["start_time"]
			end_time=event["end_time"]
			event_list[event_id]=[event_name,event_type_id,TEAM,start_time,end_time,PACK_DATA]
	return event_list
	
def getUserNames(json_string):
	user_map={}
	global PROFILE_LIST
	result={}
	try:
		result = json.loads(json_string)
	except Exception as e:
		print(str(e))
	if type(result) != dict: return user_map
	if "profiles" not in result.keys(): return user_map
	result=result["profiles"]
	if type(result) != list: return user_map
	if len(result) < 1: return user_map
	for profile in result:
		if type(profile) == dict and \
			"profileId" in profile.keys() and \
			"nameOnPlatform" in profile.keys():
			profileId=profile["profileId"]
			nameOnPlatform=profile["nameOnPlatform"]
			platformType="NULL"
			if "platformType" in profile.keys():
				platformType=profile["platformType"]
			user_map[profileId]=[nameOnPlatform,platformType]
	return user_map

def processUserDetails(json_string):
	user_details={}
	result={}
	try:
		result = json.loads(json_string)
	except Exception as e:
		print(str(e))
	if type(result) != dict: return user_details
	RANK=0
	MAXMMR=0
	MMR=0
	NKLEVEL=1
	DONATED_CUR=0
	DONATED_ALL=0
	WINS_PVP=0
	WINS_TW=0
	WINS_CHLG=0
	WINS_PVE=0
	WINS_FF=0
	WINS_FFP=0
	WINS_PVPP=0
	TW_TOKENS=0
	CHLG_CMP=0
	CHLG_MAX_SCORE=0
	DECK=None
	OUTFIT={'active_gear': [], 'outfit': []}
	if "statistics" in result:
		if "wins" in result["statistics"]:
			if "pvp" in result["statistics"]["wins"]:
				WINS_PVP=result["statistics"]["wins"]["pvp"]
			if "tw" in result["statistics"]["wins"]:
				WINS_TW=result["statistics"]["wins"]["tw"]
			if "chlg" in result["statistics"]["wins"]:
				WINS_CHLG=result["statistics"]["wins"]["chlg"]
			if "pve" in result["statistics"]["wins"]:
				WINS_PVE=result["statistics"]["wins"]["pve"]
			if "ff" in result["statistics"]["wins"]:
				WINS_FF=result["statistics"]["wins"]["ff"]
			if "ff_perfect" in result["statistics"]["wins"]:
				WINS_FFP=result["statistics"]["wins"]["ff_perfect"]
			if "pvp_perfect" in result["statistics"]["wins"]:
				WINS_PVPP=result["statistics"]["wins"]["pvp_perfect"]
		if "teamwar" in result["statistics"]:
			if "tokens" in result["statistics"]["teamwar"]:
				TW_TOKENS=result["statistics"]["teamwar"]["tokens"]
		if "mmr" in result["statistics"]:
			MAXMMR=result["statistics"]["mmr"]
		if "chlg_completed" in result["statistics"]:
			CHLG_CMP=result["statistics"]["chlg_completed"]
		if "chlg_max_score" in result["statistics"]:
			CHLG_MAX_SCORE=result["statistics"]["chlg_max_score"]
	'''
	"mmr": 8255.87391566826,
	"chlg_completed": 197,
	"chlg_max_score": 12
	'''
	if "deck" in result and type(result["deck"]) == list:
		DECK=result["deck"]
	if "global_standing" in result: RANK = result["global_standing"]
	if RANK == 0: rank = 99999
	if "mmr" in result: MMR = int(result["mmr"])
	if "level" in result and result["level"] != None: NKLEVEL = result["level"]
	if "donated" in result:
		DONATED_CUR = getDonationPoints(result["donated"])
	if "donated_total" in result:
		DONATED_ALL = getDonationPoints(result["donated_total"])
	if "avatar" in result and "active_gear" in result:
		active_gear = result["active_gear"]
		for i in range(min(3,len(result["active_gear"]))):
			cur_gear = result["active_gear"][i]
			if 'id' not in cur_gear or\
				'custom' not in cur_gear or\
				'a' not in cur_gear['custom'] or\
				'b' not in cur_gear['custom']:
				continue
			id = cur_gear['id']
			a = cur_gear['custom']['a']
			b = cur_gear['custom']['b']
			OUTFIT["active_gear"].append([id,a,b])
		avatar = result["avatar"]
		if 'outfit' in avatar:
			for i in range(min(7,len(avatar['outfit']))):
				cur_outfit = avatar['outfit'][i]
				if 'c' not in cur_outfit or 'id' not in cur_outfit: continue
				OUTFIT["outfit"].append([cur_outfit['id'],cur_outfit['c']])
		if 'skin_color' in avatar:
			OUTFIT['skin_color'] = avatar['skin_color']
		if 'female' in avatar:
			OUTFIT['female'] = avatar['female']
	user_details={
		'RANK':RANK,
		'MMR':MMR,
		'NKLEVEL':NKLEVEL,
		'DONATED_CUR':DONATED_CUR,
		'DONATED_ALL':DONATED_ALL,
		'WINS_PVP':WINS_PVP,
		'WINS_TW':WINS_TW,
		'WINS_CHLG':WINS_CHLG,
		'WINS_PVE':WINS_PVE,
		'WINS_FF':WINS_FF,
		'WINS_FFP':WINS_FFP,
		'WINS_PVPP':WINS_PVPP,
		'TW_TOKENS':TW_TOKENS,
		'MAXMMR':MAXMMR,
		'CHLG_CMP':CHLG_CMP,
		'CHLG_MAX_SCORE':CHLG_MAX_SCORE,
		'OUTFIT':OUTFIT,
	}
	return user_details, DECK

def processPVPLeaderboard(json_string):
	name_rank_mmr_details={}
	result={}
	try:
		result = json.loads(json_string)
	except Exception as e:
		print(str(e))
	if type(result) != dict: return None
	if "rows" not in result.keys(): return None
	if type(result["rows"]) != list: return None
	for elem in result["rows"]:
		meta_player={}
		user_id=elem["population"]
		if user_id not in name_rank_mmr_details:
			name_rank_mmr_details[user_id]={}
		name_rank_mmr_details[user_id]["RANK"]=elem["rank"]
		name_rank_mmr_details[user_id]["MMR"]=int(elem["score"])
		name_rank_mmr_details[user_id]["NAME"]=elem["metadata"]["player_name:infinite"]
		if "team_name:infinite" in elem["metadata"]:
			name_rank_mmr_details[user_id]["TEAM"]=elem["metadata"]["team_name:infinite"]
		else: 
			name_rank_mmr_details[user_id]["TEAM"]="No Team"
	return name_rank_mmr_details
"""
            "player": "None",
            "population": "179d939b-3784-43fb-aea5-885c21c6f1d5",
            "score": 8902.79614579,
            "rank": 1,
            "metadata": {
                "team_name:infinite": "F2P Whales",
                "player_name:infinite": "Shane0292",
                "highlight:infinite": 1576065600
            }
"""

def processTeamDetails(json_string):
	team_details={}
	result={}
	try:
		result = json.loads(json_string)
	except Exception as e:
		print(str(e))
	if type(result) != dict: return None
	if "league" not in result.keys(): return None
	if "name" not in result.keys(): return None
	if "countryCode" not in result.keys(): return None
	if "trophies" not in result.keys(): return None
	if "applicationStatus" not in result.keys(): return None
	if "membersCount" not in result.keys(): return None
	if "metadata" not in result.keys(): return None
	
	description=''
	nklevel=0
	if "new_kid_level" in result['metadata'].keys():
		nklevel=result['metadata']['new_kid_level']
	if "description" in result['metadata'].keys():
		description=result['metadata']['description']
		
	team_details["TROPHIES"]=result['trophies']
	team_details["MEMBERS"]=result['membersCount']
	team_details["COUNTRY"]=result['countryCode']
	team_details["STATUS"]=result['applicationStatus']
	team_details["NAME"]=result['name']
	team_details["NKLEVEL"]=nklevel
	team_details["DESCRIPTION"]=description
	return team_details

def processTeamMembers(json_string):
	member_list={}
	result={}
	try:
		result = json.loads(json_string)
	except Exception as e:
		print(str(e))
	if type(result) != dict: return member_list
	if "members" not in result.keys(): return member_list
	if type(result["members"]) != list: return member_list
	for member in result["members"]:
		if type(member) == dict and\
			"profileId" in member.keys():
			USERID = member["profileId"]
			ROLE=None
			JOINDATE=None
			RANK=None
			MMR=None
			NKLEVEL=None
			DONATED_CUR=None
			DONATED_ALL=None
			if "role" in member: ROLE = member["role"]
			if "joinDate" in member: JOINDATE = member["joinDate"].split("T")[0]
			if "global_standing" in member: RANK = member["global_standing"]
			if RANK == 0: rank = 99999
			if "mmr" in member: MMR = int(member["mmr"])
			if "level" in member: NKLEVEL = member["level"]
			if "donated" in member: DONATED_CUR = getDonationPoints(member["donated"])
			if "donated_total" in member: DONATED_ALL = getDonationPoints(member["donated_total"])
			member_list[USERID]={
				'ROLE':f"'{ROLE}'",
				'JOINDATE':f"'{JOINDATE}'",
				'RANK':RANK,
				'MMR':MMR,
				'NKLEVEL':NKLEVEL,
				'DONATED_CUR':DONATED_CUR,
				'DONATED_ALL':DONATED_ALL,
			}
	return member_list

"""
"donated": {
	"1": 22,
	"0": 34
},
"donated_total": {
	"1": 3566,
	"0": 6634
},
"""
def getDonationPoints(donated):
	donation_points=0
	for key in donated:
		if key == "0":
			donation_points+=(2*donated[key])
		else:
			donation_points+=(6*donated[key])
	return donation_points


def processTVTLeaderboard(json_string):
	rank_details={}
	result={}
	try:
		result = json.loads(json_string)
	except Exception as e:
		print(str(e))
	if type(result) != dict: return None
	if "rows" not in result.keys(): return None
	if type(result["rows"]) != list: return None
	for elem in result["rows"]:
		if "population" in elem and "rank" in elem:
			team_id = elem["population"]
			if team_id not in rank_details:
				rank_details[team_id]={}
			rank_details[team_id]["RANK"]=elem["rank"]
	return rank_details
	
def getTeamIDFromName(team_name):
	#First Search our own database
	lower_team_name=team_name.lower()
	team_id=HELPER_DB.getInGameTeamIDFromName(lower_team_name)
	if team_id != None: return team_id
	#Then search the game
	json_string=SPPD_API.getTeamID(lower_team_name)
	result={}
	try:
		result = json.loads(json_string)
	except Exception as e:
		print(str(e))
	if type(result) != list: return team_id #No Team/Unknown
	for row in result:
		if "name" in row and "id" in row:
			search_lower=row["name"].lower()
			if search_lower == lower_team_name:
				team_id = row["id"]
				#Because we didn't have it in our database apparently, we need to add it!
				uploadTeam(team_id, lower_team_name)
				#Let's add their entire team as well, why not?
				refreshTeam(team_id, True)
				break
	return team_id
"""
[
    {
        "league": 3,
        "name": "F2P Whales",
        "countryCode": "US",
        "trophies": 6735,
        "applicationStatus": "Moderated",
        "members": [],
        "maxMembersCount": 50,
        "membersCount": 49,
        "id": 178572,
        "metadata": {
            "new_kid_level": 22,
            "banner": 6,
            "description": "Join the Nambla discord at 'https:\/\/discord.gg\/maBgDXu' to apply for any of our teams. #1 sinc"
        }
    },
]
"""

def getWALOffset(id):
	if id in DATABASE.DECK_MAP:
		if "leg" in DATABASE.DECK_MAP[id]: return 3
		if "epi" in DATABASE.DECK_MAP[id]: return 2
		if "rar" in DATABASE.DECK_MAP[id]: return 1
		if "com" in DATABASE.DECK_MAP[id]: return 0
	return -1
	
def processCardComparisonData(team_id, data, cur_data):
	cards_to_update={} #card_id : {'l': level, 'v': vote}, ...
	for elem in data:
		#Example: { 'id': 'Dogpoo', 'Leader Vote': 3, 'Target Level': 0 }
		card_name=elem['id'].lower()
		if card_name == 'total': continue #skip that summary line
		if card_name not in DATABASE.LOWER_NAME_TO_ID: continue
		card_id=DATABASE.LOWER_NAME_TO_ID[card_name]
		target_vote=elem['Leader Vote']
		vote=0
		if target_vote == 'Yes': vote=1
		level=elem['Target Level']
		if level != None and level != 0:
			old_vote=-1
			old_level=4-getWALOffset(card_id)
			if card_id in cur_data:
				#Need to check if it's already in the list
				old_vote,old_level=cur_data[card_id]
			if level != old_level or vote != old_vote:
				#print(f"level {level}, old_level {old_level}, vote {vote}, old_vote {old_vote}")
				cards_to_update[card_id]={'l': level, 'v': vote}
	if len(cards_to_update) > 0:
		ingame_team_id=HELPER_DB.getInGameTeamID(team_id)
		uploadCardComparisonData(ingame_team_id, cards_to_update)
		
def processBracketSubscribe(cur_data, data, email):
	subscriptions_to_update={} #team_name : is_subscribed, ...
	for elem in data:
		#Example: { 'id': 'Dogpoo', 'Leader Vote': 3, 'Target Level': 0 }
		team_name=elem['Team Name']
		#team_name is currently markdown format as link. Strip.
		team_name = team_name.split("]")[0].strip("[")
		if type(team_name) == str: team_name=team_name.lower()
		target_sub=elem['Subscribe']
		sub=0
		if target_sub == 'Yes': sub=1
		if target_sub != None:
			old_sub=0
			#Need to check if it's already in the list
			if team_name in cur_data:
				old_sub=cur_data[team_name]
			if old_sub != sub:
				subscriptions_to_update[team_name]=sub
	if len(subscriptions_to_update) > 0:
		uploadBracketSubscription(email, subscriptions_to_update)
	
def processTeamApplications(ingame_team_id, data, cur_data):
	#Get the reverse map (name to userid)
	username_map=HELPER_DB.getAllUserNamesReverse(ingame_team_id)
	players_to_update={} #userid : {'s': status, 'r': role}, ...
	for elem in data:
		#Example: { 'id': 'Player Name', 'status': 'ignore', 'role': 'elder' }
		player_name=elem['name']
		status=elem['status']
		role=elem['role']
		userid=None
		if player_name in username_map:
			userid=username_map[player_name]
		#print(f"userid {userid}, status {status}, role {role}")
		if userid != None and status != None and role != None:
			old_status='ignore'
			old_role='regular'
			#Get the player's USERID
			if userid in cur_data:
				#Need to check if it's already in the list
				old_status,old_role=cur_data[userid]
			if status != old_status or role != old_role:
				#print(f"status {status}, old_status {old_status}, role {role}, old_role {old_role}")
				players_to_update[userid]=[status, role]
	if len(players_to_update) > 0:
		uploadTeamApplicationData(ingame_team_id, players_to_update)
	

###Meta Report

def uploadMetaChalReport(cards,themes,total_decks,meta_decks=None):
	HOST=f'{EndpointTarget}/meta_chal_report'
	payload = {}
	payload["THEMES"]=themes #{ "adv,fan" : 12.30 }
	payload["CARDS"]=cards #{ 123 : 12.30 }
	payload["TOTALDECKS"]=total_decks
	if meta_decks != None:
		payload["METADECKS"]=meta_decks
	
	payload_str=json.dumps(payload)
	r = requests.post(HOST, data=payload_str)
	response_body=r.text
	print("uploadMetaChalReport: " + response_body.strip("\n"))

def uploadMetaReport(cards,themes,total_decks,name,search,meta_decks=None,costs=None):
	HOST=f'{EndpointTarget}/meta_report'
	payload = {}
	payload["SEARCH"]=search
	payload["NAME"]=name
	payload["THEMES"]=themes #{ "adv,fan" : 12.30 }
	payload["CARDS"]=cards #{ 123 : 12.30 }
	payload["TOTALDECKS"]=total_decks
	if meta_decks != None:
		payload["METADECKS"]=meta_decks
	if costs != None:
		payload["COSTS"]=costs #{ 3.3 : 100 }
	
	payload_str=json.dumps(payload)
	r = requests.post(HOST, data=payload_str)
	response_body=r.text
	print("uploadMetaReport: " + response_body.strip("\n"))

def uploadTeamWarCardChoices(card_choices):
	HOST=f'{EndpointTarget}/card_choices'
	payload = {}
	payload["CARDS"]=card_choices
	#[ [ { "id": 1272 }, { "id": 186 } ], ... ]
	payload_str=json.dumps(payload)
	r = requests.post(HOST, data=payload_str)
	response_body=r.text
	print("uploadTeamWarCardChoices: " + response_body.strip("\n"))

def processTeamWarInit(json_string):
	card_choices={}
	result={}
	try:
		result = json.loads(json_string)
	except Exception as e:
		print(str(e))
	if type(result) != dict: return card_choices
	if "cards" not in result: return card_choices
	if type(result["cards"]) != list: return card_choices
	return result["cards"]
	#[ [ { "id": 1272 }, { "id": 186 } ], ... ]

def getUsersThatAreMissingData(arena=None):
	TOTAL_PLAYERS=400 #PER TIER
	if arena != None:
		if arena > 10: TOTAL_PLAYERS=400
		elif arena > 5: TOTAL_PLAYERS=200
		else: TOTAL_PLAYERS=100
	user_id_list=[]
	#Null
	USERIDS=HELPER_DB.getPlayersWithNull(TOTAL_PLAYERS,arena)
	for row in USERIDS:
		user_id_list.append(row[0])
	
	limit = TOTAL_PLAYERS - len(user_id_list)
	USERIDS=HELPER_DB.getPlayersWithOldUpdated(limit,arena)
	#X Days Ago
	if len(user_id_list) < TOTAL_PLAYERS:
		time_to_beat = int(time.time()) - 3600 * 24 * 7
		for row in USERIDS:
			updated = row[1]
			if len(user_id_list) < TOTAL_PLAYERS and updated < time_to_beat:
				user_id_list.append(row[0])
	#X Hours Ago
	if len(user_id_list) < TOTAL_PLAYERS:
		time_to_beat = int(time.time()) - 3600 * 18
		for row in USERIDS:
			updated = row[1]
			if len(user_id_list) < TOTAL_PLAYERS and updated < time_to_beat:
				user_id_list.append(row[0])
	index=0
	total_selected=len(user_id_list)
	for key in user_id_list:
		print(f"getUsersThatAreMissingData index: {index} out of {total_selected}, arena{arena}")
		team_id = HELPER_DB.getInGameTeamIDFromUserID(key)
		if team_id == None: team_id = 0
		try:
			result=SPPD_API.getUserDetails(key)
			user_details, deck=processUserDetails(result)
			if deck != None:
				uploadUserDetails(key, team_id, user_details, deck)
		except Exception as e:
			print("EXCEPTION: "+str(e))
			traceback.print_exc()
		time.sleep(0.2)
		index+=1
	print("getUsersThatAreMissingData complete")
	
def getSpecificUser(key):
	team_id = HELPER_DB.getInGameTeamIDFromUserID(key)
	if team_id == None: team_id = 0
	try:
		result=SPPD_API.getUserDetails(key)
		print(result)
		user_details, deck=processUserDetails(result)
		if deck != None:
			uploadUserDetails(key, team_id, user_details, deck)
	except Exception as e:
		print("EXCEPTION: "+str(e))
		traceback.print_exc()

def getTeamWarCardChoices():
	result = SPPD_API.getTeamWarInit()
	card_choices=processTeamWarInit(result)
	if len(card_choices) > 0:
		uploadTeamWarCardChoices(card_choices)
		
def getAllEvents():
	result = SPPD_API.getAllEvents()
	print(result)
	events=processAllEvents(result)
	if len(events) > 0:
		uploadEvents(events)
		
def getMetaPercentiles(cards_dict, themes_dict, total_decks, cap_min=0):
	PRINTREPORT=False
	
	final_themes={}
	#Process Themes
	if PRINTREPORT: print("\nThemes")
	sorted_collection=[]
	for themes in themes_dict.keys():
		if themes_dict[themes] > total_decks:
			print(f"{themes_dict[themes]} : {total_decks}")
		percent=100*float(themes_dict[themes])/total_decks
		sorted_collection.append([themes, "%.2f" % (percent)])
	sorted_l = sorted(sorted_collection, key=lambda x: (x[1], x[0]), reverse=True)
	for line in sorted_l:
		percent = line[1]
		theme=line[0]
		if PRINTREPORT: print(str(percent) + "% | " + theme)
		final_themes[theme]=percent
		if float(percent) > 100:
			print("getMetaPercentiles themes")
			sys.exit()
		
	final_cards={}
	#Process Cards
	if PRINTREPORT: print("\nCards")
	sorted_collection=[]
	for card in cards_dict.keys():
		if cards_dict[card] > total_decks:
			print(f"{cards_dict[card]} : {total_decks}")
		percent=100*float(cards_dict[card])/total_decks
		if percent > cap_min:
			sorted_collection.append([card, "%.2f" % (percent)])
	PLAYED=[]
	sorted_l = sorted(sorted_collection, key=lambda x: (x[1], x[0]), reverse=True)
	for line in sorted_l:
		percent = line[1]
		card_id=line[0]
		PLAYED.append(card_id)
		if PRINTREPORT:
			card_name=HELPER_DB.getCardName(card_id)
			print(str(percent) + "% | " + card_name)
		final_cards[card_id]=percent
		if float(percent) > 100:
			print("getMetaPercentiles cards")
			sys.exit()
		
	"""	
	print("\nNot Played Cards")
	NOT_PLAYED=[]
	for card_id in getAllCardIDs():
		if card_id not in PLAYED:
			card_name=getCardName(card_id)
			print("-1 " + card_name)
	"""
	return final_cards, final_themes

def refreshTeam(unique_team_id,override=False,rank=9999,tophundred=False):
	ingame_team_id=0
	if override: ingame_team_id=unique_team_id #manually add a new team
	else: ingame_team_id=HELPER_DB.getInGameTeamID(unique_team_id)
	#SPPD_API get the team members
	#Update the team members in TEAM_MEMBERS
	# { userid1 : role, userid2 : role, ... }
	#Set the TEAMS UPDATED time to now.
	result=SPPD_API.getTeamDetails(ingame_team_id)
	#Add the team if it doesn't exist
	team_details=processTeamDetails(result)
	if team_details != None:
		name=team_details["NAME"]
		uploadTeam(ingame_team_id,name)
	else:
		print(f"[Critical] Name not found for teamid {ingame_team_id}")
		team_details={}
		team_details["TROPHIES"]=0
		team_details["MEMBERS"]=0
		team_details["NKLEVEL"]=0
		team_details["COUNTRY"]=""
		team_details["STATUS"]="Closed"
		team_details["DESCRIPTION"]="Unable to find team"
		rank_details={}
		rank_details[ingame_team_id]={"RANK":rank}
		uploadTVTMeta(ingame_team_id, rank_details, team_details)
		return
	member_list=processTeamMembers(result)
	uploadTeamMembers(ingame_team_id,member_list)
	rank_details=None
	if override:
		rank_details={}
		rank_details[ingame_team_id]={"RANK":rank}
	uploadTVTMeta(ingame_team_id, rank_details, team_details)
	#Insert user-id names for all users
	index=0
	WIDTH=20
	all_names_dict={}
	members_profile_ids=list(member_list.keys())
	for i in range(0,len(members_profile_ids),WIDTH):
		print(f"Updating Team Members {unique_team_id}, index: {index}")
		search_str=",".join(x for x in members_profile_ids[i:i+WIDTH])
		try:
			result=SPPD_API.getUserName(search_str)
			names_dict=getUserNames(result)
			all_names_dict.update(names_dict)
		except Exception as e:
			print("EXCEPTION: "+str(e))
			traceback.print_exc()
		index+=1
	if tophundred:
		for key in member_list.keys():
			getSpecificUser(key)
			time.sleep(0.2)
	if len(all_names_dict) > 0:
		try:
			uploadUserPlatform(all_names_dict, {'TEAM': ingame_team_id})
		except Exception as e:
			print("EXCEPTION: "+str(e))

def refresh_old_teams():
	#Refresh old teams that were in the top 1000 but not updated within 48 hours
	index=1
	old_teams_list=HELPER_DB.findOldTeams()
	len_old_teams=len(old_teams_list)
	for teamid in old_teams_list:
		print(f"refresh_old_teams index: {index} out of {len_old_teams}")
		try:
			refreshTeam(teamid, True, 9999)
		except Exception as e:
			print("EXCEPTION: "+str(e))
			traceback.print_exc()
		time.sleep(0.2)
		index+=1
	print("Completed refresh_old_teams")
		
def findTeamByRank(rank):
	result=SPPD_API.getTVTLeaderboardAtOffset(rank)
	print(result)
	
def full_team_report(primary=True):
	rank_details={}
	START=1
	#END=1000
	END=2000
	LIMIT=50
	for i in range(START,END,LIMIT):
		end_offset=i+LIMIT-1
		print(f"Collecting Teams Ranked {i} to {end_offset}")
		result=SPPD_API.getTVTLeaderboardAtOffset(i)
		sub_team_list=processTVTLeaderboard(result)
		rank_details.update(sub_team_list)
		time.sleep(0.2)
	index=START
	for key in rank_details.keys():
		print(f"full_team_report index: {index} out of {END}")
		rank=rank_details[key]["RANK"]
		try:
			refreshTeam(key, True, rank, False)
		except Exception as e:
			print("EXCEPTION: "+str(e))
			traceback.print_exc()
		time.sleep(0.2)
		index+=1
	refresh_old_teams()
	completed_pretty=time.strftime('%Y-%m-%d %H:%M', time.localtime(int(time.time())))
	print(f"Completed full_team_report {completed_pretty}")
	
def processChallengeMetaReport():
	#TO-DO - Check if there was a challenge match upload in the last hour
	if not HELPER_DB.needChallengeMetaReport(): return
	cards_dict,themes_dict,total_decks,meta_decks = HELPER_DB.getChalCardsAndThemes()
	print(f"processChallengeMetaReport - total_decks: {total_decks}")
	if total_decks > 0:
		final_cards,final_themes=getMetaPercentiles(cards_dict,themes_dict,total_decks,cap_min=5)
		#Final Check Before Upload
		if HELPER_DB.getChalReportTotalDecks() != total_decks:
			uploadMetaChalReport(final_cards,final_themes,total_decks,meta_decks)

def collect_meta_report():
	"""
	#Grab the top 1000 player's userids
	#Combine it with every user id in the top 100 teams
	#Find all their decks
	#Generate a 1-day meta report for each search radius and rank filter
	#X-day or patch meta reports are merge the previous 1-day meta reports spanning that amount of time.
	"""
	START=1
	END=1000
	LIMIT=50
	name_rank_mmr_details={}
	for i in range(START,END,LIMIT):
		end_offset=i+LIMIT-1
		print(f"Collecting Players Ranked {i} to {end_offset}")
		result=SPPD_API.getGlobalLeaderboardAtOffset(i,LIMIT)
		sub_player_list=processPVPLeaderboard(result)
		if sub_player_list != None:
			name_rank_mmr_details.update(sub_player_list)
		time.sleep(0.2)
	index=START
	for key in name_rank_mmr_details.keys():
		print(f"collect_meta_report index: {index} out of {END}")
		try:
			rank=name_rank_mmr_details[key]["RANK"]
			team_name=name_rank_mmr_details[key]["TEAM"]
			team_id=getTeamIDFromName(team_name)
			mmr=name_rank_mmr_details[key]["MMR"]
			result=SPPD_API.getUserDetails(key)
			user_details, deck=processUserDetails(result)
			if rank != None and mmr != None and deck != None:
				uploadUserDetails(key, team_id, user_details, deck)
		except Exception as e:
			print("EXCEPTION: "+str(e))
			traceback.print_exc()
		time.sleep(0.2)
		index+=1
	names_dict={}
	for key in name_rank_mmr_details.keys():
		names_dict[key]=name_rank_mmr_details[key]["NAME"]
	uploadUser(names_dict, {'RANK': END})
	completed_pretty=time.strftime('%Y-%m-%d %H:%M', time.localtime(int(time.time())))
	print(f"Completed collect_meta_report {completed_pretty}")
		
def generatedMetaReportFromCards(filter_rank_min = None, filter_mmr_min = None, filter_mmr_max = None):
	search="Last 1 day"
	name=None
	if filter_rank_min==None and filter_mmr_min==None and filter_mmr_max==None:
		name="All"
	elif filter_mmr_min!=None and filter_mmr_max!=None:
		name=f"MMR {filter_mmr_min}-{filter_mmr_max}"
	elif filter_mmr_min!=None and filter_mmr_max==None:
		name=f"MMR {filter_mmr_min}+"
	elif filter_rank_min!=None and filter_mmr_min==None and filter_mmr_max==None:
		name=f"Top {filter_rank_min}"
	else:
		print(f"Not supported, filter_rank_min: {filter_rank_min}, filter_mmr_min: {filter_mmr_min}, filter_mmr_max: {filter_mmr_max}")
	cards_dict,themes_dict,total_decks,meta_decks,cost_map = HELPER_DB.getCardsAndThemesByFilter(filter_rank_min, filter_mmr_min, filter_mmr_max)
	print(f"search: {search}, name: {name}, total_decks: {total_decks}")
	if total_decks > 0:
		final_cards,final_themes=getMetaPercentiles(cards_dict,themes_dict,total_decks)
		uploadMetaReport(final_cards,final_themes,total_decks,name,search,meta_decks,cost_map)

def generateMetaReportFromPastReports(filter_rank_min = None, filter_mmr_min = None, filter_mmr_max = None, search_radius=24*60*6):
	search=None
	if search_radius == 24*60*60: #1 day
		search="Last 1 day"
	elif search_radius == 24*60*60 * 3: #3 day
		search="Last 3 days"
	elif search_radius == 24*60*60 * 7: #7 day
		search="Last 7 days"
	elif search_radius == 24*60*60 * 14: #14 day
		search="Last 14 days"
	else: #patch
		search="Last Patch"
	name=None
	if filter_rank_min==None and filter_mmr_min==None and filter_mmr_max==None:
		name="All"
	elif filter_mmr_min!=None and filter_mmr_max!=None:
		name=f"MMR {filter_mmr_min}-{filter_mmr_max}"
	elif filter_mmr_min!=None and filter_mmr_max==None:
		name=f"MMR {filter_mmr_min}+"
	elif filter_rank_min!=None and filter_mmr_min==None and filter_mmr_max==None:
		name=f"Top {filter_rank_min}"
	else:
		print(f"Not supported, filter_rank_min: {filter_rank_min}, filter_mmr_min: {filter_mmr_min}, filter_mmr_max: {filter_mmr_max}")
	
	cards_dict,themes_dict,total_decks = HELPER_DB.getCardsAndThemesByFilter_Report(name, search_radius)
	print(f"search: {search}, name: {name}, total_decks: {total_decks}")
	if total_decks > 0:
		final_cards,final_themes=getMetaPercentiles(cards_dict,themes_dict,total_decks)
		uploadMetaReport(final_cards,final_themes,total_decks,name,search)

def generateAllMetaReports(arena=None):
	#filter_rank_min = None, filter_mmr_min = None, filter_mmr_max = None
	if arena==None:
		for rank in [250,1000]:
			generatedMetaReportFromCards(filter_rank_min=rank)
			generatePastMetaReports(filter_rank_min=rank)
	else:
		mmr_min,mmr_max=DATABASE.ARENA_MAP[arena]
		generatedMetaReportFromCards(filter_mmr_min=mmr_min, filter_mmr_max=mmr_max)
		generatePastMetaReports(filter_mmr_min=mmr_min, filter_mmr_max=mmr_max)
		
def generatePastMetaReports(filter_rank_min = None, filter_mmr_min = None, filter_mmr_max = None):
	#Combine previous days
	#LAST_PATCH=int(time.time())-datetime.datetime(2020, 2, 4, 5, 0).timestamp()
	#LAST_PATCH=int(time.time())-datetime.datetime(2020, 3, 3, 5, 0).timestamp()
	#LAST_PATCH=int(time.time())-datetime.datetime(2020, 4, 7, 5, 0).timestamp()
	#LAST_PATCH=int(time.time())-datetime.datetime(2020, 5, 5, 5, 0).timestamp()
	#LAST_PATCH=int(time.time())-datetime.datetime(2020, 6, 6, 5, 0).timestamp()
	#LAST_PATCH=int(time.time())-datetime.datetime(2020, 7, 7, 5, 0).timestamp()
	LAST_PATCH=int(time.time())-datetime.datetime(2020, 8, 4, 5, 0).timestamp()
	DAY=24*60*60
	for search_radius in [3*DAY,7*DAY,14*DAY,LAST_PATCH]:
		generateMetaReportFromPastReports(filter_rank_min, filter_mmr_min, filter_mmr_max, search_radius)
		
def full_meta_report():
	collect_meta_report()
	generateAllMetaReports() #For top 250/top 1000 only
	for arena in sorted(DATABASE.ARENA_MAP.keys(), reverse=True):
		getUsersThatAreMissingData(arena)
		generateAllMetaReports(arena)
	completed_pretty=time.strftime('%Y-%m-%d %H:%M', time.localtime(int(time.time())))
	print(f"Completed full_meta_report {completed_pretty}")
	
def arena_meta_report():
	for arena in sorted(DATABASE.ARENA_MAP.keys(), reverse=True):
		getUsersThatAreMissingData(arena)
		generateAllMetaReports(arena)
	print("Completed arena_meta_report")
	
def weeklyBackupDatabase():
	HELPER_DB.weeklyBackupDatabase()
def dailyBackupDatabase():
	HELPER_DB.dailyBackupDatabase()
		
###Read the file everytime it expires
###Add a random number between 1 and 1000 seconds to the expirations
if __name__ == '__main__':
	#updatePastNames()
	#updatePastTeams()
	#findTeamByRank(1488)
	#for arena in sorted(DATABASE.ARENA_MAP.keys(), reverse=True):
	#	generateAllMetaReports(arena)
	#getSpecificUser('c8993b71-10dc-4ed2-beb3-59691f6b7fc7')
	#getSpecificUser('03c38027-b16f-4079-9b10-ab94a78422b4') #Butmaam
	#getSpecificUser('bb65fae2-27b4-4e3e-a28f-982a356b74c2b') #Free Win
	#getSpecificUser('a0ce2453-f63b-464c-b96c-9b574d369190') #Random request
	#full_meta_report()
	#full_team_report()
	#getTeamWarCardChoices()
	#getTeamIDFromName("towel qaeda")
	#getTeamIDFromName("rolling stoners")
	#getTeamIDFromName("inmortales")
	#getTeamIDFromName("puticlanbutters")
	#getTeamIDFromName("watson")
	#refreshTeam(225303, True) #TheyTerkErrLSR
	#refreshTeam(173340, True, 9999) #towel qaeda
	#refreshTeam(216892, True, 9999) #theyterkerrelo
	#refreshTeam(132473, True, 23) #illuminated
	#refreshTeam(184) #DONATION CENTER
	#refreshTeam(370)
	#refreshTeam(22) #illuminated
	#refreshTeam(188970, True, 64) #coon legends
	#refreshTeam(150848, True, 23) #M3RCENARI3S
	#refreshTeam(216875, True, 9999) #NotFatBigBoned
	#refreshTeam(155655, True, 85) #Chef's Army
	#refreshTeam(213490, True, 9999) #FKN_CULT
	#refreshTeam(211496, True, 575) #NAMBLUES
	#refreshTeam(211824, True, 9999) #NTWITHOUTMYANUS
	#refreshTeam(140279, True, 118) #THE KENNY CREW
	#refresh_old_teams()
	#full_team_report(True)
	getAllEvents()
	#processChallengeMetaReport()
	#arena_meta_report()
	#doCleanup()
	pass