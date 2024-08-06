from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageChops
import base64
import DATABASE
import os, sys, time
import mysql.connector as mariadb
import random
'''
TO-DO

Modify mask found search to look in the form of an outward spiral for the closest matching color.
xd,yd =  1, 0
xd,yd =  0,-1	until  i == -j
xd,yd = -1, 0	until -i == -j
xd,yd =  0, 1	until -i ==  j
xd,yd =  1, 0	until  i ==  j+1

all while i < delta and j < delta
[
	[1,0],
	[0,-1],
	[-1,0],
	[0,1],
	[1,-1],
	[-1,-1],
	[-1,1],
	[1,1],
	[2,0],
]

add all delta coords to list, then sort by the distance from the center: sqrt(x^2+y^2)
'''

def executeQuery(query, commit=False, debug=False, quiet=False):
	mariadb_connection = mariadb.connect(
							user='root',
							password='password',
							database='decktracker')
	cursor = mariadb_connection.cursor()
	result=None
	try:
		cursor.execute(query)
		if commit: mariadb_connection.commit()
		else:
			result = cursor.fetchall()
			if len(result) == 0: result=None
			elif len(result) == 1: result=result[0]
	except:
		print(f"\n[ERROR] Failed Query: {query}\n")
		traceback.print_exc()
		sys.exit()
	mariadb_connection.close()
	query=query.replace('\t',' ').replace('\n',' ')
	if debug: print(f"executeQuery query {query} -> result {result}")
	elif not quiet: print(f"executeQuery query {query}")
	time.sleep(0.05)
	return result

def find(element,mask=False):
	if element == None: return None
	elem_id = element[0]
	if elem_id == None: return None
	path = r'C:\Users\Remin\Downloads\hero_gear'
	#Find the Name of the file
	name = ''
	if elem_id in DATABASE.OUTFIT_MAP:
		name = DATABASE.OUTFIT_MAP[elem_id]['AssetId']
	if elem_id in DATABASE.GEAR_MAP:
		name = DATABASE.GEAR_MAP[elem_id]['AssetId']
	if mask: name+='_MaskRGB'
	name += '.png'
	for root, dirs, files in os.walk(path):
		if name in files:
			#print(f'\t{name}')
			return os.path.join(root, name)
	print(f'[WARNING] {name} not found!')
	return None
	
'''	
Mask Notes:
* Magenta - Primary Color ( 253,0,253 )
* Light Blue - Secondary Color ( 2,255,255 )
* Dark Blue- Do not change ( 9,0,213 )
* Black - Skin ( 0,0,0 )
* Red - Primary (skin underneith) ( 253,0,0 )
* White - ? ( 255,255,255 )
* Green - Secondary (skin underneath) ( 2,255,2 )

#Draw the skin underneath first, then overlay the outfit on top.

'''
all_masks={
	'magenta':( 253,0,253 ),	#primary
	'lightblue':( 2,255,255 ),	#secondary
	'red':( 253,0,0 ),			#primary | sometimes skin sometimes delete
	'green':( 2,255,2 ),		#secondary | sometimes skin sometimes delete
	'black':( 0,0,0 ),			#delete | 100% skin
	#'blue':( 9,0,213 ),			#ignore
	'blue':( 0,0,253 ),			#ignore
	#'white':( 255,255,255 ),	#unknown
	'softred':( 255,127,127 ),	#wear_front primary
	'softgreen':( 127,255,127 ),#wear_front secondary
	'yellow':( 255,255,2 ),	#random delete
	None:None
}

def ApplyMask(Elem,target_image,mask_image,skin=None):
	result = DATABASE.GEAR_MAP[Elem[0]]
	mask_offset = result['mask_offset']
	primary = [all_masks['magenta']]
	secondary = [all_masks['lightblue'],all_masks['green']]
	tertiary = [all_masks['black'],all_masks['red']]
	ignore = all_masks['blue']
	skin_colors = [all_masks['black'],all_masks['red'],all_masks['green']]
	if 'colors' in result:
		if 'primary' in result['colors']:
			primary = [all_masks[x] for x in result['colors']['primary']]
		if 'secondary' in result['colors']:
			secondary = [all_masks[x] for x in result['colors']['secondary']]
		if 'tertiary' in result['colors']:
			tertiary = [all_masks[x] for x in result['colors']['tertiary']]
		if 'skin' in result['colors']:
			skin_colors = [all_masks[x] for x in result['colors']['skin']]
		if 'ignore' in result['colors']:
			ignore = all_masks[result['colors']['ignore']]
	R,G,B = None,None,None
	if skin != None: R,G,B = int(skin[:2], 16),int(skin[2:4], 16),int(skin[4:], 16)
	
	ALL_MASK_VALUES = all_masks.values()
	
	a1,r1,g1,b1 = None,None,None,None
	a2,r2,g2,b2 = None,None,None,None
	if Elem[1] in DATABASE.COLOR_MAP:
		zcolor1 = DATABASE.COLOR_MAP[Elem[1]]
		a1,r1,g1,b1 = int(zcolor1[:2],16),int(zcolor1[2:4],16),int(zcolor1[4:6],16),int(zcolor1[6:],16)
	else:
		r1,g1,b1,a1=result['colorA']
	if Elem[2] in DATABASE.COLOR_MAP:
		zcolor2 = DATABASE.COLOR_MAP[Elem[2]]
		a2,r2,g2,b2 = int(zcolor2[:2],16),int(zcolor2[2:4],16),int(zcolor2[4:6],16),int(zcolor2[6:],16)
	else:
		r2,g2,b2,a2=result['colorB']
	
	#crop the mask
	mask_image = mask_image.crop(box=(mask_offset[0],mask_offset[1],target_image.size[0]+mask_offset[0],target_image.size[1]+mask_offset[1]))
	W,H = mask_image.size
	tmp_image = Image.new(mask_image.mode, mask_image.size)
	pixelsNew = tmp_image.load()
	DELTA = 2
	#Build the Skin
	if skin != None:
		for i in range(W):
			for j in range(H):
				r,g,b,a = mask_image.getpixel((i,j))
				for color in skin_colors:
					if (r,g,b) == color:
						pixelsNew[i,j]=(R,G,B,255)
						for x in range(-DELTA,DELTA+1):
							for y in range(-DELTA,DELTA+1):
								if x == 0 or y == 0: continue
								if 0 < i+x < W and 0 < j+y < H:
									r,g,b,a = mask_image.getpixel((i+x,j+y))
									if (r,g,b) not in ALL_MASK_VALUES:
										cr,cg,cb,ca = target_image.getpixel((i+x,j+y))
										pixelsNew[i,j]=(R,G,B,255)
	#Build the Outfit
	for i in range(W):
		for j in range(H):
			found=False
			cr,cg,cb,ca = target_image.getpixel((i,j))
			if (cr,cg,cb,ca) == (0,0,0,0): continue
			r,g,b,a = mask_image.getpixel((i,j))
			pixelsNew[i,j]=(cr,cg,cb,255)
			if (r,g,b) == ignore:
				found=True
				#pixelsNew[i,j]=(cr,cg,cb,255)
				continue
			for color in primary:
				if (r,g,b,) != color: continue
				pixelsNew[i,j]=(r1-(255-cr),g1-(255-cg),b1-(255-cb), ca)
				found = True
				break
			for color in secondary:
				if (r,g,b,) != color: continue
				pixelsNew[i,j]=(r2-(255-cr),g2-(255-cg),b2-(255-cb), ca)
				found = True
				break
			if skin == None:
				for color in tertiary:
					if (r,g,b) != color: continue
					pixelsNew[i,j]=(0,0,0,0)
					found = True
					break
			if not found:
				#Look for the closest pixel in primary/secondary and color it
				DELTA=4
				complete=False
				for x in range(-DELTA,DELTA+1):
					if complete: break
					for y in range(-DELTA,DELTA+1):
						if complete: break
						if x == 0 and y == 0: continue
						if 0 < i+x < W and 0 < j+y < H:
							r,g,b,a = mask_image.getpixel((i+x,j+y))
							if (r,g,b) in primary:
								cr,cg,cb,ca = target_image.getpixel((i+x,j+y))
								pixelsNew[i,j]=(r1-(255-cr),g1-(255-cg),b1-(255-cb), ca)
								complete=True
							elif (r,g,b) in secondary:
								cr,cg,cb,ca = target_image.getpixel((i+x,j+y))
								pixelsNew[i,j]=(r2-(255-cr),g2-(255-cg),b2-(255-cb), ca)
								complete=True
							#elif (r,g,b) == ignore:
							#	complete=True
								
	return tmp_image
		
def DrawHat(pixelMap, Head):
	head = find(Head)
	if head != None:
		result = DATABASE.GEAR_MAP[Head[0]]
		tmp_image = Image.new(pixelMap.mode, pixelMap.size)
		b_image = Image.open(head)
		if "mask_offset" in result:
			mask_fn = find(Head,True)
			if mask_fn != None:
				m_image = Image.open(mask_fn)
				#mask_offset = result['mask_offset']
				#primary,secondary,delete,ignore=getColorsFromResult(result)
				#b_image=ApplyMask(b_image,m_image,mask_offset,Head[1],Head[2],primary,secondary,delete,ignore)
				b_image=ApplyMask(Head,b_image,m_image)
		if "scale" in result:
			b_image = b_image.resize((round(b_image.size[0]*result["scale"]), round(b_image.size[1]*result["scale"])))
		x,y,yoffset = 200,250,84
		W,H = b_image.size
		x = x - int(W / 2)
		y = y - (H - yoffset)
		if "offset" in result:
			x,y = x+result["offset"][0],y+result["offset"][1]
		tmp_image.paste(b_image,box=(x,y))
		pixelsNew = tmp_image.load()
		for i in range(tmp_image.size[0]):
			for j in range(tmp_image.size[1]):
				if tmp_image.getpixel((i,j)) == (0,0,0,0):
					pixelsNew[i,j] = pixelMap.getpixel((i,j))
		if 'alpha' in result:
			pixelMap = Image.alpha_composite(pixelMap, tmp_image)
		else:
			pixelMap.paste(tmp_image)
	return pixelMap
	
def DrawHair(pixelMap,Hair):
	hair = find(Hair)
	if hair != None:
		zcolor = Hair[1]
		if zcolor == 0 or zcolor not in DATABASE.COLOR_MAP:
			zcolor = DATABASE.COLOR_MAP[1362] #fudge
		else:
			zcolor = DATABASE.COLOR_MAP[zcolor]
		a,r,g,b = int(zcolor[:2],16),int(zcolor[2:4],16),int(zcolor[4:6],16),int(zcolor[6:],16)
		tmp_image = Image.new(pixelMap.mode, pixelMap.size)
		b_image = Image.open(hair)
		result = DATABASE.OUTFIT_MAP[Hair[0]]
		if "scale" in result:
			b_image = b_image.resize((round(b_image.size[0]*result["scale"]), round(b_image.size[1]*result["scale"])))
		x,y = 200,160
		W,H = b_image.size
		x = x - int(W / 2)
		#y = y - int(H / 2)
		if "offset" in result:
			x,y = x+result["offset"][0],y+result["offset"][1]
		tmp_image.paste(b_image,box=(x,y))
		pixelsNew = tmp_image.load()
		#mod_pixels = pixelMap.load()
		#weight = 0.75
		for i in range(tmp_image.size[0]):
			for j in range(tmp_image.size[1]):
				cr,cg,cb,ca = tmp_image.getpixel((i,j))
				if (cr,cg,cb,ca) == (0,0,0,0):
					pixelsNew[i,j] = pixelMap.getpixel((i,j))
				else:
					#mr,mg,mb = int( (weight*r+(1-weight)*cr) /2),int( (weight*g+(1-weight)*cg) /2),int( (weight*b+(1-weight)*cb)/2)
					mr,mg,mb = r-(255-cr),g-(255-cg),b-(255-cb)
					pixelsNew[i,j] = (mr,mg,mb,a)
		pixelMap.paste(tmp_image)
	return pixelMap

def DrawBody(pixelMap, Body, skin):
	body = find(Body)
	if body != None:
		tmp_image = Image.new(pixelMap.mode, pixelMap.size)
		b_image = Image.open(body)
		result = DATABASE.GEAR_MAP[Body[0]]
		if "mask_offset" in result:
			mask_fn = find(Body,True)
			if mask_fn != None:
				m_image = Image.open(mask_fn)
				#mask_offset = result['mask_offset']
				#primary,secondary,delete,ignore = getColorsFromResult(result)
				#b_image=ApplyMask(b_image,m_image,mask_offset,Body[1],Body[2],primary,secondary,delete,ignore,skin)
				b_image=ApplyMask(Body,b_image,m_image,skin)
		x,y = 200,535
		W,H = b_image.size
		x = x - int(W / 2)
		y = y - H
		if "offset" in result:
			x,y = x+result["offset"][0],y+result["offset"][1]
		tmp_image.paste(b_image,box=(x,y))
		pixelsNew = tmp_image.load()
		for i in range(tmp_image.size[0]):
			for j in range(tmp_image.size[1]):
				if tmp_image.getpixel((i,j)) == (0,0,0,0):
					pixelsNew[i,j] = pixelMap.getpixel((i,j))
		#pixelMap = Image.alpha_composite(pixelMap, tmp_image)
		pixelMap.paste(tmp_image)
		if "no_hands" not in result:
			R = int(skin[:2], 16)
			G = int(skin[2:4], 16)
			B = int(skin[4:], 16)
			draw = ImageDraw.Draw(pixelMap)
			x,y,r = 100,471,20
			leftUpPoint = (x-r, y-r)
			rightDownPoint = (x+r, y+r)
			twoPointList = [leftUpPoint, rightDownPoint]
			draw.ellipse(twoPointList, fill=(R,G,B,255))
			x,y,r = 300,471,20
			leftUpPoint = (x-r, y-r)
			rightDownPoint = (x+r, y+r)
			twoPointList = [leftUpPoint, rightDownPoint]
			draw.ellipse(twoPointList, fill=(R,G,B,255))
	return pixelMap

def DrawBoxSkin(pixelMap, BoxSkin):
	box_skin = find(BoxSkin)
	if box_skin != None:
		result = DATABASE.GEAR_MAP[BoxSkin[0]]
		tmp_image = Image.new(pixelMap.mode, pixelMap.size)
		b_image = Image.open(box_skin)
		x,y = 195,627
		W,H = b_image.size
		x = x - int(W / 2)
		y = y - int(H / 2)
		if "offset" in result:
			x,y = x+result["offset"][0],y+result["offset"][1]
		tmp_image.paste(b_image,box=(x,y))
		pixelsNew = tmp_image.load()
		for i in range(tmp_image.size[0]):
			for j in range(tmp_image.size[1]):
				r,g,b,a = tmp_image.getpixel((i,j))
				if (r,g,b,a) == (0,0,0,0) or (r,g,b) == (255,255,255):
					pixelsNew[i,j] = pixelMap.getpixel((i,j))
		pixelMap = Image.alpha_composite(pixelMap, tmp_image)
	return pixelMap
	
def DrawHead(pixelMap,skin):
	R = int(skin[:2], 16)
	G = int(skin[2:4], 16)
	B = int(skin[4:], 16)
	draw = ImageDraw.Draw(pixelMap)
	x,y,r = 200,295,120
	leftUpPoint = (x-r, y-r)
	rightDownPoint = (x+r, y+r)
	twoPointList = [leftUpPoint, rightDownPoint]
	draw.ellipse(twoPointList, fill=(R,G,B,255))
	
def DrawDetail(pixelMap,Detail):
	detail = find(Detail)
	if detail != None:
		zcolor = Detail[1]
		if zcolor == 0 or zcolor not in DATABASE.COLOR_MAP:
			zcolor = DATABASE.COLOR_MAP[1362] #fudge
		else:
			zcolor = DATABASE.COLOR_MAP[zcolor]
		a,r,g,b = int(zcolor[:2],16),int(zcolor[2:4],16),int(zcolor[4:6],16),int(zcolor[6:],16)
		result = DATABASE.OUTFIT_MAP[Detail[0]]
		tmp_image = Image.new(pixelMap.mode, pixelMap.size)
		b_image = Image.open(detail)
		x,y = 200,299
		W,H = b_image.size
		x = x - int(W / 2)
		y = y - int(H / 2)
		if "offset" in result:
			x,y = x+result["offset"][0],y+result["offset"][1]
		tmp_image.paste(b_image,box=(x,y))
		pixelMap = Image.alpha_composite(pixelMap, tmp_image)
	return pixelMap
	
def DrawEyebrows(pixelMap,Eyebrows):
	eyebrows = find(Eyebrows)
	if eyebrows != None:
		zcolor = Eyebrows[1]
		if zcolor == 0 or zcolor not in DATABASE.COLOR_MAP:
			zcolor = DATABASE.COLOR_MAP[1362] #fudge
		else:
			zcolor = DATABASE.COLOR_MAP[zcolor]
		a,r,g,b = int(zcolor[:2],16),int(zcolor[2:4],16),int(zcolor[4:6],16),int(zcolor[6:],16)
		result = DATABASE.OUTFIT_MAP[Eyebrows[0]]
		tmp_image = Image.new(pixelMap.mode, pixelMap.size)
		b_image = Image.open(eyebrows)
		x,y = 200,250
		W,H = b_image.size
		x = x - int(W / 2)
		y = y - int(H / 2)
		if "offset" in result:
			x,y = x+result["offset"][0],y+result["offset"][1]
		tmp_image.paste(b_image,box=(x,y))
		pixelsNew = tmp_image.load()
		for i in range(tmp_image.size[0]):
			for j in range(tmp_image.size[1]):
				if tmp_image.getpixel((i,j)) == (0,0,0,0):
					pixelsNew[i,j] = pixelMap.getpixel((i,j))
				else:
					pixelsNew[i,j] = (r,g,b,a)
		#pixelMap = Image.alpha_composite(pixelMap, tmp_image)
		pixelMap.paste(tmp_image)
	return pixelMap
	
def DrawEyes(pixelMap,Eyes):
	#3. Draw the Eyes
	eyes = find(Eyes)
	if eyes != None:
		result = DATABASE.OUTFIT_MAP[Eyes[0]]
		tmp_image = Image.new(pixelMap.mode, pixelMap.size)
		b_image = Image.open(eyes)
		x,y = 200,299
		W,H = b_image.size
		x = x - int(W / 2)
		y = y - int(H / 2)
		if "offset" in result:
			x,y = x+result["offset"][0],y+result["offset"][1]
		tmp_image.paste(b_image,box=(x,y))
		pixelsNew = tmp_image.load()
		for i in range(tmp_image.size[0]):
			for j in range(tmp_image.size[1]):
				if tmp_image.getpixel((i,j)) == (0,0,0,0):
					pixelsNew[i,j] = pixelMap.getpixel((i,j))
		pixelMap = Image.alpha_composite(pixelMap, tmp_image)
		#pixelMap.paste(tmp_image)
	return pixelMap

def DrawMouth(pixelMap,Mouth):
	mouth = find(Mouth)
	if mouth != None:
		result = DATABASE.OUTFIT_MAP[Mouth[0]]
		tmp_image = Image.new(pixelMap.mode, pixelMap.size)
		b_image = Image.open(mouth)
		x,y = 200,375
		W,H = b_image.size
		x = x - int(W / 2)
		y = y - int(H / 2)
		if 'offset' in result:
			x,y = x+result["offset"][0],y+result["offset"][1]
		tmp_image.paste(b_image,box=(x,y))
		pixelsNew = tmp_image.load()
		for i in range(tmp_image.size[0]):
			for j in range(tmp_image.size[1]):
				if tmp_image.getpixel((i,j)) == (0,0,0,0):
					pixelsNew[i,j] = pixelMap.getpixel((i,j))
		pixelMap = Image.alpha_composite(pixelMap, tmp_image)
	return pixelMap

def DrawFacialHair(pixelMap,FacialHair):
	facialhair = find(FacialHair)
	if facialhair != None:
		zcolor = FacialHair[1]
		if zcolor == 0 or zcolor not in DATABASE.COLOR_MAP:
			zcolor = DATABASE.COLOR_MAP[1362] #fudge
		else:
			zcolor = DATABASE.COLOR_MAP[zcolor]
		a,r,g,b = int(zcolor[:2],16),int(zcolor[2:4],16),int(zcolor[4:6],16),int(zcolor[6:],16)
		result = DATABASE.OUTFIT_MAP[FacialHair[0]]
		tmp_image = Image.new(pixelMap.mode, pixelMap.size)
		b_image = Image.open(facialhair)
		x,y = 200,411
		W,H = b_image.size
		x = x - int(W / 2)
		y = y - H
		if "offset" in result:
			x,y = x+result["offset"][0],y+result["offset"][1]
		if 'alpha' in result:
			pixelsNew = b_image.load()
			for i in range(b_image.size[0]):
				for j in range(b_image.size[1]):
					cr,cg,cb,ca = b_image.getpixel((i,j))
					if (cr,cg,cb,ca) != (0,0,0,0):
						pixelsNew[i,j] = (r,g,b,ca)
			tmp_image.paste(b_image,box=(x,y))
			pixelMap = Image.alpha_composite(pixelMap, tmp_image)
		else:
			tmp_image.paste(b_image,box=(x,y))
			pixelsNew = tmp_image.load()
			for i in range(tmp_image.size[0]):
				for j in range(tmp_image.size[1]):
					cr,cg,cb,ca = tmp_image.getpixel((i,j))
					if (cr,cg,cb,ca) == (0,0,0,0):
						pixelsNew[i,j] = pixelMap.getpixel((i,j))
					else:
						mr,mg,mb = r-(255-cr),g-(255-cg),b-(255-cb)
						pixelsNew[i,j] = (mr,mg,mb,a)
			pixelMap.paste(tmp_image)
	return pixelMap

def DrawGlasses(pixelMap,Glasses):
	glasses = find(Glasses)
	if glasses != None:
		result = DATABASE.OUTFIT_MAP[Glasses[0]]
		tmp_image = Image.new(pixelMap.mode, pixelMap.size)
		b_image = Image.open(glasses)
		x,y = 200,299
		W,H = b_image.size
		x = x - int(W / 2)
		y = y - int(H / 2)
		if "offset" in result:
			x,y = x+result["offset"][0],y+result["offset"][1]
		tmp_image.paste(b_image,box=(x,y))
		pixelsNew = tmp_image.load()
		for i in range(tmp_image.size[0]):
			for j in range(tmp_image.size[1]):
				if tmp_image.getpixel((i,j)) == (0,0,0,0):
					pixelsNew[i,j] = pixelMap.getpixel((i,j))
		pixelMap = Image.alpha_composite(pixelMap, tmp_image)
	return pixelMap

def build_new_kid(skin, BoxSkin, Head, Body, Eyebrows, Eyes, FacialHair, Glasses, Hair, Mouth, Detail):
	#Need - from lowest layer to highest layer
	pixelMap = Image.new(mode = 'RGBA', size = (400,800))
	pixelMap = DrawBoxSkin(pixelMap, BoxSkin)
	pixelMap = DrawBody(pixelMap, Body, skin)
	DrawHead(pixelMap,skin)
	pixelMap = DrawDetail(pixelMap,Detail)
	pixelMap = DrawEyebrows(pixelMap,Eyebrows)
	pixelMap = DrawEyes(pixelMap,Eyes)
	pixelMap = DrawMouth(pixelMap,Mouth)
	pixelMap = DrawFacialHair(pixelMap,FacialHair)
	pixelMap = DrawGlasses(pixelMap,Glasses)
	pixelMap = DrawHair(pixelMap,Hair)
	pixelMap = DrawHat(pixelMap, Head)
	
	#pixelMap.save('test.png')
	#pixelMap.show()

	tmp_file = BytesIO()
	pixelMap.save(tmp_file,"PNG")
	encoded_image = base64.b64encode(tmp_file.getvalue())
	return encoded_image
	
def build_douglas_new_kid(USERID = None):
		#r = random.choice([1,2,3,4]) == 4
		NAME = None
		skin = "%x" % random.choice([16769476,8543288,14265215])
		female = random.choice([True,False])
		BoxSkin = [2211,0,0]
		Head = [None,0,0]
		Body = [204,0,0]
		Eyebrows = None
		Eyes = [1554,0]
		FacialHair = None
		Glasses = None
		Hair = None
		Mouth = [1555,0]
		Detail = None
		r = random.choice([True,False])
		if USERID != None:
			result = executeQuery(f"SELECT SKIN,FEMALE,GEAR1,A1,B1,GEAR2,A2,B2,GEAR3,A3,B3,OUTFIT1,C1,OUTFIT2,C2,OUTFIT3,C3,OUTFIT4,C4,OUTFIT5,C5,OUTFIT6,C6,OUTFIT7,C7,NAME FROM users\
				WHERE USERID = (SELECT USERID FROM users WHERE ID = {USERID})",quiet=True)
			if result[0] == None:
				return None, None
			active_test = {
				"avatar": {
					"outfit": [],
					"skin_color": result[0],
					"female": int(result[1]) == 1,
				},
				"active_gear": []
			}
			for i in range(2,11,3):
				if result[i] == None: continue
				active_test['active_gear'].append({
				  "id": result[i],
				  "custom": {
					"a": result[i+1],
					"b": result[i+2]
				  }
				})
			for i in range(11,25,2):
				if result[i] == None: continue
				active_test['avatar']['outfit'].append({ "c": result[i+1], "id": result[i]})
			NAME = result[25]
			skin = "%x" % result[0]
			female = int(result[1]) == 1
			active_gear = active_test["active_gear"]
			for g in active_gear:
				if 'id' not in g or g['id'] not in DATABASE.GEAR_MAP: continue
				g_id = g['id']
				result = DATABASE.GEAR_MAP[g_id]
				slot = result["Slot"]
				if slot == 'BoxSkin':
					BoxSkin[0] = g_id
					if 'custom' in g:
						if 'a' in g['custom']:
							BoxSkin[1] = g['custom']['a']
						if 'b' in g['custom']:
							BoxSkin[2] = g['custom']['b']
				elif slot == 'Head':
					Head[0] = g_id
					if 'custom' in g:
						if 'a' in g['custom']:
							Head[1] = g['custom']['a']
						if 'b' in g['custom']:
							Head[2] = g['custom']['b']
				elif slot == 'Body':
					Body[0] = g_id
					if 'custom' in g:
						if 'a' in g['custom']:
							Body[1] = g['custom']['a']
						if 'b' in g['custom']:
							Body[2] = g['custom']['b']
			outfit = active_test["avatar"]["outfit"]
			for g in outfit:
				if 'id' not in g or g['id'] not in DATABASE.OUTFIT_MAP: continue
				g_id = g['id']
				result = DATABASE.OUTFIT_MAP[g['id']]
				slot = result["Slot"]
				if slot == 'Eyebrows':
					color = 0 if 'c' not in g else g['c']
					Eyebrows = [g_id,color]
				elif slot == 'Eyes':
					color = 0 if 'c' not in g else g['c']
					Eyes = [g_id,color]
				elif slot == 'FacialHair':
					color = 0 if 'c' not in g else g['c']
					FacialHair = [g_id,color]
				elif slot == 'Glasses':
					color = 0 if 'c' not in g else g['c']
					Glasses = [g_id,color]
				elif slot == 'Hair':
					color = 0 if 'c' not in g else g['c']
					Hair = [g_id,color]
				elif slot == 'Mouth':
					color = 0 if 'c' not in g else g['c']
					Mouth = [g_id,color]
				elif slot == 'Detail':
					color = 0 if 'c' not in g else g['c']
					Detail = [g_id,color]
		elif r:
			result = executeQuery("SELECT SKIN,FEMALE,GEAR1,A1,B1,GEAR2,A2,B2,GEAR3,A3,B3,OUTFIT1,C1,OUTFIT2,C2,OUTFIT3,C3,OUTFIT4,C4,OUTFIT5,C5,OUTFIT6,C6,OUTFIT7,C7,NAME FROM users\
				WHERE USERID IN (SELECT USERID FROM team_members WHERE RANK < 1000 AND RANK <> 0) AND SKIN IS NOT NULL ORDER BY RAND() LIMIT 1",quiet=True)
			#print(result)
			active_test = {
				"avatar": {
					"outfit": [],
					"skin_color": result[0],
					"female": int(result[1]) == 1,
				},
				"active_gear": []
			}
			for i in range(2,11,3):
				if result[i] == None: continue
				active_test['active_gear'].append({
				  "id": result[i],
				  "custom": {
					"a": result[i+1],
					"b": result[i+2]
				  }
				})
			for i in range(11,25,2):
				if result[i] == None: continue
				active_test['avatar']['outfit'].append({ "c": result[i+1], "id": result[i]})
			NAME = result[25]
			skin = "%x" % result[0]
			female = int(result[1]) == 1
			active_gear = active_test["active_gear"]
			for g in active_gear:
				if 'id' not in g or g['id'] not in DATABASE.GEAR_MAP: continue
				g_id = g['id']
				result = DATABASE.GEAR_MAP[g_id]
				slot = result["Slot"]
				if slot == 'BoxSkin':
					BoxSkin[0] = g_id
					if 'custom' in g:
						if 'a' in g['custom']:
							BoxSkin[1] = g['custom']['a']
						if 'b' in g['custom']:
							BoxSkin[2] = g['custom']['b']
				elif slot == 'Head':
					Head[0] = g_id
					if 'custom' in g:
						if 'a' in g['custom']:
							Head[1] = g['custom']['a']
						if 'b' in g['custom']:
							Head[2] = g['custom']['b']
				elif slot == 'Body':
					Body[0] = g_id
					if 'custom' in g:
						if 'a' in g['custom']:
							Body[1] = g['custom']['a']
						if 'b' in g['custom']:
							Body[2] = g['custom']['b']
			outfit = active_test["avatar"]["outfit"]
			for g in outfit:
				if 'id' not in g or g['id'] not in DATABASE.OUTFIT_MAP: continue
				g_id = g['id']
				result = DATABASE.OUTFIT_MAP[g['id']]
				slot = result["Slot"]
				if slot == 'Eyebrows':
					color = 0 if 'c' not in g else g['c']
					Eyebrows = [g_id,color]
				elif slot == 'Eyes':
					color = 0 if 'c' not in g else g['c']
					Eyes = [g_id,color]
				elif slot == 'FacialHair':
					color = 0 if 'c' not in g else g['c']
					FacialHair = [g_id,color]
				elif slot == 'Glasses':
					color = 0 if 'c' not in g else g['c']
					Glasses = [g_id,color]
				elif slot == 'Hair':
					color = 0 if 'c' not in g else g['c']
					Hair = [g_id,color]
				elif slot == 'Mouth':
					color = 0 if 'c' not in g else g['c']
					Mouth = [g_id,color]
				elif slot == 'Detail':
					color = 0 if 'c' not in g else g['c']
					Detail = [g_id,color]
		else:
			#randomly select all the attributes
			ALL_BoxSkin = []
			ALL_Body = []
			ALL_Head = []
			for key,value in DATABASE.GEAR_MAP.items():
				slot = value["Slot"]
				if slot == 'BoxSkin':
					ALL_BoxSkin.append(key)
				elif slot == 'Body':
					ALL_Body.append(key)
				elif slot == 'Head':
					ALL_Head.append(key)

			ALL_COLORS = [x for x in DATABASE.COLOR_MAP.keys()]
			ALL_Eyebrows = []
			ALL_Eyes = []
			ALL_FacialHair = []
			ALL_Glasses = []
			ALL_Hair = []
			ALL_Mouth = []
			ALL_Detail = []
			for key,value in DATABASE.OUTFIT_MAP.items():
				slot = value["Slot"]
				if slot == 'Eyebrows':
					ALL_Eyebrows.append(key)
				elif slot == 'Eyes':
					ALL_Eyes.append(key)
				elif slot == 'FacialHair':
					ALL_FacialHair.append(key)
				elif slot == 'Glasses':
					ALL_Glasses.append(key)
				elif slot == 'Hair':
					ALL_Hair.append(key)
				elif slot == 'Mouth':
					ALL_Mouth.append(key)
				elif slot == 'Detail':
					ALL_Detail.append(key)
					
			#Select elements at random
			BoxSkin = [random.choice(ALL_BoxSkin),random.choice(ALL_COLORS),random.choice(ALL_COLORS)] #default
			Head = [random.choice(ALL_Head),random.choice(ALL_COLORS),random.choice(ALL_COLORS)] #default
			Body = [random.choice(ALL_Body),random.choice(ALL_COLORS),random.choice(ALL_COLORS)] #default
			Eyebrows = [random.choice(ALL_Eyebrows),random.choice(ALL_COLORS)] #default
			Eyes = [random.choice(ALL_Eyes),random.choice(ALL_COLORS)]
			FacialHair = [random.choice(ALL_FacialHair),random.choice(ALL_COLORS)]
			Glasses = [random.choice(ALL_Glasses),random.choice(ALL_COLORS)]
			Hair = [random.choice(ALL_Hair),random.choice(ALL_COLORS)]
			Mouth = [random.choice(ALL_Mouth),random.choice(ALL_COLORS)]
			Detail = [random.choice(ALL_Detail),random.choice(ALL_COLORS)]
		IMAGE = build_new_kid(skin, BoxSkin, Head, Body, Eyebrows, Eyes, FacialHair, Glasses, Hair, Mouth, Detail)
			
		return IMAGE, NAME
	
if __name__ == '__main__':
	RESULT = executeQuery(f"SELECT SKIN,FEMALE,GEAR1,A1,B1,GEAR2,A2,B2,GEAR3,A3,B3,OUTFIT1,C1,OUTFIT2,C2,OUTFIT3,C3,OUTFIT4,C4,OUTFIT5,C5,OUTFIT6,C6,OUTFIT7,C7 FROM USERS WHERE ID IN (10,3777) AND SKIN IS NOT NULL LIMIT 3")
	if type(RESULT) == tuple: RESULT = [RESULT]
	test_array = []
	for row in RESULT:
		#print(row)
		tmp_test = {
		  "avatar": {
			"outfit": [],
			"skin_color": row[0],
			"female": int(row[1]) == 1,
		  },
		  "active_gear": []
		}
		for i in range(2,11,3):
			if row[i] == None: continue
			tmp_test['active_gear'].append({
			  "id": row[i],
			  "custom": {
				"a": row[i+1],
				"b": row[i+2]
			  }
			})
		for i in range(11,25,2):
			if row[i] == None: continue
			tmp_test['avatar']['outfit'].append({ "c": row[i+1], "id": row[i]})
		test_array.append(tmp_test)
		
	index = 0
	#test_array = []
	for active_test in test_array:
		index+=1
		skin = "%x" % active_test["avatar"]["skin_color"]
		female = active_test["avatar"]["female"]

		###
		active_gear = active_test["active_gear"]
		BoxSkin = [2211,0,0]
		Head = [None,0,0]
		Body = [204,0,0]
		Eyebrows = None
		Eyes = [1554,0]
		FacialHair = None
		Glasses = None
		Hair = None
		Mouth = [1555,0]
		Detail = None
		for g in active_gear:
			if 'id' not in g or g['id'] not in DATABASE.GEAR_MAP: continue
			g_id = g['id']
			result = DATABASE.GEAR_MAP[g_id]
			slot = result["Slot"]
			if slot == 'BoxSkin':
				BoxSkin[0] = g_id
				if 'custom' in g:
					if 'a' in g['custom']:
						BoxSkin[1] = g['custom']['a']
					if 'b' in g['custom']:
						BoxSkin[2] = g['custom']['b']
			elif slot == 'Head':
				Head[0] = g_id
				if 'custom' in g:
					if 'a' in g['custom']:
						Head[1] = g['custom']['a']
					if 'b' in g['custom']:
						Head[2] = g['custom']['b']
			elif slot == 'Body':
				Body[0] = g_id
				if 'custom' in g:
					if 'a' in g['custom']:
						Body[1] = g['custom']['a']
					if 'b' in g['custom']:
						Body[2] = g['custom']['b']


		outfit = active_test["avatar"]["outfit"]
		for g in outfit:
			if 'id' not in g or g['id'] not in DATABASE.OUTFIT_MAP: continue
			g_id = g['id']
			result = DATABASE.OUTFIT_MAP[g['id']]
			slot = result["Slot"]
			if slot == 'Eyebrows':
				color = 0 if 'c' not in g else g['c']
				Eyebrows = [g_id,color]
			elif slot == 'Eyes':
				color = 0 if 'c' not in g else g['c']
				Eyes = [g_id,color]
			elif slot == 'FacialHair':
				color = 0 if 'c' not in g else g['c']
				FacialHair = [g_id,color]
			elif slot == 'Glasses':
				color = 0 if 'c' not in g else g['c']
				Glasses = [g_id,color]
			elif slot == 'Hair':
				color = 0 if 'c' not in g else g['c']
				Hair = [g_id,color]
			elif slot == 'Mouth':
				color = 0 if 'c' not in g else g['c']
				Mouth = [g_id,color]
			elif slot == 'Detail':
				color = 0 if 'c' not in g else g['c']
				Detail = [g_id,color]
		#print(f'skin {skin}, BoxSkin {BoxSkin}, Head {Head}, Body {Body}, Eyebrows {Eyebrows}, Eyes {Eyes}, FacialHair {FacialHair}, Glasses {Glasses}, Hair {Hair}, Mouth {Mouth}, Detail {Detail}')
		build_new_kid(skin, BoxSkin, Head, Body, Eyebrows, Eyes, FacialHair, Glasses, Hair, Mouth, Detail)
		print('Complete')
		input('Continue...?')
	sys.exit()
	
	ALL_BoxSkin = []
	ALL_Body = []
	ALL_Head = []
	for key,value in DATABASE.GEAR_MAP.items():
		slot = value["Slot"]
		if slot == 'BoxSkin':
			ALL_BoxSkin.append(key)
		elif slot == 'Body':
			ALL_Body.append(key)
		elif slot == 'Head':
			ALL_Head.append(key)

	ALL_COLORS = [x for x in DATABASE.COLOR_MAP.keys()]
	ALL_Eyebrows = []
	ALL_Eyes = []
	ALL_FacialHair = []
	ALL_Glasses = []
	ALL_Hair = []
	ALL_Mouth = []
	ALL_Detail = []
	for key,value in DATABASE.OUTFIT_MAP.items():
		slot = value["Slot"]
		if slot == 'Eyebrows':
			ALL_Eyebrows.append(key)
		elif slot == 'Eyes':
			ALL_Eyes.append(key)
		elif slot == 'FacialHair':
			ALL_FacialHair.append(key)
		elif slot == 'Glasses':
			ALL_Glasses.append(key)
		elif slot == 'Hair':
			ALL_Hair.append(key)
		elif slot == 'Mouth':
			ALL_Mouth.append(key)
		elif slot == 'Detail':
			ALL_Detail.append(key)
	#Select elements at random
	for index in range(max(len(ALL_Body),len(ALL_Head))):
		skin = "%x" % random.choice([16769476,8543288,14265215])
		female = random.choice([True,False])

		BoxSkin = [ALL_BoxSkin[index % len(ALL_BoxSkin)],random.choice(ALL_COLORS),random.choice(ALL_COLORS)] #default
		Head = [ALL_Head[index % len(ALL_Head)],random.choice(ALL_COLORS),random.choice(ALL_COLORS)] #default
		Body = [ALL_Body[index % len(ALL_Body)],random.choice(ALL_COLORS),random.choice(ALL_COLORS)] #default
		Eyebrows = [ALL_Eyebrows[index % len(ALL_Eyebrows)],random.choice(ALL_COLORS)] #default
		Eyes = [ALL_Eyes[index % len(ALL_Eyes)],random.choice(ALL_COLORS)]
		FacialHair = [ALL_FacialHair[index % len(ALL_FacialHair)],random.choice(ALL_COLORS)]
		Glasses = [ALL_Glasses[index % len(ALL_Glasses)],random.choice(ALL_COLORS)]
		Hair = [ALL_Hair[index % len(ALL_Hair)],random.choice(ALL_COLORS)]
		Mouth = [ALL_Mouth[index % len(ALL_Mouth)],random.choice(ALL_COLORS)]
		Detail = [ALL_Detail[index % len(ALL_Detail)],random.choice(ALL_COLORS)]
			
			
		build_new_kid(skin, BoxSkin, Head, Body, Eyebrows, Eyes, FacialHair, Glasses, Hair, Mouth, Detail)
		print('Complete')
		input('Continue...?')
		