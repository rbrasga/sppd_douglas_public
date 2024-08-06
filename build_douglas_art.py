from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageChops
import base64
import textwrap
import DATABASE
import sys
import codecs
codecs.register_error("strict", codecs.ignore_errors)
import LOCALIZATION

import os,time
import random
import NK_ART
	
def findImage2(name,USERID=None):
	path = r'C:\Users\Remin\Documents\GitHub\sppd-data\bundledassets\cards'
	default_file = os.path.join(path, 'PlaceholderCard.png')
	if name == "NewKid":
		filepath, name = NK_ART.build_douglas_new_kid(USERID)
		if filepath == None:
			return default_file, None
		else:
			return filepath, name
	tmp_name = f'{name}.png'
	for root, dirs, files in os.walk(path):
		if tmp_name in files:
			return os.path.join(root, tmp_name), None
	print(f'[WARNING] {tmp_name} image - not found!')
	return default_file, None

def getFontSizeOffset(txt_string, xoffset, yoffset, maxfontsize=24, isDescription=False, lang_index=0):
	font_path = '/Users/Remin/Documents/GitHub/sppd-data/card_bases/south_park.ttf'
	font = ImageFont.truetype(font_path, maxfontsize)
	font_length = font.getsize(txt_string)
	while (font_length[0] > xoffset or font_length[1] > yoffset) and maxfontsize > 2:
		# iterate until the text size is just larger than the criteria
		maxfontsize -= 1
		font = ImageFont.truetype(font_path, maxfontsize)	
		font_length = font.getsize(txt_string)
	
	x = (font_length[0] + (xoffset - font_length[0]))/2 - font_length[0]/2
	y = (font_length[1] + (yoffset - font_length[1]))/2 - font_length[1]/2
	#if lang_index != 0: y -= 20
	offset = x,y #X,Y coordinates
	return font, offset
	
def builder_dropdown(theme, rarity, card_type, level, cost, health, attack, card_art, n_clicks, name, description, filename=None, lang_index=0):
	if n_clicks == None: return ""
	#Stich the image together
	c_image = None
	#0. Pick the card base
	theme_lower = theme.lower().replace('-','')
	rarity_lower = rarity.lower()
	type_lower = card_type.lower()
	pixelMap = Image.open(f'/Users/Remin/Documents/GitHub/sppd-data/card_bases/{theme}/{theme_lower}_{rarity_lower}_{type_lower}.png')
	W,H = pixelMap.size
	#1. Start with the card art (lowest layer)
	if card_art != None:
		try:
			index = card_art.find("base64,")+7
			card_art = card_art[index:]
			image = BytesIO(base64.b64decode(card_art))
			c_image = Image.open(image)
			w2,h2,w2offset,h2offset=67,166,569,796
			if c_image.mode != "RGBA": c_image = c_image.convert('RGBA')
			x,y = c_image.size
			multiplier = 1
			if float(w2offset)/x > float(h2offset)/y: #X is the smaller ratio
				multiplier = float(w2offset)/x
			else: #Y is the smaller ratio
				multiplier = float(h2offset)/y
			c_image = c_image.resize((round(c_image.size[0]*multiplier+1), round(c_image.size[1]*multiplier+1)))
			#Center the cardart
			x,y = 0,0
			if c_image.size[0] > w2offset+10:
				x = c_image.size[0]/2 - w2offset/2
			elif c_image.size[1] > h2offset+10:
				y = c_image.size[1]/2 - h2offset/2
			c_image = c_image.crop(box=(x,y,w2offset+x,h2offset+y))
			full_res = Image.new(pixelMap.mode, pixelMap.size)
			full_res.paste(c_image,box=(w2,h2))
			c_image = full_res
		except:
			return "Invalid Image. Please try a different file."
			
	#2. Then pick the overlay based on Theme/Rarity/Type
	core_image = None
	weight = 0.80 # percent
	if c_image == None:
		core_image = pixelMap
	else:
		#c_image = Image.new(pixelMap.mode, pixelMap.size)
		pixelsNew = c_image.load()
		for i in range(c_image.size[0]):
			for j in range(c_image.size[1]):
				r,g,b,a = pixelMap.getpixel((i,j))
				if a == 0 or a == 255:
					pixelsNew[i,j] = (0,0,0,0)
		#core_image = c_image
		core_image = Image.alpha_composite(c_image, pixelMap)
	#3. Then add the attributes Level/Cost/Health/Attack/Name
	draw_text_list = [] # [ [xoffset,yoffset,string,font,border], ... ]
	#NAME
	x,y,xoffset,yoffset = DATABASE.CARD_BUILDER["NAME"]
	font,offset = getFontSizeOffset(name,xoffset*2,yoffset*2,35,lang_index=lang_index)
	draw_text_list.append([x-xoffset+offset[0],y-yoffset+offset[1],name,font,2])
	#LEVEL
	x,y,xoffset,yoffset = DATABASE.CARD_BUILDER["LEVEL"]
	if 'L' not in level: level = f"LVL {level}"
	font,offset = getFontSizeOffset(level,xoffset*2,yoffset*2,22)
	draw_text_list.append([x-xoffset+offset[0],y-yoffset+offset[1],level,font,1])
	if card_type not in ["Spell", "Trap"]:
		if health != "":
			#HEALTH
			x,y,xoffset,yoffset = DATABASE.CARD_BUILDER["HEALTH"]
			font,offset = getFontSizeOffset(health,xoffset*2,yoffset*2,39)
			draw_text_list.append([x-xoffset+offset[0],y-yoffset+offset[1],health,font,2])
		if attack != "":
			#ATTACK
			x,y,xoffset,yoffset = DATABASE.CARD_BUILDER["ATTACK"]
			font,offset = getFontSizeOffset(attack,xoffset*2,yoffset*2,39)
			draw_text_list.append([x-xoffset+offset[0],y-yoffset+offset[1],attack,font,2])
	#COST
	x,y,xoffset,yoffset = DATABASE.CARD_BUILDER["COST"]
	font,offset = getFontSizeOffset(str(cost),xoffset*2,yoffset*2,90)
	draw_text_list.append([x-xoffset+offset[0],y-yoffset+offset[1],str(cost),font,6])
	
	#DESCRIPTION
	x,y,xoffset,yoffset = DATABASE.CARD_BUILDER["DESC"]
	pad=28
	para = textwrap.wrap(description, width=30)
	para_len = len(para)
	text_yoffset=y-pad/2
	if para_len % 2 == 0:
		text_yoffset = text_yoffset - pad/2
		text_yoffset += 7 # To adjust for pad height on even lines.
		para_len -= 1
	text_yoffset = text_yoffset - pad * (para_len-1) / 2
	current_h = text_yoffset
	for line in para:
		font,offset = getFontSizeOffset(line,xoffset*2,yoffset*2,24,lang_index=lang_index)
		draw_text_list.append([x-xoffset+offset[0],current_h,line,font,1])
		current_h += pad
	outline="black"
	draw = ImageDraw.Draw(core_image)
	for x,y,string,font,border in draw_text_list:
		for i in range(1,border+1):
			if i == 1 or i < border/2:
				draw.text((x, y-i), string, font=font, fill=outline)
				draw.text((x-i, y), string, font=font, fill=outline)
				draw.text((x+i, y), string, font=font, fill=outline)
			draw.text((x, y+i), string, font=font, fill=outline)
		draw.text((x,y), string, font=font, fill = 'rgb(230,226,197)')
	
	#core_image.save('test.png')
	core_image.save(filename)
	#core_image.show()

	#tmp_file = BytesIO()
	#core_image.save(tmp_file,"PNG")
	#encoded_image = base64.b64encode(tmp_file.getvalue())
	#return html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode('utf-8')))
	
def getTheme(theme):
	THEMES = ["Adventure","Fantasy","Mystical","Neutral","Sci-fi","Superheroes"]
	if theme == 'Adv': return THEMES[0]
	if theme == 'Fan': return THEMES[1]
	if theme == 'Mys': return THEMES[2]
	if theme == 'Gen': return THEMES[3]
	if theme == 'Sci': return THEMES[4]
	if theme == 'Sup': return THEMES[5]
	print(f"ERROR - Theme {theme}")
	
def getRarity(rarity):
	RARITY = ["Common","Rare","Epic","Legendary"]
	if rarity == 0: return RARITY[0]
	if rarity == 1: return RARITY[1]
	if rarity == 2: return RARITY[2]
	if rarity == 3: return RARITY[3]
	print(f"ERROR - Rarity {rarity}")
	
def getType(ctype):
	CTYPE = ["Assassin","Fighter","Ranged","Spell","Tank","Totem","Trap"]
	if ctype == 'Assassin': return CTYPE[0]
	if ctype == 'Melee': return CTYPE[1]
	if ctype == 'Ranged': return CTYPE[2]
	if ctype == 'Spell': return CTYPE[3]
	if ctype == 'Tank': return CTYPE[4]
	if ctype == 'Totem': return CTYPE[5]
	if ctype == 'Trap': return CTYPE[6]
	print(f"ERROR - Type {ctype}")
	
def findDescription(card_id):
	if card_id not in LOCALIZATION.ASSET:
		print(f'Error, unable to find asset for {card_id}')
		return ["Unknown" for i in range(7)], ["Unknown" for i in range(7)]
		#sys.exit()
	asset_substr = LOCALIZATION.ASSET[card_id]
	asset_name_key = None
	asset_desc_key = None
	if type(asset_substr) == list:	
		asset_name_key = asset_substr[0]
		asset_desc_key = asset_substr[1]
	else:
		asset_name_key = asset_substr
		asset_desc_key = asset_substr
	
	asset_desc = f'DF_DESC_{asset_desc_key}'
	asset_name = f'DF_NAME_{asset_name_key}'
	override_name = None
	override_desc = None
	if asset_desc not in LOCALIZATION.LOCAL:
		print(f'Error, unable to find asset for {asset_desc_key}')
		override_desc = ["" for i in range(7)]
		#sys.exit()
	if asset_name not in LOCALIZATION.LOCAL:
		print(f'Error, unable to find asset for {asset_name_key}')
		override_name = [asset_name for i in range(7)]
		#sys.exit()
	if override_name == None:
		override_name = LOCALIZATION.LOCAL[asset_name]
	if override_desc == None:
		override_desc = LOCALIZATION.LOCAL[asset_desc]
	return override_name, override_desc

def build_card_art(card_id, art_filename, card_name, card_details, static_details, lang_index = 0, BOSS=False, skip_cache=False, USERID=None):
	#if card_id not in DATABASE.DECK_MAP: return None
	if card_name == 'Unknown': return None
	COST = static_details[0]
	CTYPE = static_details[1]
	if CTYPE == "Character": CTYPE = getType(static_details[2])
	else: CTYPE = getType(static_details[1])
	THEME = getTheme(static_details[3])
	RARITY = getRarity(static_details[4])
	card_art = None
	NAME = None
	is_new_kid = art_filename == "NewKid"
	if is_new_kid:
		image_data,tmp_name = findImage2(art_filename,USERID)
		if tmp_name != None: NAME = tmp_name
		card_art = 'data:image/png;base64,' + image_data.decode('utf8')
	else:
		image_filename,_ = findImage2(art_filename)
		if image_filename == None: return None
		card_art = 'data:image/png;base64,' + base64.b64encode(open(image_filename, 'rb').read()).decode('utf8')
	#Get the dynamic card stats from the database
	LANG_NAMES,LANG_DESCRIPTIONS=findDescription(card_id)
	if card_details == None: return None
	if NAME == None:
		NAME = LANG_NAMES[lang_index].upper()
	DESCRIPTION = LANG_DESCRIPTIONS[lang_index]
	LEVEL,UPGRADE,HEALTH,ATTACK,SPECIAL1,STYPE1,SPECIAL2,STYPE2,SPECIAL3,STYPE3 = card_details
	LEVEL_DISPLAY=LEVEL
	if SPECIAL1 != None and SPECIAL1 % 1 == 0: SPECIAL1 = int(SPECIAL1)
	if SPECIAL2 != None and SPECIAL2 % 1 == 0: SPECIAL2 = int(SPECIAL2)
	if SPECIAL3 != None and SPECIAL3 % 1 == 0: SPECIAL3 = int(SPECIAL3)
	if CTYPE == 'Spell' or CTYPE == 'Trap':
		LEVEL_DISPLAY = f'LVL {LEVEL}'
		LEVEL = f'L{LEVEL}'
	else:
		LEVEL_DISPLAY = f'L{LEVEL}U{UPGRADE}'
		LEVEL = f'L{LEVEL}U{UPGRADE}'
	filename = f'{card_id}-{lang_index}-{LEVEL}.png'
	filepath = f'/Users/Remin/Documents/GitHub/sppd_sim/static/{filename}'
	if not is_new_kid and os.path.exists(filepath): return filename
	print(f'In Progress: {card_name}')
	HEALTH = f'{HEALTH}'
	ATTACK = f'{ATTACK}'
	tmp_description = DESCRIPTION
	if (STYPE1 == 'EnablePower' and SPECIAL1 == 0) or\
		(STYPE2 == 'EnablePower' and SPECIAL2 == 0) or\
		(STYPE3 == 'EnablePower' and SPECIAL3 == 0):
		tmp_description = 'SPECIAL POWER LOCKED'
	tmp_description = tmp_description.replace('.1}','}')
	tmp_description = tmp_description.replace('.2}','}')
	tmp_description = tmp_description.replace('{PowerMaxHealthBoost}','{PowerMaxHPGain}')
	tmp_description = tmp_description.replace('{PowerInterval.1}','{PowerInterval}')
	tmp_description = tmp_description.replace('{PowerTargetAmount}','{PowerTarget}')
	tmp_description = tmp_description.replace('{PowerMaxHealthDecrease}','{PowerMaxHPLoss}')
	tmp_description = tmp_description.replace('{powerAttackBoost}','{PowerAttackBoost}')
	tmp_description = tmp_description.replace('{powerDuration}','{PowerDuration}')
	tmp_description = tmp_description.replace('{Duration}','{PowerDuration}')
	if card_id == DATABASE.NAME_TO_ID['Marcus'] and '{PowerHeroDamage}' in tmp_description and STYPE1 == 'PowerDamageAbs':
		tmp_description = tmp_description.replace('{PowerHeroDamage}',f'{int(SPECIAL1)}')
	if card_id == DATABASE.NAME_TO_ID['City Wok Guy'] and '{PowerHeroDamage}' in tmp_description and STYPE1 == 'PowerDamageAbs':
		tmp_description = tmp_description.replace('{PowerHeroDamage}',f'{int(SPECIAL1/2)}')
	if '{PowerHeroDamage}' in tmp_description and STYPE1 == 'PowerDamageAbs':
		tmp_description = tmp_description.replace('{PowerHeroDamage}',f'{int(SPECIAL1/10)}')
	if '{PowerHeroPoison}' in tmp_description and STYPE1 == 'PowerPoisonAmountAbs':
		tmp_description = tmp_description.replace('{PowerHeroPoison}',f'{int(SPECIAL1/3)}')
	if '{PowerDurationMin}' in tmp_description and STYPE1 == 'PowerDurationAbs':
		tmp_description = tmp_description.replace('{PowerDurationMin}',f'{SPECIAL1}')
	if '{PowerDurationMax}' in tmp_description and STYPE1 == 'PowerDurationAbs':
		tmp_description = tmp_description.replace('{PowerDurationMax}',f'{SPECIAL1+2}')
	if '{PowerStealAmount}' in tmp_description:
		tmp_description = tmp_description.replace('{PowerStealAmount}',f'{int(HEALTH)/2}')
	if STYPE1 != None:
		STYPE1 = STYPE1.replace('Abs','')
		tmp_description = tmp_description.replace('{%s}' % STYPE1, f'{SPECIAL1}')
	if STYPE2 != None:
		STYPE2 = STYPE2.replace('Abs','')
		tmp_description = tmp_description.replace('{%s}' % STYPE2, f'{SPECIAL2}')
	if STYPE3 != None:
		STYPE3 = STYPE3.replace('Abs','')
		tmp_description = tmp_description.replace('{%s}' % STYPE3, f'{SPECIAL3}')
	if '{' in tmp_description or '}' in tmp_description:
		print(f'ERROR unknown description for {NAME} : {tmp_description}')
		return None
	tmp_description=tmp_description.upper()
	builder_dropdown(THEME, RARITY, CTYPE, LEVEL_DISPLAY, COST, HEALTH, ATTACK, card_art, 1, NAME, tmp_description, filepath, lang_index)
	return filename

if __name__ == '__main__':
	
	card_details = [1,1,200,50,None,None,None,None,None,None]
	static_details = [3,"Character","Ranged","Sci",0]
	lang_index=1
	filename = build_card_art(1805, "BebeSciCard", "Robo Bebe", card_details, static_details, lang_index, False, False, None)
	print(filename)