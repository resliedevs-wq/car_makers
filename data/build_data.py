"""Build the 2025 light-vehicle production dataset (country x brand x model).

Units are thousands of light vehicles (cars, SUVs, pickups, vans) built in that
country in calendar 2025. Confidence: "r" = reported by an official body or the
maker for that country, "e" = estimate (split of a reported group figure, or
derived from plant/model knowledge). Models are relative weights within the
brand-in-country volume, always estimates.

Run:  python3 -I data/build_data.py   ->  writes data/cars2025.json and data/cars2025.csv
"""
import csv
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# Brand -> home origin group (used for colour in the chart).
ORIGIN = {
    "Chinese": "BYD Denza Fangchengbao Geely Lynk&Co Zeekr Chery Jetour Exeed iCar Changan Deepal Avatr "
               "Hongqi Bestune Jetta Wuling Baojun Roewe MG IM Maxus Haval Tank GWM Wey Leapmotor Xpeng "
               "LiAuto Xiaomi NIO Aito Trumpchi Aion Dongfeng Voyah Forthing BAIC Arcfox Foton JAC JMC "
               "Jinbei DFSK Tenet",
    "Japanese": "Toyota Lexus Honda Acura Nissan Mazda Subaru Suzuki Daihatsu Mitsubishi Isuzu Fuso",
    "German": "Volkswagen Audi Porsche Mercedes-Benz BMW Mini Opel",
    "American": "Ford Lincoln Chevrolet GMC Cadillac Buick Jeep Ram Dodge Chrysler Tesla",
    "Korean": "Hyundai Kia Genesis KGM",
    "Other European": "Renault Dacia Peugeot Citroen Fiat AlfaRomeo Volvo Skoda SEAT Cupra LandRover Iveco",
    "Other": "Maruti Tata Mahindra Perodua Proton Lada GAZ IranKhodro Saipa KMC Bahman VinFast",
}
BRAND_ORIGIN = {b: o for o, names in ORIGIN.items() for b in names.split()}
DISPLAY = {"Lynk&Co": "Lynk & Co", "LiAuto": "Li Auto", "AlfaRomeo": "Alfa Romeo",
           "LandRover": "Land Rover", "IranKhodro": "Iran Khodro", "GWM": "GWM pickups",
           "Maruti": "Maruti Suzuki", "KMC": "Kerman Motor (KMC)"}

# country: (light-vehicle total k, OICA all-vehicle total k, source note, brands)
# brands: "Brand units conf | Model:w, Model:w"
C = {}

def country(name, light, oica, note, rows):
    C[name] = {"light": light, "oica": oica, "note": note, "rows": rows.strip().splitlines()}

country("China", 33300, 34531, "OICA/CAAM total 34.53M incl. ~1.2M medium & heavy trucks and buses; CPCA passenger output 29.63M", """
BYD 4100 r | Seagull:500, Qin PLUS:450, Song PLUS:400, Yuan PLUS (Atto 3):350, Qin L:350, Sealion 05/06:300, Song Pro:300, Seal 06:300, Yuan UP:250, Dolphin:250, Han:200, Tang:150, Seal:150
Denza 150 e | D9:90, N9/N8L:60
Fangchengbao 230 e | Tai 3:90, Bao 5:70, Tai 7:70
Geely 2450 r | Galaxy Xingyuan:450, Emgrand:350, Coolray/Binyue:300, Xingyue L:230, Galaxy E5:200, Boyue:200, Galaxy A7:150, Galaxy Starship 7:150, Monjaro:120
Lynk&Co 350 e | 08:90, 900:80, 06:70, 03:60, Z10:50
Zeekr 220 e | 7X:80, 001:60, 007:50, Mix:30
Volvo 150 e | XC60:70, S90:40, XC40:25, S60:15
Chery 1750 r | Tiggo 7:400, Tiggo 8:350, Tiggo 4 / Omoda 5:300, Jaecoo 7:200, Arrizo 5:200, Arrizo 8:150, Fengyun A8/T9:150
Jetour 650 e | Traveller:250, X70:200, Dashing:150, X90:50
Exeed 150 e | Yaoguang:70, Sterra:50, TX/LX:30
iCar 100 e | 03:60, V23:40
Changan 1900 r | Kaicene vans & trucks:350, CS75 PLUS:300, Eado:250, CS55 PLUS:200, Qiyuan:150, UNI-K/UNI-V:150, Lumin:150, CS35 PLUS:100, X5 PLUS:100
Deepal 330 r | S07:110, S05:90, L07:70, G318:60
Avatr 130 r | 07:60, 11:40, 12:30
Ford 280 e | Ranger/Transit (JMC):120, Explorer:60, Territory:60, Mondeo:40
JMC 200 e | Yuhu pickups:90, Kaiyun light trucks:110
Mazda 100 e | CX-5:40, Mazda3:35, EZ-6:25
Volkswagen 1880 e | Lavida:350, Sagitar:300, Magotan/Passat:200, Tiguan L:200, Bora:150, Tayron:150, T-Roc:150, ID. series:150, Teramont:100, Lamando:80
Audi 600 e | A6L:200, A4L:150, Q5L:150, Q3/A3:100
Jetta 120 e | VS5:70, VS7:30, VA3:20
Toyota 1500 e | Corolla/Levin:350, Camry:250, RAV4/Wildlander:250, Corolla Cross/Frontlander:200, Highlander/Crown Kluger:150, bZ3X/bZ5:150, Sienna/Granvia:80, Avalon/Crown:70
Honda 600 e | Accord:120, CR-V/Breeze:180, Civic/Integra:150, Vezel/XR-V:90, Odyssey/Elysion:60
Nissan 600 e | Sylphy:300, Qashqai:80, X-Trail:80, Teana:60, N7:50, Frontier (Dongfeng):30
Hongqi 460 r | H5:150, HS5:110, H9:60, EH7/HQ9:80, HS3:60
Bestune 150 e | Pony:70, T77/B70:80
Buick 400 e | GL8:110, Excelle GT/Verano:120, Envision:90, Envista:80
Cadillac 90 e | CT5:30, XT5:30, GT4/Lyriq:30
Chevrolet 60 e | Cavalier/Monza:40, Trax/Seeker:20
Wuling 1250 e | Bingo:250, Hongguang Mini EV:250, Starlight:200, Hongguang MPV:200, Rongguang vans:150, Xingguang/Jiachen:200
Baojun 380 e | Yep/Yep Plus:150, Yunduo:120, Xiangjing/510:110
Roewe 330 e | i5:110, RX5:90, D7:60, Imax8:70
MG 560 e | MG ZS/ZS Hybrid+:200, MG4:130, MG3:100, MG HS:80, MG5:50
IM 80 r | LS6:45, L6:35
Maxus 220 e | Deliver 9 vans:80, T60/T90 pickups:80, Mifa 9/G10:60
Tesla 852 r | Model Y:560, Model 3:292
BMW 620 e | 3 Series Li:200, 5 Series Li:160, X3 Li:160, X1:100
Mercedes-Benz 480 e | C-Class L:180, E-Class L:140, GLC L:120, EQE/GLA/GLB:40
Hyundai 200 e | Elantra:80, Tucson L:60, Custo/Sonata:60
Kia 250 e | Seltos/Sportage:120, K3/K5:70, EV5 (export):60
Haval 600 e | H6:250, Jolion:150, Big Dog / Raptor:120, H9:80
Tank 230 r | 300:110, 400:60, 500:60
GWM 180 e | Poer/Cannon:180
Wey 100 e | Lanshan:60, Gaoshan:40
Leapmotor 597 r | C10:150, C11:120, B10:110, C16:90, T03:70, B01:57
Xpeng 429 r | Mona M03:170, P7+:80, G6:60, G7:60, X9:59
LiAuto 406 r | L6:170, L7:70, L8/L9:80, i8/i6:50, Mega:36
Xiaomi 410 r | SU7:220, YU7:190
NIO 326 r | Onvo L60/L90:130, NIO ES6/EC6/ET5:140, Firefly:56
Aito 420 r | M8:150, M9:120, M7:100, M5:50
Trumpchi 380 e | GS4/GS3:130, M8/M6:110, E8/S7:80, Empow:60
Aion 300 e | S/S Max:110, Y Plus:90, V/RT/UT:100
Dongfeng 476 e | eπ 007/008:140, Fengshen L7/Mage:136, Captain light trucks:200
Voyah 150 r | Free:60, Dreamer:60, Passion/Courage:30
Forthing 150 e | Lingzhi MPV:70, T5 EVO / Xinghai:80
BAIC 350 e | BJ40/BJ60:150, X7/X55:100, U5 Plus:100
Arcfox 160 r | αT5:90, Kaola:70
Foton 400 e | Aumark light trucks:180, View/Toano vans:120, Tunland pickups:100
JAC 450 e | Shuailing light trucks:160, JS4/JS6:120, T8/T9 pickups:90, Refine MPV:80
Jinbei 100 e | Haise vans:100
DFSK 150 e | K-series mini trucks:90, Glory:60
""")

country("United States", 10000, 10244, "OICA total 10.24M (Ward's); manufacturer split from Automotive World / Omdia 2025 light-vehicle forecast by group", """
Ford 1950 r | F-150 / Super Duty:900, Bronco:200, Explorer:200, Escape:130, Transit:150, Expedition:110, Ranger:70, Mustang:50, Bronco/others:140
Lincoln 90 e | Navigator:40, Aviator:30, Corsair:20
Chevrolet 1050 e | Silverado:550, Tahoe/Suburban:200, Traverse:150, Colorado:100, Express:30, Corvette:20
GMC 420 e | Sierra:300, Yukon:70, Canyon:30, Hummer EV:20
Cadillac 140 e | Escalade:50, Lyriq/Vistiq:40, XT4/XT5/XT6:30, CT4/CT5:20
Toyota 1250 e | Camry:300, RAV4:200, Grand Highlander/Highlander:250, Tundra:150, Corolla Cross:150, Sienna:100, Sequoia:40, Tacoma (TX):60
Lexus 110 e | TX:60, ES:30, RX:20
Honda 860 e | CR-V:300, Civic:150, Pilot/Passport:170, Accord:100, Odyssey:100, Ridgeline:40
Acura 115 e | MDX:60, RDX:35, Integra/TLX:20
Jeep 450 e | Grand Cherokee:250, Wrangler:150, Gladiator:50
Ram 400 e | Ram 1500:400
Dodge 80 e | Durango:60, Ram ProMaster/others:20
Hyundai 420 e | Tucson:130, Santa Fe:110, Ioniq 5/Ioniq 9:100, Santa Cruz:40, Elantra/Genesis GV70:40
Kia 350 e | Telluride:120, Sorento:90, Sportage:80, EV9/EV6:60
Tesla 632 r | Model Y:400, Model 3:150, Model S/X:40, Cybertruck:42
Nissan 470 e | Rogue:200, Altima:100, Frontier:70, Pathfinder:60, Murano:40
BMW 387 r | X3:150, X5:140, X7:50, X6/XM:47
Subaru 337 r | Outback:110, Ascent:60, Crosstrek:90, Forester:77
Mercedes-Benz 260 e | GLE:110, GLS:60, GLE Coupé/EQ SUVs:50, Sprinter:40
Volkswagen 180 e | Atlas/Atlas Cross Sport:130, ID.4:50
Mazda 140 e | CX-50:140
""")

country("Japan", 8100, 8410, "OICA/JAMA total 8.41M; maker domestic production from company releases (via MarkLines)", """
Toyota 2900 r | RAV4:300, Corolla family:300, Yaris/Yaris Cross:350, Prius:150, Alphard/Vellfire:180, Noah/Voxy:250, Sienta:180, Land Cruiser 250/300:280, Harrier:150, Crown:100, Hiace:100, Roomy/Raize:200, others:360
Lexus 380 e | RX:100, NX:110, LX/GX:60, ES/IS:60, UX/LBX:50
Suzuki 956 r | Spacia:180, Hustler:110, Wagon R:90, Swift:100, Jimny:90, Every/Carry:130, Solio:80, Alto:80, others:96
Daihatsu 779 r | Tanto:180, Move:160, Mira e:S:110, Hijet:120, Taft:80, Rocky/Raize:60, others:69
Mazda 717 r | CX-5:250, CX-30:130, Mazda3:100, CX-60/CX-80:120, CX-3:50, MX-5:30, CX-90:37
Honda 690 r | N-Box:220, Freed:120, Step WGN:70, N-WGN/N-One/N-Van:120, ZR-V/Vezel:100, Civic:60
Nissan 565 r | Serena:90, Note/Aura:100, Roox/Dayz/Sakura:110, X-Trail/Rogue:90, Leaf:30, Patrol/Kicks/others:145
Subaru 540 r | Forester:180, Crosstrek:150, Outback:80, Impreza:60, WRX/Solterra/BRZ:70
Mitsubishi 471 r | Outlander:120, eK/Delica Mini:110, Delica:60, Eclipse Cross:40, Nissan kei (OEM):141
Isuzu 90 e | Elf light trucks:90
Fuso 60 e | Canter light trucks:60
""")

country("India", 5900, 6491, "OICA/SIAM total 6.49M incl. ~0.55M medium & heavy trucks and buses; Maruti CY2025 production 2.255M (company)", """
Maruti 2150 r | Dzire:220, Swift:210, Baleno:200, Fronx:200, Brezza:190, Ertiga:190, WagonR:180, Eeco:130, Grand Vitara/Victoris:180, Alto/S-Presso:140, Super Carry/others:150, e Vitara/XL6/Jimny:160
Toyota 435 e | Innova Hycross/Crysta:130, Hyryder:80, Fortuner/Hilux:60, Glanza/Taisor/Rumion (Maruti-built):165
Hyundai 760 e | Creta:220, Venue:150, Exter:90, i20:80, Verna:70, Grand i10 Nios:90, Alcazar/Aura:60
Mahindra 850 e | Scorpio-N/Classic:200, XUV 3XO:120, Thar/Thar Roxx:130, XUV700/7XO:100, Bolero SUV:90, Bolero pickups:180, BE 6/XEV 9e:30
Tata 780 e | Nexon:200, Punch:190, Tiago/Tigor:110, Harrier/Safari:70, Altroz/Curvv:70, Ace small trucks:140
Kia 330 e | Sonet:120, Seltos:100, Carens:70, Syros:40
Honda 110 e | Amaze:45, City:25, Elevate/WR-V:40
Skoda 130 e | Kylaq:60, Kushaq:35, Slavia:35
Volkswagen 80 e | Virtus:45, Taigun:35
Nissan 60 e | Magnite:60
MG 70 e | Windsor EV:40, Hector/Astor/Comet:30
Renault 50 e | Kiger:20, Triber:20, Kwid:10
""")

country("Germany", 4360, 4149, "VDA passenger-car output 4.15M (cars only) + ~0.2M Mercedes vans; brand split estimated from plant volumes", """
Volkswagen 1050 e | Golf:350, Tiguan:250, Passat:120, ID.3/ID.4/ID.7:200, ID. Buzz/Multivan:80, Touran:50
Mercedes-Benz 1100 e | C-Class:220, E-Class:180, GLC:200, S-Class/EQS:110, A/B/CLA:190, Sprinter/Vito vans:200
BMW 870 e | 3 Series:200, 5 Series/i5:200, X1:150, 1/2 Series:120, 7 Series/i7:60, i4:80, iX:60
Mini 100 e | Countryman:100
Audi 520 e | A5/A4:150, A6:120, A3:90, Q6 e-tron:70, Q4/Q5 e-tron (Zwickau):60, A8/e-tron GT:30
Porsche 230 e | Macan:80, Panamera:30, 911:50, Taycan:20, 718:20, Cayenne coupé:30
Opel 130 e | Astra:70, Grandland:60
Ford 160 e | Focus:100, Explorer/Capri EV:60
Tesla 200 e | Model Y:200
""")

country("Mexico", 3953, 4092, "INEGI RAIAVL light-vehicle production by manufacturer, Jan-Dec 2025 (official)", """
Chevrolet 657 e | Silverado:280, Equinox:150, Blazer:70, Equinox EV / Blazer EV:110, Cheyenne/others:47
GMC 200 e | Sierra:200
Nissan 659 r | Versa:160, Sentra:160, Kicks:130, NP300/Frontier:150, March/others:59
Ford 417 r | Maverick:220, Bronco Sport:140, Mustang Mach-E:57
Volkswagen 336 r | Jetta:200, Taos:110, Tiguan:26
Toyota 310 r | Tacoma:310
Kia 288 r | K3/K4:200, Rio/Hyundai HB20 (OEM):88
Ram 340 e | Ram 2500/3500:180, Ram 1500 Classic:80, ProMaster:80
Jeep 56 e | Compass:56
Mazda 175 r | CX-30:90, Mazda3:85
Honda 159 r | HR-V:159
Audi 147 r | Q5:147
BMW 95 r | 3 Series:75, 2 Series Coupé:20
Mercedes-Benz 57 r | GLB:57
""")

country("South Korea", 4045, 4102, "OICA/KAMA total 4.10M; maker split estimated from company domestic-plant data", """
Hyundai 1550 e | Avante/Elantra:200, Tucson:180, Santa Fe:180, Grandeur:150, Palisade:150, Kona:150, Sonata:80, Ioniq 5/6:120, Casper:60, Porter light truck:110, Staria:90, Venue:60
Genesis 200 e | G80:60, GV80:50, GV70:50, G90/GV60:40
Kia 1600 e | Sorento:200, Sportage:200, Carnival:170, Seltos:150, Niro:110, K5/K8:150, Ray:80, EV3/EV9/EV6:160, Bongo light truck:100, Trailblazer-sized others:280
Chevrolet 420 e | Trax Crossover:270, Trailblazer:150
Buick 70 e | Envista:40, Encore GX:30
Renault 100 e | Grand Koleos:60, Arkana:25, QM6:15
KGM 105 e | Torres:50, Actyon:25, Rexton/Musso:30
""")

country("Brazil", 2470, 2644, "ANFAVEA total 2.64M incl. ~0.17M trucks and buses; brand split estimated from registrations and exports", """
Fiat 560 e | Strada:180, Argo:90, Mobi:60, Pulse:60, Fastback:40, Toro:70, Titano/others:60
Jeep 220 e | Compass:100, Renegade:70, Commander:50
Volkswagen 470 e | Polo:130, T-Cross:100, Nivus:60, Virtus:50, Tera:80, Saveiro:50
Chevrolet 340 e | Onix/Onix Plus:150, Tracker:100, S10:40, Spin:30, Montana:20
Hyundai 210 e | HB20:140, Creta:70
Toyota 230 e | Corolla Cross:120, Corolla:50, Yaris:60
Renault 200 e | Kwid:60, Kardian:60, Duster:50, Oroch:30
Honda 90 e | HR-V:50, City:25, WR-V:15
Nissan 80 e | Kicks:80
Citroen 60 e | Basalt/C3/Aircross:60
Peugeot 50 e | 208:50
""")

country("Spain", 2240, 2274, "ANFAC total 2.27M; brand split estimated from plant volumes", """
SEAT 230 e | Ibiza:110, Arona:120
Cupra 180 e | Formentor:130, Leon:50
Volkswagen 250 e | T-Cross:150, Taigo:100
Renault 380 e | Captur:120, Austral:100, Symbioz:80, Espace/Rafale:80
Peugeot 330 e | 2008:150, 208:80, Rifter/Partner:100
Citroen 270 e | C4/C4 X:80, Berlingo:120, C3 Aircross:70
Opel 220 e | Corsa:150, Combo:70
Toyota 50 e | Proace City:50
Mercedes-Benz 110 e | V-Class/Vito:110
Ford 120 e | Kuga:120
""")

country("Czechia", 1450, 1453, "Autosap total 1.45M; brand split estimated", """
Skoda 900 e | Octavia:330, Kodiaq:150, Karoq:100, Fabia:90, Kamiq:70, Scala:50, Enyaq/Elroq:110
Hyundai 330 e | Tucson:180, Kona Electric:80, i30:70
Toyota 220 e | Yaris:140, Aygo X:80
""")

country("Turkey", 1240, 1419, "OSD total 1.42M incl. ~0.18M trucks and buses; brand split estimated", """
Ford 370 e | Transit Custom:170, Transit:120, Transit Courier/Puma Gen-E:80
Renault 280 e | Clio:180, Duster:100
Hyundai 230 e | i20:120, i10:70, Bayon:40
Toyota 200 e | C-HR:140, Corolla:60
Fiat 160 e | Egea:100, Doblo:60
""")

country("France", 1410, 1464, "CCFA total 1.46M (cars and LCV); brand split estimated", """
Renault 520 e | Clio:130, R5/R4:110, Scenic/Megane E-Tech:80, Kangoo:80, Master/Trafic:120
Peugeot 450 e | 3008:130, 5008:70, 308/408:120, Expert/Boxer:130
Citroen 120 e | C5 Aircross:60, Jumpy/Jumper:60
Toyota 250 e | Yaris:170, Yaris Cross:80
Opel 70 e | Vivaro/Movano:70
""")

country("Thailand", 1350, 1456, "TAIA total 1.46M; brand split estimated", """
Toyota 560 e | Hilux:280, Fortuner:80, Yaris Ativ:110, Corolla Cross:90
Isuzu 290 e | D-Max:240, MU-X:50
Mitsubishi 150 e | Triton:90, Pajero Sport:30, Attrage/Mirage:30
Honda 110 e | City:60, HR-V:30, Civic:20
Ford 130 e | Ranger:100, Everest:30
BYD 50 e | Atto 3:20, Dolphin:20, Seal:10
""")

country("Canada", 1214, 1237, "OICA total 1.24M; group split from Automotive World / Omdia 2025 forecast", """
Toyota 430 e | RAV4:300, others:130
Lexus 100 e | RX:100
Honda 416 r | CR-V:250, Civic:166
Chrysler 100 e | Pacifica/Voyager:100
Dodge 42 e | Charger Daytona:42
Chevrolet 126 r | Silverado:120, BrightDrop:6
""")

country("Indonesia", 1120, 1148, "Gaikindo total 1.15M; brand split estimated", """
Toyota 420 e | Avanza/Veloz:150, Innova Zenix:90, Calya:60, Rush:60, Fortuner:60
Daihatsu 280 e | Sigra:80, Xenia:50, Gran Max:70, Ayla:50, Terios:30
Mitsubishi 130 e | Xpander:90, L300:25, Pajero Sport:15
Honda 110 e | Brio:60, BR-V/HR-V:50
Suzuki 110 e | Carry:50, Ertiga/XL7:60
Hyundai 50 e | Creta/Stargazer:50
""")

country("Slovakia", 1100, 1070, "AIA SR total 1.07M; brand split estimated", """
Kia 340 e | Sportage:180, Ceed/XCeed:160
Peugeot 230 e | 208:230
Citroen 60 e | C3:60
Volkswagen 110 e | Touareg:60, Up!/others:50
Porsche 70 e | Cayenne:70
Audi 70 e | Q7/Q8:70
Skoda 90 e | Superb:90
LandRover 130 e | Defender:110, Discovery:20
""")

country("Russia", 750, 854, "OAR total 0.85M; brand split estimated", """
Lada 330 e | Granta:200, Vesta:100, Niva:30
Haval 140 e | Jolion:60, F7:50, H6/Dargo:30
GAZ 60 e | Gazelle:60
Tenet 60 e | T7:35, T4:25
""")

country("United Kingdom", 700, 765, "SMMT total 0.76M; brand split estimated", """
Nissan 270 e | Qashqai:170, Juke:80, Leaf:20
LandRover 170 e | Range Rover/RR Sport:120, Velar/Discovery Sport:50
Mini 140 e | Cooper:140
Toyota 110 e | Corolla:110
""")

country("Malaysia", 690, 748, "MAA total 0.75M; brand split estimated", """
Perodua 360 e | Bezza:110, Myvi:100, Axia:80, Ativa/Alza:70
Proton 170 e | Saga:70, X50:50, X70/X90:30, Persona:20
Honda 80 e | City:40, HR-V:40
Toyota 60 e | Vios/Yaris Cross:60
""")

country("Poland", 580, 628, "PZPM total 0.63M; brand split estimated", """
Volkswagen 250 e | Caddy:150, Crafter:100
Jeep 100 e | Avenger:100
Fiat 80 e | 600:80
""")

country("South Africa", 590, 618, "Naamsa total 0.62M; brand split estimated", """
Toyota 150 e | Hilux:90, Corolla Cross:40, Hiace:20
Volkswagen 130 e | Polo:130
Ford 130 e | Ranger:130
BMW 65 e | X3:65
Mercedes-Benz 60 e | C-Class:60
""")

country("Romania", 545, 546, "APIA total 0.55M; brand split estimated", """
Dacia 300 e | Duster:200, Bigster:100
Ford 240 e | Puma:150, Transit Courier:90
""")

country("Morocco", 500, 502, "OICA total 0.50M; brand split estimated", """
Dacia 280 e | Sandero:200, Jogger/Logan:80
Peugeot 120 e | 208:120
""")

country("Argentina", 480, 491, "ADEFA total 0.49M (cars and LCV); brand split estimated", """
Toyota 160 e | Hilux:120, SW4:40
Volkswagen 80 e | Amarok:40, Taos:40
Ford 60 e | Ranger:60
Peugeot 60 e | 208:40, 2008:20
Fiat 50 e | Cronos:50
""")

country("Uzbekistan", 462, 462, "OAR total 0.46M; brand split estimated", """
Chevrolet 380 e | Cobalt:120, Onix:100, Tracker:80, Damas/Labo:80
BYD 50 e | Song PLUS:30, Chazor:20
""")

country("Italy", 440, 474, "ANFIA total 0.47M; brand split estimated", """
Fiat 300 e | Ducato:200, Pandina:100
Jeep 60 e | Compass:40, Renegade:20
Iveco 50 e | Daily:50
""")

country("Hungary", 410, 412, "OICA total 0.41M; brand split estimated", """
Mercedes-Benz 150 e | CLA:90, GLB/A-Class:60
Audi 150 e | Q3/Q3 Sportback:150
Suzuki 100 e | Vitara:60, S-Cross:40
""")

country("Portugal", 330, 341, "ACAP total 0.34M; brand split estimated", """
Volkswagen 230 e | T-Roc:230
""")

country("Sweden", 252, 252, "Mobility Sweden total 0.25M (cars only)", """
Volvo 250 e | XC60:130, XC90/EX90:70, V60/V90:50
""")

country("Belgium", 240, 253, "Febiac total 0.25M; brand split estimated", """
Volvo 200 e | XC40/EX40:130, EX30:70
""")

country("Iran", 1050, None, "Inside OICA 'other countries' (2.13M); maker split estimated from Iranian ministry reports", """
IranKhodro 500 e | Tara:120, Dena:120, Peugeot Pars/207i:160, Runna/others:100
Saipa 380 e | Shahin:150, Quick:100, Saina/Tiba:130
KMC 80 e | J7/T8 (JAC/Chery-based):80
Bahman 50 e | Fidelity/Dignity:50
""")

country("Vietnam", 300, None, "Inside OICA 'other countries'; maker split estimated", """
VinFast 150 e | VF 3:60, VF 5:50, VF 6/VF 7:40
Hyundai 60 e | Accent/Creta:60
""")

country("Taiwan", 230, None, "Inside OICA 'other countries'; maker split estimated", """
Toyota 100 e | Corolla Cross:70, Hiace/others:30
""")

country("Pakistan", 180, 190, "PAMA total 0.19M; brand split estimated", """
Suzuki 100 e | Alto:60, Swift/Cultus:20, Ravi/Bolan:20
""")

country("Philippines", 120, None, "Inside OICA 'other countries'; maker split estimated", """
Toyota 80 e | Vios:30, Innova/Tamaraw:50
""")

country("Kazakhstan", 160, 171, "OAR total 0.17M; brand split estimated", """
Hyundai 60 e | Creta/Elantra/Tucson:60
""")

country("Slovenia", 61, 61, "OICA total 0.06M (Revoz)", """
Renault 61 e | Clio:61
""")

country("Serbia", 51, 51, "UPDVS total 0.05M (Kragujevac)", """
Fiat 51 e | Grande Panda:51
""")

# Countries with production but no brand above half a car (shown in methodology only):
SMALL = {"Egypt": 90, "Austria": 71, "Algeria": 43, "Colombia": 35, "Finland": 27, "Australia": 6}

# OICA world total 96.38M, minus ~3.4M medium/heavy trucks and buses, plus ~0.2M German vans.
WORLD_LIGHT = 93200
TOTAL_CARS = 1000
CUTOFF = WORLD_LIGHT / TOTAL_CARS / 2  # half a mini car, in thousands


def parse(rows):
    out = []
    for line in rows:
        head, models = line.split("|")
        brand, units, conf = head.split()
        ms = []
        for m in models.split(","):
            name, w = m.rsplit(":", 1)
            ms.append([name.strip(), float(w)])
        out.append({"brand": DISPLAY.get(brand, brand), "origin": BRAND_ORIGIN[brand],
                    "units": int(units), "conf": conf, "models": ms})
    return out


def allocate(values, total):
    """Round to nearest whole car (every kept value is >= 0.5 car, so >= 1),
    then nudge the slices with the largest rounding error until the sum is exact."""
    s = sum(values)
    raw = [v / s * total for v in values]
    n = [max(1, round(r)) for r in raw]
    while sum(n) != total:
        if sum(n) > total:
            i = min((i for i in range(len(n)) if n[i] > 1), key=lambda i: raw[i] - n[i])
            n[i] -= 1
        else:
            i = max(range(len(n)), key=lambda i: raw[i] - n[i])
            n[i] += 1
    return n


def main():
    all_b = [(cname, b) for cname, c in C.items() for b in parse(c["rows"])]
    # A mini car is 1/1000 of what is shown; dropping sub-half-car brands shrinks
    # that total, which moves the cutoff, so iterate until the kept set is stable.
    cutoff = CUTOFF
    while True:
        slices = [(cn, b) for cn, b in all_b if b["units"] >= cutoff]
        new = sum(b["units"] for _, b in slices) / TOTAL_CARS / 2
        if abs(new - cutoff) < 1e-9:
            break
        cutoff = new
    cars = allocate([b["units"] for _, b in slices], TOTAL_CARS)

    countries = {}
    for (cname, b), n in zip(slices, cars):
        if n == 0:
            continue
        b["cars"] = n
        countries.setdefault(cname, []).append(b)

    out = []
    for cname, brands in countries.items():
        c = C[cname]
        brands.sort(key=lambda b: -b["units"])
        out.append({
            "country": cname, "light": c["light"], "oica": c["oica"], "note": c["note"],
            "cars": sum(b["cars"] for b in brands),
            "attributed": sum(b["units"] for b in brands),
            "brands": brands,
        })
    out.sort(key=lambda c: -c["cars"])

    shown = sum(b["units"] for _, b in slices)
    meta = {"world_light_k": WORLD_LIGHT, "shown_k": shown, "total_cars": TOTAL_CARS,
            "vehicles_per_car": round(shown * 1000 / TOTAL_CARS),
            "dropped_countries_k": SMALL, "year": 2025}
    with open(os.path.join(HERE, "cars2025.json"), "w") as f:
        json.dump({"meta": meta, "countries": out}, f, ensure_ascii=False, separators=(",", ":"))

    with open(os.path.join(HERE, "cars2025.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["country", "brand", "brand_origin", "units_k", "mini_cars", "confidence", "model", "model_weight"])
        for c in out:
            for b in c["brands"]:
                for m, wt in b["models"]:
                    w.writerow([c["country"], b["brand"], b["origin"], b["units"], b["cars"],
                                "reported" if b["conf"] == "r" else "estimated", m, wt])

    # Summary to stdout for sanity checks.
    for c in out:
        print(f'{c["country"]:16} cars={c["cars"]:4}  brands={len(c["brands"]):3}  '
              f'attributed={c["attributed"]:6}k of light {c["light"]:6}k ({c["attributed"]/c["light"]:.0%})')
    print("total cars", sum(c["cars"] for c in out), " brand slices", sum(len(c["brands"]) for c in out))


if __name__ == "__main__":
    main()
