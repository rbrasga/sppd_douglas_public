
'''


#Application Command Types
#- CHAT INPUT 1
#- USER 2
#- MESSAGE 3

#Applciation Command Option Types
#- 1 SUB_COMMAND
#- 2 SUB_COMMAND_GROUP
#- 3 STRING
#- 4 INTEGER
#- 5 BOOLEAN
#- 6 USER
#- 7 CHANNEL
#- 8 ROLE
#- 9 MENTIONABLE
#- 10 NUMBER
'''

# Global Command:

import requests
import json
import time

#/card command
CARD = {
    "name": "card",
    "type": 1,
    "description": "Send card details",
    "options": [
        {
            "name": "name",
            "description": "The in-game name of the card",
            "type": 3,
            "required": True,
        },
        {
            "name": "level",
            "description": "Card Levels from 1 to 7",
            "type": 4,
            "required": False
        },
        {
            "name": "upgrades",
            "description": "Card Upgrades from 1 to 70",
            "type": 4,
            "required": False
        },
        {
            "name": "max",
            "description": "Max level? Otherwise base level",
            "type": 5,
            "required": False
        }
    ]
}

#/art command
ART = {
    "name": "art",
    "type": 1,
    "description": "Send card art",
    "options": [
        {
            "name": "name",
            "description": "The in-game name of the card",
            "type": 3,
            "required": True,
        }
    ]
}

#/player command
PLAYER = {
    "name": "player",
    "type": 1,
    "description": "Send player details",
    "options": [
        {
            "name": "name",
            "description": "The full name of the player",
            "type": 3,
            "required": True,
        },
        {
            "name": "deep",
            "description": "Query SPPD Servers for latest details",
            "type": 5,
            "required": False
        }
    ]
}

#/team command
TEAM = {
    "name": "team",
    "type": 1,
    "description": "Send team details",
    "options": [
        {
            "name": "name",
            "description": "The full name of the team",
            "type": 3,
            "required": True,
        },
        {
            "name": "deep",
            "description": "Query SPPD Servers for latest details",
            "type": 5,
            "required": False
        }
    ]
}

#/bracket command
#guild command id: 885965611996446831
BRACKET = {
    "name": "bracket",
    "type": 1,
    "description": "Get TVT bracket details",
    "options": [
        {
            "name": "name",
            "description": "The full name a team on that bracket",
            "type": 3,
            "required": True,
        },
        {
            "name": "subscribe",
            "description": "Ignore,Subscribe,Unsubscribe",
            "type": 3,
            "required": False,
            "choices": [
                {
                    "name": "Subscribe",
                    "value": "subscribe"
                },
                {
                    "name": "Unsubscribe",
                    "value": "unsubscribe"
                },
                {
                    "name": "Ignore",
                    "value": "ignore"
                }
            ]
        },
        {
            "name": "webhook",
            "description": "The name of the bot to post updates",
            "type": 3,
            "required": False,
        }
    ]
}

#/bind command
BIND = {
    "name": "bind",
    "type": 1,
    "description": "Create custom command",
    "options": [
        {
            "name": "word",
            "description": "Command word",
            "type": 3,
            "required": True,
        },
        {
            "name": "content",
            "description": "Text or File URL",
            "type": 3,
            "required": True,
        }
    ]
}

#/unbind command
UNBIND = {
    "name": "unbind",
    "type": 1,
    "description": "Delete custom command",
    "options": [
        {
            "name": "word",
            "description": "Command word",
            "type": 3,
            "required": True,
        }
    ]
}

#/unbind command
IMPORT_BINDS = {
    "name": "import_binds",
    "type": 1,
    "description": "Bring binds from Douglas v2 to Douglas v3 (me)",
}

#/unbind command
UPDATE_EVENTS = {
    "name": "update_events",
    "type": 1,
    "description": "Update the events on the SPPD Replay website, in case it's not showing.",
}

#/unbind command
BIND_LIST = {
    "name": "bind_list",
    "type": 1,
    "description": "List all the binds",
}

#/search command
SEARCH = {
    "name": "search",
    "type": 1,
    "description": "Lookup player/team/card details",
    "options": [
        {
            "name": "name",
            "description": "Part of the player/team's name, or card tag(s)",
            "type": 3,
            "required": True,
        },
        {
            "name": "type",
            "description": "Default: Player",
            "type": 3,
            "required": False,
            "choices": [
                {
                    "name": "Player",
                    "value": "player"
                },
                {
                    "name": "Team",
                    "value": "team"
                },
                {
                    "name": "Card",
                    "value": "card"
                }
            ]
        }
    ]
}

#/calc command
CALC = {
    "name": "calc",
    "type": 1,
    "description": "Upgrades Calculator for required materials",
    "options": [
        {
            "name": "rarity",
            "description": "Part of the player/team's name, or card tag(s)",
            "type": 3,
            "required": True,
            "choices": [
                {
                    "name": "Common",
                    "value": "Common"
                },
                {
                    "name": "Rare",
                    "value": "Rare"
                },
                {
                    "name": "Epic",
                    "value": "Epic"
                },
                {
                    "name": "Legendary",
                    "value": "Legendary"
                }
            ]
        },
        {
            "name": "from",
            "description": "1, m3, u40, etc.",
            "type": 3,
            "required": True,
        },
        {
            "name": "to",
            "description": "2, m4, u55, etc.",
            "type": 3,
            "required": True,
        }
    ]
}

#/compare command
COMPARE = {
    "name": "compare",
    "type": 1,
    "description": "Compare card details between levels",
    "options": [
        {
            "name": "name",
            "description": "Part of the card name as it appears in-game",
            "type": 3,
            "required": True
        },
        {
            "name": "from",
            "description": "1, m3, u40, etc.",
            "type": 3,
            "required": True,
        },
        {
            "name": "to",
            "description": "2, m4, u55, etc.",
            "type": 3,
            "required": True,
        }
    ]
}

#/chat command
CHAT = {
    "name": "chat",
    "type": 1,
    "description": "Integrated SPPD <-> Discord Chat",
    "options": [
        {
            "name": "command",
            "description": "What would you like to do?",
            "type": 3,
            "required": True,
            "choices": [
                {
                    "name": "Subscribe",
                    "value": "subscribe"
                },
                {
                    "name": "Unsubscribe",
                    "value": "unsubscribe"
                },
                {
                    "name": "Confirm",
                    "value": "confirm"
                },
                {
                    "name": "Set TVT Channel",
                    "value": "tvtset"
                },
                {
                    "name": "Status",
                    "value": "status"
                }
            ]
        },
        {
            "name": "name",
            "description": "Full Team Name",
            "type": 3,
            "required": False
        },
        {
            "name": "option",
            "description": "Ignore, or follow as directed",
            "type": 4,
            "required": False,
        },
        {
            "name": "webhook",
            "description": "The name of the bot to post updates",
            "type": 3,
            "required": False,
        },
        {
            "name": "channel",
            "description": "Used for setting the TVT Channel",
            "type": 3,
            "required": False,
        }
    ]
}

#/help command
HELP = {
    "name": "help",
    "type": 1,
    "description": "List of available commands",
    "options": [
        {
            "name": "command",
            "description": "What would you like to do?",
            "type": 3,
            "required": False,
            "choices": [
                {
                    "name": "art",
                    "value": "art"
                },
                {
                    "name": "bind",
                    "value": "bind"
                },
                {
                    "name": "bind_list",
                    "value": "bind_list"
                },
                {
                    "name": "bracket",
                    "value": "bracket"
                },
                {
                    "name": "calc",
                    "value": "calc"
                },
                {
                    "name": "card",
                    "value": "card"
                },
                {
                    "name": "chat",
                    "value": "chat"
                },
                {
                    "name": "compare",
                    "value": "compare"
                },
                {
                    "name": "import_binds",
                    "value": "import_binds"
                },
                {
                    "name": "player",
                    "value": "player"
                },
                {
                    "name": "search",
                    "value": "search"
                },
                {
                    "name": "team",
                    "value": "team"
                },
                {
                    "name": "unbind",
                    "value": "unbind"
                },
                {
                    "name": "help",
                    "value": "help"
                },
            ]
        }
	]
}

# For authorization, you can use either your bot token
headers = {
    "Authorization": "Bot <token>"
}

def getChannelMessages(channel_id):
	url = f"https://discord.com/api/channels/{channel_id}/messages"
	r = requests.get(url, headers=headers)
	return r.json()

def getUserInfo(user_id):
	url = f"https://discord.com/api/users/{user_id}"
	r = requests.get(url, headers=headers)
	return r.json()
	
def getGuildUserInfo(server_id,user_id):
	url = f"https://discord.com/api/guilds/{server_id}/members/{user_id}"
	r = requests.get(url, headers=headers)
	return r.json()
	
def getChannelInfo(channel_id):
	url = f"https://discord.com/api/channels/{channel_id}"
	r = requests.get(url, headers=headers)
	return r.json()

#Webhook URL
#{"type": 1, "id": "885931301163655268", "name": "ILLUMINATED BRACKET", "avatar": null, "channel_id": "612453232546938890", "guild_id": "582490427832270850", "application_id": "885580479846297641", "token": "7TwHXBI0EmUvNO1oYQUXP3BA-vTG5GcbWA4OtXcjacmGDp7lq_P10bLJr_28rF41PXYc", "user": {"id": "885580479846297641", "username": "Douglas v3", "avatar": "ea56dd513ec996299c5b5c44962592bf", "discriminator": "6563", "public_flags": 0, "bot": true}}
def testWebhook():
	webhook_url = "https://discord.com/api/webhooks/885931301163655268/7TwHXBI0EmUvNO1oYQUXP3BA-vTG5GcbWA4OtXcjacmGDp7lq_P10bLJr_28rF41PXYc"
	json = {
		"content": "Testing Webhook"
	}
	r = requests.post(webhook_url, json=json)
	print(f"testWebhook {r.json}")
	

def createWebhook(webhook_name, channel):
	webhook_url = f"https://discord.com/api/channels/{channel}/webhooks"
	wsid = None
	wstoken = None
	json = {"name": webhook_name}
	r = requests.post(webhook_url, headers=headers, json=json)
	if r.status_code == 200:
		result = r.json()
		wsid = result["id"]
		wstoken = result["token"]
	return wsid, wstoken
	
def getGuildFromChannel(channel):
	url = f"https://discord.com/api/channels/{channel}"
	guild=None
	r = requests.get(url, headers=headers)
	if r.status_code == 200:
		result = r.json()
		print(result)
	return guild
	
def deleteWebhook(wsid, wstoken):
	webhook_url = f"https://discord.com/api/webhooks/{wsid}/{wstoken}"
	r = requests.delete(webhook_url)
	return r.status_code == 204
	
def createGuildApplicationCommand(json):
	url = "https://discord.com/api/v8/applications/885580479846297641/guilds/582490427832270850/commands"
	r = requests.post(url, headers=headers, json=json)
	print(f"createGuildApplicationCommand {r.text}")

def createGlobalApplicationCommand(json):
	url = "https://discord.com/api/v8/applications/885580479846297641/commands"
	r = requests.post(url, headers=headers, json=json)
	print(f"createGlobalApplicationCommand {r.text}")
	
def deleteGuildApplicationCommand(cid):
	url = f"https://discord.com/api/v8/applications/885580479846297641/guilds/582490427832270850/commands/{cid}"
	r = requests.delete(url, headers=headers)
	print(f"deleteGuildApplicationCommand {cid} returned {r.status_code}")
	
def deleteGlobalApplicationCommand(cid):
	url = f"https://discord.com/api/v8/applications/885580479846297641/commands/{cid}"
	r = requests.delete(url, headers=headers)
	print(f"deleteGlobalApplicationCommand {cid} returned {r.status_code}")
	
def getGuildApplicationCommands():
	url = "https://discord.com/api/v8/applications/885580479846297641/guilds/582490427832270850/commands"
	r = requests.get(url, headers=headers)
	print(f"getGuildApplicationCommands {r.text}")
	
def getGlobalApplicationCommands():
	url = "https://discord.com/api/v8/applications/885580479846297641/commands"
	r = requests.get(url, headers=headers)
	print(f"getGlobalApplicationCommands {r.text}")
	
#Get Commands for Guild/Global
#getGuildApplicationCommands()
#getGlobalApplicationCommands()
#createWebhook()
#testWebhook()
#while True:
#	print(json.dumps(getChannelMessages(612453232546938890)))
#	time.sleep(5)
#print(json.dumps(getChannelMessages(612453232546938890)))
#print(json.dumps(getUserInfo(647543059067699200)))
#print(json.dumps(getGuildUserInfo(582490427832270850,647543059067699200)))
#print(json.dumps(getGuildUserInfo(393416804875239434,425469453325828107)))
#print(json.dumps(getChannelInfo(825958699947524136)))
#sys.exit()
#message="thmc masz prezent od mojej znajomej przez ktÃ³rÄ mnie rozÅÄczyÅo :-)"
#print(message.encode('utf-8').decode('utf-8', 'ignore'))
#print(message.encode('raw_unicode_escape').decode('utf-8', 'ignore'))

#Create Guild Commands
COMMANDS_TO_CREATE=[]
for c in COMMANDS_TO_CREATE:
	createGuildApplicationCommand(c)
#Create Global Commands
COMMANDS_TO_CREATE=[]
for c in COMMANDS_TO_CREATE:
	createGlobalApplicationCommand(c)

#Delete Guild Commands
COMMANDS_TO_DELETE=[]
for cid in COMMANDS_TO_DELETE:
	deleteGuildApplicationCommand(cid)
#Delete Global Commands
COMMANDS_TO_DELETE=[]
for cid in COMMANDS_TO_DELETE:
	deleteGlobalApplicationCommand(cid)
	
CHANNEL=582490428373205024
getGuildFromChannel(CHANNEL)
'''
# Guild Command (i.e. Server-specific Command)
import requests


url = "https://discord.com/api/v8/applications/<my_application_id>/guilds/<guild_id>/commands"

# This is an example USER command, with a type of 2
json = {
    "name": "High Five",
    "type": 2
}

# For authorization, you can use either your bot token
headers = {
    "Authorization": "Bot <my_bot_token>"
}

# or a client credentials token for your app with the applications.commands.update scope
headers = {
    "Authorization": "Bearer <my_credentials_token>"
}

r = requests.post(url, headers=headers, json=json)

#Commands can be deleted and updated by making DELETE and PATCH calls to the command endpoint. Those endpoints are
#- applications/<my_application_id>/commands/<command_id> for global commands, or
#- applications/<my_application_id>/guilds/<guild_id>/commands/<command_id> for guild commands
#Because commands have unique names within a type and scope, we treat POST requests for new commands as upserts. That means making a new command with an already-used name for your application will update the existing command.

'''

'''
import HELPER_DB
import RESTFUL
RESULT = HELPER_DB.downloadTokens()
for row in RESULT:
	TEAM,CHANNEL,WSID,WSTOKEN = [row[2],row[3],row[4],row[5]]
	NAME=HELPER_DB.getTeamNameFromIngameTeamID(TEAM)
	wsid, wstoken = createWebhook(f"{NAME} chat", CHANNEL)
	if wsid == None:
		print(f"Unable to get webhook for {NAME}")
		continue
	#deleteWebhook(WSID, WSTOKEN)
	RESTFUL.updateChatSupport(TEAM,wsid,wstoken)
'''