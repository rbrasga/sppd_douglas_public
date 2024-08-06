
from flask import Flask, request, make_response, abort, jsonify
import cherrypy
import DATABASE, HELPER_DB, RESTFUL
import asyncio, datetime, os, random, requests, sys, threading, time
from enum import Enum
from dotenv import load_dotenv
import validators
import urllib
import discord
from discord.ext import commands, tasks
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

BASE_URL = "https://discord.com/api/v8"


class InteractionResponseType(Enum):
    pong = 1
    channel_message_with_source = 4
    deferred_channel_message_with_source = 5

class ApplicationCommandOptionType(Enum):
    sub_command = 1
    sub_command_group = 2
    string = 3
    integer = 4
    boolean = 5
    user = 6
    channel = 7
    role = 8

class FollowupMessage:

    def __init__(self, data, interaction):
        self.data = data
        self.interaction = interaction
        self.session = interaction.session
        self.id = int(data["id"])
        self.content = data.get("content")
        self.embeds = [
            discord.Embed.from_dict(embed)
            for embed in data.get("embeds", [])
        ]


    def __repr__(self):
        return f"<FollowupMessage id={self.id}>"


    def _update(self, data):
        self.content = data.get("content")
        self.embeds = [
            discord.Embed.from_dict(embed)
            for embed in data.get("embeds", [])
        ]


    async def edit(self, *, content=None, embed=None, embeds=None):
        '''
        Edits the message
        '''
        if embeds is None and embed is None:
            embeds = []
        elif embeds is None and embed:
            embeds = [embed]
        url = f"{BASE_URL}/webhooks/{self.interaction.application_id}/{self.interaction.token}/messages/{self.id}"
        payload = {
            "content": content,
            "embeds": embeds
        }
        async with self.session.patch(url, json=payload) as resp:
            resp.raise_for_status()
            data = await resp.json()
            self._update(data)
            return self


    async def delete(self):
        '''
        Deletes this message
        '''
        embeds = embeds or [embed] or []
        url = f"{BASE_URL}/webhooks/{self.interaction.application_id}/{self.interaction.token}/messages/{self.id}"

        async with self.session.delete(url) as resp:
            resp.raise_for_status()

class Interaction:
    def __init__(self, data):
        self.data = data
        self.session = requests.Session()
        self.id = data["id"]
        self.application_id = data["application_id"]
        self.token = data["token"]
        self.guild = data["guild_id"]
        self.author = data["member"]["user"]["id"]
        self.author_name = data["member"]["user"]["username"]
        self.channel = data["channel_id"]
        
        self.command_name = self.data["data"]["name"]
        self.command_id = int(self.data["data"]["id"])
        self.options = {}
        if "options" in data["data"]:
            self.options = self.build_options(data["data"]["options"])

    def __repr__(self):
        return f"<Interaction name={self.command_name} options={self.options}>"

    def build_options(self, options):
        ret = {}
        for option in options:
            name = option["name"]
            value = option["value"]
            type_ = ApplicationCommandOptionType(option["type"])
            if type_ in (ApplicationCommandOptionType.sub_command_group,
                         ApplicationCommandOptionType.sub_command):
                value = self.build_options(value)
            elif type_ is ApplicationCommandOptionType.integer:
                value = int(value)

            ret[name] = value

        return ret

    #async def ack(self):
    def ack(self):
        '''
        Acknowledge the slash command to get more time
        to issue followups
        
        Note: You cannot use Message.respond after this
        You must use Message.edit_original or Message.followup
        after acknowledging
        '''
        url = f"{BASE_URL}/interactions/{self.id}/{self.token}/callback"
        payload = {
            "type": InteractionResponseType.deferred_channel_message_with_source.value
        }
        return jsonify(payload)
        #async with self.session.post(url, json=payload) as resp:
        #    return


    #async def respond(self, content=None, *, tts=False, embed=None, embeds=None, hidden=False):
    def respond(self, content=None, *, tts=False, embed=None, embeds=None, hidden=False):
        '''
        Send the initial response message
        '''
        if embeds is None and embed is None:
            embeds = []
        elif embeds is None and embed:
            embeds = [embed]
        url = f"{BASE_URL}/interactions/{self.id}/{self.token}/callback"
        payload = {
            "type": InteractionResponseType.channel_message_with_source.value,
            "data": {
                "content": content,
                "tts": tts,
                "embeds": embeds
            }
        }
        if hidden:
            payload["data"]["flags"] = 64
        return jsonify(payload)
        #async with self.session.post(url, json=payload) as resp:
        #    resp.raise_for_status()


    async def edit_original(self, *, content=None, embed=None, embeds=None):
        '''
        Edit the original response message
        Can only be used after Message.ack or Message.respond
        '''
        if embeds is None and embed is None:
            embeds = []
        elif embeds is None and embed:
            embeds = [embed]
        url = f"{BASE_URL}/webhooks/{self.application_id}/{self.token}/messages/@original"
        payload = {
            "content": content,
            "embeds": embeds
        }
        self.session.patch(url, json=payload)

    async def delete_original(self):
        '''
        Deletes the original response message
        '''
        url = f"{BASE_URL}/webhooks/{self.application_id}/{self.token}/messages/@original"
        async with self.session.delete(url) as resp:
            resp.raise_for_status()


    async def followup(self, content=None, *, tts=False, embed=None, embeds=None):
        '''
        Sends a follow up message
        '''
        if embeds is None and embed is None:
            embeds = []
        elif embeds is None and embed:
            embeds = [embed]
        url = f"{BASE_URL}/webhooks/{self.application_id}/{self.token}"
        payload = {
            "tts": tts,
            "content": content,
            "embeds": embeds
        }
        async with self.session.post(url, json=payload) as resp:
            resp.raise_for_status()
            data = await resp.json()
            return FollowupMessage(data, self)
'''
class SlashCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_socket_response(self, payload):
        if payload['t'] != 'INTERACTION_CREATE':
            return
        data = payload['d']
        self.bot.dispatch('slash_command', Interaction(data, self.bot))


def setup(bot):
    cog = SlashCommands(bot)
    bot.add_cog(cog)
	
# Source: https://gist.github.com/AXVin/0be0b8997e24fa191e23e1dce651f37d
'''

'''
{
	'application_id': '885580479846297641',
	'channel_id': '582490428373205024',
	'data': {
		'id': '885593861555105792',
		'name': 'blep',
		'options': [
			{
				'name': 'animal',
				'type': 3,
				'value': 'animal_cat'
			},
			{
				'name': 'only_smol',
				'type': 5,
				'value': True
			}
		],
		'type': 1
	},
	'guild_id': '582490427832270850',
	'id': '885603548203716658',
	'member': {
		'avatar': None,
		'deaf': False,
		'is_pending': False,
		'joined_at': '2019-05-27T08:49:00.261000+00:00',
		'mute': False, 'nick': None,
		'pending': False,
		'permissions': '549755813887',
		'premium_since': None,
		'roles': [
			'582710726184009728',
			'640461537483423756',
			'719813932994265109'
		],
		'user': {
			'avatar': '3ccb7832b47e52a63c3bfcd2d028aac2',
			'discriminator': '3617',
			'id': '369526401365311491',
			'public_flags': 0,
			'username': 'LuckyPenguin'
		}
	},
	'token': 'aW50ZXJhY3Rpb246ODg1NjAzNTQ4MjAzNzE2NjU4Om9hUVZNaVRrY1pvZnBOMGNXYXVkOFVHTzU4cFdVMlI1UEtUd2ZzdmZTMmhnVVlJbWNkS2FGS3JXbnFzVVNrZUxrVVdNM0NHenRackZxRmtkV0hmQzRMUFVLOHFkdmVBRVRDazNOc3J3VzFxenFEWEVWY1p3Sks3MjZSUmtlTDVr',
	'type': 2,
	'version': 1
}

Slash Command list:
***player
***team
***card
***art
***bracket
***bind/unbind
   - Still need to support shortcut commands
***search
***calc
***compare
suprise

BRACKET
***subscribe
   - Create Webhook
   
CHAT
subscribe
   - https://discord.com/developers/docs/resources/channel#get-channel-messages
   - Create Webhook

/chat subscribe name: <name>
/chat unsubscribe
/chat status
/chat confirm: (disable|enable)

'''

# Your public key can be found on your application in the Developer Portal

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
PUBLIC_KEY = os.getenv('PUBLIC_KEY')
APP_ID = os.getenv('APP_ID')

last_updated = int(time.time())-20
BRACKET_SUBSCRIPTION_SLEEP = 60
DEEP_REFRESH = 15 * 60 # Only once every 15 minutes.
author_tracker = {}
request_tracker = {
	"help" : 0,
	"player" : 0,
	"team" : 0,
	"search" : 0,
	"cards": 0,
	"art": 0,
	"bracket": 0,
	"subscribe": 0,
	"bind": 0,
	"calc": 0,
	"surprise": 0,
	"compare": 0
}

server = Flask(__name__)


def getMyStatus():
	url = f"{BASE_URL}//users/@me/guilds"
	headers = {"Authorization": f"Bot {SECRET_KEY}"}
	result = None
	try:
		r = requests.get(url, headers=headers)
		json_object = r.json()
		result = len(json_object)
	except:
		print("ERROR: getMyStatus")
	return result
	
class THREADBOT(threading.Thread):
	
	def __init__(self, func):
		threading.Thread.__init__(self)
		self._stop_event = threading.Event()
		self.func = func
		
	def stop(self):
		global stop_event
		self._stop_event.set()
		stop_event.set() #in HELPER_BOT

	def run(self):
		self.func()

class DEEPBOT(threading.Thread):
	
	def __init__(self, interaction, target, name=None, options=None):
		threading.Thread.__init__(self)
		self._stop_event = threading.Event()
		self.interaction = interaction
		self.target = target
		self.name = name
		self.options = options
		
	def stop(self):
		global stop_event
		self._stop_event.set()
		stop_event.set() #in HELPER_BOT

	def run(self):
		time.sleep(0.1)
		self.loop = asyncio.new_event_loop()
		asyncio.set_event_loop(self.loop)
		if self.target == 'player':
			self.player_command()
		elif self.target == 'team':
			self.team_command()
		elif self.target == 'card':
			self.card_command()
		elif self.target == 'import_binds':
			self.import_binds_command()
		elif self.target == 'chat':
			self.chat_command()
		elif self.target == 'bracket':
			self.bracket_command()
		elif self.target == 'update_events':
			self.update_events_command()
		self.loop.close()
		
	def player_command(self):
		global author_tracker, DEEP_REFRESH
		response, success, delete_me = HELPER_DB.getPlayerResponse(self.name, self.options != None)
		if success:
			author_tracker[self.options] = int(time.time()) + DEEP_REFRESH
		self.loop.run_until_complete(self.interaction.edit_original(content=response))
		
	def team_command(self):
		global author_tracker, DEEP_REFRESH
		response, success = HELPER_DB.getTeamResponse(self.name, self.options != None)
		if success:
			author_tracker[self.options] = int(time.time()) + DEEP_REFRESH
		self.loop.run_until_complete(self.interaction.edit_original(content=response))
		
	def card_command(self):
		response, success, filename = HELPER_DB.getCardDataAtLevel(self.name,self.options)
		embed = None
		if filename != None:
			embed = {
				"type": "rich",
				"color": 65535,
				"image":{
					"url": f"https://sppdreplay.net/static/{filename}"
				}
			}
		self.loop.run_until_complete(self.interaction.edit_original(content=response,embed=embed))
		
	def import_binds_command(self):
		#Submit the guild binds
		#for DWORD in all DWORDS:
		old_binds = HELPER_DB.getOldBinds(self.interaction.guild)
		for WORD,TYPE,CONTENT in old_binds:
			if " " in WORD: continue
			if validators.url(CONTENT):
				TYPE = "FILE"
			success = RESTFUL.unbindWord(self.interaction.guild,WORD)
			if success:
				command_id = create_guild_command(self.interaction.guild, WORD, self.interaction.author_name)
				success = RESTFUL.bindWord(self.interaction.guild,WORD,TYPE,CONTENT,f"{self.interaction.author}", command_id)
			time.sleep(0.1)
		self.loop.run_until_complete(self.interaction.edit_original(content="This servers binds are now available as slash commands."))
		
	def update_events_command(self):
		success = True
		time.sleep(5)
		success = success and RESTFUL.getAllEvents()
		time.sleep(5)
		success = success and RESTFUL.getAllEvents_two()
		content = "Events were updated!"
		if not success:
			content = "There was an error processing the events!"
		self.loop.run_until_complete(self.interaction.edit_original(content=content))
		
	def bracket_command(self):
		team_name = self.interaction.options.get("name").lower()	
		subscribe = self.interaction.options.get("subscribe")
		WEBHOOK = self.interaction.options.get("webhook")
		response, success = HELPER_DB.getBracketResponse(team_name)
		#Subscribe
		if subscribe == "subscribe":
			if success:
				#Try to delete the old bracket subscription...
				#Grab the wsid
				wsid, wstoken = HELPER_DB.getBracketSubscribeWSID(team_name, self.interaction.channel)
				deleted = unsubscribe_channel(team_name, self.interaction.channel)
				if deleted and wsid != None:
					deleteWebhook(wsid, wstoken)
				#Now generate the subscription
				#Get a webhook
				target_name = f"{team_name} bracket"
				if WEBHOOK != None:
					target_name = f"{WEBHOOK}"
				wsid, wstoken = createWebhook(f"{target_name}", self.interaction.channel)
				if wsid == None:
					response = "Sorry, but I need the `MANAGE_WEBHOOKS` permission OR your team has special characters and you need to specify a different webhook name."
				else:
					#Update database
					subscribe_channel(team_name, self.interaction.channel, wsid, wstoken)
					response = "You are subscribed to that team. Here is their last bracket update:\n\n" + response
			else: response = "Sorry, I can't find a team with that name."
		elif subscribe == "unsubscribe":
			if success:
				#Grab the wsid
				wsid, wstoken = HELPER_DB.getBracketSubscribeWSID(team_name, self.interaction.channel)
				success = unsubscribe_channel(team_name, self.interaction.channel)
				if success:
					response = random.choice(["Good idea. You unsubscriber you!","Yay... Enjoy NOT being spammed with updates :P", "Cool. Unsubscribed."])
					if wsid != None:
						result = deleteWebhook(wsid, wstoken)
						if not result:
							response = "You unsubscribed, but there was an issue removing the webhook."
				else: response = "You can't unsubscribe, because you were not subscribed to that team."
			else: response = "Sorry, I can't find a team with that name."
		self.loop.run_until_complete(self.interaction.edit_original(content=response))
		
	def chat_command(self):
		COMMAND = self.interaction.options.get("command")
		NAME = self.interaction.options.get("name")
		OPTION = self.interaction.options.get("option")
		CHANNEL = self.interaction.options.get("channel")
		WEBHOOK = self.interaction.options.get("webhook")
		if COMMAND == 'status':
			m = HELPER_DB.getChatStatus(self.interaction.channel)
			self.loop.run_until_complete(self.interaction.edit_original(content=m))
			return
		if COMMAND == 'confirm':
			enable = None
			response = "Use Option - 0: Enable, 1: Disable"
			if OPTION == 0:
				enable = True
				response = "Discord-to-SPPD message confirmations **Enabled**, please wait a few minutes to synchronize."
			elif OPTION == 1:
				enable = False
				response = "Discord-to-SPPD message confirmations **Disabled**, please wait a few minutes to synchronize."
			if enable != None: confirm_chat(self.interaction.channel,enable)
			self.loop.run_until_complete(self.interaction.edit_original(content=response))
			return
		if COMMAND == 'tvtset':
			print(f'CHANNEL="{CHANNEL}"')
			response = "Oops."
			if CHANNEL == None:
				subscribe_chat_tvt(self.interaction.channel,delete=True)
				response = "TVT Channel was set to NULL, please wait a few minutes to synchronize. Use `Option: #Channel` to set a channel."
			else:
				try:
					CHANNEL=int(CHANNEL.strip("<>").strip("#"))
				except:
					response = "That doesn't look like a channel to me. Channels start with #."
					self.loop.run_until_complete(self.interaction.edit_original(content=response))
					return
				# Verify that `CHANNEL` is in the same server as `self.interaction.channel`!
				new_channels_guild = getGuildFromChannel(CHANNEL)
				print(f'{new_channels_guild} == {self.interaction.guild}')
				if new_channels_guild == None:
					response = "I don't have access there. Sorry..."
				elif new_channels_guild != self.interaction.guild:
					response = "Stop! You cannot move your TVT scores to a different discord server!"
				else:
					wsid, wstoken = createWebhook("TVT Tracker", CHANNEL)
					if wsid == None:
						response = "Sorry, but I need the `MANAGE_WEBHOOKS` permission under that channel."
						self.loop.run_until_complete(self.interaction.edit_original(content=response))
						return
					subscribe_chat_tvt(self.interaction.channel,CHANNEL,wsid,wstoken)
					response = f"TVT Channel was set to <#{CHANNEL}>, please wait a few minutes to synchronize."
			self.loop.run_until_complete(self.interaction.edit_original(content=response))
			return
		delete = None
		EMAIL = None
		TEAMID = None
		if COMMAND == "unsubscribe":
			delete = True
		if COMMAND == "subscribe":
			delete = False
			if NAME == None:
				self.loop.run_until_complete(self.interaction.edit_original(content="You must specify a team name."))
				return
			TEAMID = HELPER_DB.getTeamIDByName(NAME)
			if TEAMID == -1:
				self.loop.run_until_complete(self.interaction.edit_original(content=f"Sorry, I can't find the team `{NAME}`"))
				return
			email_list = HELPER_DB.getEmailsForChatByTeamID(TEAMID)
			if len(email_list) == 0:
				self.loop.run_until_complete(self.interaction.edit_original(content="Looks like your team isn't part of Team Manager Cloud. Sign up here: https://sppdreplay.net/teammanagercloud..."))
				return
			if OPTION != None:
				OPTION -= 1
				#Look up the email address by index
				if OPTION < 0 or OPTION >= len(email_list):
					self.loop.run_until_complete(self.interaction.edit_original(content="Nice Try. That's not a valid option."))
					return
				EMAIL = email_list[int(OPTION)]
		if delete == None:
			self.loop.run_until_complete(self.interaction.edit_original(content=f"`{COMMAND}` is not yet supported..."))
			return
			
		if type(NAME) == str:
			NAME = NAME.lower()
			
		wsid = None
		wstoken = None
		result = ""
		if delete:
			result = subscribe_chat(None, self.interaction.channel, delete=delete)
		else:
			target_name = f"{NAME} chat"
			if WEBHOOK != None:
				target_name = f"{WEBHOOK}"
			wsid, wstoken = createWebhook(target_name, self.interaction.channel)
			if wsid == None:
				response = "Sorry, but I need the `MANAGE_WEBHOOKS` permission OR your team has special characters and you need to specify a different webhook name."
				self.loop.run_until_complete(self.interaction.edit_original(content=response))
				return
			result = subscribe_chat(TEAMID, self.interaction.channel, wsid, wstoken, EMAIL, delete)
		if delete:
			try:
				teamid = int(result.strip('\n'))
				TEAM_NAME = HELPER_DB.getTeamNameFromIngameTeamID(teamid)
				if TEAM_NAME != None:
					self.loop.run_until_complete(self.interaction.edit_original(content=f"Unsubscribed {TEAM_NAME} from this channel."))
					return
			except:
				pass
			if "None" in result:
				self.loop.run_until_complete(self.interaction.edit_original(content="There wasn't a team subscribed here..."))
				return
		if "OK" in result:
			if delete:
				self.loop.run_until_complete(self.interaction.edit_original(content="If you input a valid team, this channel will be unsubscribed in a few minutes..."))
				return
			else:
				self.loop.run_until_complete(self.interaction.edit_original(content="Nice. You will receive a confirmation request from your custom Bot in the next few minutes."))
				return
		elif "FAIL" in result:
			self.loop.run_until_complete(self.interaction.edit_original(content="Looks like your team isn't part of Team Manager Cloud. Sign up here: https://sppdreplay.net/teammanagercloud..."))
			return
		elif "EXCEPTION" in result:
			if wsid != None: deleteWebhook(wsid, wstoken)
			#await send_to_discord(message.channel,"Looks like you have multiple team manager clients. Contact the developer for support. Or just run a single team manager instance for your team...")
			#Look up the emails for that teamid. Present them with Option 1 - 2 - 3
			email_list = HELPER_DB.getEmailsForChatByTeamID(TEAMID)
			long_string = "You have multiple active team manager clients. Please input the **option** you would like to use:\n"
			index = 1
			for email in email_list:
				split_email = email.split("@")
				first_part = split_email[0]
				last_part = split_email[1]
				prefix = first_part[0]
				postfix = first_part[-1]
				long_string += f"\t {index}. `{prefix}******{postfix}@{last_part}`\n"
				index+=1
			self.loop.run_until_complete(self.interaction.edit_original(content=long_string))
			return
		elif "DUPLICATE" in result:
			if wsid != None: deleteWebhook(wsid, wstoken)
			self.loop.run_until_complete(self.interaction.edit_original(content="This channel already is already hooked up with a SPPD team."))
			return
		elif "VERIFIED" in result:
			if wsid != None: deleteWebhook(wsid, wstoken)
			self.loop.run_until_complete(self.interaction.edit_original(content="That team is already bound to a channel."))
			return
		elif "PENDING" in result:
			if wsid != None: deleteWebhook(wsid, wstoken)
			self.loop.run_until_complete(self.interaction.edit_original(content="That team is pending verification to a channel"))
			return
		if wsid != None: deleteWebhook(wsid, wstoken)
		self.loop.run_until_complete(self.interaction.edit_original(content="Oops. There was a bug. Contact the developer ASAP!"))
		return
		
def postMessageToWebhook(wsid, wstoken, content):
	webhook_url = f"https://discord.com/api/webhooks/{wsid}/{wstoken}"
	json = {"content": content}
	r = requests.post(webhook_url, json=json)
	
def check_deep(interaction):
	deep_refresh = None
	deep_request = False
	if "deep" in interaction.options:
		deep_request = interaction.options["deep"]
	wait_time = 0
	
	orig_author = interaction.author
	if deep_request:
		if orig_author not in author_tracker:
			author_tracker[orig_author]=0
		timeleft = author_tracker[orig_author]
		if timeleft < int(time.time()):
			deep_refresh = orig_author
		else:
			wait_time = timeleft - int(time.time())
	return deep_refresh, wait_time

def card_command(interaction):
	card_name = interaction.options.get("name").lower()
	level = interaction.options.get("level")
	upgrades = interaction.options.get("upgrades")
	max_upgrades = interaction.options.get("max")
	if card_name == None:
		return interaction.respond(content="How did you manage to not include a card name?!?")
	level_upgrade = None
	if upgrades != None:
		level_upgrade = f"u{upgrades}"
	elif level != None and max_upgrades:
		level_upgrade = f"m{level}"
	elif level != None:
		level_upgrade = f"l{level}"
	if level_upgrade == None:
		level_upgrade = "1l"
		
	db = DEEPBOT(interaction, "card", card_name, level_upgrade)
	db.start()
	request_tracker["cards"] += 1
	count = request_tracker["cards"]
	print(f"cards {count}")
	return interaction.ack()
	
def art_command(interaction):
	card_name = interaction.options.get("name").lower()
	card_id, _, _, _, _, _ = HELPER_DB.getCardIDFromName(card_name)
	if card_id == None:
		return interaction.respond(content="Try typing the card name as it appears in-game...")
		
	response, success, path_to_file = HELPER_DB.getCardArt(card_id)
	filename = os.path.basename(path_to_file)
	embed = None
	if filename != None:
		embed = {
			"type": "rich",
			"color": 65535,
			"image":{
				"url": f"https://sppdreplay.net/static/cards/{filename}"
			}
		}
	request_tracker["art"] += 1
	count = request_tracker["art"]
	print(f"art {count}")
	return interaction.respond(content=response,embed=embed)
	
def search_command(interaction):
	#is_player = interaction.options.get("type") == "player"
	is_team = interaction.options.get("type") == "team"
	is_card = interaction.options.get("type") == "card"
	NAME = interaction.options.get("name").lower()
	response, success = HELPER_DB.getSearchResponse(NAME,is_team,is_card)
	request_tracker["search"] += 1
	count = request_tracker["search"]
	print(f"search {count}")
	return interaction.respond(content=response)
	
def calc_command(interaction):
	rarity = interaction.options.get("rarity")
	from_level = interaction.options.get("from")
	to_level = interaction.options.get("to")
	response, success = HELPER_DB.getCalcResponse(rarity, from_level, to_level)
	request_tracker["calc"] += 1
	count = request_tracker["calc"]
	print(f"calc {count}")
	return interaction.respond(content=response)
	
def compare_command(interaction):
	#find card name or part of card name
	#5 = base 5
	#L5 = base 5
	#m5 = max 5
	#u55 = upgrade 55 (both of them...wtf?)
	#List Health, Attack, DPS, and Special Ability
	#Full Stats: https://sppdreplay.net/cards/2299
	card_name = interaction.options.get("name").lower()
	from_level = interaction.options.get("from")
	to_level = interaction.options.get("to")
	response, success = HELPER_DB.getCompareResponse(card_name,from_level,to_level)
	request_tracker["compare"] += 1
	count = request_tracker["compare"]
	print(f"compare {count}")
	return interaction.respond(content=response)
	
def player_command(interaction):
	deep_refresh, wait_time = check_deep(interaction)
	if wait_time > 0:
		return interaction.respond(content=f"No `--deep` for you... Need to wait {wait_time} seconds...")
	player_name = interaction.options.get("name").lower()	
	
	db = DEEPBOT(interaction, "player", player_name, deep_refresh)
	db.start()
	
	request_tracker["player"] += 1
	count = request_tracker["player"]
	print(f"player {count}")
	return interaction.ack()
	
def team_command(interaction):
	deep_refresh, wait_time = check_deep(interaction)
	if wait_time > 0:
		return interaction.respond(content=f"No `--deep` for you... Need to wait {wait_time} seconds...")
	team_name = interaction.options.get("name").lower()	
	
	db = DEEPBOT(interaction, "team", team_name, deep_refresh)
	db.start()

	request_tracker["team"] += 1
	count = request_tracker["team"]
	print(f"team {count}")
	return interaction.ack()

# Post Bracket Subscriptions
def post_bracket(wsid, wstoken, teamname):
	response, success = HELPER_DB.getBracketResponseSubscribed(teamname)
	request_tracker["subscribe"] += 1
	count = request_tracker["subscribe"]
	print(f"subscribe {count}")
	try:
		postMessageToWebhook(wsid, wstoken, response)
	except:
		print("ERROR post_bracket")
		
def bracket_subscribe_loop():
	global last_updated
	while True:
		#print(f"Checking Brackets {last_updated}")
		#Every 10 seconds, check if the bracket is updated.
		#Assuming it is the weekend.
		teamnames_webhook, last_updated = HELPER_DB.check_bracket_subscribe(last_updated)
		if len(teamnames_webhook) != 0:
			for teamname, wsid, wstoken in teamnames_webhook:
				post_bracket(wsid, wstoken, teamname)
		time.sleep(BRACKET_SUBSCRIPTION_SLEEP)
	
def getGuildFromChannel(channel):
	url = f"https://discord.com/api/channels/{channel}"
	guild = None
	headers = {"Authorization": f"Bot {SECRET_KEY}"}
	r = requests.get(url, headers=headers)
	if r.status_code == 200:
		result = r.json()
		if "guild_id" in result:
			guild = result["guild_id"]
	return guild
	
def createWebhook(webhook_name, channel):
	webhook_url = f"https://discord.com/api/channels/{channel}/webhooks"
	wsid = None
	wstoken = None
	json = {"name": webhook_name}
	headers = {"Authorization": f"Bot {SECRET_KEY}"}
	r = requests.post(webhook_url, headers=headers, json=json)
	if r.status_code == 200:
		result = r.json()
		wsid = result["id"]
		wstoken = result["token"]
	return wsid, wstoken
	
def deleteWebhook(wsid, wstoken):
	webhook_url = f"https://discord.com/api/webhooks/{wsid}/{wstoken}"
	r = requests.delete(webhook_url)
	return r.status_code == 204

def subscribe_channel(teamname, channel, wsid, wstoken):
	response = RESTFUL.uploadDouglasSubscriptions(teamname,channel,wsid,wstoken)
	print(f'subscribe_channel {teamname},{channel}',{response})
	return True

def unsubscribe_channel(teamname, channel):
	response = RESTFUL.uploadDouglasSubscriptions(teamname,channel,delete=True)
	print(f'unsubscribe_channel {teamname},{channel}',{response})
	return True
	
def bracket_command(interaction):
	db = DEEPBOT(interaction, "bracket")
	db.start()
	request_tracker["bracket"] += 1
	count = request_tracker["bracket"]
	print(f"bracket {count}")
	return interaction.ack()
	
def update_events_command(interaction):
	db = DEEPBOT(interaction, "update_events")
	db.start()
	return interaction.ack()
	
def create_guild_command(DSERVER, DWORD, author_name):
	url = f"https://discord.com/api/v8/applications/{APP_ID}/guilds/{DSERVER}/commands"
	json = {
		"name": f"{DWORD}",
		"type": 1,
		"description": f"Custom Bind, Created by {author_name}",
	}
	# For authorization, you can use either your bot token
	headers = {"Authorization": f"Bot {SECRET_KEY}"}
	r = requests.post(url, headers=headers, json=json)
	# Extract the Discord Command ID
	result = r.json()
	command_id = None
	if "id" in result:
		command_id = result["id"]
	return command_id
	
def bind_command(interaction):
	WORD = interaction.options.get("word")
	if " " in WORD:
		return interaction.respond(content=f"You can't have spaces in a slash command. `/{WORD}` can't be created.")
	CONTENT = interaction.options.get("content")
	# content can be <text>, or <url>
	text_result, file_result = HELPER_DB.getBind(interaction.guild,WORD)
	success = (len(text_result) == 0) and (len(file_result) == 0)
	if not success:
		return interaction.respond(content=f"`{WORD}` already had a bind.")
		
	if validators.url(CONTENT):
		#continue with file approach
		'''
		a = urllib.parse.urlparse(CONTENT)
		filename = os.path.basename(a.path)
		try:
			r = requests.get(CONTENT, timeout=10)
			with open(filename, 'wb') as f:
				f.write(r.content)
		except Exception as e:
			print(str(e))
			success = False
		finally:
			try: os.remove(filename)
			except: pass
		if not success:
			return interaction.respond(content="Oops. Either the file doesn't exist or it was too large...")
		'''
		if success:
			command_id = create_guild_command(interaction.guild, WORD, interaction.author_name)
			success = RESTFUL.bindWord(interaction.guild,WORD,"FILE",CONTENT,f"{interaction.author}", command_id)
		else:
			return interaction.respond(content=f"Failed to create bind for `{WORD}`")
		if success:
			request_tracker["bind"] += 1
			count = request_tracker["bind"]
			print(f"bind file {count}")
			return interaction.respond(content=f"Success. Added `{WORD}`")
		return interaction.respond(content="How did you mess that up? `/help`")
		
	#continue with text approach
	command_id = create_guild_command(interaction.guild, WORD, interaction.author_name)
	success = RESTFUL.bindWord(interaction.guild,WORD,"TEXT",CONTENT,f"{interaction.author}", command_id)
	if success:
		request_tracker["bind"] += 1
		count = request_tracker["bind"]
		print(f"bind text {count}")
		return interaction.respond(content=f"Success. Added `{WORD}`")
	return interaction.respond(content="How did you mess that up? `/help`")
	
def delete_guild_command(DSERVER, DISCORDID):
	url = f"https://discord.com/api/v8/applications/{APP_ID}/guilds/{DSERVER}/commands/{DISCORDID}"
	headers = {"Authorization": f"Bot {SECRET_KEY}"}
	r = requests.delete(url, headers=headers)
	return r.status_code == 204
	
def unbind_command(interaction):
	WORD = interaction.options.get("word")
	bindID = HELPER_DB.getBindID(interaction.guild,WORD)
	if bindID != None:
		deleted = delete_guild_command(interaction.guild, bindID)
		if not deleted:
			return interaction.respond(content="There was a problem removing your custom command from your server.")
	success = RESTFUL.unbindWord(interaction.guild,WORD)
	if success:
		return interaction.respond(content=f"Success. Removed `{WORD}`")
	return interaction.respond(content="How did you mess that up? `/help`")
	
def bind_list_command(interaction):
	#List all binds for that server.
	DWORD_LIST = HELPER_DB.getAllBinds(interaction.guild)
	if len(DWORD_LIST) == 0:
		return interaction.respond(content="Your server has no binds.")
	DWORD_LIST = sorted(DWORD_LIST)
	long_string = f"Your server has {len(DWORD_LIST)} binds:\n" + '\n'.join(x for x in DWORD_LIST)
	return interaction.respond(content=long_string)
		
def custom_guild_command(interaction, result, TYPE):
	content = None
	embed = None
	if TYPE == "FILE":
		embed = {
			"type": "rich",
			"color": 65535,
			"image":{
				"url": f"{result}"
			}
		}
		return interaction.respond(embed=embed)
	#TYPE == "TEXT":
	#content=result
	# Check if the content is a command - if so, try to execute it.
	#/bracket name: asdf asdf subscribe: asdf
	if not result.startswith("/"):
		return interaction.respond(content=result)
	split_result = result.split(" ")
	# len must be >0 because it starts with "/"
	#if len(split_result) < 0: return interaction.respond(content="...")
	interaction.command_name = split_result[0].strip("/")
	#options must be {} because custom guild commands have no options.
	#interaction.options = {}
	last_option = ""
	for word in split_result[1:]:
		if word.endswith(":"):
			word = word.strip(":")
			last_option = word
			interaction.options[last_option]=""
			continue
		if last_option == "": continue
		if word.isnumeric():
			word = int(word)
		elif word in ["True", "true", "False", "false"]:
			word = word == "True" or word == "true"
		if interaction.options[last_option] == "":
			interaction.options[last_option] = word
		else:
			interaction.options[last_option] += f" {word}"
		
	if interaction.command_name == "art":
		return art_command(interaction)
	if interaction.command_name == "card":
		return card_command(interaction)
	if interaction.command_name == "player":
		return player_command(interaction)
	if interaction.command_name == "team":
		return team_command(interaction)
	if interaction.command_name == "bracket":
		return bracket_command(interaction)
	if interaction.command_name == "update_events":
		return update_events_command(interaction)
	if interaction.command_name == "bind_list":
		return bind_list_command(interaction)
	if interaction.command_name == "import_binds":
		return import_binds_command(interaction)
	if interaction.command_name == "search":
		return search_command(interaction)
	if interaction.command_name == "calc":
		return calc_command(interaction)
	if interaction.command_name == "compare":
		return compare_command(interaction)
	if interaction.command_name == "chat":
		return chat_command(interaction)
	if interaction.command_name == "help":
		return help_command(interaction)
	if interaction.command_name == "status":
		return status_command(interaction)
	
	return interaction.respond(content=result)

def import_binds_command(interaction):
	db = DEEPBOT(interaction, "import_binds")
	db.start()
	return interaction.ack()

#-chat subscribe F2P Whales
#-chat unsubscribe
def subscribe_chat(teamid, channel_id, wsid = None, wstoken = None, email = None, delete = False):
	response = RESTFUL.uploadChatSupport(teamid,channel_id,wsid,wstoken,email,delete)
	print(f'subscribe_chat {teamid},{channel_id}',{response})
	return response
	
def subscribe_chat_tvt(channel_id, tvt_channel_id = None, wsid = None, wstoken = None, delete = False):
	response = RESTFUL.uploadChatSupportTVT(channel_id,tvt_channel_id,wsid,wstoken,delete)
	print(f'subscribe_chat_tvt {channel_id},{tvt_channel_id}',{response})
	return response
	
def confirm_chat(channel_id, enable = False):
	response = RESTFUL.uploadChatSupportConf(channel_id,enable)
	print(f'confirm_chat {channel_id}',{response})
	return response
	
def chat_command(interaction):
	db = DEEPBOT(interaction, "chat")
	db.start()
	return interaction.ack()

def help_command(interaction):
	COMMAND = interaction.options.get("command")
	long_response = "Hello, I'm your Douglas v3 Bot.\n"
	if COMMAND == None:
		long_response += "Here are the available commands.\n"
		long_response += "\t* `/help [command: <command>]`\n"
		long_response += "\t* `/art name: <card>`\n"
		long_response += "\t* `/bind word: <one word> content: (url | text)`\n"
		long_response += "\t* `/bind_list`\n"
		long_response += "\t* `/bracket name: <name> [subscribe: (subscribe|unsubscribe)]`\n"
		long_response += "\t* `/calc rarity: (C|R|E|L) from: <level|upgrade> to: <level|upgrade>`\n"
		long_response += "\t* `/card name: <card> [level: <number>] [upgrades: <number>] [max: (true|false)]`\n"
		long_response += "\t* `/chat command: <command> [name: <name>] [option: <number>]`\n"
		long_response += "\t* `/compare name: <name> from: <level|upgrade> to: <level|upgrade>`\n"
		long_response += "\t* `/import_binds`\n"
		long_response += "\t* `/player name: <player> [deep: (true|false)]`\n"
		long_response += "\t* `/search name: <name> [type: (player|team|card)]`\n"
		long_response += "\t* `/team name: <team> [deep: (true|false)]`\n"
		long_response += "\t* `/unbind word: <word>`\n"
		long_response += "Note: [] = optional, () = choices, <> = user input\n"
		long_response += "Lastly, a friendly reminder that we run off community donations.\n"
	elif COMMAND == "art":
		long_response += "Get card art\n"
		long_response += "`/art name: <card>`\n"
		long_response += "\t* `<card>` can be an abbreviation or acryonym\n"
		long_response += "\t* Example: **Shield** or **SMW** instead of **Shieldmaiden Wendy**\n"
	elif COMMAND == "bind":
		long_response += "Bind a command on your server to show text or picture.\n"
		long_response += "`/bind word: <one word> content: (url | text)`\n"
		long_response += "\t* `<one word>` should not contain any spaces\n"
		long_response += "\t* `(url | text)` if it is a URL, the URL will be embedded\n"
		long_response += "Note: You are limited to 100 server binds per day, per Discord's API\n"
	elif COMMAND == "bind_list":
		long_response += "List the binds available on your server.\n"
		long_response += "`/bind_list`\n"
	elif COMMAND == "bracket":
		long_response += "List the TVT bracket details available on SPPD Replay\n"
		long_response += "Data is provided by the SPPD Team Manager Client.\n"
		long_response += " Or subscribe to be updated as the data becomes available.\n"
		long_response += "`/bracket name: <name> [subscribe: (subscribe|unsubscribe)] [webhook: <name of the webhook bot>]`\n"
		long_response += "\t* If you subscribe to a specific team on a bracket, you will only get notifications when that team completes a run.\n"
		long_response += "\t* - If the target team has special characters in the name, you may need the `webhook` option.\n"
	elif COMMAND == "calc":
		long_response += "Calculate the materials required to go from one rarity's level/upgrade to another.\n"
		long_response += "`/calc rarity: (C|R|E|L) from: <level|upgrade> to: <level|upgrade>`\n"
		long_response += "\t* `<rarity>` can be Common, Rare, Epic, Legendary\n"
		long_response += "\t* `<level|upgrade>` can be m3 for max level 3, u55 for upgrade 55, or just 1 for base level 1.\n"
	elif COMMAND == "card":
		long_response += "List a specific cards details details\n"
		long_response += "`/card name: <card> [level: <number>] [upgrades: <number>] [max: (true|false)]`\n"
		long_response += "\t* `<card>` can be an abbreviation or acryonym\n"
		long_response += "\t\t* Example: **Shield** or **SMW** instead of **Shieldmaiden Wendy**\n"
		long_response += "\t* You should specify level or upgrades, not both."
		long_response += "\t* `<level>` can be 1 to 7 (or SPPD Replay ID for new kid)\n"
		long_response += "\t* `<upgrades>` can be 1 to 70\n"
		long_response += "\t* `<max>` can be true or false\n"
		long_response += "\t\t* This will show you the max upgrades for a certain level (max 3 or base 3)\n"
	elif COMMAND == "chat":
		long_response += "Integrated Discord <-> SPPD Chat\n"
		long_response += "Synchronized a Discord Channel and SPPD Team Chat.\n"
		long_response += "Douglas creates a new chat bot dynamically via webhook.\n"
		long_response += "`/chat command: <command> [name: <name>] [option: <number>] [webhook: <name of the webhook bot>]`\n"
		long_response += "\t* `<command>` can be subscribe, unsubscribe, confirm, status\n"
		long_response += "\t* `command: subscribe` requires the `name` option\n"
		long_response += "\t* - If your team has special characters in the name, you may need the `webhook` option.\n"
		long_response += "\t* `command: unsubscribe` does not require the `name` option. Unsubscribes based on the channel.\n"
		long_response += "\t* `command: confirm` to enable (`option: 0`) or disable (`option: 1`) confirmation messages that a message made it from discord to in-game.\n"
		long_response += "\t* `command: status` List the status of the Chat Bot on this channel\n"
	elif COMMAND == "compare":
		long_response += "Compare a specific card's details between levels\n"
		long_response += "`/compare name: <name> from: <level|upgrade> to: <level|upgrade>`\n"
		long_response += "\t* `<card>` can be an abbreviation or acryonym\n"
		long_response += "\t\t* Example: **Shield** or **SMW** instead of **Shieldmaiden Wendy**\n"
		long_response += "\t* `<level|upgrade>` can be m3 for max level 3, u55 for upgrade 55, or just 1 for base level 1.\n"
	elif COMMAND == "import_binds":
		long_response += "Import your binds from old Douglas to new Douglas\n"
		long_response += "`/import_binds`\n"
		long_response += "Note: You are limited to 100 server binds per day, per Discord's API\n"
		long_response += "\t - So you may need to run it again each day to transition the remainder over.\n"
	elif COMMAND == "player":
		long_response += "List a specific player's details.\n"
		long_response += "`/player name: <player> [deep: (true|false)]`\n"
		long_response += "\t* `<name>` the full name of the player\n"
		long_response += "\t* `deep` will query SPPD servers for the latest information\n"
	elif COMMAND == "search":
		long_response += "Search for players, teams, or cards by tags\n"
		long_response += "`/search name: <name> [type: (player|team|card)]`\n"
		long_response += "\tDefault type: player\n"
		long_response += "\t* `<name>` the full name of the player, team, or one or more card tags\n"
		long_response += "\t* `<type>` can be player, team, card\n"
	elif COMMAND == "team":
		long_response += "List a specific team's details.\n"
		long_response += "`/team name: <team> [deep: (true|false)]`\n"
		long_response += "\t* `<name>` the full name of the team\n"
		long_response += "\t* `deep` will query SPPD servers for the latest information\n"
	elif COMMAND == "unbind":
		long_response += "Unbind a command\n"
		long_response += "`/unbind word: <word>`\n"
	elif COMMAND == "help":
		long_response += "Help command\n"
		long_response += "`/help command: <command>`\n"
		long_response += "Congratulations. You already know how to use `/help`\n"
		long_response += "Commands are:\n - art\n - bind\n - bind_list\n - bracket\n - calc\n - card\n - chat\n - compare\n - import_binds\n - player\n - search\n - team\n - unbind\n - help\n"
	return interaction.respond(content=long_response)
	
def status_command(interaction):
	num = getMyStatus()
	long_response = f'{num}'
	return interaction.respond(content=long_response)

@server.route('/', methods=['POST'])
def slash_commands():
	# Security Check
	verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))
	signature = request.headers["X-Signature-Ed25519"]
	timestamp = request.headers["X-Signature-Timestamp"]
	body = request.data.decode("utf-8")
	try:
		verify_key.verify(f'{timestamp}{body}'.encode(), bytes.fromhex(signature))
	except BadSignatureError:
		abort(401, 'invalid request signature')

	# Interaction Type
	# PING - Type = 1
	if request.json["type"] == 1:
		return jsonify({
			"type": 1
		})
	
	# APPLICATION_COMMAND - Type = 2
	if request.json["type"] == 2:
		if "guild_id" not in request.json:
			return jsonify({
				"type": 4,
				"data": {
					"tts": False,
					"content": "Not supported, but if there's enough demand, I can try to do it.",
					"embeds": [],
					"allowed_mentions": { "parse": [] }
				}
			})
		interaction = Interaction(request.json)
		
		#Check if it's a guild command first, so we don't mistaken pick our global commands
		result, TYPE = HELPER_DB.getBindByCommandID(interaction.guild, interaction.command_id)
		if result != None:
			return custom_guild_command(interaction, result, TYPE)
			
		if interaction.command_name == "art":
			return art_command(interaction)
		if interaction.command_name == "card":
			return card_command(interaction)
		if interaction.command_name == "player":
			return player_command(interaction)
		if interaction.command_name == "team":
			return team_command(interaction)
		if interaction.command_name == "bracket":
			return bracket_command(interaction)
		if interaction.command_name == "bind":
			return bind_command(interaction)
		if interaction.command_name == "bind_list":
			return bind_list_command(interaction)
		if interaction.command_name == "unbind":
			return unbind_command(interaction)
		if interaction.command_name == "import_binds":
			return import_binds_command(interaction)
		if interaction.command_name == "update_events":
			return update_events_command(interaction)
		if interaction.command_name == "search":
			return search_command(interaction)
		if interaction.command_name == "calc":
			return calc_command(interaction)
		if interaction.command_name == "compare":
			return compare_command(interaction)
		if interaction.command_name == "chat":
			return chat_command(interaction)
		if interaction.command_name == "help":
			return help_command(interaction)
		
		return jsonify({
			"type": 4,
			"data": {
				"tts": False,
				"content": "Work in progress...",
				"embeds": [],
				"allowed_mentions": { "parse": [] }
			}
		})
	# MESSAGE COMPONENT - Type = 3
	if request.json["type"] == 3:
		print(f"WHAT IS THIS?!?!? {requests.json}")
		return jsonify({
				"type": 4,
				"data": {
					"tts": False,
					"content": "[ERROR] Please tell me how you generated this error message...",
					"embeds": [],
					"allowed_mentions": { "parse": [] }
				}
			})

class SPPDDOUGLAS():

	def main(self):
		
		#Dash only
		#app.run_server(port=8000,host='0.0.0.0',debug=False)
		#Flask -> Dash
		#server.run(port=8000,host='0.0.0.0',debug=False)
		#Waitress -> Flask -> Dash
		#serve(server, host='0.0.0.0', port=8000, threads=6)
		
		#CherryPy -> Flask -> Dash
		# Mount the application
		global server
		cherrypy.tree.graft(server, "/")

		# Unsubscribe the default server
		cherrypy.server.unsubscribe()
		
		# Instantiate a new server object
		cserver = cherrypy._cpserver.Server()

		# Configure the server object
		cserver.socket_host = "0.0.0.0"
		cserver.socket_port = 5004
		cserver.thread_pool = 2
		cherrypy.config.update({'engine.autoreload.on': False,
							'tools.sessions.timeout': 10,
							'log.access_file': './access.log',
							'log.error_file': './error.log'})

		# For SSL Support
		# server.ssl_module            = 'pyopenssl'
		cserver.ssl_certificate       = 'domain.cert.pem'
		cserver.ssl_private_key       = 'private.key.pem'
		# server.ssl_certificate_chain = 'ssl/bundle.crt'

		# Subscribe this server
		cserver.subscribe()

		# Start the server engine (Option 1 *and* 2)
		cherrypy.engine.start()
		#cherrypy.engine.block()
		
		#After updating libraries, expect plenty of `dash.exceptions.DependencyException`
		#	due to caching, and people not refreshing their page.

if __name__ == '__main__':
	print("Starting Bracket Subscriptions...")
	bracket_subscriptions = THREADBOT(bracket_subscribe_loop)
	bracket_subscriptions.start()
	douglas_server = SPPDDOUGLAS()
	douglas_server.main()