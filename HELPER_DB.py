#DATABASE READ ONLY

import mysql.connector as mariadb
import traceback
import json
import time, sys, datetime, re
from decimal import *
import RESTFUL
import DATABASE
import decimal
import LOCALIZATION
import build_douglas_art
from tabulate import tabulate
import random

'''
Count active players since last month
SELECT Y.MMR, COUNT(DISTINCT X.USERID) FROM users_history X
	JOIN (SELECT DISTINCT MMR - (MMR % 1000) AS MMR FROM users_history) Y
WHERE X.MMR BETWEEN Y.MMR AND (Y.MMR + 1000) AND x.updated > 1592633169 GROUP BY y.mmr

modify current time variables to `SELECT UNIX_TIMESTAMP();`
'''

VALID_TAGS = ['Adults','Adv','Character','Epic','Female','Human','Indians','Male','Melee','Parent','Kids','Legendary','Mys','Ranged','Holy','Rare','Sci','Spell','Common','Unholy','Assassin','HasMovementSounds','Pirates','AttackchangeImmune','AttractImmune','FreezeImmune','HealImmune','KillAbilityImmune','LifestealImmune','MAXHPchangeImmune','MindcontrolImmune','Object','PoisonImmune','PowerbindImmune','PurifyImmune','ResurrectImmune','ShieldImmune','SpeedchangeImmune','TeleportImmune','Totem','TransformImmune','Canadian','Kindergarteners','Fan','Animal','Gen','IgnoreDublicates','Cock','Alien','Tank','Disabled','HasAoeOnTarget','Flying','HasAoeOnUnit','Cowboys','Sup','AbilityImmune','SpellImmune','MovingObject','Trap','HasReviveAbility','isDarkAngelRed','Goth','isHumanKite2']
#Helper functions

def executeSanitize(query, name, debug=False, like_search=True):
	#Only allows SELECT
	result=None
	try:
		mariadb_connection = mariadb.connect(
								user='readonly',
								password='password',
								database='decktracker')
		cursor = mariadb_connection.cursor()
		if like_search:
			name = "%" + name + "%"
		cursor.execute(query, {'name': name})
		result = cursor.fetchall()
		if len(result) == 0: result=None
		elif len(result) == 1: result=result[0]
	except:
		print(f"[ERROR] Failed Query: {query}, where NAME = '{name}'")
		traceback.print_exc()
	finally:
		try: mariadb_connection.close()
		except: pass
	if debug: print(f"executeQuery query {query} -> result {result}")
	time.sleep(0.05)
	return result
	
def executeQuery(query, debug=False, multiple=False):
	#Only allows SELECT
	result=None
	try:
		mariadb_connection = mariadb.connect(
								user='readonly',
								password='password',
								database='decktracker')
		cursor = mariadb_connection.cursor()
		iterator = cursor.execute(query, multi=multiple)
		result = None
		if multiple:
			result = []
			for x in iterator:
				if x.with_rows:
					result = x.fetchall()
		else:
			result = cursor.fetchall()
		if len(result) == 0: result=None
		elif len(result) == 1: result=result[0]
	except:
		print(f"[ERROR] Failed Query: {query}")
		traceback.print_exc()
	finally:
		try: mariadb_connection.close()
		except: pass
	if debug: print(f"executeQuery query {query} -> result {result}")
	time.sleep(0.05)
	return result
	
def getPlayerResponse(player_name, deep_refresh):
	delete_me = False
	if player_name == '':
		return "Seriously...?", False, delete_me
	match = re.match('^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$', player_name)
	USERID = None
	if match != None:
		USERID = player_name.lower()
		delete_me = True
	else:
		USERID = getPlayerIDByName(player_name)
	if USERID == None:
		return "Sorry, I can't find that player.", False, delete_me
	if deep_refresh: RESTFUL.getSpecificUser(USERID)
	return *getPlayerDetails(USERID), delete_me
	
def getEmailsForChatByTeamID(TEAMID):
	EMAILS = []
	result = executeQuery(f"SELECT EMAIL FROM CHAT_SUPPORT WHERE TEAM={TEAMID} AND UPDATED > UNIX_TIMESTAMP() - 24*3600")
	if result == None:
		return EMAILS
	if type(result) == tuple: result = [result]
	for row in result:
		EMAILS.append(row[0])
	return EMAILS
	
def getChatStatus(channel_id):
	result = executeQuery(f"SELECT Y.NAME,X.STATE,X.TEMPORARY,X.CONFIRM,X.TVTCHANNEL,X.UPDATED < UNIX_TIMESTAMP()-24*3600 FROM CHAT_SUPPORT X \
		JOIN TEAMS Y\
		WHERE X.CHANNEL={channel_id} AND X.TEAM = Y.TEAMID AND X.WSID IS NOT NULL")
	if result == None:
		return "There is no team registered to this channel."
	if type(result) == list:
		return "Oops. Error. That's not supposed to happen."
	NAME,STATE,TEMPORARY,CONFIRM,TVT_CHANNEL,EXPIRED = [result[0],result[1],result[2],result[3],result[4],result[5]]
	confirm_str = "Yes" if CONFIRM == 'Y' else "No"
	expired_str = "Yes" if EXPIRED == 1 else "No"
	tvt_channel_str = f"<#{TVT_CHANNEL}>" if TVT_CHANNEL != None else "None"
	return f"Team: {NAME}\nVerified or Pending? {STATE}\nDiscord-to-SPPD Confirmation Messages: {confirm_str}\nTVT Channel: {tvt_channel_str}\nExpired: {expired_str}"
	
def getBind(dServer,dWord):
	result_text = ""
	result_file = ""
	result = executeSanitize(f"SELECT DTYPE, DCONTENT FROM DOUGLAS_BINDER WHERE DSERVER={dServer} AND DWORD = %(name)s", dWord, like_search = False)
	if result == None or type(result) == list: return result_text, result_file
	DTYPE = str(result[0])
	DCONTENT = str(result[1])
	if DTYPE == "TEXT":
		result_text = DCONTENT
	elif DTYPE == "FILE":
		result_file = DCONTENT
	return result_text, result_file
	
def getBindByCommandID(dServer,discordID):
	result = executeQuery(f"SELECT DTYPE, DCONTENT FROM DOUGLAS_BINDER WHERE DSERVER={dServer} AND DISCORDID = {discordID}")
	if result == None or type(result) == list: return None, None
	DTYPE = str(result[0])
	DCONTENT = str(result[1])
	return DCONTENT, DTYPE
	
def getBindID(dServer,dWord):
	result = executeSanitize(f"SELECT DISCORDID FROM DOUGLAS_BINDER WHERE DSERVER={dServer} AND DWORD = %(name)s", dWord, like_search = False)
	if result == None or type(result) == list: return None
	DISCORDID = result[0]
	return DISCORDID
	
def getOldBinds(dServer):
	old_binds = []
	result = executeQuery(f"SELECT DWORD, DTYPE, DCONTENT FROM DOUGLAS_BINDER WHERE DSERVER={dServer} AND DISCORDID IS NULL")
	if result == None: return old_binds
	if type(result) == tuple: result = [result]
	for row in result:
		old_binds.append([row[0],row[1],row[2]])
	return old_binds
	
def getAllBinds(dServer):
	DWORD_LIST=[]
	result = executeQuery(f"SELECT DWORD FROM DOUGLAS_BINDER WHERE DSERVER={dServer} AND DISCORDID IS NOT NULL")
	if result == None: return DWORD_LIST
	if type(result) == tuple: result = [result]
	for row in result:
		DWORD_LIST.append(row[0])
	return DWORD_LIST
	
def getNameFromCardID(card_id):
	card_name = "Unknown"
	if card_id in LOCALIZATION.ASSET:
		df_key = LOCALIZATION.ASSET[card_id]
		if type(df_key) == list:
			df_key = df_key[0]
		keyword = "DF_NAME_" + df_key
		if keyword in LOCALIZATION.LOCAL: 
			card_name = LOCALIZATION.LOCAL[keyword][0]
		else:
			card_name = df_key
	return card_name
	
def getCardIDFromName(card_name):
	card_id = None
	orig_name = None
	lang_index = 0
	lower_card_name = card_name.lower()
	skip_cache = False
	try:
		card_id = int(card_name)
		if card_id in LOCALIZATION.ASSET:
			df_key = LOCALIZATION.ASSET[card_id]
			if type(df_key) == list:
				df_key = df_key[0]
			keyword = "DF_NAME_" + df_key
			if keyword in LOCALIZATION.LOCAL: 
				card_name = LOCALIZATION.LOCAL[keyword][0]
				orig_name = card_name
				skip_cache = True
			else:
				card_name = df_key
				orig_name = df_key
		else:
			card_id = None
	except:
		card_id = None
		
	BOSS = 'boss' in lower_card_name
	if card_id == None and not BOSS:
		if card_name.upper() in DATABASE.ACRO_MAP:
			card_id = DATABASE.ACRO_MAP[card_name.upper()]
			card_name = DATABASE.DECK_MAP[card_id][0]
			orig_name = card_name
		if card_id == None:
			for lower_name in DATABASE.LOWER_NAME_TO_ID:
				if card_name in lower_name:
					card_id = DATABASE.LOWER_NAME_TO_ID[lower_name]
					card_name = DATABASE.DECK_MAP[card_id][0]
					orig_name = card_name
					break
	if card_id == None:
		lower_card_name = lower_card_name.replace('boss','').strip()
		if card_id == None:
			for key in DATABASE.IGNORE_LIST:
				tmp_name = DATABASE.IGNORE_LIST[key][0]
				if lower_card_name in tmp_name.lower():
					card_id = key
					card_name = tmp_name
					orig_name = card_name
					break
	if card_id == None:
		found_name = False
		for key in LOCALIZATION.LOCAL:
			if found_name: break
			if key[:7] != 'DF_NAME': continue
			for cname in LOCALIZATION.LOCAL[key]:
				if card_name in cname.lower():
					lang_index = LOCALIZATION.LOCAL[key].index(cname)
					card_name = cname
					orig_name = card_name
					#Find the cardid
					tmp_key = key.replace('DF_NAME_','')
					if tmp_key in LOCALIZATION.REVERSE_ASSET:
						card_id = LOCALIZATION.REVERSE_ASSET[tmp_key]
						if card_id in DATABASE.DECK_MAP:
							orig_name = DATABASE.DECK_MAP[card_id][0]
					found_name = True
					break
	return card_id, orig_name, card_name, skip_cache, lang_index, BOSS
	
def getCardDataAtLevel(card_name,level_upgrade):
	LEVEL=None
	UPGRADE=None
	USERID=None
	filename = None
	success = False
	response = "I don't understand... We're sorry..."
	
	card_id, card_name, orig_name, skip_cache, lang_index, BOSS = getCardIDFromName(card_name)
	
	if card_id == None or orig_name == None:
		response="Try typing the card name as it appears in the game."
		return response,success,None
	
	max_upgrades = False
	upgrade = None
	level = None
	try:
		level_upgrade = level_upgrade.lower()
		if 'l' in level_upgrade:
			level = int(level_upgrade.strip('l'))
		elif 'm' in level_upgrade:
			level = int(level_upgrade.strip('m'))
			max_upgrades = True
		elif 'u' in level_upgrade:
			upgrade = int(level_upgrade.strip('u'))
		else:
			level = int(level_upgrade)
	except:
		response = 'The level you asked for is weird...'
		return response, success,None
		
	if card_id == 1 and level > 25: 
		USERID = level
		result = executeQuery(f"SELECT NKLEVEL FROM team_members WHERE USERID = (SELECT USERID FROM users WHERE ID = {USERID})")
		if result != None:
			level = result[0]
	WHERE_QUERY = ''
	LIMIT = 1
	if level != None:
		WHERE_QUERY = f'X.LEVEL = {level}'
	elif upgrade != None:
		WHERE_QUERY = f'X.UPGRADE = {upgrade}'
		LIMIT = 2
	if max_upgrades:
		WHERE_QUERY += ' ORDER BY X.UPGRADE DESC'
	WHERE_QUERY += f' LIMIT {LIMIT}'
	
	#result = executeQuery(f"SELECT LEVEL,UPGRADE,HEALTH,ATTACK,SPECIAL1,STYPE1,SPECIAL2,STYPE2,SPECIAL3,STYPE3 FROM CARDS_DYNAMIC_STATS WHERE CARDID = {card_id} AND {WHERE_QUERY}")
	result = executeQuery(f"SELECT X.LEVEL,X.UPGRADE,X.HEALTH,X.ATTACK,X.SPECIAL1,X.STYPE1,X.SPECIAL2,X.STYPE2,X.SPECIAL3,X.STYPE3,\
		Y.TAGS,Y.RANG,Y.TBA,Y.HLOSS,Y.CASTAREA,Y.AOE,Y.ARADIUS,Y.APERCENT,Y.ACONE,Y.TRADIUS,Y.MARENA,Y.CRADIUS,Y.WEIGHT,Y.KNOCKBACK,Y.CREGEN,Y.CANIM,Y.CACTIVE,Y.WANIM,Y.DANIM,Y.TVELOCITY,Y.MVELOCITY,Y.AGGRO,Y.UNITS,Y.SRADIUS,\
		Y.COST,Y.TYPE,Y.CHARTYPE,Y.THEME,Y.RARITY,Y.IMAGE\
			FROM cards_dynamic_stats X \
			JOIN cards_static_stats Y\
		WHERE X.CARDID = {card_id} AND Y.ID = {card_id} AND {WHERE_QUERY}")
	if result == None:
		response = 'Umm... No data.'
		return response, success,None
	
	long_response = f'https://sppdreplay.net/cards/{card_id}\n'
	long_response += f'```yaml\n'
	long_response += f'Name: {card_name}\n'
	success=True
	if type(result) != tuple:
		result = result[0] #We just got 2 results
	card_details = [result[0],result[1],result[2],result[3],result[4],result[5],result[6],result[7],result[8],result[9]]
	static_stats = [result[10],result[11],result[12],result[13],result[14],result[15],result[16],result[17],result[18],result[19],result[20],result[21],result[22],result[23],result[24],result[25],result[26],result[27],result[28],result[29],result[30],result[31],result[32],result[33]]
	static_details = [result[34],result[35],result[36],result[37],result[38]]
	art_filename = result[39]
	if BOSS:
		#Get the card details of the non-boss card
		#Add X.SPECIAL1,X.STYPE1,X.SPECIAL2,X.STYPE2,X.SPECIAL3,X.STYPE3 if it doesn't exist in the boss card.
		non_boss_card_id = None
		if orig_name in DATABASE.NAME_TO_ID:
			non_boss_card_id = DATABASE.NAME_TO_ID[orig_name]
		if non_boss_card_id == None:
			print(f'Could not find {orig_name} in NAME_TO_ID')
		else:
			#Store the orig card_details
			orig_card_details = {}
			for i in range(3):
				offset = 2*i
				key, value = card_details[5+offset], card_details[4+offset]
				if key == None: break
				orig_card_details[key] = value
			result = executeQuery(f"SELECT X.LEVEL,X.UPGRADE,X.HEALTH,X.ATTACK,X.SPECIAL1,X.STYPE1,X.SPECIAL2,X.STYPE2,X.SPECIAL3,X.STYPE3\
				FROM cards_dynamic_stats X \
			WHERE X.CARDID = {non_boss_card_id} AND {WHERE_QUERY}")
			if type(result) != tuple:
				result = result[0] #We just got 2 results
			non_boss_card_details = [result[0],result[1],result[2],result[3],result[4],result[5],result[6],result[7],result[8],result[9]]
			new_card_details = {}
			for i in range(3):
				offset = 2*i
				key, value = non_boss_card_details[5+offset], non_boss_card_details[4+offset]
				if key == None: break
				new_card_details[key] = value
			count = 0
			for key,value in new_card_details.items():
				offset = 2 * count
				card_details[5+offset] = key
				if key in orig_card_details:
					value = orig_card_details[key]
				card_details[4+offset] = value
				count+=1
			for i in range(count,3):
				offset = 2 * i
				card_details[5+offset] = None
				card_details[4+offset] = None
			#print(f'{orig_card_details},{new_card_details},{card_details}')
	filename = build_douglas_art.build_card_art(card_id, art_filename, orig_name, card_details, static_details, lang_index, BOSS, skip_cache, USERID)
	LEVEL,UPGRADE,HEALTH,ATTACK,SPECIAL1,STYPE1,SPECIAL2,STYPE2,SPECIAL3,STYPE3 = card_details
	
	TAGS,RANG,TBA,HLOSS,CASTAREA,AOE,ARADIUS,APERCENT,ACONE,TRADIUS,MARENA,CRADIUS,WEIGHT,KNOCKBACK,CREGEN,CANIM,CACTIVE,WANIM,DANIM,TVELOCITY,MVELOCITY,AGGRO,UNITS,SRADIUS = static_stats
	
	CTYPE = static_details[1]
	if CTYPE == "Character": CTYPE = build_douglas_art.getType(static_details[2])
	else: CTYPE = build_douglas_art.getType(static_details[1])
	is_spell = CTYPE in ['Spell','Trap']
		
	if not is_spell:
		long_response += f'Level: {LEVEL}, Upgrade: {UPGRADE}/70\n'
		long_response += f'\tHealth: {HEALTH}\n'
		long_response += f'\tAttack: {ATTACK}\n'
	else:
		long_response += f'Level {LEVEL}\n'
	if STYPE1 != None:
		if STYPE1 in DATABASE.CARD_ABILITIES:
			STYPE1 = DATABASE.CARD_ABILITIES[STYPE1]
		if type(SPECIAL1) == decimal.Decimal and SPECIAL1 % 1 == 0:
			SPECIAL1 = int(SPECIAL1)
		long_response += f'\t{STYPE1} {SPECIAL1}\n'
	if STYPE2 != None:
		if STYPE2 in DATABASE.CARD_ABILITIES:
			STYPE2 = DATABASE.CARD_ABILITIES[STYPE2]
		if type(SPECIAL2) == decimal.Decimal and SPECIAL2 % 1 == 0:
			SPECIAL2 = int(SPECIAL2)
		long_response += f'\t{STYPE2} {SPECIAL2}\n'
	if card_id == 1:
		health_per_bar = round(HEALTH/3)
		long_response += f'\tHealth Per Bar {health_per_bar}\n'
	#If non-zero/null List TBA, DPS, TAGS, RANG, TBA, HLOSS, CASTAREA, AOE, ARADIUS, APERCENT, ACONE, TRADIUS, MARENA, CRADIUS, WEIGHT, KNOCKBACK, CREGEN, CANIM, WANIM, DANIM, TVELOCITY, MVELOCITY, AGGRO, UNITS
	if not is_spell:
		if float(TBA) > 0:
			DPS = int(round(float(ATTACK) / float(TBA)))
			long_response += f'\tDamage Per Second: {DPS}\n'
	charge_character=False
	long_response += f'Static Attributes\n'
	if not is_spell:
		long_response += f'\tTime Between Attacks: {TBA}\n'
		if UNITS != None and UNITS > 1:
			long_response += f'\tUnits: {UNITS}\n'
		long_response += f'\tRange: {RANG}\n'
		if HLOSS != None and HLOSS != 0:
			long_response += f'\tLifespan: {HLOSS} seconds\n'
		if SRADIUS != None and SRADIUS != 0:
			SRADIUS = round(SRADIUS,2)
			long_response += f'\tCharacter Radius: {SRADIUS}\n'
	if AOE != None:
		AOE = int(AOE)
		if AOE != 0:
			long_response += f'\tAOE Radius: {ARADIUS}\n'
			if ACONE != None and ACONE != 0:
				if ACONE % 1 == 0: ACONE = int(ACONE)
				long_response += f'\tAOE Cone: {ACONE}°\n'
			if APERCENT != None:
				APERCENT = 100 * APERCENT
				if APERCENT % 1 == 0: APERCENT = int(APERCENT)
				long_response += f'\tAOE Percent: {APERCENT}%\n'
	if CREGEN != None:
		if CREGEN % 1 == 0: CREGEN = int(CREGEN)
		if CREGEN != 0:
			long_response += f'\tCharge Power Regen: {CREGEN} seconds\n'
			if CRADIUS != None:
				if CRADIUS % 1 == 0: CRADIUS = int(CRADIUS)
				if CRADIUS != 0:
					long_response += f'\tCharge Power Radius: {CRADIUS}\n'
			charge_character=True
	if CANIM != None:
		if CACTIVE != None:
			if CACTIVE % 1 == 0: CACTIVE = int(CACTIVE)
		if CANIM % 1 == 0: CANIM = int(CANIM)
		if CANIM != 0:
			if charge_character:
				long_response += f'\tCharge Entire Animation: {CANIM} seconds\n'
			else:
				long_response += f'\tEnrage Entire Animation: {CANIM} seconds\n'
		if CACTIVE != 0:
			if charge_character:
				long_response += f'\tCharge Activates During Animation: {CACTIVE} seconds\n'
			else:
				long_response += f'\tEnrage Activates During Animation: {CACTIVE} seconds\n'
	if WANIM != None:
		if WANIM % 1 == 0: WANIM = int(WANIM)
		if WANIM != 0:
			long_response += f'\tWarcry Animation: {WANIM} seconds\n'
	if DANIM != None:
		if DANIM % 1 == 0: DANIM = int(DANIM)
		if DANIM != 0:
			long_response += f'\tDeathwish Animation: {DANIM} seconds\n'
	if TVELOCITY != None and TVELOCITY != 0:
		long_response += f'\tTime to Max Velocity: {TVELOCITY}\n'
		if MVELOCITY != None and MVELOCITY != 0:
			long_response += f'\tMax Velocity: {MVELOCITY}\n'
	if AGGRO != None:
		if AGGRO % 1 == 0: AGGRO = int(AGGRO)
		if AGGRO != 0:
			long_response += f'\tAggro Range Multiplier: {AGGRO}\n'
	if not is_spell and KNOCKBACK != None:
		if KNOCKBACK % 1 == 0: KNOCKBACK = int(KNOCKBACK)
		if KNOCKBACK != 0:
			long_response += f'\tKnockback: {KNOCKBACK}\n'
	if not is_spell and WEIGHT != None:
		if WEIGHT % 1 == 0: WEIGHT = int(WEIGHT)
		if WEIGHT != 0:
			long_response += f'\tWeight: {WEIGHT}\n'
	if TRADIUS != None and TRADIUS > 0:
		long_response += f'\tTargeting Radius: {TRADIUS}\n'
	long_response += f'\tCast Area: {CASTAREA}\n'
	long_response += f'\tUnlocked Arena: {MARENA}\n'
	TAGS = ', '.join(str(x) for x in TAGS)
	long_response += f'\tTags: {TAGS}\n'
	if len(long_response) >= 1997:
		long_response = long_response[:1997]
	long_response += f'```'
	
	return long_response, success, filename
	
def getCardArt(card_id):
	success = False
	response = "I don't understand... We're sorry..."
	if card_id == None:
		response="Try typing the card name as it appears in the game."
		return response,success,None
	
	result = executeQuery(f"SELECT IMAGE FROM cards_static_stats WHERE ID = {card_id}")
	if result == None:
		response="No card art exists for that card...anywhere."
		return response,success,None
	result = result[0]
	filename,_ = build_douglas_art.findImage2(result)
	if filename == None:
		response="Doesn't exist yet, but you can request it to be added."
		return response,success,None
	success=True
	long_response=''
	return long_response, success, filename
	
def getPlayerIDByName(player_name):
	USERID = None
	if type(player_name) == str: player_name=removeCharactersOutOfRange(player_name)
	result = executeSanitize("SELECT NAME, USERID FROM USERS WHERE NAME LIKE %(name)s", player_name)
	if type(result) == tuple: result = [result]
	if result == None: return USERID
	for row in result:
		NAME = row[0]
		ID = row[1]
		if player_name.upper() == NAME.upper():
			return ID
	return USERID
	
def getCardsFromDeckID(deck_id):
	if deck_id == None: return None
	cards=[]
	card_ids = executeQuery(f"SELECT CARDID1,CARDID2,CARDID3,CARDID4,CARDID5,CARDID6,CARDID7,CARDID8,CARDID9,CARDID10,CARDID11,CARDID12 from DECKS_TWO WHERE ID={deck_id}")
	if card_ids == None: return cards
	if type(card_ids) == tuple and card_ids[0] != None:
		for i in range(12):
			actual_card_id = -1
			if card_ids[i] != None:
				actual_card_id=card_ids[i]
			cards.append(actual_card_id)
	return cards
	
def getPlayerDetails(userid):
	long_response = ""
	result = executeQuery(f"SELECT y.ID, y.NAME, z.NAME, x.RANK, x.MMR, x.NKLEVEL, x.ROLE FROM TEAM_MEMBERS x\
		JOIN (SELECT ID, NAME, USERID FROM USERS WHERE USERID = '{userid}') y\
		JOIN (SELECT NAME, TEAMID FROM TEAMS WHERE TEAMID = (SELECT TEAMID FROM TEAM_MEMBERS WHERE USERID = '{userid}')) z\
		WHERE x.USERID = '{userid}' AND y.USERID = '{userid}' AND x.TEAMID = z.TEAMID")
	if result == None: return "Sorry, I can't find that player. Part 2.", False
	if type(result) == tuple:
		unique_player_id = result[0]
		player_name = result[1]
		team_name = result[2]
		RANK = result[3]
		mmr = result[4]
		nklevel = result[5]
		role = result[6]
		if type(player_name) == str: player_name=player_name.upper()
		if type(team_name) == str: team_name=team_name.upper()
		long_response += f"https://sppdreplay.net/player/{unique_player_id}\n"
		long_response += f'```yaml\n'
		long_response += f"Name : {player_name}\n"
		long_response += f"Team : {team_name}\n"
		if RANK <= 2000 and RANK != 0:
			long_response += f"Rank : {RANK}\n"
		long_response += f"MMR : {mmr}\n"
		long_response += f"NK Level : {nklevel}\n"
		long_response += f"Role : {role}\n"
	
	deck,theme = getDeckFromUserID(userid)
	if deck == None:
		long_response += f'```'
		return long_response, True
	
	avg_cost = findAvgCost(deck)
	long_response += f"Themes: {theme}, Avg Cost: {avg_cost}\n"
	long_response += f"Deck:\n"
	for card_id in deck:
		card_name = getCardName(card_id)
		long_response += f"\t- {card_name}\n"
		
	avg_collection_WAL, collection_num = getAvgCollectionWAL(userid)
	if avg_collection_WAL!=None:
		long_response += f"Average Collection WAL : {avg_collection_WAL}, Cards Found: {collection_num}\n"
		
	long_response += f'```'
	return long_response, True
	
def getAvgCollectionWAL(userid):
	collection_num=0
	result = executeQuery(f"SELECT CARDID, LEVEL, UPGRADES FROM USER_COLLECTIONS WHERE USERID = (SELECT ID FROM USERS WHERE USERID = '{userid}')")	
	if type(result) == tuple: result = [result]
	if result == None: return None, collection_num
	AVG = []
	for row in result:
		CARDID=row[0]
		LEVEL=row[1]
		UPGRADES=row[2]
		min_upgrades,max_upgrades=DATABASE.WAL_MAP[LEVEL]
		delta_upgrades=max_upgrades-min_upgrades+1
		level_with_upgrades=LEVEL+float(UPGRADES)/delta_upgrades
		wal_offset = getWALOffset(CARDID)
		if wal_offset == -1: return None, collection_num
		wal_level = level_with_upgrades + wal_offset
		AVG.append(wal_level)
		collection_num+=1
	if len(AVG) == 0: return None, collection_num
	actual_avg=float(sum(AVG)) / len(AVG)
	show_avg="%.2f" % actual_avg
	return show_avg, collection_num
	
def getWALOffset(id):
	if id in DATABASE.DECK_MAP:
		if "leg" in DATABASE.DECK_MAP[id]: return 3
		if "epi" in DATABASE.DECK_MAP[id]: return 2
		if "rar" in DATABASE.DECK_MAP[id]: return 1
		if "com" in DATABASE.DECK_MAP[id]: return 0
	return -1
	
def getDeckFromUserID(userid):
	result = executeQuery(f"SELECT DECKID FROM TEAM_MEMBERS WHERE USERID='{userid}'")
	deck=None
	theme=None
	if type(result) == tuple: result = result[0]
	if result == None: return deck, theme
	deck=getCardsFromDeckID(result)
	theme=findThemes(deck)
	theme=','.join(x for x in theme)
	return deck, theme
	
def getCost(card_id):
	if card_id in DATABASE.DECK_MAP:
		return DATABASE.DECK_MAP[card_id][1]
	return -1
	
def getTheme(card_id):
	if card_id in DATABASE.DECK_MAP:
		return DATABASE.DECK_MAP[card_id][3]
	return "Unknown"
	
def getCardName(card_id):
	if card_id in DATABASE.DECK_MAP:
		return DATABASE.DECK_MAP[card_id][0].upper()
	return "Unknown"
		
def findThemes(deck):
	themes=[]
	for id in deck:
		theme=getTheme(id)
		if theme not in themes and theme != "neu":
			themes.append(theme)
	themes.sort()
	while len(themes)<2:
		themes.append("neu")
	return themes
	
def findAvgCost(deck):
	if len(deck) != 12: return -1
	costs=[]
	for id in deck:
		cost=getCost(id)
		if cost < 0: return -1
		costs.append(cost)
	avg_cost = round(float(sum(costs))/len(deck),1)
	return avg_cost
	
def getCompareResponse(card_name,from_level,to_level):
	LEVEL=None
	UPGRADE=None
	USERID=None
	filename = None
	success = False
	response = "I don't understand... We're sorry..."
	
	if from_level == to_level:
		return random.choice([
			"Seriously? You need a bot to tell you the difference between the same level?",
			"Am I a joke to you?",
			"This isn't funny, you know.",
			"What’s wrong with you?"
		]), False
	
	card_id, card_name, orig_name, skip_cache, lang_index, BOSS = getCardIDFromName(card_name)
	
	if card_id == None or orig_name == None:
		response="Try typing the card name as it appears in the game."
		return response,success
	
	long_response = f'https://sppdreplay.net/cards/{card_id}\n'
	long_response += f'```yaml\n'
	long_response += f'Name: {card_name}\n'
	
	is_spell = None
	
	LEVEL_ = []
	UPGRADE_ = []
	HEALTH_ = []
	ATTACK_ = []
	STYPE1_ = []
	SPECIAL1_ = []
	STYPE2_ = []
	SPECIAL2_ = []
	
	TAGS = None
	RANG = None
	TBA = None
	HLOSS = None
	CASTAREA = None
	AOE = None
	ARADIUS = None
	APERCENT = None
	ACONE = None
	TRADIUS = None
	MARENA = None
	CRADIUS = None
	WEIGHT = None
	KNOCKBACK = None
	CREGEN = None
	CANIM = None
	CACTIVE = None
	WANIM = None
	DANIM = None
	TVELOCITY = None
	MVELOCITY = None
	AGGRO = None
	UNITS = None
	SRADIUS = None
	
	for level_upgrade in [from_level,to_level]:
		max_upgrades = False
		upgrade = None
		level = None
		try:
			level_upgrade = level_upgrade.lower()
			if 'l' in level_upgrade:
				level = int(level_upgrade.strip('l'))
			elif 'm' in level_upgrade:
				level = int(level_upgrade.strip('m'))
				max_upgrades = True
			elif 'u' in level_upgrade:
				upgrade = int(level_upgrade.strip('u'))
			else:
				level = int(level_upgrade)
		except:
			response = 'The level you asked for is weird...'
			return response, success
			
		if card_id == 1 and level > 25: 
			USERID = level
			result = executeQuery(f"SELECT NKLEVEL FROM team_members WHERE USERID = (SELECT USERID FROM users WHERE ID = {USERID})")
			if result != None:
				level = result[0]
		WHERE_QUERY = ''
		LIMIT = 1
		if level != None:
			WHERE_QUERY = f'X.LEVEL = {level}'
		elif upgrade != None:
			WHERE_QUERY = f'X.UPGRADE = {upgrade}'
			LIMIT = 2
		if max_upgrades:
			WHERE_QUERY += ' ORDER BY X.UPGRADE DESC'
		WHERE_QUERY += f' LIMIT {LIMIT}'
		
		#result = executeQuery(f"SELECT LEVEL,UPGRADE,HEALTH,ATTACK,SPECIAL1,STYPE1,SPECIAL2,STYPE2,SPECIAL3,STYPE3 FROM CARDS_DYNAMIC_STATS WHERE CARDID = {card_id} AND {WHERE_QUERY}")
		result = executeQuery(f"SELECT X.LEVEL,X.UPGRADE,X.HEALTH,X.ATTACK,X.SPECIAL1,X.STYPE1,X.SPECIAL2,X.STYPE2,X.SPECIAL3,X.STYPE3,\
			Y.TAGS,Y.RANG,Y.TBA,Y.HLOSS,Y.CASTAREA,Y.AOE,Y.ARADIUS,Y.APERCENT,Y.ACONE,Y.TRADIUS,Y.MARENA,Y.CRADIUS,Y.WEIGHT,Y.KNOCKBACK,Y.CREGEN,Y.CANIM,Y.CACTIVE,Y.WANIM,Y.DANIM,Y.TVELOCITY,Y.MVELOCITY,Y.AGGRO,Y.UNITS,Y.SRADIUS,\
			Y.COST,Y.TYPE,Y.CHARTYPE,Y.THEME,Y.RARITY,Y.IMAGE\
				FROM cards_dynamic_stats X \
				JOIN cards_static_stats Y\
			WHERE X.CARDID = {card_id} AND Y.ID = {card_id} AND {WHERE_QUERY}")
		if result == None:
			response = 'Umm... No data.'
			return response, success
		
		success=True
		if type(result) != tuple:
			result = result[0] #We just got 2 results
		card_details = [result[0],result[1],result[2],result[3],result[4],result[5],result[6],result[7],result[8],result[9]]
		static_stats = [result[10],result[11],result[12],result[13],result[14],result[15],result[16],result[17],result[18],result[19],result[20],result[21],result[22],result[23],result[24],result[25],result[26],result[27],result[28],result[29],result[30],result[31],result[32],result[33]]
		static_details = [result[34],result[35],result[36],result[37],result[38]]
		if BOSS:
			#Get the card details of the non-boss card
			#Add X.SPECIAL1,X.STYPE1,X.SPECIAL2,X.STYPE2,X.SPECIAL3,X.STYPE3 if it doesn't exist in the boss card.
			non_boss_card_id = None
			if orig_name in DATABASE.NAME_TO_ID:
				non_boss_card_id = DATABASE.NAME_TO_ID[orig_name]
			if non_boss_card_id == None:
				print(f'Could not find {orig_name} in NAME_TO_ID')
			else:
				#Store the orig card_details
				orig_card_details = {}
				for i in range(3):
					offset = 2*i
					key, value = card_details[5+offset], card_details[4+offset]
					if key == None: break
					orig_card_details[key] = value
				result = executeQuery(f"SELECT X.LEVEL,X.UPGRADE,X.HEALTH,X.ATTACK,X.SPECIAL1,X.STYPE1,X.SPECIAL2,X.STYPE2,X.SPECIAL3,X.STYPE3\
					FROM cards_dynamic_stats X \
				WHERE X.CARDID = {non_boss_card_id} AND {WHERE_QUERY}")
				if type(result) != tuple:
					result = result[0] #We just got 2 results
				non_boss_card_details = [result[0],result[1],result[2],result[3],result[4],result[5],result[6],result[7],result[8],result[9]]
				new_card_details = {}
				for i in range(3):
					offset = 2*i
					key, value = non_boss_card_details[5+offset], non_boss_card_details[4+offset]
					if key == None: break
					new_card_details[key] = value
				count = 0
				for key,value in new_card_details.items():
					offset = 2 * count
					card_details[5+offset] = key
					if key in orig_card_details:
						value = orig_card_details[key]
					card_details[4+offset] = value
					count+=1
				for i in range(count,3):
					offset = 2 * i
					card_details[5+offset] = None
					card_details[4+offset] = None
				#print(f'{orig_card_details},{new_card_details},{card_details}')
		LEVEL,UPGRADE,HEALTH,ATTACK,SPECIAL1,STYPE1,SPECIAL2,STYPE2,SPECIAL3,STYPE3 = card_details
		LEVEL_.append(LEVEL)
		UPGRADE_.append(UPGRADE)
		HEALTH_.append(HEALTH)
		ATTACK_.append(ATTACK)
		if type(SPECIAL1) == decimal.Decimal and SPECIAL1 % 1 == 0:
			SPECIAL1 = int(SPECIAL1)
		SPECIAL1_.append(SPECIAL1)
		STYPE1_.append(STYPE1)
		if type(SPECIAL2) == decimal.Decimal and SPECIAL2 % 1 == 0:
			SPECIAL2 = int(SPECIAL2)
		SPECIAL2_.append(SPECIAL2)
		STYPE2_.append(STYPE2)
		
		TAGS,RANG,TBA,HLOSS,CASTAREA,AOE,ARADIUS,APERCENT,ACONE,TRADIUS,MARENA,CRADIUS,WEIGHT,KNOCKBACK,CREGEN,CANIM,CACTIVE,WANIM,DANIM,TVELOCITY,MVELOCITY,AGGRO,UNITS,SRADIUS = static_stats
		CTYPE = static_details[1]
		if CTYPE == "Character": CTYPE = build_douglas_art.getType(static_details[2])
		else: CTYPE = build_douglas_art.getType(static_details[1])
		is_spell = CTYPE in ['Spell','Trap']
	
	HEADERS=[]
	card_data=[]
	if not is_spell:
		HEADERS = ['', f'L{LEVEL_[0]}U{UPGRADE_[0]}', f'L{LEVEL_[1]}U{UPGRADE_[1]}', '% Change']
		healthc = 0 if HEALTH_[0] == 0 else round(100 * (HEALTH_[1] - HEALTH_[0]) / HEALTH_[0], 1)
		attackc = 0 if ATTACK_[0] == 0 else round(100 * (ATTACK_[1] - ATTACK_[0]) / ATTACK_[0], 1)
		card_data.append(['Health:', HEALTH_[0], HEALTH_[1], f'{healthc}%'])
		card_data.append(['Attack:', ATTACK_[0], ATTACK_[1], f'{attackc}%'])
	else:
		HEADERS = ['', f'L{LEVEL_[0]}', f'L{LEVEL_[1]}', '% Change']
	if STYPE1_[0] != None and STYPE1_[0]==STYPE1_[1]:
		if STYPE1_[0] in DATABASE.CARD_ABILITIES:
			STYPE1_[0] = DATABASE.CARD_ABILITIES[STYPE1_[0]]
		special1c = 0 if SPECIAL1_[0] == 0 else round(100 * (SPECIAL1_[1] - SPECIAL1_[0]) / SPECIAL1_[0], 1)
		card_data.append([f'{STYPE1_[0]}:', SPECIAL1_[0], SPECIAL1_[1], f'{special1c}%'])
	if STYPE2_[0] != None and STYPE2_[0]==STYPE2_[1]:
		if STYPE2_[0] in DATABASE.CARD_ABILITIES:
			STYPE2_[0] = DATABASE.CARD_ABILITIES[STYPE2_[0]]
		special2c = 0 if SPECIAL2_[0] == 0 else round(100 * (SPECIAL2_[1] - SPECIAL2_[0]) / SPECIAL2_[0], 1)
		card_data.append([f'{STYPE2_[0]}:', SPECIAL2_[0], SPECIAL2_[1], f'{special2c}%'])
	if card_id == 1:
		health_per_bar = [round(HEALTH_[0]/3),round(HEALTH_[1]/3)]
		hpbc = round(100 * (health_per_bar[1] - health_per_bar[0]) / health_per_bar[0], 1)
		card_data.append(['Health Per Bar:', health_per_bar[0], health_per_bar[1], f'{hpbc}%'])
	#If non-zero/null List TBA, DPS, TAGS, RANG, TBA, HLOSS, CASTAREA, AOE, ARADIUS, APERCENT, ACONE, TRADIUS, MARENA, CRADIUS, WEIGHT, KNOCKBACK, CREGEN, CANIM, WANIM, DANIM, TVELOCITY, MVELOCITY, AGGRO, UNITS
	if not is_spell:
		if float(TBA) > 0:
			DPS = [int(round(float(ATTACK_[0]) / float(TBA))), int(round(float(ATTACK_[1]) / float(TBA)))]
			dpsc = 0 if DPS[0] == 0 else round(100 * (DPS[1] - DPS[0]) / DPS[0], 1)
			card_data.append(['Damage Per Second:', DPS[0], DPS[1], f'{dpsc}%'])
	long_response += tabulate(card_data, headers=HEADERS)
	long_response += "\n\n"
	charge_character=False
	long_response += f'Static Attributes\n'
	if not is_spell:
		long_response += f'\tTime Between Attacks: {TBA}\n'
		if UNITS != None and UNITS > 1:
			long_response += f'\tUnits: {UNITS}\n'
		long_response += f'\tRange: {RANG}\n'
		if HLOSS != None and HLOSS != 0:
			long_response += f'\tLifespan: {HLOSS} seconds\n'
		if SRADIUS != None and SRADIUS != 0:
			SRADIUS = round(SRADIUS,2)
			long_response += f'\tCharacter Radius: {SRADIUS}\n'
	if AOE != None:
		AOE = int(AOE)
		if AOE != 0:
			long_response += f'\tAOE Radius: {ARADIUS}\n'
			if ACONE != None and ACONE != 0:
				if ACONE % 1 == 0: ACONE = int(ACONE)
				long_response += f'\tAOE Cone: {ACONE}°\n'
			if APERCENT != None:
				APERCENT = 100 * APERCENT
				if APERCENT % 1 == 0: APERCENT = int(APERCENT)
				long_response += f'\tAOE Percent: {APERCENT}%\n'
	if CREGEN != None:
		if CREGEN % 1 == 0: CREGEN = int(CREGEN)
		if CREGEN != 0:
			long_response += f'\tCharge Power Regen: {CREGEN} seconds\n'
			if CRADIUS != None:
				if CRADIUS % 1 == 0: CRADIUS = int(CRADIUS)
				if CRADIUS != 0:
					long_response += f'\tCharge Power Radius: {CRADIUS}\n'
			charge_character=True
	if CANIM != None:
		if CACTIVE != None:
			if CACTIVE % 1 == 0: CACTIVE = int(CACTIVE)
		if CANIM % 1 == 0: CANIM = int(CANIM)
		if CANIM != 0:
			if charge_character:
				long_response += f'\tCharge Entire Animation: {CANIM} seconds\n'
			else:
				long_response += f'\tEnrage Entire Animation: {CANIM} seconds\n'
		if CACTIVE != 0:
			if charge_character:
				long_response += f'\tCharge Activates During Animation: {CACTIVE} seconds\n'
			else:
				long_response += f'\tEnrage Activates During Animation: {CACTIVE} seconds\n'
	if WANIM != None:
		if WANIM % 1 == 0: WANIM = int(WANIM)
		if WANIM != 0:
			long_response += f'\tWarcry Animation: {WANIM} seconds\n'
	if DANIM != None:
		if DANIM % 1 == 0: DANIM = int(DANIM)
		if DANIM != 0:
			long_response += f'\tDeathwish Animation: {DANIM} seconds\n'
	if TVELOCITY != None and TVELOCITY != 0:
		long_response += f'\tTime to Max Velocity: {TVELOCITY}\n'
		if MVELOCITY != None and MVELOCITY != 0:
			long_response += f'\tMax Velocity: {MVELOCITY}\n'
	if AGGRO != None:
		if AGGRO % 1 == 0: AGGRO = int(AGGRO)
		if AGGRO != 0:
			long_response += f'\tAggro Range Multiplier: {AGGRO}\n'
	if not is_spell and KNOCKBACK != None:
		if KNOCKBACK % 1 == 0: KNOCKBACK = int(KNOCKBACK)
		if KNOCKBACK != 0:
			long_response += f'\tKnockback: {KNOCKBACK}\n'
	if not is_spell and WEIGHT != None:
		if WEIGHT % 1 == 0: WEIGHT = int(WEIGHT)
		if WEIGHT != 0:
			long_response += f'\tWeight: {WEIGHT}\n'
	if TRADIUS != None and TRADIUS > 0:
		long_response += f'\tTargeting Radius: {TRADIUS}\n'
	long_response += f'\tCast Area: {CASTAREA}\n'
	long_response += f'\tUnlocked Arena: {MARENA}\n'
	TAGS = ', '.join(str(x) for x in TAGS)
	long_response += f'\tTags: {TAGS}\n'
	if len(long_response) >= 1997:
		long_response = long_response[:1997]
	long_response += f'```'
	return long_response, success
	
	
def getBracketResponseSubscribed(team_name):
	if team_name == '':
		return "Seriously...?", False
	TEAMID = getUniqueTeamIDByName(team_name)
	if TEAMID == -1:
		return "Sorry, I can't find that team.", False
	bracket_data, updated = getTeamwarBracketData(TEAMID)
	old_bracket_data = getTeamwarBracketHistoryData(TEAMID)
	oBRACKETID = 0
	oTEAMNAME = ""
	oRUNS = 0
	oSCORE = 0
	if old_bracket_data != None and len(old_bracket_data) == 4:
		oBRACKETID,oTEAMNAME,oRUNS,oSCORE = old_bracket_data
	if updated == None: return "Could not find that team's bracket.", False
	delta_score = None
	delta_runs = None
	delta_avg = None
	sorted_bracket_data = []
	BRACKETID = -1
	for ID,RANK,TEAMNAME,RUNS,MEMBERS,SCORE in bracket_data:
		tmp_team_name = TEAMNAME
		if type(tmp_team_name) == str: tmp_team_name = tmp_team_name.upper()
		BRACKETID=ID
		avg = 0
		if RUNS > 0:
			avg="%.2f" % (float(SCORE) / RUNS)
		if tmp_team_name == oTEAMNAME and ID == oBRACKETID:
			delta_score = SCORE-oSCORE
			delta_score = f'{oSCORE}+{delta_score}'
			delta_runs = RUNS-oRUNS
			delta_runs = f'{oRUNS}+{delta_runs}'
			old_avg=0
			if oRUNS > 0:
				old_avg = "%.2f" % (float(oSCORE) / oRUNS)
			delta_avg = "%.2f" % (float(avg) - float(old_avg))
			if float(delta_avg) >= 0: delta_avg = f'+{delta_avg}'
			delta_avg = f'{old_avg}{delta_avg}'
		projected_num = int(float(avg) * MEMBERS)
		projected = "--"
		maximum = "--"
		if MEMBERS > RUNS:
			projected="%d" % int(float(avg) * MEMBERS)
			maximum="%d" % ( SCORE + (114 * (MEMBERS - RUNS)))
		if MEMBERS < 50:
			projected+=" / %d" % int(float(avg) * 50)
			maximum+=" / %d" % ( SCORE + (114 * (50 - RUNS)))
		sorted_bracket_data.append([RANK,tmp_team_name,SCORE,RUNS,float(avg)])
	sorted_bracket_data = sorted(sorted_bracket_data, key=lambda x: (x[4]), reverse=True)
	
	delta_bracket_data = [[oTEAMNAME,delta_score,delta_runs,delta_avg]]
	long_string = f'https://sppdreplay.net/brackets/{BRACKETID}\n'
	long_string += '```elm\n'
	if delta_runs != None:
		long_string += tabulate(delta_bracket_data, headers=["Team Name","Score","Runs","Average"])
		long_string += '\n'
		long_string += '\n'
	long_string += tabulate(sorted_bracket_data, headers=["Rank","Team Name","Score","Runs","Average"])
	long_string += '```'
	return long_string, True
	
def getBracketResponse(team_name):
	if team_name == '':
		return "Seriously...?", False
	TEAMID = getUniqueTeamIDByName(team_name)
	if TEAMID == -1:
		return "Sorry, I can't find that team.", False
	bracket_data, updated = getTeamwarBracketData(TEAMID)
	if updated == None: return "Could not find that team's bracket.", False
	sorted_bracket_data = []
	BRACKETID = -1
	for ID,RANK,TEAMNAME,RUNS,MEMBERS,SCORE in bracket_data:
		tmp_team_name = TEAMNAME
		if type(tmp_team_name) == str: tmp_team_name = tmp_team_name.upper()
		BRACKETID=ID
		avg = 0
		if RUNS > 0:
			avg="%.2f" % (float(SCORE) / RUNS)
		projected_num = int(float(avg) * MEMBERS)
		projected = "--"
		maximum = "--"
		if MEMBERS > RUNS:
			projected="%d" % int(float(avg) * MEMBERS)
			maximum="%d" % ( SCORE + (114 * (MEMBERS - RUNS)))
		if MEMBERS < 50:
			projected+=" / %d" % int(float(avg) * 50)
			maximum+=" / %d" % ( SCORE + (114 * (50 - RUNS)))
		sorted_bracket_data.append([RANK,tmp_team_name,SCORE,RUNS,float(avg)])
	sorted_bracket_data = sorted(sorted_bracket_data, key=lambda x: (x[4]), reverse=True)
	long_string = f'https://sppdreplay.net/brackets/{BRACKETID}\n'
	long_string += '```elm\n'
	long_string += tabulate(sorted_bracket_data, headers=["Rank","Team Name","Score","Runs","Average"])
	long_string += '```'
	return long_string, True
	
def getUniqueTeamIDByName(team_name):
	teamid = -1
	tmp_team_name = team_name
	if type(tmp_team_name) == str: tmp_team_name=tmp_team_name.lower()
	result = executeSanitize("SELECT y.NAME, x.ID from TEAMS_REPORT X\
		JOIN TEAMS Y\
		WHERE X.TEAMID IN (SELECT TEAMID FROM TEAMS WHERE NAME LIKE %(name)s) AND Y.TEAMID=X.TEAMID", tmp_team_name)
	if result == None: return teamid
	if type(result) == tuple:
		return result[1]
	for row in result:
		NAME = row[0]
		ID = row[1]
		if tmp_team_name == NAME:
			return ID
	return teamid
	
def getTeamResponse(team_name, deep_refresh):
	if team_name == '':
		return "Seriously...?", False
	TEAMID = getTeamIDByName(team_name)
	if TEAMID == 0:
		return "You!!! -_- You know exactly what you're doing...", False
	if deep_refresh:
		if TEAMID != -1: RESTFUL.refreshTeam(TEAMID, True, None)
		else:
			new_teamid = RESTFUL.getTeamIDFromName(team_name)
			if new_teamid != None: TEAMID = new_teamid
	if TEAMID == -1:
		return "Sorry, I can't find that team. Maybe you need `--deep`", False
	return getTeamDetails(TEAMID)
	
def getTeamIDByName(team_name):
	teamid = -1
	tmp_team_name = team_name
	if type(tmp_team_name) == str: tmp_team_name=tmp_team_name.lower()
	result = executeSanitize("SELECT NAME, TEAMID FROM TEAMS WHERE NAME LIKE %(name)s", tmp_team_name)
	if result == None: return teamid
	if type(result) == tuple: result = [result]
	for row in result:
		NAME = row[0]
		ID = row[1]
		if tmp_team_name == NAME:
			return ID
	return teamid
	
def getTeamDetails(teamid):
	long_response = ""
	#Link to team on SPPDReplay
	#List Member Names with NK Level and MMR
	result = executeQuery(f"SELECT x.ID, y.NAME, x.RANK, x.TROPHIES, x.MEMBERS, x.NKLEVEL, x.DESCRIPTION FROM TEAMS_REPORT x\
		JOIN (SELECT NAME, TEAMID FROM TEAMS WHERE TEAMID = {teamid}) y\
		WHERE x.TEAMID = {teamid} AND y.TEAMID = {teamid}")
	if result == None: return "Sorry, I can't find that team's details. Need `--deep`.", False
	if type(result) == tuple:
		unique_team_id = result[0]
		team_name = result[1]
		RANK = result[2]
		trophies = result[3]
		members = result[4]
		nklevel = result[5]
		description = result[6]
		if type(team_name) == str: team_name=team_name.upper()
		long_response += f"https://sppdreplay.net/teams/{unique_team_id}\n"
		long_response += f"```yaml\n"
		long_response += f"Name : {team_name}\n"
		if RANK <= 2000 and RANK != 0:
			long_response += f"Rank : {RANK}\n"
		league = "Wood"
		if trophies >= 3500: league = "Gold"
		elif trophies >= 1500: league = "Silver"
		elif trophies >= 500: league = "Bronze"
		long_response += f"League : {league}\n"
		long_response += f"Min NK Level : {nklevel}\n"
		long_response += f"Description : {description}\n"
		long_response += f"Members ({members})\n"
	
	result = executeQuery(f"SELECT y.NAME, x.NKLEVEL, x.MMR, x.RANK FROM TEAM_MEMBERS x\
		JOIN (SELECT NAME, USERID FROM USERS WHERE USERID IN (SELECT USERID FROM TEAM_MEMBERS WHERE TEAMID = {teamid})) y\
		WHERE x.USERID = y.USERID LIMIT 50")
	if type(result) == tuple: result = [result]
	if result == None: return "Sorry, that team has no members.", False
	ORDERED_LIST = [] #[ [NAME, NKLEVEL, MMR, RANK], ... ]
	for row in result:
		NAME = row[0]
		if type(NAME) == str: NAME = NAME.upper()
		NKLEVEL = row[1]
		MMR = row[2]
		RANK = row[3]
		ORDERED_LIST.append([NAME,NKLEVEL,MMR,RANK])
	ORDERED_LIST = sorted(ORDERED_LIST, key=lambda x: (x[2]), reverse=True)
	for NAME,NKLEVEL,MMR,RANK in ORDERED_LIST:
		if RANK <=1000 and RANK != 0:
			long_response += f"\t- {NAME}\tL{NKLEVEL}\t#{MMR}\tR{RANK}\n"
		else:
			long_response += f"\t- {NAME}\tL{NKLEVEL}\t#{MMR}\n"
	long_response += f"```"
	return long_response, True
	
def getLevelUpgrade(level_upgrade):
	max_upgrades = False
	level = None
	FINAL_LEVEL = None
	try:
		level_upgrade = level_upgrade.lower()
		if 'l' in level_upgrade:
			level = int(level_upgrade.strip('l'))
		elif 'm' in level_upgrade:
			level = int(level_upgrade.strip('m'))
			max_upgrades = True
		else:
			level = int(level_upgrade)
	except:
		print(f"Unable to parse: {level_upgrade}")
		pass
	if level in DATABASE.WAL_MAP:
		BASE,MAX = DATABASE.WAL_MAP[level]
		if max_upgrades:
			FINAL_LEVEL = f"{level}-{MAX}"
		else:
			if BASE == 0: BASE = 1
			FINAL_LEVEL = f"{level}-{BASE}"
	return FINAL_LEVEL
	
def getCalcResponse(rarity, from_level, to_level):
	total_coins = 0
	total_bronze = 0
	total_silver = 0
	total_gold = 0
	total_copies = 0
	total_exp = 0
	if rarity not in DATABASE.UPGRADE_COSTS:
		return "I don't understand. Pick a rarity: Common, Rare, Epic, Legendary. `-d calc <rarity> <from level> <to level>`", False
	if from_level not in DATABASE.UPGRADE_COSTS[rarity]:
		from_level = getLevelUpgrade(from_level)
		if from_level == None:
			return "I don't understand. Pick an accurate level-upgrade, like 1-5, 3-25, M5, or L7. `-d calc <rarity> <from level> <to level>`", False
	if to_level not in DATABASE.UPGRADE_COSTS[rarity]:
		to_level = getLevelUpgrade(to_level)
		if to_level == None:
			return "I don't understand. Pick an accurate level-upgrade, like 1-5, 2-15, or 3-25, M5 or L7. `-d calc <rarity> <from level> <to level>`", False
	if from_level == to_level:
		return random.choice([
			"Seriously? You need a calculator to tell you how much it costs to keep it the same level?",
			"Am I a joke to you?",
			"This isn't funny, you know.",
			"What’s wrong with you?"
		]), False
	
	level_found=False
	long_response = ""
	for cur_level in DATABASE.UPGRADE_COSTS[rarity]:
		if not level_found:
			#If the range is in the wrong direction, it costs nothing.
			if cur_level == to_level:
				return "Wrong order. `-d calc <rarity> <from level> <to level>`", False
			if cur_level == from_level:
				level_found = True
			continue
		coins, bronze, silver, gold, copies, experience = DATABASE.UPGRADE_COSTS[rarity][cur_level]
		total_coins+=coins
		total_bronze+=bronze
		total_silver+=silver
		total_gold+=gold
		total_copies+=copies
		total_exp+=experience
		if cur_level == to_level:
			break
	table_data = [
		["Coins", total_coins],
		["Bronze", total_bronze],
		["Silver", total_silver],
		["Gold", total_gold],
		["Copies", total_copies],
		["Experience", total_exp]
	]
	long_response = "```elm\n" + tabulate(table_data, headers=["",""]) + "\n```"
	return long_response, True
	
def getSearchResponse(name,is_team,is_card):
	if name == '':
		return "Seriously...?", False
	if is_card:
		names = name.split(" ")
		return getSearchCardTag(names)
	if len(name) < 5:
		return "Sorry, you need 5 or more characters (letters/numbers).", False
	if is_team: return getSearchTeamDetails(name)
	return getSearchDetails(name)
	
def getSearchTeamDetails(name):
	name = removeCharactersOutOfRange(name)
	result = executeSanitize(f"SELECT Y.NAME, X.RANK, X.TROPHIES, X.MEMBERS FROM teams_report X\
		JOIN (SELECT NAME, TEAMID FROM teams WHERE NAME LIKE %(name)s) Y\
	WHERE X.TEAMID = Y.TEAMID ORDER BY X.TROPHIES DESC LIMIT 25", name)
	if type(result) == tuple: result = [result]
	if result == None: return "Sorry, that search returned no results.", False
	ORDERED_LIST = [] #[ [NAME, RANK, TROPHIES, MEMBERS], ... ]
	for row in result:
		NAME = row[0]
		if type(NAME) == str: NAME = NAME.upper()
		RANK = row[1]
		TROPHIES = row[2]
		MEMBERS = row[3]
		ORDERED_LIST.append([NAME,RANK,TROPHIES,MEMBERS])
	ORDERED_LIST = sorted(ORDERED_LIST, key=lambda x: (x[2]), reverse=True)
	long_response="```elm\n"
	CLEAN_LIST=[]
	for NAME,RANK,TROPHIES,MEMBERS in ORDERED_LIST:
		if RANK > 2000: RANK = '>2000'
		CLEAN_LIST.append([NAME,RANK,TROPHIES,MEMBERS])
	'''
		if RANK <=1000 and RANK != 0:
			long_response += f"+ {NAME}\tL{NKLEVEL}\t#{MMR}\tR{RANK}\n"
		elif MMR >= 6000:
			long_response += f"+ {NAME}\tL{NKLEVEL}\t#{MMR}\n"
		else:
			long_response += f"- {NAME}\tL{NKLEVEL}\t#{MMR}\n"
	'''
	long_response += tabulate(CLEAN_LIST, headers=["Name","Rank","Trophies","Members"])
	long_response += "```"
	return long_response, True
	
def getSearchCardTag(names):
	found_tags = []
	for tag in VALID_TAGS:
		for name in names:
			if name.lower() == tag.lower():
				found_tags.append(tag)
				break
	if len(found_tags) == 0: return "Sorry, that's not a valid tag.", False
	WHERE_QUERY = []
	for tag in found_tags:
		x = 2**VALID_TAGS.index(tag)
		WHERE_QUERY.append(f"TAGS & {x}")
	WHERE_QUERY = "WHERE " + ' AND '.join(x for x in WHERE_QUERY)
	found_tags = '%'.join(x for x in found_tags)
	result = executeQuery(f"SELECT ID, NAME, RARITY, THEME, COST, TYPE, CHARTYPE FROM cards_static_stats\
		{WHERE_QUERY} ORDER BY THEME, TYPE, COST, RARITY")
	if type(result) == tuple: result = [result]
	if result == None: return "Sorry, that search returned no results.", False
	ORDERED_LIST = [] #[ [ID, NAME, RARITY, THEME, COST, TYPE], ... ]
	for row in result:
		ID = row[0]
		NAME = row[1]
		NAME2 = getNameFromCardID(ID)
		if NAME2 != "Unknown":
			NAME = NAME2
		RARITY = row[2]
		THEME = row[3]
		COST = row[4]
		TYPE = row[5]
		CHARTYPE = row[6]
		if type(NAME) == str: NAME = NAME.upper()
		if RARITY == 0:
			RARITY = "Common"
		elif RARITY == 1:
			RARITY = "Rare"
		elif RARITY == 2:
			RARITY = "Epic"
		elif RARITY == 3:
			RARITY = "Legendary"
		else:
			RARITY = "Unknown"
		if CHARTYPE != None:
			TYPE = CHARTYPE
		ORDERED_LIST.append([ID,NAME,RARITY,THEME,COST,TYPE])
	#ORDERED_LIST = sorted(ORDERED_LIST, key=lambda x: (x[2]), reverse=True)
	long_response="```elm\n"
	long_response += tabulate(ORDERED_LIST, headers=["ID","Name","Rarity","Theme","Cost","Type"])
	long_response += "```"
	return long_response, True
	
def getSearchDetails(name):
	name = removeCharactersOutOfRange(name)
	result = executeSanitize(f"SELECT y.NAME, x.NKLEVEL, x.MMR, x.RANK FROM TEAM_MEMBERS x\
		JOIN (SELECT NAME, USERID FROM USERS WHERE USERID IN (SELECT USERID FROM USERS WHERE NAME LIKE %(name)s)) y\
		WHERE x.USERID = y.USERID ORDER BY MMR DESC LIMIT 25", name)
	if type(result) == tuple: result = [result]
	if result == None: return "Sorry, that search returned no results.", False
	ORDERED_LIST = [] #[ [NAME, NKLEVEL, MMR, RANK], ... ]
	for row in result:
		NAME = row[0]
		if type(NAME) == str: NAME = NAME.upper()
		NKLEVEL = row[1]
		MMR = row[2]
		RANK = row[3]
		ORDERED_LIST.append([NAME,NKLEVEL,MMR,RANK])
	ORDERED_LIST = sorted(ORDERED_LIST, key=lambda x: (x[2]), reverse=True)
	long_response="```elm\n"
	CLEAN_LIST=[]
	for NAME,NKLEVEL,MMR,RANK in ORDERED_LIST:
		if RANK == 0: RANK = ''
		CLEAN_LIST.append([NAME,NKLEVEL,MMR,RANK])
	'''
		if RANK <=1000 and RANK != 0:
			long_response += f"+ {NAME}\tL{NKLEVEL}\t#{MMR}\tR{RANK}\n"
		elif MMR >= 6000:
			long_response += f"+ {NAME}\tL{NKLEVEL}\t#{MMR}\n"
		else:
			long_response += f"- {NAME}\tL{NKLEVEL}\t#{MMR}\n"
	'''
	long_response += tabulate(CLEAN_LIST, headers=["Name","NK Level","MMR","Rank"])
	long_response += "```"
	return long_response, True
	
	
### Legacy


def convertUpgrades(level,upgrades):
	min_upgrades,max_upgrades=DATABASE.WAL_MAP[level]
	cur_upgrades=min_upgrades+upgrades
	if cur_upgrades > max_upgrades: cur_upgrades = max_upgrades #Shouldn't be possible
	return f"{cur_upgrades}/{max_upgrades}"
	
def removeCharactersOutOfRange(word):
	char_list = [word[j] for j in range(len(word)) if ord(word[j]) in range(65536)]
	new_word=''
	for j in char_list:
		new_word=new_word+j
	new_word = new_word.lower()
	return new_word


###USERS
	
def isValidUserID(id):
	if id == "": return False
	USERID = executeQuery(f"SELECT USERID FROM USERS WHERE ID={id}")
	return USERID != None
	
def getInGameUserIDfromUniqueUserID(user_id):
	result = executeQuery(f"SELECT USERID FROM USERS WHERE ID = {user_id}")
	ingame_user_id=None
	if result != None: ingame_user_id=result[0]
	return ingame_user_id
	
def getUniqueUserIDfromInGameUserID(user_id):
	result = executeQuery(f"SELECT ID FROM USERS WHERE USERID = '{user_id}'")
	unique_user_id=None
	if result != None: unique_user_id=result[0]
	return unique_user_id

def getUsersCollection(g_user, unique_user_id_override=None,access_level=0):
	user_collection={}
	if g_user == None: return None
	unique_user_id=None
	if unique_user_id_override != None:
		unique_user_id=unique_user_id_override
		if access_level == -1:
			#Check if the target userid has opted out.
			result_optout = executeQuery(f"SELECT OPTOUT FROM USER_LOGINS WHERE USERID = (SELECT USERID FROM USERS WHERE ID = {unique_user_id}) AND OKTAID != '{g_user.id}'")
			if result_optout != None:
				if type(result_optout) == tuple: result_optout = result_optout[0]
				OPTOUT=0
				if result_optout!=None: OPTOUT=int(result_optout)
				if OPTOUT==1: return None
	else:
		user_id=getUserIDFromOktaID(g_user.id)
		if user_id == None: return None
		unique_user_id=getUniqueUserIDfromInGameUserID(user_id)
	if unique_user_id==None: return None #should never fail
	
	result = executeQuery(f"SELECT CARDID, LEVEL, UPGRADES FROM USER_COLLECTIONS WHERE USERID = {unique_user_id}")	
	if result == None: return user_collection
	elif type(result) == tuple: result=[result]
	for card_data in result:
		if card_data != None:
			card_id=card_data[0]
			level=card_data[1]
			upgrades=card_data[2]
			card_name=getCardName(card_id)
			user_collection[card_name]=[level,upgrades]
	return user_collection

def getUserName(user_id,platform=False):
	if platform:
		name = None
		plat = None
		result = executeQuery(f"SELECT NAME, PLATFORM FROM USERS WHERE USERID='{user_id}'")
		if type(result)==tuple:
			name=result[0]
			plat=result[1]
		if name != None and type(name) == str: name=name.upper()
		if plat != None and type(plat) == str: plat=plat.upper()
		return name, plat
	name = executeQuery(f"SELECT NAME FROM USERS WHERE USERID='{user_id}'")
	if type(name)==tuple: name=name[0]
	if name != None and type(name) == str: name=name.upper()
	return name
	
def getUserIDFromUniqueUserID(unique_user_id):
	userid = executeQuery(f"SELECT USERID FROM USERS WHERE ID={unique_user_id}")
	if userid != None: userid=userid[0]
	return userid
	
def getUserIDFromOktaID(okta_id):
	result = executeQuery(f"SELECT USERID, MAIN from USER_LOGINS WHERE OKTAID='{okta_id}'")
	if result == None: return None
	if type(result) == tuple: result=[result]
	USERID=None
	index = 0
	for row in result:
		user_id=row[0]
		primary=0
		if row[1] != None: primary=int(row[1])
		if index == 0 and user_id != None:
			USERID=user_id
		elif primary == 1:
			USERID=user_id
		index+=1
	return USERID
	
def getAccounts(g_user):
	accounts=[]
	if g_user == None: return accounts
	okta_id=g_user.id
	
	result = executeQuery(f"SELECT USERID, MAIN, OPTOUT from USER_LOGINS WHERE OKTAID='{okta_id}'")
	if result == None: return accounts
	if type(result) == tuple: result=[result]
	for row in result:
		user_id=row[0]
		primary=0
		if row[1] != None: primary=int(row[1])
		opt_out=0
		if row[2] != None: opt_out=int(row[2])
		name = executeQuery(f"SELECT NAME from USERS WHERE USERID='{user_id}'")
		if name == None: name = "Unknown..."
		accounts.append([name[0].upper(),primary==1,opt_out==1])
	#print(f'getAccounts: {accounts}')
	return accounts
	
def isPaidUser(g_user):
	if g_user == None: return False
	okta_id=g_user.id
	result = executeQuery(f"SELECT ID from USER_DONATED WHERE OKTAID='{okta_id}'")
	return result != None
	
def getPlayerNameLink(player_name):
	search_player_name=player_name.replace("'","''")
	unique_user_id = executeQuery(f"SELECT ID from USERS WHERE NAME='{search_player_name}'")
	if unique_user_id == None: return '/player'
	unique_user_id=unique_user_id[0]
	return f'/player/{unique_user_id}'

###TEAMS
def getPastNames(ingame_user_id, cur_name):
	past_names=[]
	result = executeQuery(f"SELECT NAME FROM USERS_NAMES_PAST WHERE USERID='{ingame_user_id}'")
	if result != None:
		for row in result:
			name = row
			if type(row) == tuple: name = row[0]
			if type(name) == str: name = name.upper()
			if name != cur_name: past_names.append(name)
	return past_names
	
def getPastTeams(ingame_user_id, cur_team):
	past_teams=[]
	result = executeQuery(f"SELECT NAME FROM TEAMS WHERE TEAMID IN (SELECT TEAMID FROM USERS_TEAMS_PAST WHERE USERID='{ingame_user_id}')")
	if result != None:
		for row in result:
			name = row
			if type(row) == tuple: name = row[0]
			if type(name) == str: name = name.upper()
			if name != cur_team: past_teams.append(name)
	return past_teams

def getUsersDeck(unique_user_id):
	result = executeQuery(f"SELECT DECKID FROM TEAM_MEMBERS WHERE USERID=(SELECT USERID FROM USERS WHERE ID = {unique_user_id})")
	deck=None
	theme=None
	if type(result) == tuple: result = result[0]
	if result == None: return deck, theme
	deck=getCardsFromDeckID(result)
	theme=findThemes(deck)
	theme=','.join(x for x in theme)
	return deck, theme

def getOneTeamMember(unique_user_id):
	ingame_user_id=getInGameUserIDfromUniqueUserID(unique_user_id)
	result = executeQuery(f"SELECT ROLE, JOINDATE, RANK, MMR, NKLEVEL, WINS_PVP, WINS_TW, WINS_CHLG, WINS_PVE, WINS_FF, WINS_FFP, WINS_PVPP, TW_TOKENS, DONATED_CUR, DONATED_ALL, TEAMID, UPDATED, DECKID, MAXMMR, CHLG_CMP, CHLG_MAX_SCORE FROM TEAM_MEMBERS WHERE USERID='{ingame_user_id}'")
	deck=None
	theme=None
	if result != None:
		DECKID=result[17]
		if DECKID != None:
			deck=getCardsFromDeckID(DECKID)
			theme=findThemes(deck)
			theme=','.join(x for x in theme)
	else: return None, deck, theme
	role = result[0]
	joindate = result[1]
	rank = result[2]
	mmr = result[3]
	nklevel = result[4]
	wins_pvp = result[5]
	wins_tw = result[6]
	wins_chlg = result[7]
	wins_pve = result[8]
	wins_ff = result[9]
	wins_ffp = result[10]
	wins_pvpp = result[11]
	tw_tokens = result[12]
	donated_cur = result[13]
	donated_all = result[14]
	ingame_teamid = result[15]
	updated = result[16]
	max_mmr = result[18]
	chlg_runs = result[19]
	chlg_max_score = result[20]
	team_name=getTeamNameFromIngameTeamID(ingame_teamid)
	team_name_link=getTeamLinkFromInGameID(ingame_teamid)
	name,plat=getUserName(ingame_user_id,True)
	past_names=getPastNames(ingame_user_id, name)
	past_teams=getPastTeams(ingame_user_id, team_name)
	return [name,role,joindate,rank,mmr,nklevel,wins_pvp,wins_tw,wins_chlg,wins_pve,wins_ff,wins_ffp,wins_pvpp,donated_cur,donated_all,team_name,team_name_link,updated,max_mmr,chlg_runs,chlg_max_score,plat,past_names,past_teams], deck, theme

def getLastRefreshFromUniqueTeamID(unique_team_id):
	if not isValidTeamID(unique_team_id): return -1
	UPDATED = executeQuery(f"SELECT UPDATED FROM TEAMS_REPORT WHERE ID={unique_team_id}")	
	if UPDATED == None: return -1 #Guaranteed to return a valid result, right? Yes.
	UPDATED=UPDATED[0]
	return UPDATED
	
def getAccessLevelTeam(g_user, unique_user_id, target_team_id=None):
	if g_user == None: return -1
	user_id=getUserIDFromOktaID(g_user.id)
	if user_id == None: return -1
	team_id=getInGameTeamIDFromUserID(user_id)
	if team_id == None: return -1
	if target_team_id == None:
		ingame_user_id=getInGameUserIDfromUniqueUserID(unique_user_id)
		this_team_id=getInGameTeamIDFromUserID(ingame_user_id)
	else:
		this_team_id=getInGameTeamID(target_team_id)
	#Are they on the same team?
	if this_team_id != team_id: return -1
	
	#get the role from the team
	ROLE = executeQuery(f"SELECT ROLE FROM TEAM_MEMBERS WHERE TEAMID={team_id} AND USERID='{user_id}'")	
	if ROLE == None: return -1 #Guaranteed to return a valid result, right?
	ROLE=ROLE[0]
	#Only leaders/co-leaders can modify, all other team members can only view.
	if ROLE == 'co_leader' or ROLE == 'leader': return 1
	return 0
	
def canRefreshTeam(g_user):
	if g_user == None: return False
	user_id=getUserIDFromOktaID(g_user.id)
	if user_id == None: return False
	team_id=getInGameTeamIDFromUserID(user_id)
	if team_id == None: return False
	
	#get the role from the team
	ROLE = executeQuery(f"SELECT ROLE FROM TEAM_MEMBERS WHERE TEAMID={team_id} AND USERID='{user_id}'")
	if ROLE == None: return False #Guaranteed to return a valid result, right?
	ROLE=ROLE[0]
	return True or ROLE == 'co_leader' or ROLE == 'leader'
	
def isValidTeamID(id):
	if id == None or id == "": return False
	TEAMID = executeQuery(f"SELECT TEAMID FROM TEAMS_REPORT WHERE ID={id}")	
	return TEAMID != None
	
def isValidMatch(id):
	if id == None or id == "": return False
	MATCHID = executeQuery(f"SELECT ID FROM USER_MATCHES WHERE ID={id}")	
	return MATCHID != None
	
def getChallengeName(id):
	if id == None or id == "": return "Challenge: Unknown..."
	NAME = executeQuery(f"SELECT NAME FROM EVENTS WHERE ID = (SELECT EVENTID FROM META_CHAL_REPORT WHERE ID={id})")
	if type(NAME) == tuple: NAME = NAME[0]
	return NAME

def getTeamFromUserID(user_id):
	TEAMID=getInGameTeamIDFromUserID(user_id)
	if TEAMID == None: return None
	
	ID = executeQuery(f"SELECT ID FROM TEAMS_REPORT WHERE TEAMID={TEAMID}")	
	if ID == None: return None
	ID=ID[0]
	return ID

def getInGameTeamIDFromUserID(user_id):
	TEAMID = executeQuery(f"SELECT TEAMID FROM TEAM_MEMBERS WHERE USERID='{user_id}'")
	if TEAMID == None: return None
	TEAMID=TEAMID[0]
	return TEAMID

def getInGameTeamID(team_id):
	if team_id == None or team_id == "": return None
	TEAMID = executeQuery(f"SELECT TEAMID from TEAMS_REPORT WHERE ID={team_id}")	
	if TEAMID != None: TEAMID=TEAMID[0]
	return TEAMID
	
def getInGameTeamIDFromName(team_name):
	clean_team_name=removeCharactersOutOfRange(team_name).replace("'","''")
	TEAMID = executeQuery(f"SELECT TEAMID from TEAMS WHERE NAME='{clean_team_name}'")	
	if TEAMID != None: TEAMID=TEAMID[0]
	return TEAMID
	
def getTeamNameFromIngameTeamID(TEAMID):
	name = executeQuery(f"SELECT NAME from TEAMS WHERE TEAMID={TEAMID}")	
	if name == None: name="Unknown"
	else: name=name[0].upper()
	return name
	
def getTeamName(team_id):
	TEAMID=getInGameTeamID(team_id)
	if TEAMID == None: return "Unknown"
	name = getTeamNameFromIngameTeamID(TEAMID)
	return name
	
def getUniqueTeamIDFromInGameTeamID(ingame_teamid):
	if ingame_teamid == None: return None
	if type(ingame_teamid) == tuple: ingame_teamid=ingame_teamid[0]
	team_id = executeQuery(f"SELECT ID from TEAMS_REPORT WHERE TEAMID={ingame_teamid}")	
	if team_id != None: team_id=team_id[0]
	return team_id
	
def getTeamLinkFromInGameID(ingame_teamid):
	unique_team_id = getUniqueTeamIDFromInGameTeamID(ingame_teamid)
	if unique_team_id == None: return '/teams'
	return f'/teams/{unique_team_id}'

def getTeamNameLink(team_name):
	team_id=getInGameTeamIDFromName(team_name)
	if team_id == None: return '/teams'
	return getTeamLinkFromInGameID(team_id)
	
###Meta Report###

def getDistinctNamesFromMetaReport():
	names = executeQuery("SELECT DISTINCT NAME FROM META_REPORT ORDER BY NAME DESC")
	if type(names) == tuple: names=[names]
	if names == None: return ""
	names_list=[]
	for row in names:
		names_list.append(row[0])
	return names_list

def getCardsAndThemesByFilter(filter_rank_min = None, filter_mmr_min = None, filter_mmr_max = None):
	themes_dict={}
	cards_dict={}
	decks_dict={}
	set_of_decks=[]
	total_decks=0
	cost_map={}
	search="Last 1 day"
	search_radius=24*60*60 # Last 24 hours
	search_time=int(time.time())-search_radius
	
	deck_ids = None
	#All
	if filter_rank_min==None and filter_mmr_min==None and filter_mmr_max==None:
		deck_ids = executeQuery(f"SELECT DECKID, USERID from TEAM_MEMBERS WHERE UPDATED>={search_time}")
	elif filter_mmr_min!=None and filter_mmr_max!=None:
		deck_ids = executeQuery(f"SELECT DECKID, USERID from TEAM_MEMBERS WHERE MMR>={filter_mmr_min} AND MMR<={filter_mmr_max} AND UPDATED>={search_time}")
	elif filter_mmr_min!=None and filter_mmr_max==None:
		deck_ids = executeQuery(f"SELECT DECKID, USERID from TEAM_MEMBERS WHERE MMR>={filter_mmr_min} AND UPDATED>={search_time}")
	elif filter_rank_min!=None and filter_mmr_min==None and filter_mmr_max==None:
		deck_ids = executeQuery(f"SELECT DECKID, USERID from TEAM_MEMBERS WHERE RANK<={filter_rank_min} and RANK <> 0 AND UPDATED>={search_time}")
	else:
		print(f"Not supported, filter_rank_min: {filter_rank_min}, filter_mmr_min: {filter_mmr_min}, filter_mmr_max: {filter_mmr_max}")
	if type(deck_ids) == tuple:
		deck_ids=[deck_ids]
	if deck_ids == None: deck_ids=[]
	for deck_id in deck_ids:
		actual_deck_id=deck_id[0]
		if actual_deck_id == None:
			#print("Critical Error: Can't find Deck ID")
			continue
		cards=getCardsFromDeckID(actual_deck_id)
		set_of_decks.append(cards)
		for card in cards:
			if card not in cards_dict:
				cards_dict[card]=0
			cards_dict[card]+=1
		themes=findThemes(cards)
		themes=','.join(x for x in themes)
		if themes not in themes_dict:
			themes_dict[themes]=0
		themes_dict[themes]+=1
		avg_cost = findAvgCost(cards)
		if avg_cost > 0:
			value = "%.1f" % avg_cost
			if value not in cost_map:
				cost_map[value]=0
			cost_map[value]+=1
		total_decks+=1
	meta_decks=getMetaDecks(cards_dict, set_of_decks)
	return cards_dict, themes_dict, total_decks, meta_decks, cost_map

def needChallengeMetaReport():
	result = executeQuery("SELECT COUNT(*) >= 6 from USER_MATCHES WHERE MODE=6 AND TIME>(SELECT MAX(TIME) FROM META_CHAL_REPORT)")
	if type(result) == tuple: result = result[0]
	if result == None: return False
	return result == 1

def getChalCardsAndThemes():
	themes_dict={}
	cards_dict={}
	decks_dict={}
	set_of_decks=[]
	total_decks=0
	#MODE 6 -> Challenge Mode
	deck_ids = executeQuery("SELECT DECK2 from USER_MATCHES WHERE MODE=6 AND TIME>=(SELECT MAX(STARTTIME) FROM EVENTS WHERE TYPE=4) AND TIME<=(SELECT MAX(ENDTIME) FROM EVENTS WHERE TYPE=4)")
	if type(deck_ids) == tuple: deck_ids=[deck_ids]
	if deck_ids == None: deck_ids=[]
	for deck_id in deck_ids:
		actual_deck_id=deck_id[0]
		if actual_deck_id == None:
			#print("Critical Error: Can't find Deck ID")
			continue
		cards=getCardsFromDeckID(actual_deck_id)
		set_of_decks.append(cards)
		for card in cards:
			if card not in cards_dict:
				cards_dict[card]=0
			cards_dict[card]+=1
		themes=findThemes(cards)
		themes=','.join(x for x in themes)
		if themes not in themes_dict:
			themes_dict[themes]=0
		themes_dict[themes]+=1
		total_decks+=1
	meta_decks=getMetaDecks(cards_dict, set_of_decks)
	top_three_themes=[]
	for i in range(3):
		high_theme = None
		max_count = 0
		for key in themes_dict.keys():
			if key not in top_three_themes and themes_dict[key] > max_count:
				max_count = themes_dict[key]
				high_theme = key
		if high_theme != None:
			top_three_themes.append(high_theme)
	tmp_meta_decks={}
	for themes in top_three_themes:
		if themes in meta_decks.keys():
			tmp_meta_decks[themes]=meta_decks[themes]
	return cards_dict, themes_dict, total_decks, tmp_meta_decks
	
def getChalReportTotalDecks():
	total_decks = executeQuery("SELECT TOTALDECKS FROM META_CHAL_REPORT WHERE EVENTID = (SELECT ID FROM EVENTS WHERE TYPE=4 AND STARTTIME=(SELECT MAX(STARTTIME) FROM EVENTS WHERE TYPE=4))")
	if type(total_decks) == tuple: total_decks=total_decks[0]
	return total_decks

def getHighestPairedCard(card_name,set_of_decks):
	META_DECK_LEN=12
	filter_list=[]
	filter_list.append(card_name)
	while len(filter_list) < META_DECK_LEN:
		set_of_pairs={}
		for deck in set_of_decks:
			valid=True
			for card in filter_list:
				if card not in deck:
					valid=False
			if valid:
				for card in deck:
					if card not in filter_list:
						if card not in set_of_pairs:
							set_of_pairs[card]=0
						set_of_pairs[card]+=1
		max_card=""
		max_seen=0
		for card in set_of_pairs:
			tmp_max=set_of_pairs[card]
			if tmp_max>max_seen:
				max_seen=tmp_max
				max_card=card
		filter_list.append(max_card)
	return filter_list
	
def convertDeckNameToIDs(deck):
	deck_ids=[]
	for card in deck:
		if card == '': continue
		deck_ids.append(DATABASE.LOWER_NAME_TO_ID[card])
	return deck_ids
	
def getMetaDecks(cards_dict, set_of_decks):
	meta_decks={}
	if len(cards_dict) == 0 or len(set_of_decks) == 0: return meta_decks
	sorted_collection=[]
	for card in cards_dict.keys():
		sorted_collection.append([card, "%.2f" % (100*float(cards_dict[card])/len(set_of_decks))])
		#print( getCardName(card)+ "| %.2f" % (100*float(cards_dict[card])/len(set_of_decks)))
	sorted_l = sorted(sorted_collection, key=lambda x: (x[1], x[0]), reverse=True)
	for line in sorted_l:
		percent = int(100*float(line[1]))
		card_name=line[0]
		if percent > 4:
			meta_deck=getHighestPairedCard(card_name,set_of_decks)
			themes=findThemes(meta_deck)
			themes=','.join(x for x in themes)
			if themes not in meta_decks:
				meta_decks[themes]=meta_deck
	#print("\nMeta Decks:")
	#for theme in meta_decks:
	#	deck=meta_decks[theme]
	#	print(theme+"|"+','.join(getCardName(x) for x in deck))
	return meta_decks
	
def getCardsAndThemesByFilter_Report(NAME, search_radius=24*60*60):
	themes_dict={}
	cards_dict={}
	cost_map={}
	total_decks=0
	search="Last 1 day" #because we are combining reports
	search_time=int(time.time())-search_radius
	
	result = executeQuery(f"SELECT THEMESID,CARDSID,TOTALDECKS from META_REPORT WHERE TIME>={search_time} AND NAME='{NAME}' AND SEARCH='{search}'")
	if result == None: return cards_dict, themes_dict, total_decks
	if type(result) == tuple:
		result=[result]
	for row in result:
		THEMESID=row[0]
		CARDSID=row[1]
		TOTALDECKS=row[2]
		themes = executeQuery(f"SELECT THEMES, PERCENT from META_THEMES WHERE THEMESID={THEMESID}")
		if type(themes) == tuple: themes=[themes]
		for row_themes in themes:
			theme=row_themes[0]
			percent=row_themes[1]
			if theme not in themes_dict:
				themes_dict[theme]=0
			themes_dict[theme]+=int(TOTALDECKS*float(percent)/100)
			if int(TOTALDECKS*float(percent)/100) > TOTALDECKS:
				print(f"themes error {THEMESID}, {CARDSID}, {TOTALDECKS}")
				sys.exit()
		cards = executeQuery(f"SELECT CARDID, PERCENT from META_CARDS WHERE CARDSID={CARDSID}")
		if type(cards) == tuple: cards=[cards]
		for row_cards in cards:
			card=row_cards[0]
			percent=row_cards[1]
			if card not in cards_dict:
				cards_dict[card]=0
			cards_dict[card]+=int(TOTALDECKS*float(percent)/100)
			if int(TOTALDECKS*float(percent)/100) > TOTALDECKS:
				print(f"cards error {THEMESID}, {CARDSID}, {TOTALDECKS}")
				sys.exit()
		total_decks+=TOTALDECKS
	return cards_dict, themes_dict, total_decks
	
def findOldTeams():
	TwoDaysAgo = int(time.time()) - 3600 * 24 * 2
	old_teams = executeQuery(f"SELECT TEAMID from TEAMS_REPORT WHERE UPDATED < {TwoDaysAgo} AND RANK <= 2000 AND MEMBERS > 0")
	old_teams_list=[]
	if type(old_teams) == tuple: old_teams = [old_teams]
	if old_teams == None: old_teams = []
	for row in old_teams:
		old_teams_list.append(row[0])
	return old_teams_list
	
def getPlayersWithNull(limit=4000, arena=None):
	result=None
	if arena == None:
		result = executeQuery(f"SELECT USERID from TEAM_MEMBERS WHERE TEAMID <> 0 AND WINS_PVP IS NULL LIMIT {limit};")
	else:
		min_mmr, max_mmr=DATABASE.ARENA_MAP[arena]
		if max_mmr==None:
			result = executeQuery(f"SELECT USERID from TEAM_MEMBERS WHERE TEAMID <> 0 AND MMR >= {min_mmr} AND WINS_PVP IS NULL LIMIT {limit};")
		else:
			result = executeQuery(f"SELECT USERID from TEAM_MEMBERS WHERE TEAMID <> 0 AND MMR >= {min_mmr} AND MMR < {max_mmr} AND WINS_PVP IS NULL LIMIT {limit};")
	if type(result) == tuple: result=[result]
	if result == None: result=[]
	return result
	
def getPlayersWithOldUpdated(limit=4000, arena=None):
	result=None
	if arena == None:
		#SELECT USERID, MAX(UPDATED) AS UPDATED from USERS_HISTORY WHERE TEAMID <> 0 AND WINS_PVP IS NOT NULL AND USERID IN (SELECT USERID FROM TEAM_MEMBERS WHERE MMR >= 8500) GROUP BY USERID ORDER BY UPDATED;
		result = executeQuery(f"SELECT USERID, MAX(UPDATED) AS UPDATED from USERS_HISTORY WHERE TEAMID <> 0 AND WINS_PVP IS NOT NULL GROUP BY USERID ORDER BY UPDATED LIMIT {limit};")
	else:
		min_mmr, max_mmr=DATABASE.ARENA_MAP[arena]
		if max_mmr==None:
			result = executeQuery(f"SELECT USERID, MAX(UPDATED) AS UPDATED from USERS_HISTORY WHERE TEAMID <> 0 AND USERID IN (SELECT USERID FROM TEAM_MEMBERS WHERE MMR >= {min_mmr}) AND WINS_PVP IS NOT NULL GROUP BY USERID ORDER BY UPDATED LIMIT {limit};")
		else:
			result = executeQuery(f"SELECT USERID, MAX(UPDATED) AS UPDATED from USERS_HISTORY WHERE TEAMID <> 0 AND USERID IN (SELECT USERID FROM TEAM_MEMBERS WHERE MMR >= {min_mmr} AND MMR < {max_mmr}) AND WINS_PVP IS NOT NULL GROUP BY USERID ORDER BY UPDATED LIMIT {limit};")
	if type(result) == tuple: result=[result]
	if result == None: result=[]
	return result
	
def getMetaCardsTableData(search, rank):
	#print(f"Cards Table Data, Rank: {rank}, Search: {search}")
	result=None
	if search == "Last 1 day":
		result = executeQuery(f"SELECT CARDSID, TIME, TOTALDECKS from META_REPORT WHERE SEARCH='{search}' AND NAME='{rank}' AND TIME IN (select MAX(TIME) from META_REPORT WHERE SEARCH='{search}' AND NAME='{rank}')")
	else:
		result = executeQuery(f"SELECT CARDSID, TIME, TOTALDECKS from META_REPORT WHERE SEARCH='{search}' AND NAME='{rank}'")
	updated=None
	total_decks=0
	if result != None:
		if len(result) != 3: result = result[0]
		cards_id = result[0]
		updated = result[1]
		total_decks = result[2]
		result = executeQuery(f"SELECT CARDID, PERCENT from META_CARDS WHERE CARDSID={cards_id} ORDER BY PERCENT DESC")
		if type(result) == tuple: result=[result]
	return result, updated, total_decks
	
def getMetaChalCardsTableData(chal_id):
	#print(f"Cards Table Data, Rank: {rank}, Search: {search}")
	result = executeQuery(f"SELECT CARDSID, TIME, TOTALDECKS from META_CHAL_REPORT WHERE ID={chal_id}")
	updated=None
	total_decks=0
	if result != None:
		cards_id = result[0]
		updated = result[1]
		total_decks = result[2]
		result = executeQuery(f"SELECT CARDID, PERCENT from META_CARDS WHERE CARDSID={cards_id} ORDER BY PERCENT DESC")
		if type(result) == tuple: result=[result]
	return result, updated, total_decks
	
def getMetaThemesTableData(search, rank):
	#print(f"Themes Table Data, Rank: {rank}, Search: {search}")
	result=None
	if search == "Last 1 day":
		result = executeQuery(f"SELECT THEMESID, TIME, TOTALDECKS from META_REPORT WHERE SEARCH='{search}' AND NAME='{rank}' AND TIME IN (select MAX(TIME) from META_REPORT WHERE SEARCH='{search}' AND NAME='{rank}')")
	else:
		result = executeQuery(f"SELECT THEMESID, TIME, TOTALDECKS from META_REPORT WHERE SEARCH='{search}' AND NAME='{rank}'")
	updated=None
	total_decks=0
	if result != None:
		themes_id = result[0]
		updated = result[1]
		total_decks = result[2]
		result = executeQuery(f"SELECT THEMES, PERCENT from META_THEMES WHERE THEMESID={themes_id} ORDER BY PERCENT DESC")
		if type(result) == tuple: result=[result]
	return result, updated, total_decks
	
	
	
def getTeamDetailsTableData(ingame_team_id,access_level=-1,get_platform=False):
	#print(f"Team Details Table Data, ingame_team_id {ingame_team_id}")
	final_collection_map={}
	uniqueid_map={}
	userid_map={}
	platforms=[0,0] #iOS, Android
	collection_details_map={}
	if ingame_team_id == None:
		if get_platform: return None,final_collection_map,uniqueid_map,platforms
		return None,final_collection_map,uniqueid_map
	team_table_data = executeQuery(f"SELECT USERID, ROLE, MMR, NKLEVEL, DONATED_CUR, JOINDATE FROM TEAM_MEMBERS WHERE TEAMID={ingame_team_id} ORDER BY MMR DESC")
	if type(team_table_data) == tuple: team_table_data=[team_table_data]
	if access_level != -1:
		result = executeQuery(f"SELECT USERID, COUNT(*) FROM USER_COLLECTIONS WHERE USERID IN (SELECT ID FROM USERS WHERE USERID IN (SELECT USERID FROM TEAM_MEMBERS WHERE TEAMID={ingame_team_id})) GROUP BY USERID")
		if type(result) == tuple: result=[result]
		if result != None:
			for row in result:
				ID=row[0]
				COUNT=row[1]
				collection_details_map[ID]=COUNT
	result = executeQuery(f"SELECT USERID, ID, PLATFORM FROM USERS WHERE USERID IN (SELECT USERID FROM TEAM_MEMBERS WHERE TEAMID={ingame_team_id})")
	if type(result) == tuple: result=[result]
	if result != None:
		for row in result:
			USERID=row[0]
			ID=row[1]
			if get_platform:
				PLATFORM=row[2]
				if "gamecenter" == PLATFORM: platforms[0]+=1
				elif "google" == PLATFORM: platforms[1]+=1
			userid_map[ID]=USERID
			uniqueid_map[USERID]=ID
	if len(collection_details_map) > 0:
		for key in userid_map.keys():
			if key in collection_details_map:
				final_collection_map[userid_map[key]]=collection_details_map[key]
	if get_platform: return team_table_data,final_collection_map,uniqueid_map,platforms
	return team_table_data,final_collection_map,uniqueid_map
	
def getMyMatchesTableData(g_user):
	oppname_map={}
	oppteam_map={}
	if g_user == None:
		return None,oppname_map,oppteam_map
	USERID = getUserIDFromOktaID(g_user.id)
	mymatches_table_data = executeQuery(f"SELECT ID, TIME, USERID2, NK2, TEAM2, MODE, RESULT1, SCORE1, SCORE2, MMR2 FROM USER_MATCHES WHERE USERID1='{USERID}' OR USERID2='{USERID}' ORDER BY TIME DESC")
	if type(mymatches_table_data) == tuple: mymatches_table_data=[mymatches_table_data]
	if mymatches_table_data == None:
		return None,oppname_map,oppteam_map
	#Grab Opponent's User Names
	result = executeQuery(f"SELECT USERID, NAME, ID FROM USERS WHERE USERID IN (SELECT USERID2 FROM USER_MATCHES WHERE USERID1='{USERID}' OR USERID2='{USERID}')")
	if type(result) == tuple: result=[result]
	if result != None:
		for row in result:
			USERID2=row[0]
			NAME=row[1]
			ID=row[2]
			oppname_map[USERID2]=[ID,NAME]
	#Grab Opponent's Team Names
	result = executeQuery(f"SELECT TEAMID, NAME FROM TEAMS WHERE TEAMID IN (SELECT TEAM2 FROM USER_MATCHES WHERE USERID1='{USERID}' OR USERID2='{USERID}')")
	if type(result) == tuple: result=[result]
	if result != None:
		for row in result:
			TEAMID=row[0]
			NAME=row[1]
			oppteam_map[TEAMID]=NAME
	return mymatches_table_data,oppname_map,oppteam_map
	
def getSpecificPlayerMatchesTableData(unique_user_id):
	mymatches_table_data = executeQuery(f"SET @USERID = (SELECT USERID FROM USERS WHERE ID = {unique_user_id});\
		SET @OPTOUT = (SELECT COUNT(*) FROM USER_LOGINS WHERE OPTOUT = 1 AND USERID=@USERID) = 0;\
		SELECT x.ID, x.TIME, y.ID, y.NAME, x.NK2, z.NAME, x.MODE, x.RESULT1, x.SCORE1, x.SCORE2, x.MMR2 FROM USER_MATCHES x\
			JOIN (SELECT USERID, NAME, ID FROM USERS WHERE USERID IN (SELECT USERID2 FROM USER_MATCHES WHERE USERID1=@USERID OR USERID2=@USERID)) y\
			JOIN (SELECT TEAMID, NAME FROM TEAMS WHERE TEAMID IN (SELECT TEAM2 FROM USER_MATCHES WHERE USERID1=@USERID OR USERID2=@USERID)) z\
		WHERE x.USERID2 = y.USERID\
			AND z.TEAMID = x.TEAM2\
			AND @OPTOUT AND (SELECT COUNT(*) FROM USER_LOGINS WHERE OPTOUT = 1 AND USERID=x.USERID2) = 0\
		ORDER BY TIME DESC",multiple=True)
	if type(mymatches_table_data) == tuple: mymatches_table_data=[mymatches_table_data]
	return mymatches_table_data
	
def getLiveMatchesTableData(QUERY):
	live_matches_table_data = executeQuery(f"SELECT ID, TIME, MMR1, NK1, MMR2, NK2, MODE, SCORE1, SCORE2, RESULT1 FROM USER_MATCHES {QUERY} ORDER BY TIME DESC LIMIT 500")
	if type(live_matches_table_data) == tuple: live_matches_table_data=[live_matches_table_data]
	return live_matches_table_data
	
def getChalTableData():
	chal_table_data = executeQuery(f"SELECT x.ID, x.TIME, y.NAME FROM meta_chal_report x JOIN (SELECT ID, NAME FROM EVENTS) y WHERE x.EVENTID=y.ID")
	if type(chal_table_data) == tuple: chal_table_data=[chal_table_data]
	return chal_table_data
	
def getTeamApplicationsTableData(ingame_team_id,access_level=-1):
	if access_level == -1: return None
	team_table_data = executeQuery(f"SELECT USERID, STATUS, ROLE FROM TEAM_ACCEPT WHERE TEAMID={ingame_team_id}")	
	if type(team_table_data) == tuple: team_table_data=[team_table_data]
	return team_table_data
	
def getTeamApplicationsData(ingame_team_id):
	application_data={}
	result = executeQuery(f"SELECT USERID, STATUS, ROLE FROM TEAM_ACCEPT WHERE TEAMID={ingame_team_id}")	
	if result == None: return application_data
	elif type(result) == tuple: result=[result]
	for card_data in result:
		userid=card_data[0]
		status=card_data[1]
		role=card_data[2]
		application_data[userid]=[status,role]
	return application_data
	
def getCardRequestTableData(ingame_team_id,access_level=-1):
	if access_level == -1: return None
	#print(f"Request Details Table Data, ingame_team_id {ingame_team_id}")
	last_two_weeks = int(time.time()) - 3600 * 24 * 14
	request_table_data = executeQuery(f"SELECT UPDATED, USERID, CARDID FROM TEAM_REQUESTS WHERE TEAMID={ingame_team_id} AND UPDATED > {last_two_weeks} ORDER BY UPDATED DESC LIMIT 1000")
	if type(request_table_data) == tuple: request_table_data=[request_table_data]
	return request_table_data
	
def getCardRequestTableDataTime(ingame_team_id,timeframe=7): #timeframe in days
	search_timeframe = int(time.time()) - 3600 * 24 * timeframe
	#print(f"Request Details Table Data, ingame_team_id {ingame_team_id}")
	request_table_data = executeQuery(f"SELECT UPDATED, USERID, CARDID FROM TEAM_REQUESTS WHERE TEAMID={ingame_team_id} AND UPDATED > {search_timeframe}")
	if type(request_table_data) == tuple: request_table_data=[request_table_data]
	return request_table_data
	
def getCardDonationTableData(ingame_team_id,access_level=-1):
	if access_level == -1: return None
	#print(f"Donation Details Table Data, ingame_team_id {ingame_team_id}")
	last_two_weeks = int(time.time()) - 3600 * 24 * 14
	donation_table_data = executeQuery(f"SELECT UPDATED, RECEIVER, SENDER, CARDID FROM TEAM_DONATIONS WHERE TEAMID={ingame_team_id} AND UPDATED > {last_two_weeks} ORDER BY UPDATED DESC LIMIT 1000")
	if type(donation_table_data) == tuple: donation_table_data=[donation_table_data]
	return donation_table_data
	
def getCardDonationTableDataTime(ingame_team_id,timeframe=7): #timeframe in days
	#print(f"Donation Details Table Data, ingame_team_id {ingame_team_id}")
	search_timeframe = int(time.time()) - 3600 * 24 * timeframe
	donation_table_data = executeQuery(f"SELECT UPDATED, RECEIVER, SENDER, CARDID FROM TEAM_DONATIONS WHERE TEAMID={ingame_team_id} AND UPDATED > {search_timeframe}")
	if type(donation_table_data) == tuple: donation_table_data=[donation_table_data]
	return donation_table_data
	
def getTeamsTableData(rank,members,nklevel,status):
	WHERE='WHERE x.RANK <= 1000'
	if rank == 'Top 50': WHERE='WHERE x.RANK <= 50'
	elif rank == 'Top 250': WHERE='WHERE x.RANK <= 250'
	elif rank == '1000 to 2000': WHERE='WHERE x.RANK > 1000 AND x.RANK <= 2000'
	elif rank == '>2000': WHERE='WHERE x.RANK > 2000'	
	WHERE+=f" AND x.NKLEVEL <= {nklevel}"
	WHERE+=f" AND x.MEMBERS <= {members}"
	if status!='All' and "'" not in status:
		if status == 'Open': status='AutoAccepted'
		WHERE+=f" AND x.STATUS = '{status}'"
	result = executeQuery(f"SELECT x.ID, y.NAME, x.RANK, x.LASTRANK, x.TROPHIES, x.COUNTRY, x.MEMBERS, x.STATUS, x.NKLEVEL, x.UPDATED from TEAMS_REPORT x\
		JOIN (SELECT TEAMID, NAME FROM TEAMS) y\
		{WHERE} AND x.TEAMID = y.TEAMID\
		ORDER BY TROPHIES DESC, RANK ASC")
	if type(result) == tuple: result=[result]
	return result
	
def getPlayersByName(name):
	name = removeCharactersOutOfRange(name)
	result = executeSanitize(f"SELECT y.ID, y.NAME, z.ID, z.NAME, x.RANK, x.LASTRANK, x.MMR, x.NKLEVEL, x.DONATED_ALL, x.TW_TOKENS, x.WINS_PVP, x.WINS_PVPP, x.WINS_CHLG, x.WINS_TW, x.WINS_FF, x.WINS_FFP, x.UPDATED from TEAM_MEMBERS x\
		JOIN (SELECT ID, USERID, NAME FROM USERS) y\
		JOIN (SELECT a.ID, a.TEAMID, b.NAME FROM TEAMS_REPORT a JOIN TEAMS b WHERE a.TEAMID = b.TEAMID) z\
	WHERE x.USERID IN (SELECT USERID FROM USERS WHERE NAME LIKE %(name)s) AND\
		x.USERID = y.USERID AND\
		x.TEAMID = z.TEAMID\
	ORDER BY MMR DESC LIMIT 250", name)
	if type(result) == tuple: result=[result]
	return result
	
def getLeaderboardUserNamesByName(name):
	user_name_map={}
	result = executeSanitize(f"SELECT USERID, NAME FROM USERS WHERE NAME LIKE %(name)s", name)
	if result == None: return user_name_map
	if type(result) == tuple: result=[result]
	for row in result:
		userid=row[0]
		user_name=row[1]
		user_name_map[userid]=user_name
	return user_name_map
	
def getLeaderboardTeamsByName(name):
	team_name_map={}
	result = executeSanitize(f"SELECT TEAMID, NAME from TEAMS WHERE TEAMID IN (SELECT TEAMID FROM TEAM_MEMBERS WHERE USERID IN (SELECT USERID FROM USERS WHERE NAME LIKE %(name)s))", name)
	if result == None: return team_name_map
	if type(result) == tuple: result=[result]
	for row in result:
		teamid=row[0]
		team_name=row[1]
		team_name_map[teamid]=team_name
	return team_name_map
	
def getPlayersTableData(query,sort="RANK",name=None):
	if name != None: return getPlayersByName(name)
	#cols = ['id', 'Team', 'Rank', 'Trend', 'MMR', 'NK', 'Donated', 'TW Caps', 'PVP', 'CHLG', 'TW', 'FF', 'PVP', 'FREE', 'SHOP', 'Lockers']
	updated = executeQuery(f"SELECT MAX(UPDATED) from TEAM_MEMBERS WHERE {query}")
	if type(updated)==tuple: updated=updated[0]
	result = None
	if sort == "RANK":
		result = executeQuery(f"SELECT y.ID, y.NAME, z.ID, z.NAME, x.RANK, x.LASTRANK, x.MMR, x.NKLEVEL, x.DONATED_ALL, x.TW_TOKENS, x.WINS_PVP, x.WINS_PVPP, x.WINS_CHLG, x.WINS_TW, x.WINS_FF, x.WINS_FFP, x.UPDATED from TEAM_MEMBERS x\
			JOIN (SELECT ID, USERID, NAME FROM USERS) y\
			JOIN (SELECT a.ID, a.TEAMID, b.NAME FROM TEAMS_REPORT a JOIN TEAMS b WHERE a.TEAMID = b.TEAMID) z\
		WHERE x.USERID IN (SELECT USERID FROM USERS WHERE {query}) AND\
			x.USERID = y.USERID AND\
			x.TEAMID = z.TEAMID\
		ORDER BY RANK ASC")
	else:
		TARGET=""
		if sort=='DONATED': TARGET = "DONATED_ALL"
		elif sort=='TW CAPS': TARGET = "TW_TOKENS"
		elif sort=='PVP WINS': TARGET = "WINS_PVP"
		elif sort=='PVP WINS PERFECT': TARGET = "WINS_PVPP"
		elif sort=='CHLG WINS': TARGET = "WINS_CHLG"
		elif sort=='TW WINS': TARGET = "WINS_TW"
		elif sort=='FF WINS': TARGET = "WINS_FF"
		elif sort=='FF WINS PERFECT': TARGET = "WINS_FFP"
		else: TARGET = "MMR"
		result = executeQuery(f"SELECT y.ID, y.NAME, z.ID, z.NAME, x.RANK, x.LASTRANK, x.MMR, x.NKLEVEL, x.DONATED_ALL, x.TW_TOKENS, x.WINS_PVP, x.WINS_PVPP, x.WINS_CHLG, x.WINS_TW, x.WINS_FF, x.WINS_FFP, x.UPDATED from TEAM_MEMBERS x\
			JOIN (SELECT ID, USERID, NAME FROM USERS) y\
			JOIN (SELECT a.ID, a.TEAMID, b.NAME FROM TEAMS_REPORT a JOIN TEAMS b WHERE a.TEAMID = b.TEAMID) z\
		WHERE x.USERID IN (SELECT USERID FROM USERS) AND\
			x.USERID = y.USERID AND\
			x.TEAMID = z.TEAMID\
		ORDER BY {TARGET} DESC LIMIT 1000")
	return result
	
def getSpecificTeamTableData(team_id):
	#print(f"Specific Team Table Data, TeamID: {team_id}")
	ingame_team_id = executeQuery(f"SELECT TEAMID from TEAMS_REPORT WHERE ID={team_id}")
	if ingame_team_id == None: return None
	ingame_team_id=ingame_team_id[0]
	return executeQuery(f"SELECT RANK, TROPHIES, MEMBERS, NKLEVEL, COUNTRY, STATUS, DESCRIPTION from TEAMS_REPORT WHERE TEAMID={ingame_team_id}")
	
def getAllUserNames(ingame_team_id, unique_user_id=False):
	user_name_map={}
	if ingame_team_id == None: return user_name_map
	result=None
	if unique_user_id:
		result = executeQuery(f"SELECT ID, NAME FROM USERS WHERE USERID IN (SELECT USERID FROM TEAM_MEMBERS WHERE TEAMID={ingame_team_id})")
	else:
		result = executeQuery(f"SELECT USERID, NAME FROM USERS WHERE USERID IN (SELECT USERID FROM TEAM_MEMBERS WHERE TEAMID={ingame_team_id})")
	if type(result) == tuple: result=[result]
	if result == None: return user_name_map
	for row in result:
		userid=row[0]
		user_name=row[1]
		if type(user_name) == str: user_name=user_name.upper()
		user_name_map[userid]=user_name
	return user_name_map
	
def getAllUserNamesFromUniqueTeamID(unique_team_id):
	user_name_map={}
	if unique_team_id == None: return user_name_map
	result = executeQuery(f"SELECT USERID, NAME FROM USERS WHERE USERID IN (SELECT USERID FROM TEAM_MEMBERS WHERE TEAMID=(SELECT TEAMID FROM TEAMS_REPORT WHERE ID = {unique_team_id}))")
	if type(result) == tuple: result=[result]
	if result == None: return user_name_map
	for row in result:
		userid=row[0]
		user_name=row[1]
		if type(user_name) == str: user_name=user_name.upper()
		user_name_map[userid]=user_name
	return user_name_map
	
def getAllUserNamesApplications(ingame_team_id):
	user_name_map={}
	result = executeQuery(f"SELECT USERID, NAME FROM USERS WHERE USERID IN (SELECT USERID FROM TEAM_ACCEPT WHERE TEAMID={ingame_team_id}) OR USERID IN (SELECT USERID FROM TEAM_MEMBERS WHERE TEAMID={ingame_team_id})")
	if type(result) == tuple: result=[result]
	if result == None: return user_name_map
	for row in result:
		userid=row[0]
		user_name=row[1]
		if type(user_name) == str: user_name=user_name.upper()
		user_name_map[userid]=user_name
	return user_name_map
	
def getAllUserNamesReverse(ingame_team_id):
	user_name_map={}
	if ingame_team_id == None: return user_name_map
	result = executeQuery(f"SELECT USERID, NAME FROM USERS WHERE USERID IN (SELECT USERID FROM TEAM_MEMBERS WHERE TEAMID={ingame_team_id})")
	if type(result) == tuple: result=[result]
	if result == None: return user_name_map
	for row in result:
		userid=row[0]
		user_name=row[1]
		if type(user_name) == str: user_name = user_name.upper()
		user_name_map[user_name]=userid
	return user_name_map
	
def getLeaderboardUserNames(limit, WHERE=None):
	user_name_map={}
	result=None
	if WHERE == None:
		result = executeQuery(f"SELECT USERID, NAME FROM USERS WHERE USERID IN (SELECT USERID from TEAM_MEMBERS WHERE RANK <= {limit} AND RANK <> 0)")
	else:
		result = executeQuery(f"SELECT USERID, NAME FROM USERS WHERE USERID IN (SELECT USERID from TEAM_MEMBERS WHERE {WHERE})")
	if result == None: return user_name_map
	if type(result) == tuple: result=[result]
	for row in result:
		userid=row[0]
		user_name=row[1]
		user_name_map[userid]=user_name
	return user_name_map
	
def getLeaderboardTeams(limit, WHERE=None):
	team_name_map={}
	result=None
	if WHERE == None:
		result = executeQuery(f"SELECT TEAMID, NAME from TEAMS WHERE TEAMID IN (SELECT TEAMID FROM TEAM_MEMBERS WHERE RANK <= {limit} AND RANK <> 0)")
	else:
		result = executeQuery(f"SELECT TEAMID, NAME from TEAMS WHERE TEAMID IN (SELECT TEAMID FROM TEAM_MEMBERS WHERE {WHERE})")
	if result == None: return team_name_map
	if type(result) == tuple: result=[result]
	for row in result:
		teamid=row[0]
		team_name=row[1]
		team_name_map[teamid]=team_name
	return team_name_map
	
###TEAMWAR###

def getTeamwarBracketData(unique_team_id):
	bracket_data=[]
	updated = None
	if unique_team_id == None: return bracket_data, updated
	result = executeQuery(f"SELECT y.BRACKETID, y.RANK, x.TEAMNAME, x.RUNS, x.MEMBERS, x.SCORE, x.UPDATED FROM TEAMWAR_BRACKET x\
		JOIN (SELECT DISTINCT a.ID, c.BRACKETID, a.RANK, a.TEAMID, b.NAME FROM TEAMS_REPORT a\
				JOIN (SELECT TEAMID, NAME FROM TEAMS) b\
				JOIN (SELECT TEAMNAME, BRACKETID FROM TEAMWAR_BRACKET) c\
			WHERE a.TEAMID = b.TEAMID AND c.BRACKETID = (SELECT MAX(BRACKETID) FROM TEAMWAR_BRACKET WHERE TEAMNAME = (SELECT NAME FROM TEAMS WHERE TEAMID = (SELECT TEAMID FROM TEAMS_REPORT WHERE ID = {unique_team_id}))) AND (c.TEAMNAME = b.NAME OR (a.TEAMID = 0 AND c.TEAMNAME NOT IN (SELECT NAME FROM TEAMS)))) y\
	WHERE x.BRACKETID = (SELECT MAX(BRACKETID) FROM TEAMWAR_BRACKET WHERE TEAMNAME = (SELECT NAME FROM TEAMS WHERE TEAMID = (SELECT TEAMID FROM TEAMS_REPORT WHERE ID = {unique_team_id}))) AND (y.NAME = x.TEAMNAME OR (x.TEAMNAME NOT IN (SELECT NAME FROM TEAMS) AND y.TEAMID = 0))")
	if result == None: return bracket_data, updated
	if type(result) == tuple: result=[result]
	for row in result:
		ID=row[0]
		RANK=row[1]
		TEAMNAME=row[2]
		RUNS=row[3]
		MEMBERS=row[4]
		SCORE=row[5]
		if updated == None or updated < row[6]: updated=row[6]
		bracket_data.append([ID,RANK,TEAMNAME,RUNS,MEMBERS,SCORE])
	return bracket_data, updated

def getTeamwarBracketHistoryData(unique_team_id):
	bracket_data=None
	result = executeQuery(f"SELECT BRACKETID, TEAMNAME, RUNS, SCORE FROM TEAMWAR_BRACKET_HISTORY\
		WHERE TEAMNAME = (SELECT NAME FROM TEAMS WHERE TEAMID = (SELECT TEAMID FROM TEAMS_REPORT WHERE ID = {unique_team_id})) AND\
		UPDATED < (SELECT MAX(UPDATED) FROM TEAMWAR_BRACKET WHERE TEAMNAME = (SELECT NAME FROM TEAMS WHERE TEAMID = (SELECT TEAMID FROM TEAMS_REPORT WHERE ID = {unique_team_id})))\
		ORDER BY UPDATED DESC LIMIT 1")
	if result == None: return bracket_data
	if type(result) == list: return bracket_data
	BRACKETID=result[0]
	TEAMNAME=result[1]
	RUNS=result[2]
	SCORE=result[3]
	if type(TEAMNAME) == str: TEAMNAME = TEAMNAME.upper()
	bracket_data=[BRACKETID,TEAMNAME,RUNS,SCORE]
	return bracket_data

def getSpecificBracketData(unique_bracket_id):
	bracket_data=[]
	updated = None
	if unique_bracket_id == None: return bracket_data, updated
	result = executeQuery(f"SELECT y.ID, y.RANK, x.TEAMNAME, x.RUNS, x.MEMBERS, x.SCORE, x.UPDATED FROM TEAMWAR_BRACKET x\
		JOIN (SELECT DISTINCT a.ID, a.RANK, a.TEAMID, b.NAME FROM TEAMS_REPORT a\
				JOIN (SELECT TEAMID, NAME FROM TEAMS) b\
				JOIN (SELECT TEAMNAME, BRACKETID FROM TEAMWAR_BRACKET) c\
			WHERE a.TEAMID = b.TEAMID AND c.BRACKETID = {unique_bracket_id} AND (c.TEAMNAME = b.NAME OR (a.TEAMID = 0 AND c.TEAMNAME NOT IN (SELECT NAME FROM TEAMS)))) y\
	WHERE x.BRACKETID = {unique_bracket_id} AND (y.NAME = x.TEAMNAME OR (x.TEAMNAME NOT IN (SELECT NAME FROM TEAMS) AND y.TEAMID = 0))")
	#result = executeQuery(f"SELECT x.ID, x.RANK, y.NAME, z.RUNS, z.MEMBERS, z.SCORE, z.UPDATED FROM TEAMS_REPORT x\
	#	JOIN (SELECT TEAMID, NAME FROM TEAMS) y\
	#	JOIN (SELECT TEAMNAME, RUNS, MEMBERS, SCORE, UPDATED FROM TEAMWAR_BRACKET WHERE BRACKETID = {unique_bracket_id}) z\
	#WHERE y.TEAMID = x.TEAMID AND y.NAME = z.TEAMNAME")
	if result == None: return bracket_data, updated
	if type(result) == tuple: result=[result]
	for row in result:
		ID=row[0]
		RANK=row[1]
		TEAMNAME=row[2]
		RUNS=row[3]
		MEMBERS=row[4]
		SCORE=row[5]
		if updated == None or updated < row[6]: updated=row[6]
		bracket_data.append([ID,RANK,TEAMNAME,RUNS,MEMBERS,SCORE])
	return bracket_data, updated
	
def getAllTeamwarBracketData(league):
	TROPHIES=[3500,None] #min, max
	if league == 'gold': TROPHIES=[3500,None]
	elif league == 'silver': TROPHIES=[1500,3500]
	elif league == 'bronze': TROPHIES=[500,1500]
	elif league == 'wood': TROPHIES=[None,500]
	bracket_data=[]
	updated = None
	FILTER = "WHERE"
	MINT,MAXT=TROPHIES
	min_set=False
	if MINT != None:
		FILTER+=f" TROPHIES >= {MINT}"
		min_set=True
	if MAXT != None:
		if min_set: FILTER+=f" AND TROPHIES < {MAXT}"
		else: FILTER+=f" TROPHIES < {MAXT}"
	cur_time=int(time.time())
	result = executeQuery(f"SELECT x.BRACKETID, z.RANK, x.TEAMNAME, x.RUNS, x.MEMBERS, x.SCORE, x.UPDATED FROM TEAMWAR_BRACKET x\
		JOIN (SELECT TEAMID, NAME FROM TEAMS) y\
		JOIN (SELECT RANK, TEAMID FROM TEAMS_REPORT {FILTER}) z\
	WHERE x.TEAMNAME = y.NAME AND y.TEAMID = z.TEAMID AND x.UPDATED > (SELECT MAX(STARTTIME)+3600*24*5-3600 FROM EVENTS WHERE TYPE=5 AND STARTTIME+3600*24*5-3600 < {cur_time})")
	if result == None: return bracket_data, updated
	if type(result) == tuple: result=[result]
	for row in result:
		BRACKETID=row[0]
		RANK=row[1]
		TEAMNAME=row[2].upper()
		RUNS=row[3]
		MEMBERS=row[4]
		SCORE=row[5]
		if updated == None or updated < row[6]: updated=row[6]
		if RANK == None: RANK=">2000"
		bracket_data.append([BRACKETID,RANK,TEAMNAME,RUNS,MEMBERS,SCORE])
	return bracket_data, updated
	
def getEventData(search_time):
	event_data=[]
	result = executeQuery(f"SELECT NAME, TEAM, TYPE, STARTTIME, ENDTIME, FINALPACK, PACK1,PACK2,PACK3,PACK4,PACK5,PACK6,PACK7,PACK8 FROM EVENTS WHERE ENDTIME > {search_time}")
	if result == None: return event_data
	if type(result) == tuple: result=[result]
	for row in result:
		NAME=row[0]
		if "TW_" in NAME:
			tw_split = NAME.split('_')
			if len(tw_split) == 3:
				NAME="Team War - Week "
				NAME+=tw_split[1]
				NAME+=" - " + tw_split[2]
		TEAM=int(row[1])
		TYPE=row[2]
		STARTTIME=row[3]
		ENDTIME=row[4]
		FINALPACK=row[5]
		PACK1=row[6]
		PACK2=row[7]
		PACK3=row[8]
		PACK4=row[9]
		PACK5=row[10]
		PACK6=row[11]
		PACK7=row[12]
		PACK8=row[13]
		event_data.append([NAME, TEAM, TYPE, STARTTIME, ENDTIME, FINALPACK, PACK1,PACK2,PACK3,PACK4,PACK5,PACK6,PACK7,PACK8])
	return event_data
	
def getTeamwarHistoryData(unique_team_id):
	history_data={}
	all_dates=[]
	ingame_team_id=getInGameTeamID(unique_team_id)
	if ingame_team_id == None: return history_data,all_dates
	#print(f"Teamwar Bracket Table Data, Team Name {team_name}")
	result = executeQuery(f"SELECT USERID, SCORE, CAPS, WEEK, YEAR FROM TEAMWAR_HISTORY WHERE USERID IN (SELECT USERID FROM TEAM_MEMBERS WHERE TEAMID = {ingame_team_id})")
	if result == None: return history_data,all_dates
	if type(result) == tuple: result=[result]
	usernames_map = getAllUserNames(ingame_team_id)
	for row in result:
		USERID=row[0]
		SCORE=row[1]
		CAPS=row[2]
		WEEK=row[3]
		if WEEK < 10:
			WEEK = f"0{WEEK}"
		YEAR=row[4]
		cur_week=f"{YEAR}-{WEEK}"
		if cur_week not in all_dates:
			all_dates.append(cur_week)
		if SCORE == None: SCORE = "X"
		if CAPS == None or CAPS == 0: SCORE = "N/A"
		username="Unknown-"+USERID[:4]
		if USERID in usernames_map:
			username=usernames_map[USERID]
		if username not in history_data:
			history_data[username]={}
		history_data[username][cur_week]=SCORE
	all_dates=sorted(all_dates, reverse=True)
	return history_data,all_dates
	
def getTeamwarHistoryCapsData(unique_team_id):
	history_data={}
	all_dates=[]
	if unique_team_id == None: return history_data,all_dates
	result = executeQuery(f"SELECT USERID, CAPS, WEEK, YEAR FROM TEAMWAR_HISTORY WHERE USERID IN (SELECT USERID FROM TEAM_MEMBERS WHERE TEAMID = (SELECT TEAMID FROM TEAMS_REPORT WHERE ID = {unique_team_id}))")
	if result == None: return history_data,all_dates
	if type(result) == tuple: result=[result]
	usernames_map = getAllUserNamesFromUniqueTeamID(unique_team_id)
	for row in result:
		USERID=row[0]
		CAPS=row[1]
		WEEK=row[2]
		if WEEK < 10:
			WEEK = f"0{WEEK}"
		YEAR=row[3]
		cur_week=f"{YEAR}-{WEEK}"
		if cur_week not in all_dates:
			all_dates.append(cur_week)
		if CAPS == None: CAPS = "X"
		username="Unknown-"+USERID[:4]
		if USERID in usernames_map:
			username=usernames_map[USERID]
		if username not in history_data:
			history_data[username]={}
		history_data[username][cur_week]=CAPS
	all_dates=sorted(all_dates, reverse=True)
	return history_data,all_dates
	
def getTeamEventHistoryData(unique_team_id):
	history_data={}
	all_events={}
	result = executeQuery(f"SELECT USERID, EVENTID, SCORE FROM TEAM_EVENT_PARTICIPATION WHERE USERID IN (SELECT USERID FROM TEAM_MEMBERS WHERE TEAMID = (SELECT TEAMID FROM TEAMS_REPORT WHERE ID = {unique_team_id}))")
	if result == None: return history_data,all_events
	if type(result) == tuple: result=[result]
	usernames_map = getAllUserNamesFromUniqueTeamID(unique_team_id)
	for row in result:
		USERID=row[0]
		EVENTID=row[1]
		SCORE=row[2]
		if EVENTID not in all_events:
			all_events[EVENTID]=None
		username="Unknown-"+USERID[:4]
		if USERID in usernames_map:
			username=usernames_map[USERID]
		if username not in history_data:
			history_data[username]={}
		history_data[username][EVENTID]=SCORE
	EVENT_LIST=",".join(str(x) for x in all_events.keys())
	result = executeQuery(f"SELECT EVENTID,NAME,PACK1,PACK2,PACK3,PACK4,PACK5,PACK6,PACK7,PACK8,FINALPACK,STARTTIME FROM EVENTS WHERE EVENTID IN ({EVENT_LIST})")
	if result == None: return history_data,all_events
	if type(result) == tuple: result=[result]
	for row in result:
		EVENTID=row[0]
		NAME=row[1]
		PACK1=row[2]
		PACK2=row[3]
		PACK3=row[4]
		PACK4=row[5]
		PACK5=row[6]
		PACK6=row[7]
		PACK7=row[8]
		PACK8=row[9]
		FINALPACK=row[10]
		STARTTIME=row[11]
		all_events[EVENTID]=[NAME,PACK1,PACK2,PACK3,PACK4,PACK5,PACK6,PACK7,PACK8,FINALPACK,STARTTIME]
	return history_data,all_events
	
def getTeamsMMR(unique_team_id, getRole=False):
	userid_to_mmr={}
	ingame_team_id=getInGameTeamID(unique_team_id)
	if ingame_team_id==None: return userid_to_mmr
	result = executeQuery(f"SELECT USERID, MMR, ROLE FROM TEAM_MEMBERS WHERE TEAMID={ingame_team_id}")
	if result == None: return userid_to_mmr
	if type(result) == tuple: result=[result]
	for row in result:
		if getRole: userid_to_mmr[row[0]]=[row[1],row[2]]
		else: userid_to_mmr[row[0]]=row[1]
	return userid_to_mmr

def getUpgradeTabData(unique_team_id):
	ordered_cards=[]
	result = executeQuery("SELECT CARDID1, CARDID2 FROM TEAMWAR_PAIRS WHERE PAIRID IN (SELECT PAIRID FROM TEAMWAR_CARDS WHERE TIME IN (SELECT MAX(TIME) FROM TEAMWAR_CARDS))")
	if type(result) == tuple: result=[result]
	for row in result:
		card1=row[0]
		card2=row[1]
		ordered_cards.append(card1)
		ordered_cards.append(card2)
	card_choices_str=",".join(str(x) for x in ordered_cards)
	leader_choice = executeQuery(f"SELECT CARDID, VOTE, LEVEL FROM TEAMWAR_CHOICE WHERE TEAMID = (SELECT TEAMID FROM TEAMS_REPORT WHERE ID = {unique_team_id}) AND CARDID IN ({card_choices_str})")
	if type(leader_choice) == tuple: leader_choice=[leader_choice]
	return ordered_cards, leader_choice
	
def getTeamWarChoices(unique_team_id):
	if not isValidTeamID(unique_team_id): return None
	card_results={}
	leader_choice = executeQuery(f"SELECT CARDID, VOTE, LEVEL FROM TEAMWAR_CHOICE WHERE TEAMID = (SELECT TEAMID FROM TEAMS_REPORT WHERE ID = {unique_team_id}) AND UPDATED > (SELECT MAX(STARTTIME) FROM EVENTS WHERE TYPE=5)")
	if leader_choice == None: return card_results
	elif type(leader_choice) == tuple: leader_choice=[leader_choice]
	for card_data in leader_choice:
		card_id=card_data[0]
		vote=int(card_data[1])
		level=card_data[2]
		card_results[card_id]=[vote,level]
	return card_results
	
def getBracketSubscribeWSID(team_name, channel):
	wsid = None
	wstoken = None
	TEAMID = getTeamIDByName(team_name)
	subscriptions = executeQuery(f"SELECT WSID, WSTOKEN FROM BRACKET_SUBSCRIBE WHERE EMAIL = '{channel}' AND TEAMNAME IN (SELECT NAME FROM TEAMS WHERE TEAMID = {TEAMID}) AND SUBSCRIBED = 1 LIMIT 1")
	if subscriptions != None:
		wsid = subscriptions[0]
		wstoken = subscriptions[1]
	return wsid, wstoken
	
def getBracketSubscribe(email):
	subscribe_results={}
	OneWeekAgo=int(time.time()) - 3600 * 24 * 4
	subscriptions = executeQuery(f"SELECT TEAMNAME, SUBSCRIBED FROM BRACKET_SUBSCRIBE WHERE EMAIL = '{email}' AND BRACKETID IN (SELECT BRACKETID FROM TEAMWAR_BRACKET WHERE UPDATED > {OneWeekAgo})")
	if subscriptions == None: return subscribe_results
	elif type(subscriptions) == tuple: subscriptions=[subscriptions]
	for sub_data in subscriptions:
		team_name=sub_data[0]
		is_subscribed=int(sub_data[1])
		subscribe_results[team_name]=is_subscribed
	return subscribe_results
	
def getCardComparisonTableData(unique_team_id):
	ordered_cards=[]
	result = executeQuery("SELECT CARDID1, CARDID2 FROM TEAMWAR_PAIRS WHERE PAIRID IN (SELECT PAIRID FROM TEAMWAR_CARDS WHERE TIME IN (SELECT MAX(TIME) FROM TEAMWAR_CARDS))")
	if type(result) == tuple: result=[result]
	for row in result:
		card1=row[0]
		card2=row[1]
		ordered_cards.append(card1)
		ordered_cards.append(card2)
	SEARCH_CARDS=",".join(str(x) for x in ordered_cards)
	card_comparison = executeQuery(f"SELECT CARDID, LEVEL, UPGRADES FROM USER_COLLECTIONS WHERE USERID IN (SELECT ID FROM USERS WHERE USERID IN (SELECT USERID FROM TEAM_MEMBERS WHERE TEAMID = (SELECT TEAMID FROM TEAMS_REPORT WHERE ID = {unique_team_id})) AND CARDID IN ({SEARCH_CARDS}))")
	if type(card_comparison) == tuple: card_comparison=[card_comparison]	
	leader_choice = executeQuery(f"SELECT CARDID, VOTE, LEVEL FROM TEAMWAR_CHOICE WHERE TEAMID = (SELECT TEAMID FROM TEAMS_REPORT WHERE ID = {unique_team_id} AND UPDATED > (SELECT MAX(STARTTIME) FROM EVENTS WHERE TYPE=5))")
	if type(leader_choice) == tuple: leader_choice=[leader_choice]
	return ordered_cards, card_comparison, leader_choice
	
def getTeamWarUpgradesSpentTableData(unique_team_id):
	cur_time = int(time.time())
	table_data={} # { blobid: [{userid: spent, userid: spent},{cardid: spent, cardid: spent} ], ...}
	blobid_to_time={}
	if not isValidTeamID(unique_team_id): return table_data,blobid_to_time
	#Merge these 4 into a single SQL query
	usernames_map = getAllUserNamesFromUniqueTeamID(unique_team_id)
	cards_spent = executeQuery(f"SELECT CARDID, SPENT, TOTAL, UPDATED, BLOBID FROM TEAMWAR_UPGRADE_CARDS WHERE TEAMID=(SELECT TEAMID FROM TEAMS_REPORT WHERE ID = {unique_team_id}) and UPDATED > (SELECT MAX(STARTTIME) + 3600 * 24 * 2 - 3600 FROM EVENTS WHERE TYPE=5 AND STARTTIME + 3600 * 24 * 2 < {cur_time}) ORDER BY UPDATED")
	users_spent = executeQuery(f"SELECT USERID, SPENT, TOTAL, UPDATED, BLOBID FROM TEAMWAR_UPGRADE_USERS WHERE TEAMID=(SELECT TEAMID FROM TEAMS_REPORT WHERE ID = {unique_team_id}) and UPDATED > (SELECT MAX(STARTTIME) + 3600 * 24 * 2 - 3600 FROM EVENTS WHERE TYPE=5 AND STARTTIME + 3600 * 24 * 2 < {cur_time}) ORDER BY UPDATED")
	'''
	cards_spent = executeQuery(f"SELECT CARDID, SPENT, TOTAL, UPDATED, BLOBID FROM TEAMWAR_UPGRADE_CARDS\
		WHERE TEAMID = (SELECT TEAMID FROM TEAMS_REPORT WHERE ID = {unique_team_id}) AND\
			UPDATED > (SELECT MAX(STARTTIME) + 3600 * 24 * 2 - 3600 FROM EVENTS WHERE TYPE=5)\
		ORDER BY UPDATED")
	users_spent = executeQuery(f"SELECT y.NAME, x.USERID, x.SPENT, x.TOTAL, x.UPDATED, x.BLOBID FROM TEAMWAR_UPGRADE_USERS x\
			JOIN (SELECT USERID, NAME FROM USERS) y\
		WHERE x.USERID = y.USERID AND\
			x.TEAMID=(SELECT TEAMID FROM TEAMS_REPORT WHERE ID = {unique_team_id}) AND\
			UPDATED > (SELECT MAX(STARTTIME) + 3600 * 24 * 2 - 3600 FROM EVENTS WHERE TYPE=5)\
			ORDER BY x.UPDATED")
	'''
	if type(cards_spent) == tuple: cards_spent=[cards_spent]
	if cards_spent == None: return table_data,blobid_to_time
	if type(users_spent) == tuple: users_spent=[users_spent]
	if users_spent == None: return table_data,blobid_to_time
	for row in cards_spent:
		CARDID, SPENT, TOTAL, UPDATED, BLOBID = [row[0],row[1],row[2],row[3],row[4]]
		blobid_to_time[BLOBID]=UPDATED
		if BLOBID not in table_data:
			table_data[BLOBID]=[{},{}]
		card_name=getCardName(CARDID)
		table_data[BLOBID][1][card_name]=SPENT
	USERS_LAST_SPENT={}
	for row in users_spent:
		USERID, SPENT, TOTAL, UPDATED, BLOBID = [row[0],row[1],row[2],row[3],row[4]]
		if SPENT == 0: continue
		if USERID in USERS_LAST_SPENT and SPENT <= USERS_LAST_SPENT[USERID]: continue
		blobid_to_time[BLOBID]=UPDATED
		if BLOBID not in table_data:
			table_data[BLOBID]=[{},{}]
		username="Unknown-"+USERID[:4]
		if USERID in usernames_map: username=usernames_map[USERID]
		LAST_SPENT=0
		if USERID in USERS_LAST_SPENT:
			LAST_SPENT=USERS_LAST_SPENT[USERID]
		else: USERS_LAST_SPENT[USERID]=0
		table_data[BLOBID][0][username]=SPENT-LAST_SPENT
		USERS_LAST_SPENT[USERID]=SPENT
	return table_data, blobid_to_time
	
def getTeamWarUpgradesCardsTableData(unique_team_id):
	table_data={} # { cardid: total, ...}
	if unique_team_id == None: return table_data
	cards_spent = executeQuery(f"SELECT CARDID, MAX(TOTAL) FROM TEAMWAR_UPGRADE_CARDS WHERE TEAMID=(SELECT TEAMID FROM TEAMS_REPORT WHERE ID = {unique_team_id}) and UPDATED > (SELECT MAX(STARTTIME)+3600*24*2-3600 FROM EVENTS WHERE TYPE=5 AND STARTTIME+3600*24*2-3600 < UNIX_TIMESTAMP()) GROUP BY CARDID")
	if cards_spent == None: return table_data
	if type(cards_spent) == tuple: cards_spent=[cards_spent]
	for row in cards_spent:
		CARDID = row[0]
		TOTAL = row[1]
		table_data[CARDID]=TOTAL
	return table_data
	
def getTeamWarStartTime():
	START_TIME = executeQuery("SELECT MAX(STARTTIME) FROM EVENTS WHERE TYPE=5")	
	if type(START_TIME) == tuple: START_TIME=START_TIME[0]
	return START_TIME
	
def getTeamWarUpgradesPlayerTableData(unique_team_id):
	table_data={} # { userid: [spent, total], ...}
	earned_data={}
	if unique_team_id == None: return table_data, earned_data
	cur_time = int(time.time())
	usernames_map = getAllUserNamesFromUniqueTeamID(unique_team_id)
	users_spent = executeQuery(f"SELECT USERID, MAX(SPENT), MAX(TOTAL) FROM TEAMWAR_UPGRADE_USERS WHERE TEAMID=(SELECT TEAMID FROM TEAMS_REPORT WHERE ID = {unique_team_id}) and UPDATED > (SELECT MAX(STARTTIME)+3600*24*2-3600 FROM EVENTS WHERE TYPE=5 AND STARTTIME+3600*24*2-3600 < {cur_time}) GROUP BY USERID")
	if users_spent == None: return table_data, earned_data
	if type(users_spent) == tuple: users_spent=[users_spent]
	for row in users_spent:
		USERID = row[0]
		username="Unknown-"+USERID[:4]
		if USERID in usernames_map: username=usernames_map[USERID]
		SPENT = row[1]
		TOTAL = row[2]
		table_data[username]=[SPENT,TOTAL]
	time_earned = executeQuery(f"SELECT USERID, TOTAL, UPDATED FROM TEAMWAR_UPGRADE_USERS WHERE TEAMID=(SELECT TEAMID FROM TEAMS_REPORT WHERE ID = {unique_team_id}) and UPDATED > (SELECT MAX(STARTTIME)+3600*24*2-3600 FROM EVENTS WHERE TYPE=5 AND STARTTIME+3600*24*2-3600 < {cur_time}) GROUP BY USERID, TOTAL;")
	if time_earned == None: return table_data, earned_data
	UPGRADE_START = getTeamWarStartTime() + 3600 * 24 * 2
	if UPGRADE_START > cur_time: UPGRADE_START = UPGRADE_START - 3600 * 24 * 7
	UPGRADE_DAY1_START = UPGRADE_START
	UPGRADE_DAY2_START = UPGRADE_DAY1_START + 3600 * 24
	UPGRADE_DAY3_START = UPGRADE_DAY2_START + 3600 * 24
	UPGRADE_DAY3_END = UPGRADE_DAY3_START + 3600 * 24
	if type(time_earned) == tuple: time_earned=[time_earned]
	for row in time_earned:
		USERID = row[0]
		username="Unknown-"+USERID[:4]
		if USERID in usernames_map: username=usernames_map[USERID]
		TOTAL = row[1]
		UPDATED = row[2]
		if username not in earned_data:
			earned_data[username]=[0,0,0]
		if UPDATED < UPGRADE_DAY1_START: continue
		elif UPGRADE_DAY2_START > UPDATED > UPGRADE_DAY1_START:
			earned_data[username][0]=TOTAL
		elif UPGRADE_DAY3_START > UPDATED > UPGRADE_DAY2_START:
			earned_data[username][1]=TOTAL-earned_data[username][0]
		elif UPGRADE_DAY3_END > UPDATED > UPGRADE_DAY3_START:
			earned_data[username][2]=TOTAL-(earned_data[username][1]+earned_data[username][0])
	for username in table_data.keys():
		if username not in earned_data:
			earned_data[username]=[0,0,0]
		result = earned_data[username]
		if result[0] == 0 and cur_time < UPGRADE_DAY2_START:
			earned_data[username][0]="Pending"
		if result[1] == 0 and cur_time < UPGRADE_DAY3_START:
			earned_data[username][1]="Pending"
		if result[2] == 0 and cur_time < UPGRADE_DAY3_END:
			earned_data[username][2]="Pending"
	return table_data, earned_data
	
def getTeamWarUpgradesPlayerTableData_nocaps(unique_team_id):
	table_data=[] # [USERNAME, ...]
	if unique_team_id == None: return table_data
	cur_time = int(time.time())
	usernames_map = getAllUserNamesFromUniqueTeamID(unique_team_id)
	users_spent = executeQuery(f"SELECT USERID FROM TEAM_MEMBERS WHERE TEAMID = (SELECT TEAMID FROM TEAMS_REPORT WHERE ID = {unique_team_id}) AND\
		USERID NOT IN (SELECT USERID FROM TEAMWAR_UPGRADE_USERS WHERE TEAMID=(SELECT TEAMID FROM TEAMS_REPORT WHERE ID = {unique_team_id}) and UPDATED > (SELECT MAX(STARTTIME)+3600*24*2-3600 FROM EVENTS WHERE TYPE=5 AND STARTTIME+3600*24*2-3600 < {cur_time}))")
	if users_spent == None: return table_data
	if type(users_spent) == tuple: users_spent=[users_spent]
	for row in users_spent:
		USERID = row[0]
		username="Unknown-"+USERID[:4]
		if USERID in usernames_map: username=usernames_map[USERID]
		table_data.append(username)
	return table_data
	
def getSummaryCardTableData(unique_team_id):
	user_cards_map={} #{ userid: {cardid : [level,upgrades], ...}, ... }
	ingame_team_id=getInGameTeamID(unique_team_id)
	if ingame_team_id == None: return user_cards_map
	CARD_DATA = executeQuery(f"SELECT USERID, CARDID, LEVEL, UPGRADES FROM USER_COLLECTIONS WHERE USERID IN \
		(SELECT ID FROM USERS WHERE USERID IN (SELECT USERID FROM TEAM_MEMBERS WHERE TEAMID={ingame_team_id}))")
	if type(CARD_DATA) == tuple: CARD_DATA=[CARD_DATA]
	if CARD_DATA == None: return user_cards_map
	for row in CARD_DATA:
		USERID, CARDID, LEVEL, UPGRADES = [row[0],row[1],row[2],row[3]]
		if USERID not in user_cards_map:
			user_cards_map[USERID]={}
		user_cards_map[USERID][CARDID]=[LEVEL, UPGRADES]
	return user_cards_map
	
def getTeamWarUpgradesSummary(unique_team_id):
	SUMMARY=[0,0,0,0] #TOTAL CARDS CAPS, UNSPENT, TOTAL USERS COLLECTED, UPDATED
	if unique_team_id == None: return SUMMARY
	if not isValidTeamID(unique_team_id): return SUMMARY
	cards_spent = executeQuery(f"SELECT CARDID, MAX(TOTAL), MAX(UPDATED) FROM TEAMWAR_UPGRADE_CARDS WHERE TEAMID=(SELECT TEAMID FROM TEAMS_REPORT WHERE ID = {unique_team_id}) and UPDATED > (SELECT MAX(STARTTIME)+3600*24*2-3600 FROM EVENTS WHERE TYPE=5 AND STARTTIME+3600*24*2-3600 < UNIX_TIMESTAMP()) GROUP BY CARDID")
	users_spent = executeQuery(f"SELECT USERID, MAX(TOTAL) AS TOTAL, MAX(UPDATED) FROM TEAMWAR_UPGRADE_USERS WHERE TEAMID=(SELECT TEAMID FROM TEAMS_REPORT WHERE ID = {unique_team_id}) and UPDATED > (SELECT MAX(STARTTIME)+3600*24*2-3600 FROM EVENTS WHERE TYPE=5 AND STARTTIME+3600*24*2-3600 < UNIX_TIMESTAMP()) GROUP BY USERID;")
	if type(cards_spent) == tuple: cards_spent=[cards_spent]
	if cards_spent == None: return SUMMARY
	if type(users_spent) == tuple: users_spent=[users_spent]
	if users_spent == None: return SUMMARY
	for row in cards_spent:
		TOTAL, UPDATED = [row[1],row[2]]
		if UPDATED > SUMMARY[3]: SUMMARY[3]=UPDATED
		SUMMARY[0]+=TOTAL
	for row in users_spent:
		TOTAL, UPDATED = [row[1],row[2]]
		if UPDATED > SUMMARY[3]: SUMMARY[3]=UPDATED
		SUMMARY[2]+=TOTAL
	SUMMARY[1] = SUMMARY[2]-SUMMARY[0]
	return SUMMARY
	
def generate_mmr_history(unique_user_id):
	if unique_user_id == None: return [],[]
	one_year_ago=int(time.time()) - 3600 * 24 * 365
	mmr_history = executeQuery(f"SELECT MMR, UPDATED FROM USERS_HISTORY WHERE USERID=(SELECT USERID FROM USERS WHERE ID={unique_user_id}) and UPDATED > {one_year_ago} ORDER BY UPDATED")
	if type(mmr_history) == tuple: mmr_history=[mmr_history]
	x=[] # Unique NK Levels (ordered)
	y=[] # % of total NKs
	if mmr_history == None: return x,y
	for row in mmr_history:
		mmr=row[0]
		updated=row[1]
		#convert to date: 2015-02-17
		timestamp=time.strftime('%Y-%m-%d', time.localtime(updated))
		x.append(timestamp)
		y.append(mmr)
	return x,y
	
def generate_card_history(card_id):
	data=[]
	target_list=[
		#"Top 250",
		"Top 1000",
		#"MMR 8000-8500",
		"MMR 7000-7500",
		"MMR 6000-6500",
		"MMR 5300-6000",
		"MMR 3900-4600",
		"MMR 2500-3200"
	]
	one_year_ago=int(time.time()) - 3600 * 24 * 365
	card_history = executeQuery(f"SELECT x.TIME, x.NAME, y.PERCENT FROM META_REPORT x \
		JOIN (SELECT CARDSID, PERCENT FROM META_CARDS WHERE CARDID = {card_id}) y \
		WHERE x.TIME > {one_year_ago} AND x.SEARCH = 'Last 1 day' AND x.CARDSID = y.CARDSID")
	if type(card_history) == tuple: card_history=[card_history]
	if card_history == None: return data
	interim_data={} # {NAME : [x_array, y_array], ...}
	for row in card_history:
		cur_time=row[0]
		name=row[1]
		percent=float(row[2])
		if name not in target_list: continue
		#convert to date: 2015-02-17
		timestamp=time.strftime('%Y-%m-%d', time.localtime(cur_time))
		if name not in interim_data:
			interim_data[name]=[[],[]] #[x_array, y_array]
		interim_data[name][0].append(timestamp)
		interim_data[name][1].append(percent)
	for data_name in sorted(interim_data.keys(), reverse=True):
		x_array,y_array=interim_data[data_name]
		data.append(
			dict(
				x=x_array,
				y=y_array,
				name=data_name,
				#marker=dict(
				#	color='rgb(55, 83, 109)'
				#)
			)
		)
	return data
	
def check_bracket_subscribe(last_checked):
	teamnames_webhook=[]
	max_time = last_checked
	result = executeQuery(f"SELECT Y.TEAMNAME, Y.WSID, Y.WSTOKEN, X.UPDATED FROM TEAMWAR_BRACKET X\
		JOIN BRACKET_SUBSCRIBE Y\
		WHERE X.UPDATED > {last_checked} AND\
		X.TEAMNAME = Y.TEAMNAME AND Y.bracketid = 0 AND Y.subscribed = 1 AND Y.WSID IS NOT NULL")
	if result == None: return teamnames_webhook, max_time
	if type(result) == tuple: result = [result]
	for row in result:
		TEAMNAME, WSID, WSTOKEN, UPDATED = [row[0],row[1],row[2],row[3]]
		if UPDATED > max_time: max_time = UPDATED
		teamnames_webhook.append([TEAMNAME,WSID,WSTOKEN])
	return teamnames_webhook, max_time

def weeklyBackupDatabase():
	cur_time = time.strftime('%Y%m%d_%H%M', time.localtime(time.time()))
	backupName = f"decktracker_weekly_{cur_time}"
	executeQuery(f"BACKUP DATABASE decktracker TO DISK = 'C:\\backups\\{backupName}'")
	
def dailyBackupDatabase():
	backupName = "decktracker_daily"
	executeQuery(f"BACKUP DATABASE decktracker TO DISK = 'C:\\backups\\{backupName}' WITH DIFFERENTIAL")
	
def getRandomPlayer():
	RESULT = executeQuery(f"SELECT NAME FROM users ORDER BY RAND() LIMIT 1")
	RESULT = RESULT[0]
	return RESULT
def getRandomTeam():
	RESULT = executeQuery(f"SELECT NAME FROM TEAMS X\
							JOIN teams_report Y \
							WHERE X.TEAMID = Y.TEAMID ORDER BY RAND() LIMIT 1")
	RESULT = RESULT[0]
	return RESULT
def getRandomCardID():
	RESULT = executeQuery(f"SELECT DISTINCT CARDID FROM cards_dynamic_stats ORDER BY RAND() LIMIT 1")
	RESULT = RESULT[0]
	return RESULT
def getRandomBracket():
	RESULT = executeQuery(f"SELECT TEAMNAME FROM teamwar_bracket WHERE updated > UNIX_TIMESTAMP()-7*24*3600 ORDER BY RAND() LIMIT 1")
	RESULT = RESULT[0]
	return RESULT
def downloadTokens():
	result = executeQuery(f"SELECT EMAIL,TOKEN,TEAM,CHANNEL,WSID,WSTOKEN,TEMPORARY,CONFIRM FROM CHAT_SUPPORT WHERE STATE IN ('VERIFIED','PENDING') AND UPDATED > UNIX_TIMESTAMP() - 24*3600 AND WSID IS NOT NULL")
	if type(result) == tuple: result = [result]
	return result
