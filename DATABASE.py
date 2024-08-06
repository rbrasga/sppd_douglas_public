CARD_ABILITIES = {
	'EnablePower': 'Power Enabled',
	'PowerSummonLevelAbs': 'Summon Level',
	'PowerAttackBoostAbs': 'Attack Boost',
	'PowerDurationAbs': 'Power Duration',
	'PowerRangeAbs': 'Power Range',
	'PowerDamageAbs': 'Power Damage',
	'PowerHealAbs': 'Heal',
	'PowerMaxHPGainAbs': 'Max HP Gain',
	'ChargedPowerRegenRate': 'Charged Regen',
	'PowerTargetAbs': 'Target',
	'PowerAttackDecreaseAbs': 'Attack Decrease',
	'PowerPoisonAmountAbs': 'Poison Amount',
	'PowerMaxHPLossAbs': 'Max HP Loss',
	'PowerRangeBoostAbs': 'Range Boost',
}

GEAR_MAP = {
	#Boxes
	2211: {'AssetId': 'DefaultBoxSkinUI', 'Slot': 'BoxSkin'},
	2212: {'AssetId': 'GoldenBoxSkinUI', 'Slot': 'BoxSkin', 'offset': [-53, -87]},
	2231: {'AssetId': 'BattletestedBoxSkinUI', 'Slot': 'BoxSkin', 'offset': [-33, -87]},
	2250: {'AssetId': 'GiftBoxSkinUI', 'Slot': 'BoxSkin', 'offset': [-30, -90]},
	2280: {'AssetId': 'LoveBoxSkinUI', 'Slot': 'BoxSkin'},
	2292 : {'AssetId': 'DoomdeviceBoxSkinUI', 'Slot': 'BoxSkin'},
	2306 : {'AssetId': 'RobotBoxSkinUI', 'Slot': 'BoxSkin', 'offset': [36, 0]},
	2273 : {'AssetId': 'TegridyBoxSkinUI', 'Slot': 'BoxSkin'},
	
	#BodyGear
	1854: {'AssetId': 'AdvBanditoShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [53, 93], 'colorA': [154, 199, 93, 255], 'colorB': [238, 23, 22, 255]},
	1733: {'AssetId': 'AdvCowboy2ShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [48, 97], 'colorA': [153, 228, 233, 255], 'colorB': [110, 24, 34, 255]},
	1864: {'AssetId': 'AdvCowGirl2ShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [26, 99], 'colorA': [161, 209, 212, 255], 'colorB': [250, 177, 185, 255]},
	1856: {'AssetId': 'AdvCowGirlShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [65, 96], 'colorA': [202, 141, 190, 255], 'colorB': [138, 174, 205, 255]},
	2073: {'AssetId': 'AdvExplorerShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [51, 94], 'colorA': [255, 255, 255, 255], 'colorB': [231, 128, 51, 255]},
	2323: {'AssetId': 'AdvFrontierShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [42, 95], 'colorA': [90, 113, 176, 0], 'colorB': [170, 167, 183, 0]},
	2106: {'AssetId': 'AdvGladiator1ShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [49, 95], 'colorA': [168, 193, 136, 255], 'colorB': [255, 255, 255, 255]},
	2108: {'AssetId': 'AdvGladiator2ShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [50, 102], 'colorA': [46, 49, 47, 255], 'colorB': [115, 128, 144, 255]},
	1256: {'AssetId': 'AdvIndianShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [66, 98], 'colorA': [231, 177, 120, 255], 'colorB': [212, 164, 123, 255]},
	2077: {'AssetId': 'AdvMummyShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [46, 98], 'no_hands': True, 'colorA': [237, 237, 237, 255], 'colorB': [116, 92, 92, 255]},
	1290: {'AssetId': 'AdvNinjaShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [49, 95], 'colors': {'primary': ['magenta'], 'secondary': [], 'tertiary': ['black'], 'ignore': 'blue'},	'colorA': [230, 57, 57, 255], 'colorB': [255, 255, 255, 0]},
	1968: {'AssetId': 'AdvPeruvianShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [48, 96], 'colorA': [106, 125, 218, 255], 'colorB': [255, 220, 20, 255]},
	1877: {'AssetId': 'AdvPirate3ShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [50, 93], 'colorA': [182, 18, 37, 255], 'colorB': [142, 195, 198, 255]},
	1268: {'AssetId': 'AdvPirateShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [62, 99], 'colorA': [155, 155, 155, 255], 'colorB': [0, 0, 0, 0]},
	2062: {'AssetId': 'AdvSamuraiShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [48, 94], 'colorA': [157, 195, 75, 255], 'colorB': [231, 68, 68, 255]},
	204: {'AssetId': 'DefaultShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [50, 88], 'colorA': [118, 93, 71, 255], 'colorB': [254, 63, 57, 255]},
	2012: {'AssetId': 'FanBarbarianShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [42, 93], 'colorA': [75, 85, 106, 255], 'colorB': [255, 255, 255, 255]},
	1879: {'AssetId': 'FanDragonShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [52, 97], 'colorA': [116, 195, 129, 255], 'colorB': [153, 130, 185, 255]},
	1744: {'AssetId': 'FanDwarfGirlShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [47, 96], 'no_hands': True, 'colorA': [147, 116, 93, 255], 'colorB': [53, 58, 45, 255]},
	1302: {'AssetId': 'FanDwarfShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [26, 96], 'colorA': [75, 217, 202, 255], 'colorB': [112, 136, 222, 255]},
	2373: {'AssetId': 'FanElfetteShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [51, 98], 'colorA': [209, 35, 44, 0], 'colorB': [255, 255, 255, 0]},
	1849: {'AssetId': 'FanElfGirlShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [54, 109], 'colorA': [159, 209, 187, 255], 'colorB': [47, 92, 95, 255]},
	1988: {'AssetId': 'FanElfShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [46, 97], 'no_hands': True, 'colorA': [161, 197, 115, 255], 'colorB': [107, 143, 181, 255]},
	1750: {'AssetId': 'FanFairyShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [8, 23], 'colorA': [255, 255, 255, 0], 'colorB': [250, 177, 185, 255]},
	1858: {'AssetId': 'FanKnight2ShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [48, 92], 'no_hands': True, 'colorA': [252, 252, 252, 255], 'colorB': [244, 65, 65, 255]},
	180: {'AssetId': 'FanKnightShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [52, 86], 'colorA': [255, 255, 255, 255], 'colorB': [79, 103, 157, 255]},
	1753: {'AssetId': 'FanWitchShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [45, 98], 'no_hands': True, 'colorA': [255, 171, 171, 255], 'colorB': [148, 112, 161, 255]},
	1860: {'AssetId': 'FanWizardShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [46, 90], 'colorA': [139, 185, 195, 255], 'colorB': [88, 128, 154, 255]},
	2354: {'AssetId': 'FanWizard2ShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [40, 90], 'colorA': [183, 74, 206, 0], 'colorB': [231, 171, 225, 0]},
	1811: {'AssetId': 'MysAncientGreekShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [50, 96], 'colorA': [255, 255, 255, 255], 'colorB': [209, 67, 67, 255]},
	2375: {'AssetId': 'MysArchangelShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [7, 63], 'colorA': [99, 182, 215, 0], 'colorB': [155, 38, 35, 0]},
	1764: {'AssetId': 'MysBuddhistMonkShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [64, 103], 'offset': [15, 0], 'colorA': [252, 141, 22, 255], 'colorB': [150, 62, 43, 255]},
	1920: {'AssetId': 'MysCleopatraShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [50, 99], 'colorA': [255, 255, 255, 255], 'colorB': [236, 120, 94, 255]},
	2314: {'AssetId': 'MysDarkAngelShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [16, 77], 'colorA': [153, 73, 163, 0], 'colorB': [39, 39, 39, 0]},
	1862: {'AssetId': 'MysDarkPriestShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [46, 96], 'colorA': [53, 53, 53, 255], 'colorB': [174, 32, 25, 255]},
	1294: {'AssetId': 'MysGenieShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [47, 97], 'colorA': [118, 231, 233, 255], 'colorB': [193, 60, 58, 255]},
	1341: {'AssetId': 'MysGothShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [51, 96], 'colorA': [192, 98, 255, 255], 'colorB': [255, 255, 255, 0]},
	1746: {'AssetId': 'MysGreekGodShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [16, 90], 'colorA': [255, 255, 255, 0], 'colorB': [0, 0, 0, 0]},
	196: {'AssetId': 'MysPopeShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [48, 97], 'colorA': [255, 255, 255, 255], 'colorB': [255, 255, 255, 0]},
	1922: {'AssetId': 'MysPriestShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [53, 97], 'colorA': [50, 47, 50, 255], 'colorB': [112, 125, 93, 255]},
	2084: {'AssetId': 'MysSatanicShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [50, 98], 'colorA': [109, 88, 80, 255], 'colorB': [0, 0, 0, 0]},
	1766: {'AssetId': 'MysVirginMaryShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [52, 98], 'colorA': [193, 220, 241, 255], 'colorB': [234, 241, 244, 255]},
	2010: {'AssetId': 'MysVoodooPriestShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [50, 95], 'colorA': [58, 50, 58, 255], 'colorB': [128, 128, 128, 255]},
	2087: {'AssetId': 'NeutAlGoreShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [52, 92], 'colorA': [197, 19, 37, 255], 'colorB': [151, 177, 193, 255]},
	2240: {'AssetId': 'NeutArcheologistShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [47, 99], 'no_hands': True, 'colorA': [150, 139, 89, 0], 'colorB': [237, 237, 237, 0]},
	1758: {'AssetId': 'NeutBearShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [46, 99], 'colorA': [135, 90, 68, 255], 'colorB': [178, 155, 141, 255], 'no_hands': True},
	2303: {'AssetId': 'NeutBrainiacShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [46, 97], 'colorA': [39, 147, 85, 0], 'colorB': [187, 73, 173, 0]},
	1952: {'AssetId': 'NeutBubbleBathShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [64, 102], 'colors': {'primary': [], 'secondary': [], 'tertiary': [], 'ignore': 'green', 'skin': ['red']}, 'colorA': [182, 192, 255, 255], 'colorB': [255, 206, 53, 255]},
	2151: {'AssetId': 'NeutBucketBasherShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [49, 98], 'colorA': [225, 225, 225, 255], 'colorB': [219, 112, 227, 255]},
	2293: {'AssetId': 'NeutBunnyShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [52, 97], 'colorA': [244, 244, 244, 0], 'colorB': [235, 187, 202, 0]},
	1818: {'AssetId': 'NeutButchShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [49, 95], 'colorA': [197, 55, 55, 255], 'colorB': [241, 233, 87, 255]},
	2256: {'AssetId': 'NeutCableGuyShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [38, 98], 'colorA': [79, 95, 99, 0], 'colorB': [148, 101, 29, 0]},
	2090: {'AssetId': 'NeutCartmansXmasShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [49, 98], 'colorA': [70, 85, 116, 255], 'colorB': [201, 62, 68, 255]},
	2321: {'AssetId': 'NeutChaos42ShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [45, 97], 'colorA': [62, 55, 62, 0], 'colorB': [0, 0, 0, 0]},
	2244: {'AssetId': 'NeutChristmasTreeShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [19, 97], 'colorA': [127, 170, 89, 0], 'colorB': [255, 255, 255, 0]},
	1976: {'AssetId': 'NeutClassiShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [48, 99], 'colorA': [255, 150, 0, 255], 'colorB': [100, 136, 171, 255]},
	2086: {'AssetId': 'NeutClownShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [21, 97], 'colorA': [200, 120, 228, 255], 'colorB': [76, 168, 246, 255]},
	2289: {'AssetId': 'NeutCptCosmosShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [46, 91], 'colorA': [185, 116, 221, 0], 'colorB': [192, 37, 37, 0]},
	1931: {'AssetId': 'NeutCupidShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [0, 131], 'colorA': [255, 255, 255, 255], 'colorB': [219, 182, 93, 255]},
	2332: {'AssetId': 'NeutDandelionShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [30, 98], 'colorA': [152, 193, 83, 0], 'colorB': [55, 46, 57, 0]},
	2049: {'AssetId': 'NeutDayOfTheDeadShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [51, 99], 'colorA': [55, 55, 55, 255], 'colorB': [255, 255, 255, 255]},
	2139: {'AssetId': 'NeutDrBadShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [0, 106], 'colorA': [69, 69, 69, 255], 'colorB': [36, 60, 111, 255]},
	2233: {'AssetId': 'NeutFingerBang2ShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [56, 95], 'colorA': [255, 255, 255, 0], 'colorB': [74, 192, 190, 0]},
	2229: {'AssetId': 'NeutFingerBangShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [44, 92], 'colorA': [247, 247, 247, 0], 'colorB': [85, 166, 70, 0]},
	2155: {'AssetId': 'NeutFirezoneShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [0, 102], 'no_hands': True, 'colorA': [238, 47, 44, 255], 'colorB': [78, 88, 125, 255]},
	1986: {'AssetId': 'NeutFourthOfJulyShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [2, 89], 'colors': {'primary': ['magenta'], 'secondary': ['lightblue'], 'tertiary': ['black', 'green', 'red']}, 'colorA': [247, 51, 51, 255], 'colorB': [170, 67, 70, 255]},
	2338: {'AssetId': 'NeutGardenerShirtBodyGearUI',  'Slot': 'Body', 'mask_offset': [56,99], 'colorA': [117, 192, 213, 0], 'colorB': [255, 255, 255, 0] },
	2236: {'AssetId': 'NeutGooManShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [42, 96], 'colorA': [51, 42, 40, 0], 'colorB': [67, 54, 53, 0]},
	2346: {'AssetId': 'NeutGothDressShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [54, 98], 'colorA': [47, 46, 54, 0], 'colorB': [19, 19, 23, 0]},
	2345: {'AssetId': 'NeutGothGlamShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [31, 87], 'colorA': [47, 46, 54, 0], 'colorB': [68, 81, 104, 0]},
	2060: {'AssetId': 'NeutHempShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [54, 100], 'colors': {'primary': ['magenta'], 'secondary': ['lightblue'], 'tertiary': ['red']}, 'colorA': [158, 134, 108, 255], 'colorB': [122, 140, 179, 255]},
	1905: {'AssetId': 'NeutHogmanayKiltShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [52, 97], 'colorA': [30, 33, 40, 255], 'colorB': [96, 179, 203, 255]},
	2218: {'AssetId': 'NeutICEShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [50, 95], 'colorA': [88, 168, 209, 0], 'colorB': [240, 240, 240, 0]},
	2067: {'AssetId': 'NeutJesterShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [52, 95], 'colorA': [238, 74, 100, 255], 'colorB': [58, 233, 110, 255]},
	2370: {'AssetId': 'NeutKiteShirtBodyGearUI', 'Slot': 'Body', 'no_hands': True, 'mask_offset': [5, 22], 'colorA': [61, 147, 157, 0], 'colorB': [255, 255, 255, 0]},
	2039: {'AssetId': 'NeutLeatherJacketShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [52, 98], 'colorA': [61, 61, 61, 255], 'colorB': [93, 93, 93, 255]},
	1817: {'AssetId': 'NeutLuchadorShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [40, 99], 'colors': {'primary': ['magenta'], 'secondary': ['lightblue'], 'tertiary': [], 'skin': ['green']}, 'colorA': [216, 69, 69, 255], 'colorB': [180, 50, 50, 255]},
	1828: {'AssetId': 'NeutManBearPigShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [8, 91], 'no_hands': True, 'colorA': [174, 173, 190, 255], 'colorB': [85, 102, 167, 255]},
	2057: {'AssetId': 'NeutMasgueradeShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [44, 98], 'colorA': [141, 30, 30, 255], 'colorB': [255, 255, 255, 255]},
	2352: {'AssetId': 'NeutMonsterShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [53, 96], 'colorA': [153, 113, 82, 0], 'colorB': [91, 65, 48, 0]},
	1936: {'AssetId': 'NeutPajamasShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [52, 97], 'colorA': [50, 63, 110, 255], 'colorB': [0, 0, 0, 0]},
	1897: {'AssetId': 'NeutPCPrincipalShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [66, 99], 'colorA': [16, 104, 142, 255], 'colorB': [184, 146, 95, 255]},
	2104: {'AssetId': 'NeutPeacockShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [35, 0], 'colorA': [255, 173, 222, 255], 'colorB': [54, 155, 88, 255]},
	1938: {'AssetId': 'NeutPhillipShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [51, 99], 'colorA': [70, 193, 202, 255], 'colorB': [94, 82, 83, 255]},
	2064: {'AssetId': 'NeutPinataShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [48, 98], 'colorA': [255, 85, 136, 255], 'colorB': [106, 206, 255, 255]},
	2255: {'AssetId': 'NeutPoopShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [42, 97], 'colorA': [100, 74, 70, 0], 'colorB': [0, 0, 0, 0]},
	2032: {'AssetId': 'NeutPopcornShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [46, 96], 'colorA': [241, 0, 0, 255], 'colorB': [62, 55, 64, 255]},
	2100: {'AssetId': 'NeutSafetyVestShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [50, 100], 'colorA': [255, 95, 11, 255], 'colorB': [250, 255, 53, 255]},
	2241: {'AssetId': 'NeutScaryPajamasShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [47, 97], 'colorA': [255, 255, 255, 0], 'colorB': [51, 60, 84, 0]},
	1880: {'AssetId': 'NeutScientistShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [52, 100], 'colorA': [73, 183, 82, 255], 'colorB': [133, 209, 205, 255]},
	2260: {'AssetId': 'NeutSnowManShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [48, 77], 'colorA': [255, 255, 255, 0], 'colorB': [167, 63, 63, 0]},
	2038: {'AssetId': 'NeutSoccerShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [57, 98], 'colorA': [170, 33, 58, 255], 'colorB': [115, 173, 75, 255]},
	2247: {'AssetId': 'NeutStrongwomanShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [50, 101], 'colorA': [114, 162, 67, 0], 'colorB': [70, 70, 70, 0]},
	2138: {'AssetId': 'NeutSuperGirlShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [23, 94], 'colorA': [47, 47, 49, 255], 'colorB': [85, 104, 183, 255]},
	1939: {'AssetId': 'NeutTandPShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [58, 98], 'colorA': [244, 244, 244, 255], 'colorB': [145, 182, 204, 255]},
	2227: {'AssetId': 'NeutTegridyShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [47, 91], 'colorA': [91, 77, 69, 0], 'colorB': [190, 206, 214, 0]},
	1937: {'AssetId': 'NeutTerranceShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [53, 98], 'colorA': [227, 42, 73, 255], 'colorB': [94, 82, 83, 255]},
	2089: {'AssetId': 'NeutTestDummyShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [50, 101], 'colorA': [255, 200, 47, 255], 'colorB': [185, 138, 45, 255]},
	1815: {'AssetId': 'NeutThugLifeShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [65, 98], 'colors': {'primary': ['magenta'],'secondary': ['lightblue'],'tertiary': ['red','black'],'skin': ['red']}, 'colorA': [255, 255, 255, 255], 'colorB': [87, 107, 171, 255]},
	1954: {'AssetId': 'NeutTowelieHateShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [57, 98], 'colorA': [244, 244, 244, 255], 'colorB': [204, 91, 108, 255]},
	1955: {'AssetId': 'NeutTowelieLoveShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [58, 99], 'colorA': [244, 244, 244, 255], 'colorB': [142, 180, 112, 255]},
	1932: {'AssetId': 'NeutValentinesDressShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [63, 97], 'colorA': [227, 34, 35, 255], 'colorB': [255, 255, 255, 0]},
	1934: {'AssetId': 'NeutValentinesSuitShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [52, 96], 'colorA': [227, 34, 35, 255], 'colorB': [255, 255, 255, 255]},
	1884: {'AssetId': 'NeutWaterBearShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [4, 88], 'colorA': [212, 187, 160, 255], 'colorB': [127, 180, 129, 255]},
	1903: {'AssetId': 'NeutXmasElfShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [52, 93], 'colorA': [113, 174, 101, 255], 'colorB': [241, 95, 95, 255]},
	1916: {'AssetId': 'NeutXmasReindeerShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [51, 99], 'colorA': [237, 66, 66, 255], 'colorB': [255, 255, 255, 255]},
	1907: {'AssetId': 'NeutXmasSweater2ShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [53, 99], 'colorA': [141, 211, 255, 255], 'colorB': [218, 74, 74, 255]},
	1900: {'AssetId': 'NeutXmasSweaterShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [47, 99], 'colorA': [233, 79, 79, 255], 'colorB': [87, 203, 131, 255]},
	1866: {'AssetId': 'SciAlien3ShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [49, 101], 'colorA': [92, 92, 92, 255], 'colorB': [255, 255, 255, 255]},
	1336: {'AssetId': 'SciAlienShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [52, 99], 'colorA': [186, 235, 91, 255], 'colorB': [62, 96, 89, 255]},
	194: {'AssetId': 'SciAstronautShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [45, 83], 'colorA': [108, 181, 255, 255], 'colorB': [255, 255, 255, 255]},
	2022: {'AssetId': 'SciCosmicShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [52, 102], 'colorA': [81, 75, 106, 255], 'colorB': [160, 160, 160, 255]},
	1283: {'AssetId': 'SciCyborgShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [44, 86], 'colorA': [78, 88, 125, 255], 'colorB': [255, 255, 255, 0]},
	1830: {'AssetId': 'SciFutureGuyShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [50, 102], 'colorA': [151, 98, 155, 255], 'colorB': [185, 233, 228, 255]},
	1851: {'AssetId': 'SciHazmatShirtBodyGearUI', 'Slot': 'Body', 'no_hands': True, 'mask_offset': [46, 100], 'colorA': [255, 234, 0, 255], 'colorB': [255, 234, 0, 255]},
	1756: {'AssetId': 'SciRobotShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [50, 100], 'colorA': [206, 200, 140, 255], 'colorB': [206, 200, 140, 255]},
	1980: {'AssetId': 'SciSpaceDudeShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [53, 95], 'colorA': [136, 195, 217, 255], 'colorB': [197, 120, 198, 255]},
	1945: {'AssetId': 'SciSpaceFighterShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [43, 101], 'colorA': [199, 199, 199, 255], 'colorB': [225, 56, 61, 255]},
	1970: {'AssetId': 'SciSpaceShipShirtBodyGearUI', 'Slot': 'Body', 'offset': [0, 40], 'mask_offset': [0, 86], 'colorA': [187, 146, 100, 255], 'colorB': [255, 255, 255, 255]},
	2048: {'AssetId': 'SciTronShirtBodyGearUI', 'Slot': 'Body', 'mask_offset': [42, 97], 'colorA': [35, 31, 36, 255], 'colorB': [255, 192, 0, 255]},
	
	#Head
	1853: {'AssetId': 'AdvBanditoHatHeadGearUI', 'Slot': 'Head', 'mask_offset': [22, 0], 'colorA': [174, 155, 120, 255], 'colorB': [77, 64, 42, 255]},
	1734: {'AssetId': 'AdvCowboy2HatHeadGearUI', 'Slot': 'Head', 'mask_offset': [20, 66], 'offset': [5, -40], 'colorA': [120, 95, 64, 255], 'colorB': [65, 46, 34, 255]},
	1863: {'AssetId': 'AdvCowGirl2HatHeadGearUI', 'Slot': 'Head', 'mask_offset': [34, 69], 'offset': [0, -35], 'colorA': [224, 222, 224, 255], 'colorB': [203, 46, 42, 255]},
	1855: {'AssetId': 'AdvCowGirlHatHeadGearUI', 'Slot': 'Head', 'mask_offset': [75, 82], 'offset': [0, -45], 'colorA': [244, 158, 157, 255], 'colorB': [255, 224, 130, 255]},
	2072: {'AssetId': 'AdvExplorerHatHeadGearUI', 'Slot': 'Head', 'mask_offset': [49, 80], 'offset': [0, 35], 'colorA': [164, 136, 102, 255], 'colorB': [255, 110, 68, 255]},
	2105: {'AssetId': 'AdvGladiator1HatHeadGearUI', 'Slot': 'Head', 'mask_offset': [70, 41], 'offset': [-14, -5], 'colorA': [228, 48, 25, 255], 'colorB': [91, 91, 91, 255]},
	2107: {'AssetId': 'AdvGladiator2HatHeadGearUI', 'Slot': 'Head', 'offset': [0, 75], 'colorA': [0, 0, 0, 0], 'colorB': [0, 0, 0, 0]},
	2076: {'AssetId': 'AdvMummyHatHeadGearUI', 'Slot': 'Head', 'mask_offset': [99, 140], 'offset': [0, 87], 'colorA': [237, 237, 237, 255], 'colorB': [0, 0, 0, 0]},
	1291: {'AssetId': 'AdvNinjaHatHeadGearUI', 'Slot': 'Head', 'mask_offset': [101, 141], 'offset': [0, 88], 'colors': {'primary': [], 'secondary': [], 'tertiary': ['red'], 'ignore': 'magenta'}, 'colorA': [79, 204, 173, 0], 'colorB': [104, 159, 223, 0]},
	1967: {'AssetId': 'AdvPeruvianHatHeadGearUI', 'Slot': 'Head', 'mask_offset': [91, 118], 'offset': [0, 45], 'colors': {'primary': ['magenta'], 'tertiary': ['green', 'red']}, 'colorA': [106, 125, 218, 255], 'colorB': [255, 220, 20, 255]},
	1876: {'AssetId': 'AdvPirate3HatHeadGearUI', 'Slot': 'Head', 'mask_offset': [33, 38], 'offset': [0, -40], 'colorA': [72, 72, 72, 255], 'colorB': [255, 236, 78, 255]},
	1267: {'AssetId': 'AdvPirateHatHeadGearUI', 'Slot': 'Head', 'mask_offset': [77, 123], 'offset': [-10, 0], 'colorA': [234, 34, 68, 255], 'colorB': [182, 21, 240, 0]},
	2061: {'AssetId': 'AdvSamuraiHatHeadGearUI', 'Slot': 'Head', 'mask_offset': [29, 65], 'offset': [-10, -30], 'colorA': [238, 58, 63, 255], 'colorB': [255, 247, 122, 255]},
	2322: {'AssetId': 'AdvFrontierHatHeadGearUI', 'Slot': 'Head', 'mask_offset': [66, 50], 'offset': [0, -30], 'colorA': [60, 54, 62, 0], 'colorB': [0, 0, 0, 0]},
	155: {'AssetId': 'DefaultHatHeadGearUI', 'Slot': 'Head', 'mask_offset': [39, 86], 'offset': [0, -70], 'colors': {'primary': ['green'], 'secondary': ['red'], 'tertiary': []}, 'colorA': [118, 93, 71, 255], 'colorB': [146, 122, 100, 255]},
	2011: {'AssetId': 'FanBarbarianHatHeadGearUI', 'Slot': 'Head', 'mask_offset': [56, 33], 'offset': [-5, -20], 'colors': {'tertiary': ['red', 'green', 'black']}, 'colorA': [160, 193, 220, 255], 'colorB': [255, 255, 255, 255]},
	1878: {'AssetId': 'FanDragonHatHeadGearUI', 'Slot': 'Head', 'mask_offset': [99, 97], 'offset': [0, 88], 'colorA': [116, 195, 129, 255], 'colorB': [153, 130, 185, 255]},
	1743: {'AssetId': 'FanDwarfGirlHatHeadGearUI', 'Slot': 'Head', 'offset': [0, -100], 'colorA': [0, 0, 0, 0], 'colorB': [0, 0, 0, 0]},
	1303: {'AssetId': 'FanDwarfHatHeadGearUI', 'Slot': 'Head', 'offset': [-45, -35], 'colorA': [255, 143, 87, 255], 'colorB': [255, 255, 255, 0]},
	2372: {'AssetId': 'FanElfetteHatHeadGearUI', 'Slot': 'Head', 'mask_offset': [103, 0], 'colorA': [209, 35, 44, 0], 'colorB': [255, 255, 255, 0]},
	1848: {'AssetId': 'FanElfGirlHatHeadGearUI', 'Slot': 'Head', 'mask_offset': [73, 162], 'offset': [0, 3], 'colors': {'primary': ['red'], 'secondary': [], 'tertiary': [], 'ignore': 'black'}, 'colorA': [255, 41, 117, 255], 'colorB': [113, 153, 197, 255]},
	1987: {'AssetId': 'FanElfHatHeadGearUI', 'Slot': 'Head', 'mask_offset': [68, 98], 'offset': [0, 5], 'colors': {'primary': ['red'], 'secondary': ['green'], 'tertiary': [], 'ignore': 'black'}, 'colorA': [27, 119, 53, 255], 'colorB': [135, 190, 60, 255]},
	1749: {'AssetId': 'FanFairyHatHeadGearUI', 'Slot': 'Head', 'offset': [-5, -130], 'colorA': [255, 76, 76, 255], 'colorB': [0, 0, 0, 0]},
	2027: {'AssetId': 'FanFaunHatHeadGearUI', 'Slot': 'Head', 'mask_offset': [52, 67], 'offset': [-2, 5], 'colors': {'primary': ['red'], 'secondary': ['green'], 'tertiary': [], 'ignore': 'black'}, 'colorA': [97, 80, 77, 255], 'colorB': [67, 67, 67, 255]},
	1857: {'AssetId': 'FanKnight2HatHeadGearUI', 'Slot': 'Head', 'mask_offset': [100, 72], 'offset': [0, 100], 'colorA': [225, 225, 225, 255], 'colorB': [255, 255, 255, 255]},
	1867: {'AssetId': 'FanKnightBrushHatHeadGearUI', 'Slot': 'Head', 'mask_offset': [102, 52], 'offset': [0, -100], 'colors': {'primary': ['magenta'], 'secondary': ['lightblue'], 'tertiary': ['green']}, 'colorA': [255, 104, 97, 255], 'colorB': [227, 227, 227, 255]},
	198: {'AssetId': 'FanKnightHatHeadGearUI', 'Slot': 'Head', 'mask_offset': [64, 54], 'colorA': [255, 62, 62, 255], 'colorB': [255, 255, 255, 0]},
	1752: {'AssetId': 'FanWitchHatHeadGearUI', 'Slot': 'Head', 'mask_offset': [23, 2], 'offset': [0, -100], 'colorA': [157, 147, 252, 255], 'colorB': [148, 112, 161, 255]},
	1859: {'AssetId': 'FanWizardHatHeadGearUI', 'Slot': 'Head', 'mask_offset': [12, 0], 'offset': [0, -80], 'colorA': [184, 102, 196, 255], 'colorB': [255, 206, 77, 255]},
	2353: {'AssetId': 'FanWizard2HatHeadGearUI', 'Slot': 'Head', 'mask_offset': [91, 12], 'offset': [0, -110], 'colorA': [174, 74, 198, 0], 'colorB': [255, 255, 255, 0], 'colors': {'primary': ['red'], 'secondary': ['green'], 'tertiary': []}},
	1812: {'AssetId': 'MysAncientGreekHatHeadGearUI', 'Slot': 'Head', 'mask_offset': [78, 127], 'offset': [0, -50], 'colors': {'primary': ['red'], 'secondary': ['green'], 'tertiary': []}, 'colorA': [255, 255, 255, 0], 'colorB': [255, 255, 255, 0]},
	2374: {'AssetId': 'MysArchangelHatHeadGearUI', 'Slot': 'Head', 'mask_offset': [90, 51], 'colorA': [255, 255, 255, 0], 'colorB': [255, 255, 255, 0]},
	1919: {'AssetId': 'MysCleopatraHatHeadGearUI', 'Slot': 'Head', 'mask_offset': [88, 82], 'offset': [0, 60], 'colors': {'primary': ['magenta'], 'secondary': ['lightblue'], 'tertiary': ['red']}, 'colorA': [255, 255, 255, 255], 'colorB': [238, 219, 82, 255]},
	2315: {'AssetId': 'MysDarkAngelHatHeadGearUI', 'Slot': 'Head', 'mask_offset': [74, 93], 'offset': [0, -15], 'colors': {'primary': ['magenta'], 'secondary': ['lightblue'], 'tertiary': ['green']}, 'colorA': [153, 73, 163, 0], 'colorB': [39, 39, 39, 0]},
	1861: {'AssetId': 'MysDarkPriestHatHeadGearUI', 'Slot': 'Head', 'offset': [0, -75], 'colorA': [0, 0, 0, 0], 'colorB': [0, 0, 0, 0]},
	1293: {'AssetId': 'MysGenieHatHeadGearUI', 'Slot': 'Head', 'mask_offset': [80, 63], 'offset': [-5, 50], 'colorA': [231, 187, 255, 255], 'colorB': [255, 255, 255, 0]},
	1747: {'AssetId': 'MysGreekGodHatHeadGearUI', 'Slot': 'Head', 'offset': [-5, -75], 'colorA': [0, 0, 0, 0], 'colorB': [0, 0, 0, 0]},
	181: {'AssetId': 'MysPopeHatHeadGearUI', 'Slot': 'Head', 'mask_offset': [91, 17], 'offset': [0, -95], 'colors': {'primary': ['red'], 'secondary': [], 'tertiary': [], 'ignore': 'black'}, 'colorA': [255, 214, 104, 255], 'colorB': [255, 255, 255, 0]},
	1921: {'AssetId': 'MysPriestHatHeadGearUI', 'Slot': 'Head', 'mask_offset': [0, 0], 'offset': [-2, -40], 'colors': {'primary': ['red'], 'secondary': [], 'tertiary': []}, 'colorA': [50, 47, 50, 255], 'colorB': [0, 0, 0, 0]},
	2083: {'AssetId': 'MysSatanicHatHeadGearUI', 'Slot': 'Head', 'mask_offset': [86, 81], 'offset': [5, -35], 'colors': {'primary': ['magenta', 'red'], 'secondary': [], 'tertiary': ['black']}, 'colorA': [222, 228, 230, 255], 'colorB': [0, 0, 0, 0]},
	1765: {'AssetId': 'MysVirginMaryHatHeadGearUI', 'Slot': 'Head', 'mask_offset': [72, 118], 'offset': [0, 120], 'colorA': [0, 0, 0, 0], 'colorB': [0, 0, 0, 0]},
	2009: {'AssetId': 'MysVoodooPriestHatHeadGearUI', 'Slot': 'Head', 'mask_offset': [47, 49], 'offset': [10, -60], 'colors': {'primary': ['red'], 'secondary': ['green'], 'tertiary': [], 'ignore': 'black'}, 'colorA': [79, 72, 82, 255], 'colorB': [148, 182, 56, 255]},
	2239: {'AssetId': 'NeutArcheologistHatHeadGearUI', 'Slot': 'Head', 'mask_offset': [38, 115], 'offset': [0, -25], 'colors': {'primary': ['magenta'], 'secondary': ['lightblue'], 'tertiary': ['green', 'red']}, 'colorA': [171, 174, 148, 0], 'colorB': [110, 107, 78, 0]},
	1757: {'AssetId': 'NeutBearHatHeadGearUI', 'Slot': 'Head', 'mask_offset': [62, 99], 'offset': [-5, -65], 'colors': {'primary': ['red'], 'secondary': ['green'], 'tertiary': []}, 'colorA': [135, 90, 68, 255], 'colorB': [178, 155, 141, 255]},
	2046: {'AssetId': 'NeutBirthdayHatHeadGearUI', 'Slot': 'Head', 'mask_offset': [159, 16], 'offset': [10, -90], 'colors': {'primary': ['red'], 'secondary': ['green'], 'tertiary': []}, 'colorA': [255, 216, 34, 255], 'colorB': [255, 30, 0, 255]},
	2304: {'AssetId': 'NeutBrainiacHatHeadGearUI', 'Slot': 'Head', 'mask_offset': [76, 48], 'offset': [2, 12], 'colorA': [39, 147, 87, 0], 'colorB': [170, 38, 153, 0]},
	1951: {'AssetId': 'NeutBubbleBathHatHeadGearUI', 'Slot': 'Head', 'offset': [20, -50], 'colorA': [255, 0, 0, 0], 'colorB': [255, 255, 255, 0]},
	2150: {'AssetId': 'NeutBucketBasherHatHeadGearUI', 'Slot': 'Head', 'mask_offset': [80, 126], 'offset': [0, 75], 'colorA': [255, 255, 255, 255], 'colorB': [209, 106, 217, 255]},
	2094: {'AssetId': 'NeutBuddhaBoxHatHeadGearUI', 'Slot': 'Head', 'offset': [0, 80], 'mask_offset': [79, 97], 'colors': {'primary': ['red'], 'secondary': ['green'], 'tertiary': [], 'ignore': 'black'}, 'colorA': [163, 138, 100, 255], 'colorB': [171, 27, 40, 255]},
	2294: {'AssetId': 'NeutBunnyHatHeadGearUI', 'Slot': 'Head', 'offset': [0, -100], 'mask_offset': [110, 0], 'colors': {'primary': ['red'], 'secondary': ['green'], 'tertiary': []}, 'colorA': [244, 244, 244, 0], 'colorB': [235, 187, 202, 0]},
	1835: {'AssetId': 'NeutButchHatHeadGearUI', 'Slot': 'Head', 'offset': [0, -30], 'mask_offset': [94, 96], 'colors': {'primary': ['magenta'], 'secondary': ['lightblue'], 'tertiary': ['green']}, 'colorA': [91, 46, 30, 255], 'colorB': [200, 55, 55, 255]},
	2320: {'AssetId': 'NeutChaos42HatHeadGearUI', 'Slot': 'Head', 'offset': [0, -15], 'mask_offset': [86, 80], 'colorA': [0, 0, 0, 0], 'colorB': [0, 0, 0, 0]},
	2243: {'AssetId': 'NeutChristmasTreeHatHeadGearUI', 'Slot': 'Head', 'offset': [0, -50], 'mask_offset': [60, 18], 'colors': {'primary': ['magenta'], 'secondary': ['lightblue'], 'tertiary': ['red']}, 'colorA': [127, 170, 89, 0], 'colorB': [255, 255, 255, 0]},
	2085: {'AssetId': 'NeutClownHatHeadGearUI', 'Slot': 'Head', 'offset': [70, -120], 'mask_offset': [176, 98], 'colors': {'primary': ['red'], 'secondary': ['green'], 'tertiary': [], 'ignore': 'black'}, 'colorA': [78, 66, 76, 255], 'colorB': [250, 77, 77, 255]},
	2341: {'AssetId': 'NeutCovidMaskHatHeadGearUI', 'Slot': 'Head', 'offset': [0, 95], 'mask_offset': [99, 253], 'colors': {'primary': ['red'], 'secondary': [], 'tertiary': [], 'ignore': 'green'}, 'colorA': [192, 235, 237, 0], 'colorB': [255, 255, 255, 0]},
	2288: {'AssetId': 'NeutCptCosmosHatHeadGearUI', 'Slot': 'Head', 'offset': [0, 25], 'mask_offset': [61, 100], 'colors': {'primary': ['magenta'], 'secondary': ['lightblue'], 'tertiary': ['yellow']}, 'colorA': [212, 208, 185, 0], 'colorB': [120, 120, 120, 0]},
	1930: {'AssetId': 'NeutCupidHatHeadGearUI', 'Slot': 'Head', 'offset': [10, -25], 'mask_offset': [21, 133], 'colors': {'primary': ['magenta'], 'secondary': ['lightblue'], 'tertiary': ['green']}, 'colorA': [253, 36, 66, 255], 'colorB': [151, 219, 100, 255]},
	2331: {'AssetId': 'NeutDandelionHatHeadGearUI', 'Slot': 'Head', 'offset': [0, 135], 'mask_offset': [54, 106], 'colors': {'primary': ['magenta'], 'secondary': [], 'tertiary': ['green'], 'ignore': 'lightblue'}, 'colorA': [255, 209, 61, 0], 'colorB': [148, 187, 81, 0]},
	2050: {'AssetId': 'NeutDayOfTheDeadHatHeadGearUI', 'Slot': 'Head', 'offset': [-10, 35], 'mask_offset': [0, 89], 'colors': {'primary': ['green'], 'secondary': ['red'], 'tertiary': ['black']}, 'colorA': [72, 61, 93, 255], 'colorB': [55, 55, 55, 255]},
	2232: {'AssetId': 'NeutFingerBang2HatHeadGearUI', 'Slot': 'Head', 'offset': [8, 45], 'mask_offset': [103, 132], 'colorA': [255, 255, 255, 0], 'colorB': [192, 12, 15, 0]},
	2228: {'AssetId': 'NeutFingerBangHatHeadGearUI', 'Slot': 'Head', 'offset': [5, 45], 'mask_offset': [103, 112], 'colorA': [250, 250, 249, 0], 'colorB': [74, 192, 190, 0]},
	2154: {'AssetId': 'NeutFirezoneHatHeadGearUI', 'Slot': 'Head', 'offset': [-15, 30], 'mask_offset': [64, 61], 'colors': {'primary': ['red'], 'secondary': ['green'], 'tertiary': [], 'ignore': 'black'}, 'colorA': [238, 47, 44, 255], 'colorB': [247, 199, 27, 255]},
	1985: {'AssetId': 'NeutFourthOfJulyHatHeadGearUI', 'offset': [0, -50], 'Slot': 'Head', 'mask_offset': [51, 66], 'colorA': [247, 51, 51, 255], 'colorB': [110, 125, 224, 255]},
	2235: {'AssetId': 'NeutGooManHatHeadGearUI', 'Slot': 'Head', 'offset': [0, -50], 'mask_offset': [28, 83], 'colorA': [103, 85, 60, 0], 'colorB': [129, 109, 81, 0]},
	2059: {'AssetId': 'NeutHempHatHeadGearUI', 'Slot': 'Head', 'offset': [0, 45], 'mask_offset': [85, 27], 'colorA': [78, 76, 140, 255], 'colorB': [255, 255, 255, 255]},
	2075: {'AssetId': 'NeutHockeyMaskHatHeadGearUI', 'Slot': 'Head', 'offset': [0, 100], 'mask_offset': [101, 148], 'colors': {'primary': ['red'], 'secondary': [], 'tertiary': [], 'ignore': 'black'}, 'colorA': [255, 255, 255, 255], 'colorB': [52, 45, 53, 255]},
	2219: {'AssetId': 'NeutICEHatHeadGearUI', 'Slot': 'Head', 'offset': [0, -18], 'mask_offset': [102, 101], 'colorA': [47, 57, 82, 0], 'colorB': [0, 0, 0, 0]},
	2070: {'AssetId': 'NeutJesterHatHeadGearUI', 'Slot': 'Head', 'offset': [0, -60], 'mask_offset': [64, 96], 'colors': {'primary': ['magenta'], 'secondary': ['lightblue'], 'tertiary': ['green']}, 'colorA': [59, 243, 114, 255], 'colorB': [79, 174, 255, 255]},
	2369: {'AssetId': 'NeutKiteHatHeadGearUI', 'Slot': 'Head', 'offset': [0, 0], 'mask_offset': [80, 125], 'colors': {'primary': ['magenta'], 'secondary': ['lightblue'], 'tertiary': ['green']}, 'colorA': [255, 255, 255, 0], 'colorB': [97, 170, 204, 0]},
	1816: {'AssetId': 'NeutLuchadorHatHeadGearUI', 'Slot': 'Head', 'offset': [-1, 83], 'mask_offset': [95, 140], 'colorA': [152, 217, 228, 255], 'colorB': [228, 73, 73, 255]},
	1827: {'AssetId': 'NeutManBearPigHatHeadGearUI', 'Slot': 'Head', 'offset': [-3, 38], 'mask_offset': [82, 101], 'colors': {'primary': ['magenta', 'red'], 'secondary': [], 'tertiary': ['black']}, 'colorA': [247, 169, 169, 255], 'colorB': [0, 0, 0, 0]},
	2055: {'AssetId': 'NeutMasgueradeHatHeadGearUI', 'Slot': 'Head', 'offset': [-12, 38], 'mask_offset': [38, 158], 'colors': {'primary': ['red'], 'secondary': ['green'], 'tertiary': [], 'ignore': 'black'}, 'colorA': [255, 255, 255, 255], 'colorB': [135, 29, 29, 255]},
	2351: {'AssetId': 'NeutMonsterHatHeadGearUI', 'Slot': 'Head', 'mask_offset': [63, 97], 'offset': [-5, -50], 'colorA': [136, 195, 89, 0], 'colorB': [52, 46, 51, 0]},
	2103: {'AssetId': 'NeutPeacockHat_Head_Wear_Front', 'Slot': 'Head', 'offset': [0, 10], 'mask_offset': [89, 154], 'colors': {'primary': ['softred'], 'secondary': ['softgreen'], 'tertiary': []}, 'colorA': [228, 228, 228, 255], 'colorB': [190, 190, 190, 190]},
	2063: {'AssetId': 'NeutPinataHatHeadGearUI', 'Slot': 'Head', 'offset': [0, -60], 'mask_offset': [54, 64], 'colors': {'primary': ['red'], 'secondary': ['green'], 'tertiary': [], 'ignore': 'black'}, 'colorA': [255, 111, 154, 255], 'colorB': [106, 206, 255, 255]},
	2253: {'AssetId': 'NeutPoopHatHeadGearUI', 'Slot': 'Head', 'offset': [0, -30], 'mask_offset': [95, 29], 'colorA': [100, 74, 70, 0], 'colorB': [0, 0, 0, 0]},
	2031: {'AssetId': 'NeutPopcornHatHeadGearUI', 'Slot': 'Head', 'alpha': True, 'offset': [-2, 10], 'mask_offset': [86, 220], 'colors': {'primary': ['red'], 'secondary': ['green'], 'tertiary': [], 'ignore': 'black'}, 'colorA': [255, 0, 168, 255], 'colorB': [0, 174, 255, 255]},
	1961: {'AssetId': 'NeutPropellerHatHeadGearUI', 'Slot': 'Head', 'mask_offset': [93, 64], 'offset': [0, -40], 'colorA': [230, 79, 60, 255], 'colorB': [255, 250, 2, 255]},
	2350: {'AssetId': 'NeutPumpkinHatHeadGearUI', 'Slot': 'Head', 'mask_offset': [75, 103], 'offset': [2, 90], 'colorA': [255, 125, 20, 0], 'colorB': [0, 0, 0, 0], 'colors': {'primary': ['red'], 'secondary': [], 'tertiary': [], 'ignore': 'black'}},
	2051: {'AssetId': 'NeutSailorHatHeadGearUI', 'Slot': 'Head', 'mask_offset': [102, 96], 'offset': [0, -90], 'colorA': [65, 65, 65, 255], 'colorB': [255, 255, 255, 0]},
	1882: {'AssetId': 'NeutScientistHatHeadGearUI', 'Slot': 'Head', 'offset': [0, 15], 'colorA': [0, 0, 0, 0], 'colorB': [0, 0, 0, 0]},
	2259: {'AssetId': 'NeutSnowManHatHeadGearUI', 'Slot': 'Head', 'offset': [0, 110], 'mask_offset': [96, 53], 'colorA': [255, 255, 255, 0], 'colorB': [167, 63, 63, 0]},
	2082: {'AssetId': 'NeutSpecialBoyHatHeadGearUI', 'Slot': 'Head', 'offset': [0, -60], 'mask_offset': [95, 50], 'colorA': [241, 209, 108, 255], 'colorB': [160, 12, 46, 255]},
	2246: {'AssetId': 'NeutStrongwomanHatHeadGearUI', 'Slot': 'Head', 'offset': [0, 69], 'mask_offset': [87, 158], 'colorA': [196, 101, 190, 0], 'colorB': [255, 255, 255, 0]},
	2226: {'AssetId': 'NeutTegridyHatHeadGearUI', 'Slot': 'Head', 'offset': [-3, -35], 'mask_offset': [26, 118], 'colorA': [203, 171, 89, 0], 'colorB': [93, 69, 64, 0]},
	2088: {'AssetId': 'NeutTestDummyHatHeadGearUI', 'Slot': 'Head', 'offset': [0, 5], 'mask_offset': [89, 120], 'colorA': [192, 179, 99, 255], 'colorB': [66, 64, 69, 255]},
	1883: {'AssetId': 'NeutWaterBearHatHeadGearUI', 'Slot': 'Head', 'offset': [0, 130], 'mask_offset': [100, 135], 'colorA': [212, 187, 160, 255], 'colorB': [212, 187, 160, 255]},
	1902: {'AssetId': 'NeutXmasElfHatHeadGearUI', 'Slot': 'Head', 'offset': [0, -60], 'mask_offset': [97, 5], 'colors': {'primary': ['red'], 'secondary': ['green'], 'tertiary': [], 'ignore': 'black'}, 'colorA': [113, 174, 101, 255], 'colorB': [241, 95, 95, 255]},
	1915: {'AssetId': 'NeutXmasReindeerHatHeadGearUI', 'Slot': 'Head', 'offset': [0, -50], 'mask_offset': [69, 50], 'colors': {'primary': ['magenta'], 'secondary': ['lightblue'], 'tertiary': ['black', 'green'], 'ignore': 'magenta'}, 'colorA': [159, 184, 78, 255], 'colorB': [233, 65, 65, 255]},
	1906: {'AssetId': 'NeutXmasSweater2HatHeadGearUI', 'Slot': 'Head', 'offset': [0, -60], 'mask_offset': [17, 26], 'colors': {'primary': ['red'], 'secondary': ['green'], 'tertiary': [], 'ignore': 'black'}, 'colorA': [160, 125, 101, 255], 'colorB': [218, 74, 74, 255]},
	1899: {'AssetId': 'NeutXmasSweaterHatHeadGearUI', 'Slot': 'Head', 'offset': [-20, -20], 'mask_offset': [58, 55], 'colors': {'primary': ['magenta'], 'secondary': ['lightblue'], 'tertiary': ['red', 'green']}, 'colorA': [204, 70, 70, 255], 'colorB': [255, 255, 255, 255]},
	1814: {'AssetId': 'NeutThugLifeHatHeadGearUI', 'Slot': 'Head', 'offset': [0, -60], 'mask_offset': [99, 59], 'colors': {'primary': ['red'], 'secondary': ['green'], 'tertiary': [], 'ignore': 'black'}, 'colorA': [63, 63, 63, 255], 'colorB': [228, 58, 58, 255]},
	1865: {'AssetId': 'SciAlien3HatHeadGearUI', 'Slot': 'Head', 'offset': [0, 150], 'mask_offset': [95, 99], 'colors': {'primary': ['red'], 'secondary': ['green'], 'tertiary': [], 'ignore': 'black'}, 'colorA': [92, 92, 92, 255], 'colorB': [255, 255, 255, 255]},
	1337: {'AssetId': 'SciAlienHatHeadGearUI', 'Slot': 'Head', 'offset': [0, -20], 'mask_offset': [72, 58], 'colors': {'primary': ['red'], 'secondary': ['green'], 'tertiary': [], 'ignore': 'black'}, 'colorA': [186, 235, 91, 255], 'colorB': [222, 255, 89, 255]},
	195: {'AssetId': 'SciAstronautHatHeadGearUI', 'Slot': 'Head', 'offset': [0, 100], 'mask_offset': [87, 134], 'colorA': [104, 187, 255, 255], 'colorB': [255, 255, 255, 0]},
	2021: {'AssetId': 'SciCosmicHatHeadGearUI', 'Slot': 'Head', 'offset': [-10, 0], 'mask_offset': [42, 31], 'colors': {'primary': ['magenta'], 'secondary': ['lightblue'], 'tertiary': ['green', 'black']}, 'colorA': [147, 203, 255, 255], 'colorB': [255, 255, 255, 255]},
	1285: {'AssetId': 'SciCyborgHatHeadGearUI', 'Slot': 'Head', 'offset': [5, 60], 'mask_offset': [101, 76], 'colorA': [255, 236, 77, 255], 'colorB': [255, 113, 114, 255]},
	1831: {'AssetId': 'SciFutureGuyHatHeadGearUI', 'Slot': 'Head', 'offset': [-10, 60], 'mask_offset': [15, 53], 'colorA': [151, 98, 155, 255], 'colorB': [255, 56, 56, 255]},
	1850: {'AssetId': 'SciHazmatHatHeadGearUI', 'Slot': 'Head', 'mask_offset': [96, 113], 'offset': [0, 136], 'colorA': [255, 234, 0, 255], 'colorB': [255, 255, 255, 255]},
	1755: {'AssetId': 'SciRobotHatHeadGearUI', 'Slot': 'Head', 'offset': [0, 60], 'mask_offset': [77, 128], 'colorA': [255, 255, 255, 0], 'colorB': [243, 234, 89, 255]},
	1979: {'AssetId': 'SciSpaceDudeHatHeadGearUI', 'Slot': 'Head', 'mask_offset': [82, 98], 'offset': [0, 30], 'colors': {'primary': ['red'], 'secondary': ['green'], 'tertiary': [], 'ignore': 'black'}, 'colorA': [255, 255, 255, 255], 'colorB': [69, 178, 201, 255]},
	1944: {'AssetId': 'SciSpaceFighterHatHeadGearUI', 'Slot': 'Head', 'offset': [15, 50], 'mask_offset': [101, 103], 'colors': {'primary': ['magenta'], 'secondary': ['lightblue'], 'tertiary': ['green']}, 'colorA': [217, 85, 75, 255], 'colorB': [220, 219, 220, 255]},
	1969: {'AssetId': 'SciSpaceShipHatHeadGearUI', 'Slot': 'Head', 'alpha': True, 'offset': [0, 65], 'mask_offset': [86, 121], 'colors': {'primary': ['red'], 'secondary': ['green'], 'tertiary': []}, 'colorA': [109, 102, 255, 255], 'colorB': [59, 59, 59, 255]},
	2047: {'AssetId': 'SciTronHatHeadGearUI', 'Slot': 'Head', 'mask_offset': [78, 105], 'colorA': [200, 27, 27, 255], 'colorB': [255, 192, 0, 255]},
	
	#Default Hand
	1: {'AssetId': 'SciHazmatShirt_Hand_LeftRight_Wear_2', 'Slot': 'Hand'}
	
	#MISSING
	#MISSING #1556: {   "AssetId": "DefaultShirtBodyGearUI",  "Slot": "Body", 'mask_offset': [50,88] }, #female
	#MISSING #1940: {   "AssetId": "NeutMountieShirtBodyGearUI",  "Slot": "Body", 'mask_offset': [0,0] },
	#MISSING #2037: {   "AssetId": "NeutPantherShirtBodyGearUI",  "Slot": "Body", 'mask_offset': [0,0] },
	#MISSING #1942: {   "AssetId": "NeutMountieHatHeadGearUI",  "Slot": "Head", 'mask_offset': [0,0] },
	#MISSING #2036: {   "AssetId": "NeutPantherHatHeadGearUI",  "Slot": "Head", 'mask_offset': [0,0] },
}

OUTFIT_MAP = {
	#Hair
	1540: {   "AssetId": "LongBasicHairUI",  "Slot": "Hair", 'offset': [0,-2] },
	1605: {   "AssetId": "LongPigtailsHairUI",  "Slot": "Hair", 'offset': [-6,-25] },
	1606: {   "AssetId": "LongSeventiesHairUI",  "Slot": "Hair", 'offset': [0,-20] },
	1607: {   "AssetId": "LongStraightenedHairUI",  "Slot": "Hair", 'offset': [1,-15] },
	1608: {   "AssetId": "LongWavyHairUI",  "Slot": "Hair", 'offset': [0,-15] },
	1609: {   "AssetId": "MediumBabygirlHairUI",  "Slot": "Hair", 'offset': [0,-15] },
	1610: {   "AssetId": "MediumEllenHairUI",  "Slot": "Hair", 'offset': [0,-25] },
	1611: {   "AssetId": "MediumRockstarHairUI",  "Slot": "Hair", 'offset': [0,-20] },
	1612: {   "AssetId": "MediumSkaterHairUI",  "Slot": "Hair", 'offset': [0,-10] },
	1552: {   "AssetId": "MediumTiedrastasHairUI",  "Slot": "Hair", 'offset': [3,-20] },
	1613: {   "AssetId": "MediumVidalsassoonHairUI",  "Slot": "Hair" },
	1623: {   "AssetId": "MediumWavyHairUI",  "Slot": "Hair", 'offset': [0,-5] },
	1792: {   "AssetId": "ShortAfropigtailsHairUI",  "Slot": "Hair", 'offset': [2,0] },
	1614: {   "AssetId": "ShortBeatlesHairUI",  "Slot": "Hair" },
	1615: {   "AssetId": "ShortClarkkentHairUI",  "Slot": "Hair", 'offset': [0,-10] },
	1616: {   "AssetId": "ShortCurlyHairUI",  "Slot": "Hair", 'offset': [0,-15]},
	1617: {   "AssetId": "ShortDavidlynchHairUI",  "Slot": "Hair", 'offset': [1,-10] },
	1618: {   "AssetId": "ShortGrandmaHairUI",  "Slot": "Hair", 'offset': [7,-30] },
	1619: {   "AssetId": "ShortGrandpaHairUI",  "Slot": "Hair", 'scale': 0.50, 'offset': [0,20] },
	1620: {   "AssetId": "ShortSpikewavyHairUI",  "Slot": "Hair", 'offset': [10,-8] },
	1621: {   "AssetId": "ShortSurferHairUI",  "Slot": "Hair", 'offset': [0,-15] },
	1793: {   "AssetId": "ShortTrekkieHairUI",  "Slot": "Hair" },
	
	#Eyebrows
	1773: {   "AssetId": "AngelinaEyebrowsUI",  "Slot": "Eyebrows" },
	1548: {   "AssetId": "AngryEyebrowsUI",  "Slot": "Eyebrows"},
	1774: {   "AssetId": "AnnoyedEyebrowsUI",  "Slot": "Eyebrows"},
	1775: {   "AssetId": "BushyEyebrowsUI",  "Slot": "Eyebrows"},
	1776: {   "AssetId": "ChiselledEyebrowsUI",  "Slot": "Eyebrows"},
	1564: {   "AssetId": "ClassicthickEyebrowsUI",  "Slot": "Eyebrows"},
	1565: {   "AssetId": "PuzzledEyebrowsUI",  "Slot": "Eyebrows" },
	1777: {   "AssetId": "RandyEyebrowsUI",  "Slot": "Eyebrows" },
	1566: {   "AssetId": "SadhappyEyebrowsUI",  "Slot": "Eyebrows" },
	1778: {   "AssetId": "SluttyEyebrowsUI",  "Slot": "Eyebrows" },
	1545: {   "AssetId": "SuspiciousEyebrowsUI",  "Slot": "Eyebrows" },
	1779: {   "AssetId": "SympatheticEyebrowsUI",  "Slot": "Eyebrows" },
	1780: {   "AssetId": "UnibrowEyebrowsUI",  "Slot": "Eyebrows" },
	
	#Eyes
	1781: {   "AssetId": "AngelinaEyesUI",  "Slot": "Eyes" },
	1568: {   "AssetId": "AsianEyesUI",  "Slot": "Eyes", "offset" : [0,0] },
	1635: {   "AssetId": "AsianGirlEyesUI",  "Slot": "Eyes", "offset" : [0,0] },
	1554: {   "AssetId": "BasicEyesUI",  "Slot": "Eyes" },
	1782: {   "AssetId": "BlackEyesUI",  "Slot": "Eyes" },
	1783: {   "AssetId": "BlackshadowEyesUI",  "Slot": "Eyes" },
	1543: {   "AssetId": "CrazyEyesUI",  "Slot": "Eyes" },
	1569: {   "AssetId": "EyelinerEyesUI",  "Slot": "Eyes" },
	1784: {   "AssetId": "HenriettaEyesUI",  "Slot": "Eyes" },
	1572: {   "AssetId": "LashesOneEyesUI",  "Slot": "Eyes" },
	1785: {   "AssetId": "LashesThreeEyesUI",  "Slot": "Eyes" },
	1786: {   "AssetId": "LashesTwoEyesUI",  "Slot": "Eyes" },
	1549: {   "AssetId": "NervousEyesUI",  "Slot": "Eyes" },
	1787: {   "AssetId": "PinkshadowEyesUI",  "Slot": "Eyes" },
	1788: {   "AssetId": "PopeEyesUI",  "Slot": "Eyes" },
	1570: {   "AssetId": "RedEyesUI",  "Slot": "Eyes" },
	1571: {   "AssetId": "SleepyEyesUI",  "Slot": "Eyes" },
	1789: {   "AssetId": "SneezeEyesUI",  "Slot": "Eyes" },
	1790: {   "AssetId": "SquintyEyesUI",  "Slot": "Eyes" },
	1791: {   "AssetId": "TearyEyesUI",  "Slot": "Eyes" },
	
	#Glasses
	1551: {   "AssetId": "BatmanGlassesUI",  "Slot": "Glasses", 'offset': [5,6] },
	1589: {   "AssetId": "CoffinGlassesUI",  "Slot": "Glasses" },
	1590: {   "AssetId": "DougieGlassesUI",  "Slot": "Glasses" },
	2174: {   "AssetId": "DrBadMaskGlassesUI",  "Slot": "Glasses", 'offset': [4,0] },
	1542: {   "AssetId": "KittyGlassesUI",  "Slot": "Glasses", 'offset': [1,4] },
	1591: {   "AssetId": "KittyShinyGlassesUI",  "Slot": "Glasses", 'offset': [1,4] },
	1592: {   "AssetId": "MalcomxGlassesUI",  "Slot": "Glasses", 'offset': [5,6] },
	1593: {   "AssetId": "MonocleGlassesUI",  "Slot": "Glasses", 'offset': [60,10] },
	1892: {   "AssetId": "PcnessGlassesUI",  "Slot": "Glasses", 'offset': [2,5] },
	1594: {   "AssetId": "RectangleGlassesUI",  "Slot": "Glasses", 'offset': [0,10] },
	1595: {   "AssetId": "RectangleShinyGlassesUI",  "Slot": "Glasses", 'offset': [0,10] },
	1917: {   "AssetId": "RudolphGlassesUI",  "Slot": "Glasses", "offset" : [0,40] },
	1596: {   "AssetId": "ShadesBasicGlassesUI",  "Slot": "Glasses", "offset" : [0,10] },
	1597: {   "AssetId": "ShadesOvalGlassesUI",  "Slot": "Glasses" },
	1598: {   "AssetId": "ShadesSuperstarGlassesUI",  "Slot": "Glasses", 'offset': [-1,6] },
	1599: {   "AssetId": "SpectaclesGlassesUI",  "Slot": "Glasses", 'offset': [3,4] },
	1600: {   "AssetId": "SpectaclesShinyGlassesUI",  "Slot": "Glasses", 'offset': [3,4] },
	2173: {   "AssetId": "SuperGirlMaskGlassesUI",  "Slot": "Glasses" },
	1601: {   "AssetId": "ThinGlassesUI",  "Slot": "Glasses", 'offset': [3,4] },
	1602: {   "AssetId": "ThinShinyGlassesUI",  "Slot": "Glasses", 'offset': [3,4] },
	1603: {   "AssetId": "WireframeGlassesUI",  "Slot": "Glasses" },
	1604: {   "AssetId": "WireframeSquareGlassesUI",  "Slot": "Glasses" },
	
	#Mouth
	1794: {   "AssetId": "AngelinaMouthUI",  "Slot": "Mouth" },
	1795: {   "AssetId": "BarfMouthUI",  "Slot": "Mouth" },
	1624: {   "AssetId": "BitelipMouthUI",  "Slot": "Mouth" },
	1796: {   "AssetId": "BurgundyMouthUI",  "Slot": "Mouth" },
	1625: {   "AssetId": "CrapMouthUI",  "Slot": "Mouth" },
	1555: {   "AssetId": "DefaultMouthUI",  "Slot": "Mouth" },
	1797: {   "AssetId": "FatMouthUI",  "Slot": "Mouth" },
	1798: {   "AssetId": "HenriettaMouthUI",  "Slot": "Mouth" },
	1541: {   "AssetId": "IckMouthUI",  "Slot": "Mouth" },
	1626: {   "AssetId": "LolMouthUI",  "Slot": "Mouth" },
	1640: {   "AssetId": "MomMouthUI",  "Slot": "Mouth" },
	1799: {   "AssetId": "NutgobblerMouthUI",  "Slot": "Mouth" },
	1627: {   "AssetId": "OhMouthUI",  "Slot": "Mouth" },
	1553: {   "AssetId": "OpenMouthUI",  "Slot": "Mouth" },
	1800: {   "AssetId": "PursedMouthUI",  "Slot": "Mouth" },
	1628: {   "AssetId": "SmirkMouthUI",  "Slot": "Mouth" },
	1801: {   "AssetId": "SurprisedMouthUI",  "Slot": "Mouth" },
	1802: {   "AssetId": "ThinMouthUI",  "Slot": "Mouth" },
	1803: {   "AssetId": "UglyMouthUI",  "Slot": "Mouth" },
	
	#FacialHair
	1573: {   "AssetId": "BeardJaakkoFacialHairUI",  "Slot": "FacialHair", 'offset': [0,30] },
	1574: {   "AssetId": "BeardKlingonFacialHairUI",  "Slot": "FacialHair", 'offset': [-1,15] },
	1575: {   "AssetId": "BeardMediumFacialHairUI",  "Slot": "FacialHair", 'offset': [0,28] },
	1896: {   "AssetId": "BeardPcnessFacialHairUI",  "Slot": "FacialHair", 'offset': [0,30] },
	1576: {   "AssetId": "BeardPetitegoateeFacialHairUI",  "Slot": "FacialHair", 'offset': [0,25] },
	1544: {   "AssetId": "BeardSantaFacialHairUI",  "Slot": "FacialHair", 'offset': [-5,24] },
	1577: {   "AssetId": "BeardSmallFacialHairUI",  "Slot": "FacialHair", 'offset': [0,30] },
	1578: {   "AssetId": "BeardThinFacialHairUI",  "Slot": "FacialHair", 'offset': [2,22] },
	1579: {   "AssetId": "MoustacheBasicFacialHairUI",  "Slot": "FacialHair", 'offset': [0,-35] },
	1550: {   "AssetId": "MoustacheChineseFacialHairUI",  "Slot": "FacialHair", 'offset': [0,35] },
	1580: {   "AssetId": "MoustacheFrenchFacialHairUI",  "Slot": "FacialHair", 'offset': [0,-40] },
	1581: {   "AssetId": "MoustacheGentlemanFacialHairUI",  "Slot": "FacialHair" },
	2340: {   "AssetId": "MoustacheRandyFacialHairUI",  "Slot": "FacialHair", 'offset': [0,-35] },
	1582: {   "AssetId": "MoustacheSpanishFacialHairUI",  "Slot": "FacialHair", 'offset': [0,-5] },
	1583: {   "AssetId": "MoustacheThickFacialHairUI",  "Slot": "FacialHair", 'offset': [0,-40] },
	1584: {   "AssetId": "MoustacheVillainFacialHairUI",  "Slot": "FacialHair", 'offset': [-5,30] },
	1639: {   "AssetId": "MoustacheWhiskersFacialHairUI",  "Slot": "FacialHair", 'offset': [0,-40] },
	1585: {   "AssetId": "MuttonchopsThickFacialHairUI",  "Slot": "FacialHair" },
	1586: {   "AssetId": "StubbleBasicFacialHairUI",  "Slot": "FacialHair", 'offset': [5,0], 'alpha': True },
	1587: {   "AssetId": "StubbleBeardedFacialHairUI",  "Slot": "FacialHair", 'offset': [0,8], 'alpha': True },
	1588: {   "AssetId": "StubbleThickFacialHairUI",  "Slot": "FacialHair", 'offset': [16,7], 'alpha': True },
	
	#Detail
	1558: {   "AssetId": "BandaidLeftDetailUI",  "Slot": "Detail", 'offset': [-70,55] },
	1768: {   "AssetId": "BeautyspotDetailUI",  "Slot": "Detail", 'offset': [50,65] },
	1769: {   "AssetId": "BloodDetailUI",  "Slot": "Detail", 'offset': [-10,30] },
	1668: {   "AssetId": "BlushDetailUI",  "Slot": "Detail", 'offset': [0,60] },
	1770: {   "AssetId": "BowieDetailUI",  "Slot": "Detail", 'offset': [0,-10] },
	1669: {   "AssetId": "BruiseRightDetailUI",  "Slot": "Detail", 'offset': [70,70] },
	1561: {   "AssetId": "CutRightDetailUI",  "Slot": "Detail", 'offset': [70,70] },
	1562: {   "AssetId": "FootballDetailUI",  "Slot": "Detail", 'offset': [0,45] },
	1546: {   "AssetId": "FrecklesLowDetailUI",  "Slot": "Detail", 'offset': [0,30] },
	1771: {   "AssetId": "GingerDetailUI",  "Slot": "Detail" },
	1560: {   "AssetId": "PenisDetailUI",  "Slot": "Detail", 'offset': [-5,30] },
	1912: {   "AssetId": "PooDetailUI",  "Slot": "Detail" },
	1547: {   "AssetId": "StitchesRightDetailUI",  "Slot": "Detail", 'offset': [60,60] },
	1772: {   "AssetId": "VaginaballsDetailUI",  "Slot": "Detail", 'offset': [-60,50] },
}

COLOR_MAP = {
1346 : 'ffffa559', #ultraorange
1347 : 'ff774733', #tampico
1348 : 'ff645859', #graphite
1349 : 'ff8c8d9f', #slate
1350 : 'fffffdfb', #ultimateWhite
1351 : 'ff727d68', #seaMist
1352 : 'ff269d3a', #green
1353 : 'ff38406c', #midnight
1354 : 'ffff84da', #ultraMelon
1355 : 'fffa0f84', #rasberry
1356 : 'ff6e243d', #cranberry
1357 : 'ffc41020', #redPepper
1358 : 'ffef8c90', #clit
1359 : 'ffff6012', #orange
1360 : 'ffa567b8', #violet
1361 : 'ffc4602a', #dirt
1362 : 'ff4e3328', #fudge
1363 : 'ff6e5639', #wood
1364 : 'ff5467a5', #seabrightblue
1365 : 'ff9d6e20', #curry
1366 : 'ff57c725', #springGreen
1367 : 'ffffc00d', #gold
1368 : 'ff2c242c', #black
1372 : 'ff8ddfee', #ultraBlue
1377 : 'ff15ad9d', #seaBlue
1379 : 'ff0c6f64', #marinaTeal
1380 : 'ffecd38e', #wheat
}

# WAL MAP for API
WAL_MAP={}
WAL_MAP[0]=[0,0]
WAL_MAP[1]=[0,5]
WAL_MAP[2]=[5,15]
WAL_MAP[3]=[15,25]
WAL_MAP[4]=[25,40]
WAL_MAP[5]=[40,55]
WAL_MAP[6]=[55,70]
WAL_MAP[7]=[70,70]

CAPS_PER_RARITY={}
CAPS_PER_RARITY["com"]=[0,0,0,0,100, 275, 575]
CAPS_PER_RARITY["rar"]=[0,0,0,125, 325, 650, 1075]
CAPS_PER_RARITY["epi"]=[0,0,175, 425, 800, 1275, 1825]
CAPS_PER_RARITY["leg"]=[0,200, 475, 875, 1375, 1950, 2575]

# { Rarity : { level-upgrade : [coins, bronze, silver, gold, copies, experience], ... }, ... }
UPGRADE_COSTS={
"Common" :
	{
		"1-1" : [0, 0, 0, 0, 0, 0],
		"1-2" : [15, 1, 0, 0, 0, 2],
		"1-3" : [30, 2, 0, 0, 0, 2],
		"1-4" : [45, 3, 0, 0, 0, 2],
		"1-5" : [60, 4, 0, 0, 0, 2],
		"2-5" : [100, 0, 0, 0, 5, 20],
		"2-6" : [20, 1, 0, 0, 0, 4],
		"2-7" : [40, 2, 1, 0, 0, 4],
		"2-8" : [60, 3, 1, 0, 0, 4],
		"2-9" : [80, 4, 2, 0, 0, 4],
		"2-10" : [120, 5, 2, 0, 0, 4],
		"2-11" : [130, 5, 3, 0, 0, 4],
		"2-12" : [140, 6, 3, 0, 0, 4],
		"2-13" : [150, 7, 4, 0, 0, 4],
		"2-14" : [160, 8, 4, 0, 0, 4],
		"2-15" : [170, 9, 5, 0, 0, 4],
		"3-15" : [500, 0, 0, 0, 10, 50],
		"3-16" : [25, 2, 1, 0, 0, 6],
		"3-17" : [55, 3, 2, 0, 0, 6],
		"3-18" : [80, 5, 2, 0, 0, 6],
		"3-19" : [105, 6, 3, 1, 0, 6],
		"3-20" : [160, 7, 3, 1, 0, 6],
		"3-21" : [170, 8, 4, 1, 0, 6],
		"3-22" : [185, 10, 4, 1, 0, 6],
		"3-23" : [200, 12, 5, 2, 0, 6],
		"3-24" : [210, 13, 5, 2, 0, 6],
		"3-25" : [225, 14, 6, 2, 0, 6],
		"4-25" : [1000, 0, 0, 0, 50, 100],
		"4-26" : [55, 3, 1, 0, 0, 8],
		"4-27" : [110, 5, 2, 1, 0, 8],
		"4-28" : [165, 7, 3, 1, 0, 8],
		"4-29" : [220, 9, 3, 1, 0, 8],
		"4-30" : [330, 10, 4, 1, 0, 8],
		"4-31" : [360, 11, 4, 2, 0, 8],
		"4-32" : [385, 12, 5, 2, 0, 8],
		"4-33" : [415, 13, 5, 2, 0, 8],
		"4-34" : [440, 14, 7, 3, 0, 8],
		"4-35" : [470, 15, 7, 3, 0, 8],
		"4-36" : [495, 16, 10, 3, 0, 8],
		"4-37" : [515, 17, 10, 4, 0, 8],
		"4-38" : [530, 20, 12, 4, 0, 8],
		"4-39" : [545, 23, 12, 4, 0, 8],
		"4-40" : [605, 25, 15, 4, 0, 8],
		"5-40" : [3500, 0, 0, 0, 250, 200],
		"5-41" : [70, 5, 1, 1, 0, 10],
		"5-42" : [135, 6, 2, 1, 0, 10],
		"5-43" : [205, 7, 3, 1, 0, 10],
		"5-44" : [270, 10, 5, 2, 0, 10],
		"5-45" : [405, 15, 6, 2, 0, 10],
		"5-46" : [440, 16, 7, 2, 0, 10],
		"5-47" : [475, 17, 8, 3, 0, 10],
		"5-48" : [510, 18, 9, 3, 0, 10],
		"5-49" : [545, 19, 10, 3, 0, 10],
		"5-50" : [575, 20, 11, 4, 0, 10],
		"5-51" : [610, 21, 11, 4, 0, 10],
		"5-52" : [630, 23, 12, 4, 0, 10],
		"5-53" : [650, 24, 12, 5, 0, 10],
		"5-54" : [670, 24, 13, 5, 0, 10],
		"5-55" : [745, 25, 15, 5, 0, 10],
		"6-55" : [7000, 0, 0, 0, 1000, 400],
		"6-56" : [95, 5, 1, 1, 0, 12],
		"6-57" : [190, 7, 2, 1, 0, 12],
		"6-58" : [285, 10, 5, 1, 0, 12],
		"6-59" : [380, 15, 7, 2, 0, 12],
		"6-60" : [575, 18, 9, 2, 0, 12],
		"6-61" : [620, 22, 10, 3, 0, 12],
		"6-62" : [670, 24, 11, 3, 0, 12],
		"6-63" : [715, 26, 12, 4, 0, 12],
		"6-64" : [765, 28, 13, 4, 0, 12],
		"6-65" : [810, 30, 14, 5, 0, 12],
		"6-66" : [860, 31, 15, 6, 0, 12],
		"6-67" : [890, 32, 16, 6, 0, 12],
		"6-68" : [915, 33, 17, 7, 0, 12],
		"6-69" : [945, 34, 18, 7, 0, 12],
		"6-70" : [1050, 35, 20, 8, 0, 12],
		"7-70" : [13000, 0, 0, 0, 3000, 800],
	},
"Rare" :
	{
		"1-1" : [0, 0, 0, 0, 0, 0],
		"1-2" : [20, 1, 0, 0, 0, 3],
		"1-3" : [40, 3, 0, 0, 0, 3],
		"1-4" : [60, 4, 1, 0, 0, 3],
		"1-5" : [80, 5, 1, 0, 0, 3],
		"2-5" : [125, 0, 0, 0, 4, 30],
		"2-6" : [25, 1, 1, 0, 0, 5],
		"2-7" : [55, 3, 2, 0, 0, 5],
		"2-8" : [80, 4, 2, 1, 0, 5],
		"2-9" : [105, 5, 3, 1, 0, 5],
		"2-10" : [160, 8, 5, 1, 0, 5],
		"2-11" : [170, 9, 5, 1, 0, 5],
		"2-12" : [185, 9, 6, 1, 0, 5],
		"2-13" : [200, 10, 6, 1, 0, 5],
		"2-14" : [210, 11, 7, 2, 0, 5],
		"2-15" : [225, 11, 7, 2, 0, 5],
		"3-15" : [750, 0, 0, 0, 8, 75],
		"3-16" : [35, 2, 1, 0, 0, 7],
		"3-17" : [70, 4, 2, 1, 0, 7],
		"3-18" : [105, 6, 3, 1, 0, 7],
		"3-19" : [135, 9, 5, 2, 0, 7],
		"3-20" : [205, 13, 7, 2, 0, 7],
		"3-21" : [225, 14, 8, 3, 0, 7],
		"3-22" : [240, 15, 8, 3, 0, 7],
		"3-23" : [255, 16, 9, 3, 0, 7],
		"3-24" : [275, 17, 9, 3, 0, 7],
		"3-25" : [290, 18, 10, 3, 0, 7],
		"4-25" : [1500, 0, 0, 0, 40, 150],
		"4-26" : [70, 3, 2, 1, 0, 9],
		"4-27" : [145, 5, 3, 1, 0, 9],
		"4-28" : [215, 8, 5, 2, 0, 9],
		"4-29" : [285, 11, 7, 2, 0, 9],
		"4-30" : [430, 16, 10, 4, 0, 9],
		"4-31" : [465, 18, 11, 4, 0, 9],
		"4-32" : [500, 19, 12, 4, 0, 9],
		"4-33" : [540, 20, 13, 4, 0, 9],
		"4-34" : [575, 22, 13, 5, 0, 9],
		"4-35" : [610, 23, 14, 5, 0, 9],
		"4-36" : [645, 25, 15, 5, 0, 9],
		"4-37" : [665, 25, 16, 5, 0, 9],
		"4-38" : [690, 26, 16, 6, 0, 9],
		"4-39" : [710, 27, 17, 6, 0, 9],
		"4-40" : [790, 30, 18, 6, 0, 9],
		"5-40" : [4500, 0, 0, 0, 200, 300],
		"5-41" : [90, 3, 2, 1, 0, 11],
		"5-42" : [175, 6, 4, 1, 0, 11],
		"5-43" : [265, 10, 6, 2, 0, 11],
		"5-44" : [355, 13, 8, 3, 0, 11],
		"5-45" : [530, 19, 12, 4, 0, 11],
		"5-46" : [575, 21, 13, 4, 0, 11],
		"5-47" : [620, 22, 14, 5, 0, 11],
		"5-48" : [660, 24, 15, 5, 0, 11],
		"5-49" : [705, 26, 16, 5, 0, 11],
		"5-50" : [750, 27, 17, 6, 0, 11],
		"5-51" : [795, 29, 18, 6, 0, 11],
		"5-52" : [820, 30, 18, 6, 0, 11],
		"5-53" : [845, 31, 19, 6, 0, 11],
		"5-54" : [875, 32, 20, 7, 0, 11],
		"5-55" : [970, 35, 22, 7, 0, 11],
		"6-55" : [9000, 0, 0, 0, 600, 600],
		"6-56" : [125, 5, 3, 1, 0, 13],
		"6-57" : [250, 10, 6, 2, 0, 13],
		"6-58" : [370, 14, 9, 3, 0, 13],
		"6-59" : [495, 19, 12, 4, 0, 13],
		"6-60" : [745, 29, 17, 6, 0, 13],
		"6-61" : [805, 31, 19, 6, 0, 13],
		"6-62" : [870, 34, 20, 7, 0, 13],
		"6-63" : [930, 36, 22, 7, 0, 13],
		"6-64" : [995, 39, 23, 8, 0, 13],
		"6-65" : [1055, 41, 25, 8, 0, 13],
		"6-66" : [1115, 43, 26, 9, 0, 13],
		"6-67" : [1155, 45, 27, 9, 0, 13],
		"6-68" : [1190, 46, 28, 9, 0, 13],
		"6-69" : [1230, 48, 29, 10, 0, 13],
		"6-70" : [1365, 53, 32, 11, 0, 13],
		"7-70" : [17000, 0, 0, 0, 1500, 1200],
	},
"Epic" :
	{
		"1-1" : [0, 0, 0, 0, 0, 0],
		"1-2" : [30, 2, 0, 0, 0, 4],
		"1-3" : [60, 5, 1, 0, 0, 4],
		"1-4" : [90, 6, 2, 1, 0, 4],
		"1-5" : [120, 7, 2, 1, 0, 4],
		"2-5" : [175, 0, 0, 0, 3, 40],
		"2-6" : [40, 2, 1, 1, 0, 6],
		"2-7" : [80, 4, 2, 1, 0, 6],
		"2-8" : [120, 5, 3, 1, 0, 6],
		"2-9" : [150, 7, 5, 1, 0, 6],
		"2-10" : [220, 10, 7, 1, 0, 6],
		"2-11" : [235, 13, 8, 2, 0, 6],
		"2-12" : [260, 15, 9, 2, 0, 6],
		"2-13" : [280, 17, 10, 2, 0, 6],
		"2-14" : [300, 18, 12, 3, 0, 6],
		"2-15" : [315, 19, 13, 3, 0, 6],
		"3-15" : [1000, 0, 0, 0, 6, 100],
		"3-16" : [50, 3, 3, 1, 0, 8],
		"3-17" : [100, 5, 4, 2, 0, 8],
		"3-18" : [150, 10, 5, 2, 0, 8],
		"3-19" : [210, 15, 7, 2, 0, 8],
		"3-20" : [290, 20, 10, 3, 0, 8],
		"3-21" : [325, 21, 12, 4, 0, 8],
		"3-22" : [350, 22, 13, 4, 0, 8],
		"3-23" : [370, 24, 14, 5, 0, 8],
		"3-24" : [400, 25, 15, 5, 0, 8],
		"3-25" : [455, 25, 17, 5, 0, 8],
		"4-25" : [2000, 0, 0, 0, 25, 200],
		"4-26" : [100, 5, 2, 2, 0, 10],
		"4-27" : [200, 7, 4, 2, 0, 10],
		"4-28" : [300, 10, 6, 3, 0, 10],
		"4-29" : [395, 15, 7, 3, 0, 10],
		"4-30" : [595, 20, 9, 4, 0, 10],
		"4-31" : [645, 25, 11, 5, 0, 10],
		"4-32" : [695, 27, 13, 5, 0, 10],
		"4-33" : [745, 29, 15, 6, 0, 10],
		"4-34" : [795, 31, 16, 6, 0, 10],
		"4-35" : [845, 33, 17, 7, 0, 10],
		"4-36" : [895, 35, 18, 7, 0, 10],
		"4-37" : [925, 37, 19, 8, 0, 10],
		"4-38" : [955, 39, 20, 8, 0, 10],
		"4-39" : [985, 42, 21, 9, 0, 10],
		"4-40" : [1090, 45, 22, 10, 0, 10],
		"5-40" : [6000, 0, 0, 0, 100, 400],
		"5-41" : [120, 4, 3, 1, 0, 12],
		"5-42" : [245, 9, 8, 2, 0, 12],
		"5-43" : [365, 13, 10, 3, 0, 12],
		"5-44" : [490, 18, 11, 4, 0, 12],
		"5-45" : [735, 27, 14, 4, 0, 12],
		"5-46" : [795, 29, 15, 5, 0, 12],
		"5-47" : [855, 31, 17, 5, 0, 12],
		"5-48" : [915, 35, 18, 6, 0, 12],
		"5-49" : [980, 38, 19, 7, 0, 12],
		"5-50" : [1040, 40, 20, 7, 0, 12],
		"5-51" : [1100, 41, 21, 8, 0, 12],
		"5-52" : [1135, 43, 22, 9, 0, 12],
		"5-53" : [1175, 45, 23, 9, 0, 12],
		"5-54" : [1210, 47, 24, 10, 0, 12],
		"5-55" : [1345, 50, 25, 10, 0, 12],
		"6-55" : [12000, 0, 0, 0, 350, 800],
		"6-56" : [170, 7, 5, 1, 0, 14],
		"6-57" : [345, 15, 10, 3, 0, 14],
		"6-58" : [515, 25, 13, 4, 0, 14],
		"6-59" : [685, 30, 17, 5, 0, 14],
		"6-60" : [1030, 35, 21, 5, 0, 14],
		"6-61" : [1115, 40, 27, 6, 0, 14],
		"6-62" : [1205, 42, 29, 7, 0, 14],
		"6-63" : [1290, 46, 30, 8, 0, 14],
		"6-64" : [1375, 52, 31, 9, 0, 14],
		"6-65" : [1460, 58, 32, 10, 0, 14],
		"6-66" : [1545, 60, 34, 12, 0, 14],
		"6-67" : [1600, 65, 35, 14, 0, 14],
		"6-68" : [1650, 70, 37, 16, 0, 14],
		"6-69" : [1700, 75, 39, 17, 0, 14],
		"6-70" : [1890, 80, 40, 18, 0, 14],
		"7-70" : [24000, 0, 0, 0, 720, 1600],
	},
"Legendary" :
	{
		"1-1" : [0, 0, 0, 0, 0, 0],
		"1-2" : [40, 2, 1, 0, 0, 5],
		"1-3" : [80, 5, 2, 1, 0, 5],
		"1-4" : [130, 8, 3, 1, 0, 5],
		"1-5" : [200, 10, 4, 2, 0, 5],
		"2-5" : [225, 0, 0, 0, 2, 50],
		"2-6" : [55, 2, 1, 0, 0, 7],
		"2-7" : [100, 5, 3, 1, 0, 7],
		"2-8" : [155, 7, 5, 1, 0, 7],
		"2-9" : [200, 9, 7, 2, 0, 7],
		"2-10" : [265, 14, 10, 2, 0, 7],
		"2-11" : [315, 15, 10, 3, 0, 7],
		"2-12" : [350, 16, 11, 3, 0, 7],
		"2-13" : [385, 18, 12, 4, 0, 7],
		"2-14" : [425, 19, 14, 4, 0, 7],
		"2-15" : [450, 20, 15, 5, 0, 7],
		"3-15" : [1500, 0, 0, 0, 4, 125],
		"3-16" : [80, 5, 3, 1, 0, 9],
		"3-17" : [130, 8, 5, 2, 0, 9],
		"3-18" : [200, 13, 8, 3, 0, 9],
		"3-19" : [270, 17, 12, 4, 0, 9],
		"3-20" : [390, 21, 13, 5, 0, 9],
		"3-21" : [425, 25, 14, 6, 0, 9],
		"3-22" : [460, 28, 15, 6, 0, 9],
		"3-23" : [500, 30, 16, 7, 0, 9],
		"3-24" : [545, 33, 18, 8, 0, 9],
		"3-25" : [600, 35, 21, 8, 0, 9],
		"4-25" : [3000, 0, 0, 0, 8, 250],
		"4-26" : [300, 5, 3, 1, 0, 11],
		"4-27" : [450, 10, 6, 2, 0, 11],
		"4-28" : [500, 14, 10, 3, 0, 11],
		"4-29" : [650, 20, 14, 4, 0, 11],
		"4-30" : [850, 29, 16, 5, 0, 11],
		"4-31" : [950, 32, 18, 6, 0, 11],
		"4-32" : [1000, 35, 19, 7, 0, 11],
		"4-33" : [1050, 36, 20, 8, 0, 11],
		"4-34" : [1100, 39, 21, 9, 0, 11],
		"4-35" : [1150, 41, 22, 10, 0, 11],
		"4-36" : [1200, 43, 23, 10, 0, 11],
		"4-37" : [1250, 45, 24, 11, 0, 11],
		"4-38" : [1350, 46, 26, 12, 0, 11],
		"4-39" : [1450, 50, 28, 13, 0, 11],
		"4-40" : [1750, 55, 30, 14, 0, 11],
		"5-40" : [7500, 0, 0, 0, 16, 500],
		"5-41" : [500, 8, 4, 2, 0, 13],
		"5-42" : [650, 12, 7, 3, 0, 13],
		"5-43" : [800, 18, 10, 3, 0, 13],
		"5-44" : [1050, 24, 15, 4, 0, 13],
		"5-45" : [1430, 35, 17, 5, 0, 13],
		"5-46" : [1590, 38, 19, 5, 0, 13],
		"5-47" : [1680, 43, 20, 6, 0, 13],
		"5-48" : [1750, 45, 22, 7, 0, 13],
		"5-49" : [1850, 50, 25, 8, 0, 13],
		"5-50" : [1950, 51, 28, 10, 0, 13],
		"5-51" : [2000, 52, 30, 12, 0, 13],
		"5-52" : [2100, 53, 32, 14, 0, 13],
		"5-53" : [2250, 56, 34, 16, 0, 13],
		"5-54" : [2400, 60, 37, 17, 0, 13],
		"5-55" : [3000, 65, 40, 18, 0, 13],
		"6-55" : [15000, 0, 0, 0, 32, 1000],
		"6-56" : [600, 9, 6, 3, 0, 15],
		"6-57" : [780, 17, 12, 5, 0, 15],
		"6-58" : [950, 26, 17, 7, 0, 15],
		"6-59" : [1300, 35, 20, 10, 0, 15],
		"6-60" : [1740, 50, 28, 11, 0, 15],
		"6-61" : [1910, 55, 30, 12, 0, 15],
		"6-62" : [200, 60, 32, 13, 0, 15],
		"6-63" : [2120, 75, 34, 14, 0, 15],
		"6-64" : [2200, 70, 36, 15, 0, 15],
		"6-65" : [2300, 74, 38, 16, 0, 15],
		"6-66" : [2400, 78, 40, 17, 0, 15],
		"6-67" : [2500, 80, 42, 18, 0, 15],
		"6-68" : [2700, 84, 45, 19, 0, 15],
		"6-69" : [2900, 88, 50, 20, 0, 15],
		"6-70" : [3600, 99, 55, 20, 0, 15],
		"7-70" : [30000, 0, 0, 0, 64, 2000],
	},
}

PROJECTED_CAPS={}
PROJECTED_CAPS[1]=10
PROJECTED_CAPS[2]=10
PROJECTED_CAPS[3]=10
PROJECTED_CAPS[4]=12
PROJECTED_CAPS[5]=18
PROJECTED_CAPS[6]=25
PROJECTED_CAPS[7]=32
PROJECTED_CAPS[8]=39
PROJECTED_CAPS[9]=46
PROJECTED_CAPS[10]=53
PROJECTED_CAPS[11]=60
PROJECTED_CAPS[12]=65
PROJECTED_CAPS[13]=69
PROJECTED_CAPS[14]=73
PROJECTED_CAPS[15]=76
PROJECTED_CAPS[16]=78

ARENA_MAP={}
ARENA_MAP[1]=[0,300]
ARENA_MAP[2]=[300,650]
ARENA_MAP[3]=[650,1200]
ARENA_MAP[4]=[1200,1800]
ARENA_MAP[5]=[1800,2500]
ARENA_MAP[6]=[2500,3200]
ARENA_MAP[7]=[3200,3900]
ARENA_MAP[8]=[3900,4600]
ARENA_MAP[9]=[4600,5300]
ARENA_MAP[10]=[5300,6000]
ARENA_MAP[11]=[6000,6500]
ARENA_MAP[12]=[6500,7000]
ARENA_MAP[13]=[7000,7500]
ARENA_MAP[14]=[7500,8000]
ARENA_MAP[15]=[8000,8500]
ARENA_MAP[16]=[8500,None]

THEME_COLORS={}
THEME_COLORS["neu"]="#665E57"
THEME_COLORS["adv"]="#4F83BD"
THEME_COLORS["sci"]="#D66D2C"
THEME_COLORS["mys"]="#488736"
THEME_COLORS["fan"]="#BD5463"
THEME_COLORS["sup"]="#A443A0"
THEME_COLORS[0]="#665E57"
THEME_COLORS[1]="#4F83BD"
THEME_COLORS[2]="#D66D2C"
THEME_COLORS[3]="#488736"
THEME_COLORS[4]="#BD5463"
THEME_COLORS[5]="#A443A0"

ACRO_MAP={
	"NK" : 1,
	"AO" : 38,
	"AC" : 193,
	"AD" : 2101,
	"AQR" : 1509,
	"AW" : 86,
	"AS" : 1276,
	"AB" : 55,
	"BS" : 1700,
	"BGA" : 1682,
	"BEB" : 1806,
	"BHK" : 1949,
	"BB" : 1808,
	"CH" : 1701,
	"CKI" : 144,
	"CW" : 140,
	"CT" : 91,
	"CBB" : 84,
	"CM" : 1472,
	"CK" : 146,
	"DMC" : 61,
	"DHB" : 27,
	"DSR" : 1972,
	"DKC" : 179,
	"EKB" : 2042,
	"EJ" : 209,
	"FB" : 24,
	"4AM" : 1824,
	"GWC" : 32,
	"GSK" : 35,
	"HC" : 51,
	"HK" : 138,
	"HHC" : 50,
	"HD" : 1269,
	"ISW" : 52,
	"IK" : 134,
	"KOTDE" : 89,
	"LBJ" : 206,
	"LB" : 186,
	"MBP" : 1672,
	"MT" : 88,
	"MWS" : 8,
	"MB" : 1804,
	"OT" : 28,
	"PB" : 57,
	"PCP" : 1886,
	"PST" : 92,
	"PT" : 87,
	"PK" : 37,
	"SNR" : 44,
	"ST" : 200,
	"SSS" : 2114,
	"SMW" : 141,
	"SER" : 137,
	"6ER" : 137,
	"SWT" : 203,
	"SOMM" : 12,
	"STG" : 29,
	"STJ" : 205,
	"SG" : 2013,
	"TNP" : 1680,
	"AR" : 135,
	"UC" : 1274,
	"WDT" : 201,
	"WG" : 176,
	"YPC" : 1218,
	"FP" : 2132,
	"CG" : 2136,
	"HK" : 2143,
	"SF" : 2117,
	"DT" : 2195,
	"BMM" : 2209,
	"PG" : 2030,
	"MBC" : 2216,
	"MM" : 2258,
	"SS" : 2251,
	"GD" : 2290,
	"CWG" : 2295,
	"SPB" : 2308,
	"DAR" : 2299,
	"MJR" : 2317,
	"NN" : 2357,
	"WC" : 2365,
	"AB" : 2376,
	"CH" : 2378,
	"HJ" : 2385,
	"WHN" : 2386,
}

# DECK MAP for API
DECK_MAP={}
DECK_MAP[1]=	["New Kid",0,"fight","neu","com","zap"]
DECK_MAP[38]=	["A.W.E.S.O.M.-O 4000",5,"tank","sci","epi","charge"]
DECK_MAP[193]=	["Alien Clyde",3,"fight","sci","com","warcry"]
DECK_MAP[2101]=	["Alien Drone",4,"fight","sci","epi","warcry","flying"]
DECK_MAP[1509]=	["Alien Queen Red",5,"fight","sci","rar","warcry"]
DECK_MAP[86]=	["Angel Wendy",3,"range","mys","com","charge"]
DECK_MAP[1276]=	["Arrowstorm",4,"spell","adv","epi","area"]
DECK_MAP[55]=	["Astronaut Butters",2,"ass","sci","com","deathwish"]
DECK_MAP[1700]=	["Bandita Sally",2,"ass","adv","com"]
DECK_MAP[1288]=	["Barrel Dougie",4,"ass","adv","rar","headhunter"]
DECK_MAP[1682]=	["Big Gay Al",5,"range","neu","rar","headhunter"]
DECK_MAP[1806]=	["Blood Elf Bebe",3,"range","fan","com","special"]
DECK_MAP[1949]=	["Bounty Hunter Kyle",3,"range","sci","epi","special"]
DECK_MAP[1808]=	["Buccaneer Bebe",4,"range","adv","rar","special"]
DECK_MAP[1701]=	["Calamity Heidi",2,"fight","adv","com"]
DECK_MAP[144]=	["Canadian Knight Ike",3,"ass","fan","rar","charge"]
DECK_MAP[140]=	["Captain Wendy",3,"range","adv","rar","charge"]
DECK_MAP[91]=	["Catapult Timmy",3,"range","fan","rar","charge"]
DECK_MAP[1656]=	["Chicken Coop",4,"tower","fan","epi"]
DECK_MAP[84]=	["Choirboy Butters",2,"ass","mys","epi","deathwish"]
DECK_MAP[1973]=	["Classi",5,"fight","neu","epi","enrage"]
DECK_MAP[1472]=	["Cock Magic",6,"spell","fan","epi"]
DECK_MAP[1923]=	["Cupid Cartman",3,"range","mys","rar"]
DECK_MAP[146]=	["Cyborg Kenny",4,"ass","sci","epi","deathwish"]
DECK_MAP[61]=	["Dark Mage Craig",3,"range","fan","rar","area"]
DECK_MAP[27]=	["Deckhand Butters",3,"ass","adv","com","deathwish"]
DECK_MAP[1674]=	["Dogpoo",3,"fight","neu","epi"]
DECK_MAP[1972]=	["Dragonslayer Red",4,"fight","fan","leg","warcry"]
DECK_MAP[1506]=	["Dwarf Engineer Dougie",4,"ass","fan","rar","headhunter"]
DECK_MAP[179]=	["Dwarf King Clyde",4,"fight","fan","rar","warcry"]
DECK_MAP[2042]=	["Elven King Bradley",3,"fight","fan","rar","aura"]
DECK_MAP[1307]=	["Energy Staff",4,"tower","mys","rar"]
DECK_MAP[209]=	["Enforcer Jimmy",2,"fight","sci","rar","aura"]
DECK_MAP[24]=	["Fireball",5,"spell","adv","rar"]
DECK_MAP[1824]=	["Four-Assed Monkey",3,"ass","sci","rar","deathwish"]
DECK_MAP[40]=	["Freeze Ray",3,"spell","sci","com"]
DECK_MAP[208]=	["Friar Jimmy",3,"fight","mys","com","aura"]
DECK_MAP[133]=	["Gizmo Ike",3,"ass","sci","epi","charge"]
DECK_MAP[32]=	["Grand Wizard Cartman",6,"tank","fan","leg"]
DECK_MAP[35]=	["Gunslinger Kyle",3,"range","adv","com","charge"]
DECK_MAP[85]=	["Hallelujah",4,"spell","mys","rar"]
DECK_MAP[51]=	["Hercules Clyde",3,"fight","mys","rar","warcry"]
DECK_MAP[138]=	["Hermes Kenny",3,"ass","mys","epi","deathwish"]
DECK_MAP[50]=	["Hookhand Clyde",3,"fight","adv","epi","warcry"]
DECK_MAP[1269]=	["Hyperdrive",2,"spell","sci","rar"]
DECK_MAP[52]=	["Ice Sniper Wendy",3,"range","sci","rar","charge"]
DECK_MAP[1983]=	["Imp Tweek",4,"fight","mys","epi","flying"]
DECK_MAP[48]=	["Incan Craig",5,"range","adv","leg","warcry"]
DECK_MAP[134]=	["Inuit Kenny",3,"ass","adv","leg","deathwish"]
DECK_MAP[89]=	["Kyle of the Drow Elves",4,"range","fan","rar","charge"]
DECK_MAP[206]=	["Le Bard Jimmy",4,"fight","fan","com","warcry"]
DECK_MAP[186]=	["Lightning Bolt",4,"spell","adv","rar"]
DECK_MAP[1672]=	["Manbearpig",7,"tank","neu","leg"]
DECK_MAP[1869]=	["Marcus",4,"fight","neu","epi","charge"]
DECK_MAP[49]=	["Marine Craig",4,"range","sci","com","warcry"]
DECK_MAP[88]=	["Mecha Timmy",4,"range","sci","leg","charge"]
DECK_MAP[8]=	["Medicine Woman Sharon",4,"range","adv","rar","charge"]
DECK_MAP[1804]=	["Medusa Bebe",4,"range","mys","leg","special"]
DECK_MAP[1661]=	["Mimsy",5,"tank","neu","com","headhunter"]
DECK_MAP[1272]=	["Mind Control",4,"spell","sci","rar"]
DECK_MAP[1872]=	["Mr. Hankey",3,"ass","neu","leg","warcry"]
DECK_MAP[2074]=	["Mr. Mackey",4,"fight","neu","com","aura"]
DECK_MAP[2035]=	["Mr. Slave Executioner",5,"tank","fan","epi","deathwish","enrage"]
DECK_MAP[15]=	["Nathan",4,"range","neu","rar","AOE"]
DECK_MAP[1666]=	["Nelly",4,"fight","neu","rar","AOE"]
DECK_MAP[1683]=	["Officer Barbrady",5,"tank","neu","rar","deathwish"]
DECK_MAP[28]=	["Outlaw Tweek",4,"range","adv","com","warcry"]
DECK_MAP[57]=	["Paladin Butters",2,"ass","fan","com","deathwish"]
DECK_MAP[1886]=	["PC Principal",4,"tank","neu","rar"]
DECK_MAP[1684]=	["Pigeon Gang",4,"fight","neu","com","flying","swarm"]
DECK_MAP[92]=	["Pirate Ship Timmy",3,"range","adv","rar","charge"]
DECK_MAP[10]=	["Pocahontas Randy",5,"fight","adv","epi","charge"]
DECK_MAP[1657]=	["Poison",3,"spell","sci","com"]
DECK_MAP[87]=	["Pope Timmy",5,"range","mys","epi","warcry"]
DECK_MAP[31]=	["Poseidon Stan",3,"fight","mys","com","charge"]
DECK_MAP[1286]=	["Power Bind",2,"spell","mys","com"]
DECK_MAP[1311]=	["Powerfist Dougie",4,"ass","sci","rar","headhunter"]
DECK_MAP[2043]=	["Priest Maxi",6,"tank","mys","com","aura","enrage"]
DECK_MAP[37]=	["Princess Kenny",2,"ass","fan","com","deathwish"]
DECK_MAP[30]=	["Program Stan",3,"fight","sci","epi","charge"]
DECK_MAP[1504]=	["Prophet Dougie",4,"ass","mys","rar","headhunter"]
DECK_MAP[1273]=	["Purify",2,"spell","mys","com"]
DECK_MAP[1407]=	["Rat Swarm",3,"ass","neu","com","swarm"]
DECK_MAP[1277]=	["Regeneration",3,"spell","mys","rar"]
DECK_MAP[47]=	["Robin Tweek",3,"range","fan","com","warcry"]
DECK_MAP[1805]=	["Robo Bebe",3,"range","sci","com","special"]
DECK_MAP[54]=	["Rogue Token",4,"fight","fan","epi","warcry"]
DECK_MAP[2081]=	["Santa Claus",5,"tank","neu","epi","charge"]
DECK_MAP[2080]=	["Satan",6,"range","neu","leg","warcry"]
DECK_MAP[132]=	["Scout Ike",3,"ass","mys","com","charge"]
DECK_MAP[44]=	["Sexy Nun Randy",5,"fight","mys","epi","charge"]
DECK_MAP[200]=	["Shaman Token",3,"fight","adv","com","charge"]
DECK_MAP[2114]=	["Sharpshooter Shelly",3,"range","adv","epi","charge"]
DECK_MAP[45]=	["Sheriff Cartman",4,"tank","adv","rar","charge"]
DECK_MAP[141]=	["Shieldmaiden Wendy",3,"fight","fan","leg","charge"]
DECK_MAP[137]=	["Sixth Element Randy",5,"fight","sci","leg","charge"]
DECK_MAP[131]=	["Smuggler Ike",2,"ass","adv","com","charge"]
DECK_MAP[203]=	["Space Warrior Token",2,"fight","sci","rar","charge"]
DECK_MAP[12]=	["Stan of Many Moons",4,"fight","adv","leg","charge"]
DECK_MAP[29]=	["Stan the Great",3,"fight","fan","com","charge"]
DECK_MAP[1670]=	["Starvin' Marvin",4,"fight","neu","rar","headhunter"]
DECK_MAP[205]=	["Storyteller Jimmy",3,"fight","adv","epi","aura"]
DECK_MAP[2044]=	["Swashbuckler Red",4,"fight","adv","epi","warcry"]
DECK_MAP[2013]=	["Swordsman Garrison",5,"fight","adv","rar","charge"]
DECK_MAP[1680]=	["Terrance and Phillip",4,"fight","neu","com","swarm"]
DECK_MAP[1665]=	["Terrance Mephesto",4,"range","neu","rar","area","flying"]
DECK_MAP[135]=	["The Amazingly Randy",4,"range","fan","epi","charge"]
DECK_MAP[1216]=	["The Master Ninjew",4,"range","mys","leg","warcry"]
DECK_MAP[1947]=	["Towelie",3,"fight","neu","epi","aura"]
DECK_MAP[1655]=	["Transmogrify",5,"spell","fan","epi"]
DECK_MAP[1686]=	["Underpants Gnomes",2,"ass","fan","rar","swarm"]
DECK_MAP[1274]=	["Unholy Combustion",5,"spell","mys","rar"]
DECK_MAP[1813]=	["Visitors",3,"range","sci","rar","swarm"]
DECK_MAP[46]=	["Warboy Tweek",3,"range","sci","rar","warcry"]
DECK_MAP[201]=	["Witch Doctor Token",4,"fight","mys","leg","charge"]
DECK_MAP[176]=	["Witch Garrison",4,"fight","fan","rar","charge"]
DECK_MAP[1218]=	["Youth Pastor Craig",3,"range","mys","rar","warcry"]
DECK_MAP[158]=	["Zen Cartman",3,"tank","mys","rar","charge"]
DECK_MAP[0]=	["Unknown",3,"unknown","neu","unknown"]
DECK_MAP[2132]=	["Fastpass",3,"fight","sup","epi","charge"]
DECK_MAP[2141]=	["The Coon",5,"tank","sup","epi","special"]
DECK_MAP[2098]=	["Tupperware",4,"fight","sup","com","special"]
DECK_MAP[2136]=	["Call Girl",6,"range","sup","leg","warcry"]
DECK_MAP[2091]=	["Mosquito",3,"fight","sup","rar","warcry"]
DECK_MAP[2143]=	["Human Kite",4,"range","sup","epi","charge"]
DECK_MAP[2117]=	["Super Fart",2,"spell","sup","com"]
DECK_MAP[2144]=	["Toolshed",3,"fight","sup","epi"]
DECK_MAP[2130]=	["The Chomper",2,"spell","sup","rar","trap"]
DECK_MAP[2147]=	["Mysterion",5,"ass","sup","leg","deathwish"]
DECK_MAP[2202]=	["Professor Chaos",3,"ass","sup","epi","warcry"]
DECK_MAP[2190]=	["Lava!",3,"spell","sup","com","trap"]
DECK_MAP[2195]=	["Doctor Timothy",4,"range","sup","rar","charge"]
DECK_MAP[2200]=	["Captain Diabetes",2,"fight","sup","com","charge"]
DECK_MAP[2209]=	["Big Mesquite Murph",5,"tank","adv","epi","charge"]
DECK_MAP[2210]=	["Sorceress Liane",5,"fight","fan","epi","deathwish"]
DECK_MAP[2030]=	["President Garrison",5,"fight","neu","epi","charge","area"]
DECK_MAP[2216]=	["Mint-Berry Crunch",4,"range","sup","leg","flying","warcry","charge"]
DECK_MAP[2217]=	["Jesus",4,"range","mys","epi","deathwish"]
DECK_MAP[2258]=	["Mayor McDaniels",4,"range","neu","rar","warcry"]
DECK_MAP[2251]=	["Sizzler Stuart",4,"fight","sci","leg","warcry"]
DECK_MAP[2261]=	["Wonder Tweek",4,"range","sup","rar","special"]
DECK_MAP[2262]=	["Super Craig",3,"fight","sup","com","warcry"]
DECK_MAP[2266]=	["Thunderbird",4,"fight","adv","rar","flying","charge","headhunter"]
DECK_MAP[2290]=	["General Disarray",4,"ass","sup","rar","warcry","headhunter"]
DECK_MAP[2295]=	["City Wok Guy",4,"range","fan","epi","Charge","AOE"]
DECK_MAP[2308]=	["Space Pilot Bradley",3,"range","sci","epi","special"]
DECK_MAP[2299]=	["Dark Angel Red",4,"range","mys","epi","warcry"]
DECK_MAP[2316]=	["Chaos Hamsters",2,"ass","sup","rar","two"]
DECK_MAP[2319]=	["Frontier Bradley",3,"range","adv","epi","special"]
DECK_MAP[2317]=	["Mary Jane Randy",5,"fight","sup","epi","charge"]
DECK_MAP[2324]=	["Firkle",2,"ass","neu","com","deathwish"]
DECK_MAP[2325]=	["Michael",3,"fight","neu","rar","special"]
DECK_MAP[2326]=	["Pete",4,"range","neu","epi","special"]
DECK_MAP[2327]=	["Henrietta",5,"tank","neu","leg","special"]
DECK_MAP[2360]=	["Alternate Human Kite",3,"range","sup","rar","flying"]
DECK_MAP[2365]=	["Woodland Critters",4,"range","neu","epi","charge"]
DECK_MAP[2376]=	["Archangel Bradley",3,"fight","mys","epi","special"]
DECK_MAP[2357]=	["Nymph Nichole",3,"fight","fan","rar","warcry"]
DECK_MAP[2378]=	["Commander Hat",4,"range","sci","epi","warcry"]
DECK_MAP[2386]=	["War Hero Ned",3,"range","adv","epi","special"]
DECK_MAP[2393]=	["Castle Defender",5,"tower","fan","rar","deathwish"]
DECK_MAP[2401]=	["Crusader",4,"tank","fan","rar","nothing"]
DECK_MAP[2385]=	["Hunter Jimbo",4,"tank","adv","rar","special"]
DECK_MAP[2399]=	["Scuzzlebutt",6,"tank","neu","rar","deathwish"]
DECK_MAP[2380]=	["Infiltrator Kevin",3,"range","sci","rar","special"]
DECK_MAP[2406]=	["Cow Stampede",5,"fight","neu","com","headhunter"]
DECK_MAP[2416]=	["Changeling Red",4,"fight","sup","leg","charge"]
DECK_MAP[2413]=	["Member Berries",5,"spell","sup","epi","trap"]
DECK_MAP[2407]=	["S-Wow Tittybang",5,"tank","mys","leg","charge"]
DECK_MAP[2429]=	["Future Randy",5,"tank","neu","leg","warcry"]
DECK_MAP[2436]=	["Full Moon Sparky",4,"fight","adv","leg","special"]
DECK_MAP[2441]=	["Arrow Tower",3,"tower","adv","com","special"]
DECK_MAP[2443]=	["Alchemist Scott",4,"range","fan","leg","special"]
DECK_MAP[2408]=	["Cyborg Tower",4,"tower","sci","rar","charge"]
DECK_MAP[2442]=	["Dr. Mephesto",5,"tank","sci","leg","special"]

NAME_TO_ID={}
for key in DECK_MAP.keys():
	name=DECK_MAP[key][0]
	NAME_TO_ID[name]=key

LOWER_NAME_TO_ID={}
for key in DECK_MAP.keys():
	name=DECK_MAP[key][0].lower()
	LOWER_NAME_TO_ID[name]=key

UNPLAYABLE={}

#OTHER
UNPLAYABLE["POOF"]=	["Cheesy Poofs",0,"cur","n/a","poofs"]#PVP Tickets: "code": "PVP"
UNPLAYABLE["PVP"]=	["PVP Tickets",0,"cur","n/a","tickets"]#PVP Tickets: "code": "PVP"
UNPLAYABLE["DM"]=	["Cash",0,"cur","n/a","cash"]#Cash: "code": "DM"
UNPLAYABLE["CN"]=	["Coins",0,"cur","n/a","coins"]#Coins: "code": "CN"
UNPLAYABLE["SUP"]=	["Eternity Gems",0,"cur","n/a","gems"]#SUP: "code": "SUP"
UNPLAYABLE[215]=	["Ancient Fossil",0,"mat","neu","bronze"]
UNPLAYABLE[216]=	["Power Serum",0,"mat","neu","silver"]
UNPLAYABLE[217]=	["Tome of Knowledge",0,"mat","neu","gold"]
UNPLAYABLE[219]=	["Indian Feather",0,"mat","adv","bronze"]
UNPLAYABLE[220]=	["Arrowhead",0,"mat","adv","silver"]
UNPLAYABLE[221]=	["Sheriff's Star",0,"mat","adv","gold"]
UNPLAYABLE[223]=	["Holy Candle",0,"mat","mys","bronze"]
UNPLAYABLE[224]=	["Prayer Beads",0,"mat","mys","silver"]
UNPLAYABLE[225]=	["Fancy Dreidel",0,"mat","mys","gold"]
UNPLAYABLE[227]=	["Top Secret Chip",0,"mat","sci","bronze"]
UNPLAYABLE[228]=	["Alien Hand",0,"mat","sci","silver"]
UNPLAYABLE[229]=	["Futuristic Robot",0,"mat","sci","gold"]
UNPLAYABLE[231]=	["Ancient Key",0,"mat","fan","bronze"]
UNPLAYABLE[232]=	["Mage's Tome",0,"mat","fan","silver"]
UNPLAYABLE[233]=	["Ring of Power",0,"mat","fan","gold"]
UNPLAYABLE[235]=	["Toxic Waste",0,"mat","sup","bronze"]
UNPLAYABLE[236]=	["Energy Drink",0,"mat","sup","silver"]
UNPLAYABLE[237]=	["Comics",0,"mat","sup","gold"]
UNPLAYABLE[259]=	["Event Tokens",0,"mat","n/a","tokens"]
UNPLAYABLE[260]=	["Bottle Caps",0,"mat","n/a","tokens"]
UNPLAYABLE[261]=	["Battle Tokens",0,"mat","n/a","tokens"]
UNPLAYABLE[262]=	["Cheesy Poofs",0,"mat","n/a","tokens"]
UNPLAYABLE[10000]=	["Gear",0,"gear","n/a","tokens"]

IGNORE_LIST = {}
IGNORE_LIST[1456]=	["A Cock",1,"fight","neu","epi"]
IGNORE_LIST[2102]=	["Auto-Vacuum",1,"tank","sci","leg"]
IGNORE_LIST[39]=	["Little Choirboy",1,"ass","mys","epi"]
IGNORE_LIST[1441]=	["Indian Brave",1,"fight","adv","epi"]
IGNORE_LIST[2093]=	["Mosquito Swarm",1,"fight","sup","rar","flying"]
IGNORE_LIST[1820]=	["Snake",1,"ass","mys","leg"]
IGNORE_LIST[2220]=	["Potted Plant",1,"tower","sup","epi"]
#NEU
IGNORE_LIST[79] = ["Pocahontas Randy", "Unknown range com neutral theme 20/686"]
IGNORE_LIST[1845] = ["A Rat", "PVE Boss 35/650 0 energy"]
IGNORE_LIST[2041] = ["Ice Sniper Wendy", "range neu rar 6 energy 19/84"]
IGNORE_LIST[1445] = ["DF_NAME_SPELLRATATTACKFAN", "fight neu com 4/21 5 energy"]
IGNORE_LIST[1456] = ["A Cock", "fight epi neu 16/50"]
IGNORE_LIST[1652] = ["Tank Kid", "PVE 13/420 neu com tank 4 energy"]
IGNORE_LIST[1667] = ["Gross Pidgeon", "Unknown 10/7 0 energy"] ###IMPOSSIBLE
IGNORE_LIST[1685] = ["Pidgeons", "Unknown 10/7 2 energy"]

#ADV
IGNORE_LIST[20] = ["Sheriff Cartman", "Unknown Range rar 1050/10"]
IGNORE_LIST[33] = ["Indian Hunter", "PVE Range com 20/70 3 energy"]
IGNORE_LIST[56] = ["Pocahontas Randy", "Unknown fight epi 20/244 4-energy"]
IGNORE_LIST[63] = ["Stan of Many Moons", "Unknown fight com 20/210 3 energy"]
IGNORE_LIST[70] = ["Deckhand Butters", "PVE Boss 20/600 2 energy"]
IGNORE_LIST[77] = ["Nathan", "Unknown adventure theme 30/325"]
IGNORE_LIST[78] = ["Mimsy", "Unknown adventure theme 20/1050"]
IGNORE_LIST[80] = ["Medicine Woman Sharon", "PVE Boss range com 20/686 3 energy"]
IGNORE_LIST[1298] = ["Arrow Tower", "tower 12/216 adv 4 energy"]
IGNORE_LIST[1470] = ["Arrow Tower", "Adv com 10/250 5 energy(range unit on top of tower)"]
IGNORE_LIST[1719] = ["Arrowstorm Caster", "PVE tower neu 0/250 3 energy"]
IGNORE_LIST[1720] = ["Lightning Bolt Caster", "PVE tower neu 0/250 3 energy"]
IGNORE_LIST[1319] = ["Inuit Kenny", "PVE Boss 40/300"]
IGNORE_LIST[1320] = ["Gunslinger Kyle", "PVE Boss 20/420 2 energy"]
IGNORE_LIST[1331] = ["Indian Brute", "tank com adv 15/350 4 energy"]
IGNORE_LIST[1441] = ["Indian Brave", "30/120 epi 1 energy"]
IGNORE_LIST[1653] = ["Indian Warrior", "PVE 20/120 fight com adv 2 energy"]
IGNORE_LIST[1474] = ["Captain Wendy", "PVE Boss 50/350 4 energy"]
IGNORE_LIST[1484] = ["Barrel Dougie", "PVE Boss 70/560 3 energy"]
IGNORE_LIST[1692] = ["Shaman Token", "PVE Boss 30/450"]
IGNORE_LIST[1703] = ["Incan Craig", "Unknown mys 5 energy common 40/805"]
IGNORE_LIST[1649] = ["Royal Archer", "PVE range com adv 3 energy 20/70"]

#SCI
IGNORE_LIST[73] = ["Program Stan", "PVE Boss 30/1050"]
IGNORE_LIST[76] = ["Astronaut Butters", "PVE Boss 60/420 3 energy"]
IGNORE_LIST[184] = ["Gizmo Ike", "Unknown 15/14"]
IGNORE_LIST[2337] = ["Gizmo Ike", "New Clone TBD/TBD"]
IGNORE_LIST[1426] = ["Space Grunt", "fight com sci PVE 25/70 3 energy"]
IGNORE_LIST[1427] = ["Space Gunner", "range com sci PVE 15/70 3 energy"]
IGNORE_LIST[1428] = ["Cyborg Titan", "tank com sci PVE 25/320 5 energy"]
IGNORE_LIST[1440] = ["Mecha Timmy", "PVE Boss 30/580"]
IGNORE_LIST[1442] = ["Alien Clyde", "PVE Boss 30/378 5 energy"]
IGNORE_LIST[1444] = ["Gizmo Ike", "PVE Boss 60/230 4 energy"]
IGNORE_LIST[1449] = ["Cyborg Kenny", "PVE Boss ass com 7/450 4 energy"]
IGNORE_LIST[1451] = ["Enforcer Jimmy", "PVE Boss 30/588 3 energy"]
IGNORE_LIST[1455] = ["Ice Sniper Wendy", "PVE Boss 60/630 4 energy"]
IGNORE_LIST[1693] = ["Alien Queen Red", "PVE Boss 40/430"]
IGNORE_LIST[1694] = ["Space Warrior Token", "PVE Boss 40/627"]
IGNORE_LIST[1696] = ["Marine Craig", "PVE Boss 40/377 3 cost"]
IGNORE_LIST[1698] = ["Bounty Hunter Kyle", "PVE Boss 20/300"]
IGNORE_LIST[1689] = ["Toxic Pylon", "PVE tower 3 energy sci com 0/175"]
IGNORE_LIST[1691] = ["Cyborg Tower", "tower rar 4 energy 15/240 sci"]
IGNORE_LIST[1641] = ["Space Assassin", "PVE ass sci 16/40 1 energy"]
IGNORE_LIST[1647] = ["Subzero Titan", "PVE tank 15/300 sci com 4 energy "]
IGNORE_LIST[1650] = ["Turbo Space Grunt", "PVE fight 25/70 3 energy com sci"]
IGNORE_LIST[1728] = ["Subzero Titan", "10/250 sci tank com 5 energy"]
IGNORE_LIST[2102] = ["Auto-Vacuum", "1 energy leg sci tank 25/225"]

#MYS
IGNORE_LIST[39] = ["Little Choirboy", "ass epi CHARGE 60/60 2 energy"]
IGNORE_LIST[65] = ["Poseidon Stan", "PVE Boss fight com 45/560"]
IGNORE_LIST[1278] = ["DF_NAME_SPELLDARKRESURRECT", "Unknown Spell mystic 5 energy"]
IGNORE_LIST[1512] = ["Choirboy Butters", "PVE Boss 60/400"]
IGNORE_LIST[1513] = ["Scout Ike", "PVE Boss 60/420"]
IGNORE_LIST[1514] = ["Hermes Kenny", "PVE Boss 80/600"]
IGNORE_LIST[1515] = ["Angel Wendy", "PVE Boss 40/530 4 energy"]
IGNORE_LIST[1516] = ["Friar Jimmy", "PVE Boss 60/730"]
IGNORE_LIST[1517] = ["Witch Doctor Token", "PVE Boss 45/530 3 energy"]
IGNORE_LIST[1518] = ["The Master Ninjew", "PVE Boss 11/666"]
IGNORE_LIST[1519] = ["Sexy Nun Randy", "PVE Boss 25/1060"]
IGNORE_LIST[1520] = ["Pope Timmy", "PVE Boss 50/400 8 energy"]
IGNORE_LIST[1533] = ["Zionist Ranger", "PVE range mys com 20/70 3 energy"]
IGNORE_LIST[1645] = ["Mormon Missionary", "PVE 15/360 mys com 5 energy"]
IGNORE_LIST[1688] = ["Healing Fountain", "PVE tower 0/350 3 energy com mys"]
IGNORE_LIST[1704] = ["Imp Tweek", "PVE Boss 40/560"]
IGNORE_LIST[1705] = ["Holy Defender", "PVE tower (range) 48/480 rare mys 3 energy"]
IGNORE_LIST[1708] = ["Prophet Dougie", "PVE Boss 60/665"]
IGNORE_LIST[1724] = ["Youth Pastor Craig", "PVE com 5 energy 40/470"]
IGNORE_LIST[1735] = ["Mormon Missionary", "15/220 4 energy mys tank com"]
IGNORE_LIST[1820] = ["Snake", "CHARGE ass leg mys 10/40"]

#FAN
IGNORE_LIST[67] = ["Paladin Butters", "PVE Boss 60/650 3 energy"]
IGNORE_LIST[68] = ["Rogue Token", "PVE Boss 30/1050"]
IGNORE_LIST[71] = ["Stan The Great", "PVE Boss 30/1050"]
IGNORE_LIST[1521] = ["Robin Tweek", "PVE Boss 45/550"]
IGNORE_LIST[1522] = ["Canadian Knight Ike", "PVE Boss com 72/350"]
IGNORE_LIST[1523] = ["Kyle of the Drow Elves", "PVE Boss 36/666"]
IGNORE_LIST[1524] = ["Catapult Timmy", "PVE Boss 60/500 4 energy"]
IGNORE_LIST[1525] = ["The Amazingly Randy", "PVE Boss 96/944 6 energy"]
IGNORE_LIST[1527] = ["Dwarf King Clyde", "PVE Boss 36/1000"]
IGNORE_LIST[1528] = ["Dark Mage Craig", "PVE Boss 25/999 4 energy"]
IGNORE_LIST[1529] = ["Le Bard Jimmy", "PVE Boss 48/1150"]
IGNORE_LIST[1531] = ["Grand Wizard Cartman", "PVE Boss 20/1350 5 energy"]
IGNORE_LIST[1532] = ["Princess Kenny", "PVE Boss 40/520"]
IGNORE_LIST[1658] = ["Beast Mode", "PVE spell 3 energy legendary fan"]
IGNORE_LIST[1659] = ["Invincibility", "PVE spell 3 energy Legendary fan"]
IGNORE_LIST[1690] = ["Rune Totem", "PVE tower 0/400 fan 3 energy"]
IGNORE_LIST[1715] = ["Castle Defender", "PVE tower 4 energy fan rare 24/240"]
IGNORE_LIST[1716] = ["Squire", "PVE 25/150 fight com fan 3 energy"]
IGNORE_LIST[1717] = ["Native Hunter", "PVE range com fan 3 energy 27/80"]
IGNORE_LIST[1718] = ["Crusader", "tank PVE com fan 5 energy 20/400"]
IGNORE_LIST[1737] = ["Shieldmaiden Wendy", "PVE Boss 60/1050"]
IGNORE_LIST[1843] = ["Underpants Gnomes", "Unknown 50/250"]

#SUP
IGNORE_LIST[2093] = ["Mosquito Swarm", "1 energy fight rare sup 12/108"]
IGNORE_LIST[2169] = ["Toolshed", "PVE Boss 3 energy sup com fight 7/400"]
IGNORE_LIST[2170] = ["Professor Chaos", "PVE Boss 3 energy sup com fight 7/425"]
IGNORE_LIST[2171] = ["Mosquito", "PVE Boss 3 energy sup com fight 7/475"]
IGNORE_LIST[2172] = ["Tupperware", "Unknown 3 energy sup com fight 22/166"]
IGNORE_LIST[2176] = ["Call Girl", "PVE Boss 3 energy sup com fight 7/210"]
IGNORE_LIST[2177] = ["Mysterion", "PVE Boss 3 energy sup com fight 7/475"]
IGNORE_LIST[2181] = ["Fastpass", "PVE Boss 3 energy sup com fight 7/425"]
IGNORE_LIST[2182] = ["Human Kite", "PVE Boss 3 energy sup com fight 7/450"]
IGNORE_LIST[2183] = ["Tupperware", "PVE Boss 3 energy sup com fight 7/450"]
IGNORE_LIST[2185] = ["The Coon", "PVE Boss 3 energy sup com fight 7/500"]
IGNORE_LIST[2220] = ["Potted Plant", "Unknown"]

IMAGE_MAP={}
IMAGE_MAP["A.W.E.S.O.M.-O 4000"]="https://i.imgur.com/RxMAkAp.png"
IMAGE_MAP["Alien Clyde"]="https://i.imgur.com/f6eiina.png"
IMAGE_MAP["Alien Drone"]="https://i.imgur.com/L1m2pis.png"
IMAGE_MAP["Alien Queen Red"]="https://i.imgur.com/1IEVzrF.png"
IMAGE_MAP["Angel Wendy"]="https://i.imgur.com/Wsmod9D.png"
IMAGE_MAP["Arrowstorm"]="https://i.imgur.com/S1ripwh.png"
IMAGE_MAP["Astronaut Butters"]="https://i.imgur.com/8mxZYey.png"
IMAGE_MAP["Bandita Sally"]="https://i.imgur.com/BaievY8.png"
IMAGE_MAP["Barrel Dougie"]="https://i.imgur.com/aVpluQf.png"
IMAGE_MAP["Big Gay Al"]="https://i.imgur.com/87GBjLl.png"
IMAGE_MAP["Big Mesquite Murph"]="https://i.imgur.com/H6N1r7X.png"
IMAGE_MAP["Blood Elf Bebe"]="https://i.imgur.com/cqnYji8.png"
IMAGE_MAP["Bounty Hunter Kyle"]="https://i.imgur.com/rgrwvjJ.png"
IMAGE_MAP["Buccaneer Bebe"]="https://i.imgur.com/59alHpI.png"
IMAGE_MAP["Calamity Heidi"]="https://i.imgur.com/77Iw26H.png"
IMAGE_MAP["Canadian Knight Ike"]="https://i.imgur.com/HMStIEv.png"
IMAGE_MAP["Captain Wendy"]="https://i.imgur.com/ucMs3wI.png"
IMAGE_MAP["Catapult Timmy"]="https://i.imgur.com/PBklFRE.png"
IMAGE_MAP["Chicken Coop"]="https://i.imgur.com/3ojGatv.png"
IMAGE_MAP["Choirboy Butters"]="https://i.imgur.com/JJ8ymYn.png"
IMAGE_MAP["City Wok Guy"]="https://i.imgur.com/FbgknLk.png"
IMAGE_MAP["Classi"]="https://i.imgur.com/fBf5FqL.png"
IMAGE_MAP["Cock Magic"]="https://i.imgur.com/HIa3kKG.png"
IMAGE_MAP["Cupid Cartman"]="https://i.imgur.com/SkDnvBR.png"
IMAGE_MAP["Cyborg Kenny"]="https://i.imgur.com/LDUlsYs.png"
IMAGE_MAP["Dark Angel Red"]="https://i.imgur.com/4qPuWwU.png"
IMAGE_MAP["Dark Mage Craig"]="https://i.imgur.com/ZrIrR6E.png"
IMAGE_MAP["Deckhand Butters"]="https://i.imgur.com/Gr4Wjqk.png"
IMAGE_MAP["Dogpoo"]="https://i.imgur.com/lFaxHc1.png"
IMAGE_MAP["Dragonslayer Red"]="https://i.imgur.com/YKAst6G.png"
IMAGE_MAP["Dwarf Engineer Dougie"]="https://i.imgur.com/px93VIk.png"
IMAGE_MAP["Dwarf King Clyde"]="https://i.imgur.com/jbxkhzd.png"
IMAGE_MAP["Elven King Bradley"]="https://i.imgur.com/3ra86Lq.png"
IMAGE_MAP["Energy Staff"]="https://i.imgur.com/FcKUgK0.png"
IMAGE_MAP["Enforcer Jimmy"]="https://i.imgur.com/koAFD4g.png"
IMAGE_MAP["Fireball"]="https://i.imgur.com/H0uPKUY.png"
IMAGE_MAP["Four-Assed Monkey"]="https://i.imgur.com/97uopmf.png"
IMAGE_MAP["Freeze Ray"]="https://i.imgur.com/KAAnlKv.png"
IMAGE_MAP["Friar Jimmy"]="https://i.imgur.com/1xFVINc.png"
IMAGE_MAP["Frontier Bradley"]="https://i.imgur.com/vS5AXF3.png"
IMAGE_MAP["Gizmo Ike"]="https://i.imgur.com/gAhJaeS.png"
IMAGE_MAP["Grand Wizard Cartman"]="https://i.imgur.com/pPAMo4m.png"
IMAGE_MAP["Gunslinger Kyle"]="https://i.imgur.com/d4kkzbQ.png"
IMAGE_MAP["Hallelujah"]="https://i.imgur.com/qZaXhv2.png"
IMAGE_MAP["Hercules Clyde"]="https://i.imgur.com/TWC9acE.png"
IMAGE_MAP["Hermes Kenny"]="https://i.imgur.com/72PBWVQ.png"
IMAGE_MAP["Hookhand Clyde"]="https://i.imgur.com/LOdy5nU.png"
IMAGE_MAP["Hyperdrive"]="https://i.imgur.com/0Pf8ffU.png"
IMAGE_MAP["Ice Sniper Wendy"]="https://i.imgur.com/7cKBal4.png"
IMAGE_MAP["Imp Tweek"]="https://i.imgur.com/WgUZH5O.png"
IMAGE_MAP["Incan Craig"]="https://i.imgur.com/PCvUvit.png"
IMAGE_MAP["Inuit Kenny"]="https://i.imgur.com/ZPRXuOQ.png"
IMAGE_MAP["Jesus"]="https://i.imgur.com/nUsfGM4.png"
IMAGE_MAP["Kyle of the Drow Elves"]="https://i.imgur.com/sPc1lfE.png"
IMAGE_MAP["Le Bard Jimmy"]="https://i.imgur.com/SgOuOOv.png"
IMAGE_MAP["Lightning Bolt"]="https://i.imgur.com/aNpiAZZ.png"
IMAGE_MAP["Manbearpig"]="https://i.imgur.com/3krEtAz.png"
IMAGE_MAP["Marcus"]="https://i.imgur.com/onRtlq2.png"
IMAGE_MAP["Marine Craig"]="https://i.imgur.com/wKNTcGI.png"
IMAGE_MAP["Mayor McDaniels"]="https://i.imgur.com/hRA9OWT.png"
IMAGE_MAP["Mecha Timmy"]="https://i.imgur.com/m8B3BlQ.png"
IMAGE_MAP["Medicine Woman Sharon"]="https://i.imgur.com/5dFuB1b.png"
IMAGE_MAP["Medusa Bebe"]="https://i.imgur.com/KP3MskO.png"
IMAGE_MAP["Mimsy"]="https://i.imgur.com/I3NTIB6.png"
IMAGE_MAP["Mind Control"]="https://i.imgur.com/0DB0TPU.png"
IMAGE_MAP["Mr. Hankey"]="https://i.imgur.com/JIQilLy.png"
IMAGE_MAP["Mr. Mackey"]="https://i.imgur.com/GXsULb1.png"
IMAGE_MAP["Mr. Slave Executioner"]="https://i.imgur.com/YeZRUGb.png"
IMAGE_MAP["Nathan"]="https://i.imgur.com/avEqT5c.png"
IMAGE_MAP["Nelly"]="https://i.imgur.com/DRLkBX9.png"
IMAGE_MAP["Officer Barbrady"]="https://i.imgur.com/Ersx6yg.png"
IMAGE_MAP["Outlaw Tweek"]="https://i.imgur.com/ynFnrQd.png"
IMAGE_MAP["Paladin Butters"]="https://i.imgur.com/LcG05ht.png"
IMAGE_MAP["PC Principal"]="https://i.imgur.com/WopGCAd.png"
IMAGE_MAP["Pigeon Gang"]="https://i.imgur.com/xjfibBX.png"
IMAGE_MAP["Pirate Ship Timmy"]="https://i.imgur.com/UfcaDZb.png"
IMAGE_MAP["Pocahontas Randy"]="https://i.imgur.com/uiwahnD.png"
IMAGE_MAP["Poison"]="https://i.imgur.com/F4IqdO6.png"
IMAGE_MAP["Pope Timmy"]="https://i.imgur.com/xAEJEHr.png"
IMAGE_MAP["Poseidon Stan"]="https://i.imgur.com/rWo7d3j.png"
IMAGE_MAP["Power Bind"]="https://i.imgur.com/NCAlbbl.png"
IMAGE_MAP["Powerfist Dougie"]="https://i.imgur.com/7CY0xdr.png"
IMAGE_MAP["President Garrison"]="https://i.imgur.com/69saQ1V.png"
IMAGE_MAP["Priest Maxi"]="https://i.imgur.com/ONbvr1E.png"
IMAGE_MAP["Princess Kenny"]="https://i.imgur.com/viQ9Q7B.png"
IMAGE_MAP["Program Stan"]="https://i.imgur.com/nplm2Ah.png"
IMAGE_MAP["Prophet Dougie"]="https://i.imgur.com/etIWhpy.png"
IMAGE_MAP["Purify"]="https://i.imgur.com/Qob9YcB.png"
IMAGE_MAP["Rat Swarm"]="https://i.imgur.com/3fFoCKc.png"
IMAGE_MAP["Regeneration"]="https://i.imgur.com/BzRNmsc.png"
IMAGE_MAP["Robin Tweek"]="https://i.imgur.com/0IJbbAC.png"
IMAGE_MAP["Robo Bebe"]="https://i.imgur.com/T0RZAku.png"
IMAGE_MAP["Rogue Token"]="https://i.imgur.com/7sF26Hj.png"
IMAGE_MAP["Santa Claus"]="https://i.imgur.com/zcRaPJm.png"
IMAGE_MAP["Satan"]="https://i.imgur.com/2R0P8qf.png"
IMAGE_MAP["Scout Ike"]="https://i.imgur.com/XGENnVa.png"
IMAGE_MAP["Sexy Nun Randy"]="https://i.imgur.com/XByocCa.png"
IMAGE_MAP["Shaman Token"]="https://i.imgur.com/v2n1fFh.png"
IMAGE_MAP["Sharpshooter Shelly"]="https://i.imgur.com/qYhZkuB.png"
IMAGE_MAP["Sheriff Cartman"]="https://i.imgur.com/c4aPwKU.png"
IMAGE_MAP["Shieldmaiden Wendy"]="https://i.imgur.com/S317fRe.png"
IMAGE_MAP["Sixth Element Randy"]="https://i.imgur.com/lprm8P1.png"
IMAGE_MAP["Sizzler Stuart"]="https://i.imgur.com/4jy6ACH.png"
IMAGE_MAP["Smuggler Ike"]="https://i.imgur.com/1ZtZ9iP.png"
IMAGE_MAP["Sorceress Liane"]="https://i.imgur.com/PtKwIja.png"
IMAGE_MAP["Space Pilot Bradley"]="https://i.imgur.com/WWNH8a5.png"
IMAGE_MAP["Space Warrior Token"]="https://i.imgur.com/dGP81dT.png"
IMAGE_MAP["Stan of Many Moons"]="https://i.imgur.com/3WuNNY3.png"
IMAGE_MAP["Stan the Great"]="https://i.imgur.com/7wddqdH.png"
IMAGE_MAP["Starvin' Marvin"]="https://i.imgur.com/aEevO0J.png"
IMAGE_MAP["Storyteller Jimmy"]="https://i.imgur.com/r5YLNq5.png"
IMAGE_MAP["Swashbuckler Red"]="https://i.imgur.com/h7HYNfC.png"
IMAGE_MAP["Swordsman Garrison"]="https://i.imgur.com/t0Cqr0J.png"
IMAGE_MAP["Terrance and Phillip"]="https://i.imgur.com/5Zvxqjt.png"
IMAGE_MAP["Terrance Mephesto"]="https://i.imgur.com/RQGv6zu.png"
IMAGE_MAP["The Amazingly Randy"]="https://i.imgur.com/pVyO6MY.png"
IMAGE_MAP["The Master Ninjew"]="https://i.imgur.com/UQCtBSS.png"
IMAGE_MAP["Thunderbird"]="https://i.imgur.com/q8nOEtZ.png"
IMAGE_MAP["Towelie"]="https://i.imgur.com/sKY0zcR.png"
IMAGE_MAP["Transmogrify"]="https://i.imgur.com/nIWtaqv.png"
IMAGE_MAP["Underpants Gnomes"]="https://i.imgur.com/2w7P6uE.png"
IMAGE_MAP["Unholy Combustion"]="https://i.imgur.com/NConqyH.png"
IMAGE_MAP["Visitors"]="https://i.imgur.com/z1W2JFY.png"
IMAGE_MAP["Warboy Tweek"]="https://i.imgur.com/Ege8b3S.png"
IMAGE_MAP["Witch Doctor Token"]="https://i.imgur.com/vQXwvg1.png"
IMAGE_MAP["Witch Garrison"]="https://i.imgur.com/jvKMdPV.png"
IMAGE_MAP["Youth Pastor Craig"]="https://i.imgur.com/EVUyV2o.png"
IMAGE_MAP["Zen Cartman"]="https://i.imgur.com/fUTDmb6.png"
IMAGE_MAP["Unknown"]="https://i.imgur.com/GFJeSzn.jpg" #Needs update
IMAGE_MAP["Captain Diabetes"]="https://i.imgur.com/qh2fE87.png"
IMAGE_MAP["Chaos Hamsters"]="https://i.imgur.com/nlJ8vmh.png"
IMAGE_MAP["The Chomper"]="https://i.imgur.com/5LX7vzk.png"
IMAGE_MAP["Super Fart"]="https://i.imgur.com/zAExzn1.png"
IMAGE_MAP["Fastpass"]="https://i.imgur.com/kVQbzHs.png"
IMAGE_MAP["Lava!"]="https://i.imgur.com/pDiq6yP.png"
IMAGE_MAP["Mosquito"]="https://i.imgur.com/LdiV4U9.png"
IMAGE_MAP["Professor Chaos"]="https://i.imgur.com/E4EgEES.png"
IMAGE_MAP["Super Craig"]="https://i.imgur.com/CG5zl37.png"
IMAGE_MAP["Toolshed"]="https://i.imgur.com/ELUrcTC.png"
IMAGE_MAP["Doctor Timothy"]="https://i.imgur.com/zhZzqDE.png"
IMAGE_MAP["General Disarray"]="https://i.imgur.com/h7i5m5a.png"
IMAGE_MAP["Human Kite"]="https://i.imgur.com/5Pq30UC.png"
IMAGE_MAP["Mint-Berry Crunch"]="https://i.imgur.com/M6AvlYn.png"
IMAGE_MAP["Tupperware"]="https://i.imgur.com/1KIv5pf.png"
IMAGE_MAP["Wonder Tweek"]="https://i.imgur.com/RLIMAwA.png"
IMAGE_MAP["Mysterion"]="https://i.imgur.com/wxGjiUX.png"
IMAGE_MAP["The Coon"]="https://i.imgur.com/71aV78Y.png"
IMAGE_MAP["Call Girl"]="https://i.imgur.com/OlhkqdV.png"
IMAGE_MAP["Mary Jane Randy"]="https://i.imgur.com/3AAWsms.png"
IMAGE_MAP["Firkle"]="https://i.imgur.com/WiT1kP4.png"
IMAGE_MAP["Michael"]="https://i.imgur.com/SmZcL6I.png"
IMAGE_MAP["Pete"]="https://i.imgur.com/I7nMVGT.png"
IMAGE_MAP["Henrietta"]="https://i.imgur.com/27GAQZu.png"
IMAGE_MAP["Alternate Human Kite"]="https://i.imgur.com/I7OH3XK.png"
IMAGE_MAP["Woodland Critters"]="https://i.imgur.com/OQo7VLO.png"
IMAGE_MAP["Archangel Bradley"]="https://i.imgur.com/heuwyjD.png"
IMAGE_MAP["Nymph Nichole"]="https://i.imgur.com/u8rGfS0.png"
IMAGE_MAP["Commander Hat"]="https://i.imgur.com/8jtiArX.png"
IMAGE_MAP["War Hero Ned"]="https://i.imgur.com/GyKZTTU.png"
IMAGE_MAP["Invincibility"]="https://i.imgur.com/T3QoQdk.png"
IMAGE_MAP["Castle Defender"]="https://i.imgur.com/0X1OM1K.png"
IMAGE_MAP["Crusader"]="https://i.imgur.com/HcdY0eE.png"
IMAGE_MAP["Hunter Jimbo"]="https://i.imgur.com/K1poLJU.png"
IMAGE_MAP["Scuzzlebutt"]="https://i.imgur.com/n81BD1p.png"
IMAGE_MAP["Infiltrator Kevin"]="https://i.imgur.com/J03Oyg4.png"
IMAGE_MAP["Cow Stampede"]="https://i.imgur.com/VLelzZ0.png"
IMAGE_MAP["Changeling Red"]="https://i.imgur.com/fdgHVTA.png"
IMAGE_MAP["Member Berries"]="https://i.imgur.com/2WtlvK8.png"
IMAGE_MAP["S-Wow Tittybang"]="https://i.imgur.com/d414hYz.png"
IMAGE_MAP["Future Randy"]="https://i.imgur.com/PVV1Viu.png"
IMAGE_MAP["Full Moon Sparky"]="https://i.imgur.com/4WxeYZ6.png"
IMAGE_MAP["Arrow Tower"]="https://i.imgur.com/xmdlEiP.png"
IMAGE_MAP["Alchemist Scott"]="https://i.imgur.com/QQAF0zD.png"
IMAGE_MAP["Cyborg Tower"]="https://i.imgur.com/N9K5Fem.png"
IMAGE_MAP["Dr. Mephesto"]="https://i.imgur.com/JJoYLFe.png"
IMAGE_MAP["New Kid"]="" #Verify if this works or not

BACKGROUND_MAP={
	'neu,neu':[IMAGE_MAP["Nelly"],IMAGE_MAP["Nelly"]]
}
for theme1 in THEME_COLORS.keys():
	for theme2 in THEME_COLORS.keys():
		if theme1==theme2 or type(theme1)!=str or type(theme2)!=str: continue
		theme1_img = None #Stan
		theme2_img = None #Cartman
		if theme1=='adv':
			theme1_img=IMAGE_MAP["Stan of Many Moons"]
		elif theme1=='sci':
			theme1_img=IMAGE_MAP["Program Stan"]
		elif theme1=='mys':
			theme1_img=IMAGE_MAP["Poseidon Stan"]
		elif theme1=='fan':
			theme1_img=IMAGE_MAP["Stan the Great"]
		elif theme1=='sup':
			theme1_img=IMAGE_MAP["Toolshed"]
		else:
			theme1_img=IMAGE_MAP["Nelly"]
		if theme2=='adv':
			theme2_img=IMAGE_MAP["Sheriff Cartman"]
		elif theme2=='sci':
			theme2_img=IMAGE_MAP["A.W.E.S.O.M.-O 4000"]
		elif theme2=='mys':
			theme2_img=IMAGE_MAP["Zen Cartman"]
		elif theme2=='fan':
			theme2_img=IMAGE_MAP["Grand Wizard Cartman"]
		elif theme2=='sup':
			theme2_img=IMAGE_MAP["The Coon"]
		else:
			theme2_img=IMAGE_MAP["Nelly"]
		BACKGROUND_MAP[f'{theme1},{theme2}']=[theme1_img,theme2_img]



current_images=list(IMAGE_MAP.keys())
for key in current_images:
	IMAGE_MAP[key.upper()]=IMAGE_MAP[key]

THEMES=[
"adv",
"fan",
"mys",
"neu",
"sci",
"sup"
]

THEME_PATH={}
THEME_PATH["adv"]="https://vignette.wikia.nocookie.net/southparkphonedestroyer/images/8/85/Advicon.png/revision/latest/scale-to-width-down/50"
THEME_PATH["fan"]="https://raw.githubusercontent.com/rbrasga/SPPD-Deck-Tracker/master/CARDS/fan.png"
THEME_PATH["mys"]="https://raw.githubusercontent.com/rbrasga/SPPD-Deck-Tracker/master/CARDS/mys.png"
THEME_PATH["neu"]="https://raw.githubusercontent.com/rbrasga/SPPD-Deck-Tracker/master/CARDS/neu.png"
THEME_PATH["sci"]="https://raw.githubusercontent.com/rbrasga/SPPD-Deck-Tracker/master/CARDS/sci.png"
THEME_PATH["sup"]="https://raw.githubusercontent.com/rbrasga/SPPD-Deck-Tracker/master/CARDS/sup.png"

CARD_BUILDER={
	# Center X, Center Y, Delta X, Delta Y (Delta -> to the edge)
	"NAME" : [375,202,225,18],
	"LEVEL" : [374,252,40,12],
	"COST" : [124,267,29,45],
	"HEALTH" : [121,467,60,40],
	"ATTACK" : [121,635,60,40],
	"DESC" : [388,865,222,72],
}