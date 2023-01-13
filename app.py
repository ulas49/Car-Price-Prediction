from flask import Flask,render_template,request
import pandas as pd 
import numpy as np 
import pickle

#venv/scripts/activate
#flask --app app.py --debug run

app=Flask(__name__)

keys = [
"Factory_Tuner,Luxury,High-Performance",
"Luxury,Performance",
"Luxury,High-Performance",
"Luxury",
"Performance",
"Flex_Fuel",
"Flex_Fuel,Performance",
"Crossover",
"Hatchback",
"Hatchback,Luxury,Performance",
"Hatchback,Luxury",
"Luxury,High-Performance,Hybrid",
"Diesel,Luxury",
"Hatchback,Performance",
"Hatchback,Factory_Tuner,Performance",
"High-Performance",
"Factory_Tuner,High-Performance",
"Exotic,High-Performance",
"Exotic,Factory_Tuner,High-Performance",
"Factory_Tuner,Performance",
"Exotic,Luxury",
"Exotic,Luxury,High-Performance",
"Exotic,Luxury,Performance",
"Factory_Tuner,Luxury,Performance",
"Flex_Fuel,Luxury",
"Crossover,Luxury",
"Hatchback,Factory_Tuner,Luxury,Performance",
"Crossover,Hatchback",
"Hybrid",
"Luxury,Performance,Hybrid",
"Crossover,Luxury,Performance,Hybrid",
"Crossover,Luxury,Performance",
"Exotic,Factory_Tuner,Luxury,High-Performance",
"Flex_Fuel,Luxury,High-Performance",
"Crossover,Flex_Fuel",
"Diesel",
"Hatchback,Diesel",
"Crossover,Luxury,Diesel",
"Crossover,Luxury,High-Performance",
"Exotic,Flex_Fuel,Factory_Tuner,Luxury,High-Performance",
"Exotic,Flex_Fuel,Luxury,High-Performance",
"Exotic,Factory_Tuner,Luxury,Performance",
"Hatchback,Hybrid",
"Crossover,Hybrid",
"Hatchback,Luxury,Hybrid",
"Flex_Fuel,Luxury,Performance",
"Crossover,Performance",
"Luxury,Hybrid",
"Crossover,Flex_Fuel,Luxury,Performance",
"Crossover,Flex_Fuel,Luxury",
"Crossover,Flex_Fuel,Performance",
"Hatchback,Factory_Tuner,High-Performance",
"Hatchback,Flex_Fuel",
"Factory_Tuner,Luxury",
"Crossover,Factory_Tuner,Luxury,High-Performance",
"Crossover,Factory_Tuner,Luxury,Performance",
"Crossover,Hatchback,Factory_Tuner,Performance",
"Crossover,Hatchback,Performance",
"Flex_Fuel,Hybrid",
"Flex_Fuel,Performance,Hybrid",
"Crossover,Exotic,Luxury,High-Performance",
"Crossover,Exotic,Luxury,Performance",
"Exotic,Performance",
"Exotic,Luxury,High-Performance,Hybrid",
"Crossover,Luxury,Hybrid",
"Flex_Fuel,Factory_Tuner,Luxury,High-Performance",
"Performance,Hybrid",
"Crossover,Factory_Tuner,Performance",
"Crossover,Diesel",
"Flex_Fuel,Diesel",
"Crossover,Hatchback,Luxury"
    
]

values = [
38,
67,
64,
63,
69,
41,
48,
0,
50,
59,
57,
65,
24,
60,
54,
61,
36,
30,
25,
40,
31,
32,
34,
39,
45,
16,
53,
11,
62,
68,
21,
20,
26,
46,
7,
23,
51,
17,
18,
28,
29,
27,
56,
15,
58,
47,
22,
66,
9,
8,
10,
52,
55,
37,
4,
5,
12,
14,
44,
49,
2,
3,
35,
33,
19,
43,
70,
6,
1,
42,
13
]

mar_cat = dict(zip(keys, values))
#array([8, 9, 7, 4, 0, 1, 2, 6, 3, 5])
fuelDic= {
    'premium_unleaded_(required)':8,
    'regular_unleaded':9,
    'premium_unleaded_(recommended)':7,
    'flex-fuel_(unleaded/E85)':4,
    'diesel':0,
    'electric':1,
    'flex-fuel_(premium_unleaded_recommended/E85)':2,
    'natural_gas':6,
    'flex-fuel_(premium_unleaded_required/E85)':3,
    'flex-fuel_(unleaded/natural_gas)':5
}

makeKeys = [
"BMW",
"Audi",
"FIAT",
"Mercedes-Benz",
"Chrysler",
"Nissan",
"Volvo",
"Mazda",
"Mitsubishi",
"Ferrari",
"Alfa Romeo",
"Toyota",
"McLaren",
"Maybach",
"Pontiac",
"Porsche",
"Saab",
"GMC",
"Hyundai",
"Plymouth",
"Honda",
"Oldsmobile",
"Suzuki",
"Ford",
"Cadillac",
"Kia",
"Bentley",
"Chevrolet",
"Dodge",
"Lamborghini",
"Lincoln",
"Subaru",
"Volkswagen",
"Spyker",
"Buick",
"Acura",
"Rolls-Royce",
"Maserati",
"Lexus",
"Aston Martin",
"Land Rover",
"Lotus",
"Infiniti",
"Scion",
"Genesis",
"HUMMER",
"Tesla",
"Bugatti"
]
makeValues = [
4,
3,
12,
31,
10,
33,
47,
29,
32,
13,
1,
45,
30,
28,
36,
37,
39,
15,
19,
35,
18,
34,
43,
14,
8,
21,
5,
9,
11,
22,
25,
42,
46,
41,
7,
0,
38,
27,
24,
2,
23,
26,
20,
40,
16,
17,
44,
6
 ]
makeDic = dict(zip(makeKeys, makeValues))

modelKeys = ['1_Series_M', '1_Series', '100', '124_Spider', '190-Class',
       '2_Series', '200', '200SX', '240SX', '240', '2',
       '3_Series_Gran_Turismo', '3_Series', '300-Class', '3000GT', '300',
       '300M', '300ZX', '323', '350-Class', '350Z', '360', '370Z', '3',
       '4_Series_Gran_Coupe', '4_Series', '400-Class', '420-Class',
       '456M', '458_Italia', '4C', '4Runner', '5_Series_Gran_Turismo',
       '5_Series', '500-Class', '500e', '500', '500L', '500X', '550',
       '560-Class', '570S', '575M', '57', '599', '5',
       '6_Series_Gran_Coupe', '6_Series', '600-Class', '6000',
       '612_Scaglietti', '626', '62', '650S_Coupe', '650S_Spider', '6',
       '7_Series', '718_Cayman', '740', '760', '780', '8_Series', '80',
       '850', '86', '9-2X', '9-3_Griffin', '9-3', '9-4X', '9-5', '9-7X',
       '9000', '900', '90', '911', '928', '929', '940', '944', '960',
       '968', 'A3', 'A4_allroad', 'A4', 'A5', 'A6', 'A7', 'A8',
       'Acadia_Limited', 'Acadia', 'Accent', 'Acclaim',
       'Accord_Crosstour', 'Accord_Hybrid', 'Accord_Plug-In_Hybrid',
       'Accord', 'Achieva', 'ActiveHybrid_5', 'ActiveHybrid_7',
       'ActiveHybrid_X6', 'Aerio', 'Aerostar', 'Alero', 'Allante',
       'allroad_quattro', 'allroad', 'ALPINA_B6_Gran_Coupe', 'ALPINA_B7',
       'Alpina', 'Altima_Hybrid', 'Altima', 'Amanti', 'AMG_GT', 'Armada',
       'Arnage', 'Aspen', 'Aspire', 'Astro_Cargo', 'Astro', 'ATS_Coupe',
       'ATS-V', 'ATS', 'Aurora', 'Avalanche', 'Avalon_Hybrid', 'Avalon',
       'Avenger', 'Aventador', 'Aveo', 'Aviator', 'Axxess', 'Azera',
       'Aztek', 'Azure_T', 'Azure', 'B-Class_Electric_Drive',
       'B-Series_Pickup', 'B-Series_Truck', 'B-Series', 'B9_Tribeca',
       'Baja', 'Beetle_Convertible', 'Beetle', 'Beretta',
       'Black_Diamond_Avalanche', 'Blackwood', 'Blazer', 'Bolt_EV',
       'Bonneville', 'Borrego', 'Boxster', 'Bravada', 'Breeze',
       'Bronco_II', 'Bronco', 'Brooklands', 'Brougham', 'BRZ', 'C-Class',
       'C-Max_Hybrid', 'C30', 'C36_AMG', 'C43_AMG', 'C70', 'C8',
       'Cabriolet', 'Cabrio', 'Cadenza', 'Caliber', 'California_T',
       'California', 'Camaro', 'Camry_Hybrid', 'Camry_Solara', 'Camry',
       'Canyon', 'Caprice', 'Captiva_Sport', 'Caravan', 'Carrera_GT',
       'Cascada', 'Catera', 'Cavalier', 'Cayenne', 'Cayman_S', 'Cayman',
       'CC', 'Celebrity', 'Celica', 'Century', 'Challenger', 'Charger',
       'Chevy_Van', 'Ciera', 'Cirrus', 'City_Express', 'Civic_CRX',
       'Civic_del_Sol', 'Civic', 'C/K_1500_Series', 'C/K_2500_Series',
       'CL-Class', 'CLA-Class', 'CL', 'Classic', 'CLK-Class', 'CLS-Class',
       'Cobalt', 'Colorado', 'Colt', 'Concorde',
       'Continental_Flying_Spur_Speed', 'Continental_Flying_Spur',
       'Continental_GT_Speed_Convertible', 'Continental_GT_Speed',
       'Continental_GT3-R', 'Continental_GT', 'Continental_GTC_Speed',
       'Continental_GTC', 'Continental_Supersports_Convertible',
       'Continental_Supersports', 'Continental', 'Contour_SVT', 'Contour',
       'Corniche', 'Corolla_iM', 'Corolla', 'Corrado', 'Corsica',
       'Corvette_Stingray', 'Corvette', 'Coupe', 'CR-V', 'CR-Z',
       'Cressida', 'Crossfire', 'Crosstour', 'Crosstrek',
       'Crown_Victoria', 'Cruze_Limited', 'Cruze', 'CT_200h', 'CT6',
       'CTS_Coupe', 'CTS-V_Coupe', 'CTS-V_Wagon', 'CTS-V', 'CTS_Wagon',
       'CTS', 'Cube', 'Custom_Cruiser', 'Cutlass_Calais', 'Cutlass_Ciera',
       'Cutlass_Supreme', 'Cutlass', 'CX-3', 'CX-5', 'CX-7', 'CX-9',
       'Dakota', 'Dart', 'Dawn', 'Daytona', 'DB7', 'DB9_GT', 'DB9', 'DBS',
       'Defender', 'DeVille', 'Diablo', 'Diamante', 'Discovery_Series_II',
       'Discovery_Sport', 'Discovery', 'DTS', 'Durango', 'Dynasty',
       'E-150', 'E-250', 'E-Class', 'e-Golf', 'E-Series_Van',
       'E-Series_Wagon', 'E55_AMG', 'ECHO', 'Eclipse_Spyder', 'Eclipse',
       'Edge', 'Eighty-Eight_Royale', 'Eighty-Eight', 'Elantra_Coupe',
       'Elantra_GT', 'Elantra_Touring', 'Elantra', 'Eldorado', 'Electra',
       'Element', 'Elise', 'Enclave', 'Encore', 'Endeavor', 'Entourage',
       'Envision', 'Envoy_XL', 'Envoy_XUV', 'Envoy', 'Enzo', 'Eos',
       'Equator', 'Equinox', 'Equus', 'ES_250', 'ES_300h', 'ES_300',
       'ES_330', 'ES_350', 'Escalade_ESV', 'Escalade_EXT',
       'Escalade_Hybrid', 'Escalade', 'Escape_Hybrid', 'Escape', 'Escort',
       'Esprit', 'Estate_Wagon', 'Esteem', 'EuroVan', 'Evora_400',
       'Evora', 'EX35', 'Excel', 'Exige', 'EX', 'Expedition',
       'Explorer_Sport_Trac', 'Explorer_Sport', 'Explorer', 'Expo',
       'Express_Cargo', 'Express', 'F-150_Heritage',
       'F-150_SVT_Lightning', 'F-150', 'F-250', 'F12_Berlinetta', 'F430',
       'Festiva', 'FF', 'Fiesta', 'Firebird', 'Fit_EV', 'Fit',
       'Five_Hundred', 'FJ_Cruiser', 'Fleetwood', 'Flex', 'Flying_Spur',
       'Focus_RS', 'Focus_ST', 'Focus', 'Forenza', 'Forester', 'Forte',
       'Fox', 'FR-S', 'Freelander', 'Freestar', 'Freestyle', 'Frontier',
       'Fusion_Hybrid', 'Fusion', 'FX35', 'FX45', 'FX50', 'FX', 'G-Class',
       'G_Convertible', 'G_Coupe', 'G_Sedan', 'G20', 'G35',
       'G37_Convertible', 'G37_Coupe', 'G37_Sedan', 'G37', 'G3', 'G5',
       'G6', 'G80', 'G8', 'Galant', 'Gallardo', 'Genesis_Coupe',
       'Genesis', 'Ghibli', 'Ghost_Series_II', 'Ghost', 'GL-Class',
       'GLA-Class', 'GLC-Class', 'GLE-Class_Coupe', 'GLE-Class', 'GLI',
       'GLK-Class', 'GLS-Class', 'Golf_Alltrack', 'Golf_GTI', 'Golf_R',
       'Golf_SportWagen', 'Golf', 'Grand_Am', 'Grand_Caravan',
       'Grand_Prix', 'Grand_Vitara', 'Grand_Voyager', 'GranSport',
       'GranTurismo_Convertible', 'GranTurismo', 'GS_200t', 'GS_300',
       'GS_350', 'GS_400', 'GS_430', 'GS_450h', 'GS_460', 'GS_F', 'GT-R',
       'GT', 'GTI', 'GTO', 'GX_460', 'GX_470', 'H3', 'H3T', 'HHR',
       'Highlander_Hybrid', 'Highlander', 'Horizon', 'HR-V', 'HS_250h',
       'Huracan', 'i-MiEV', 'I30', 'I35', 'i3', 'iA', 'ILX_Hybrid', 'ILX',
       'Impala_Limited', 'Impala', 'Imperial', 'Impreza_WRX', 'Impreza',
       'iM', 'Insight', 'Integra', 'Intrepid', 'Intrigue', 'iQ',
       'IS_200t', 'IS_250_C', 'IS_250', 'IS_300', 'IS_350_C', 'IS_350',
       'IS_F', 'J30', 'Jetta_GLI', 'Jetta_Hybrid', 'Jetta_SportWagen',
       'Jetta', 'Jimmy', 'Journey', 'Juke', 'Justy', 'JX', 'K900',
       'Kizashi', 'LaCrosse', 'Lancer_Evolution', 'Lancer_Sportback',
       'Lancer', 'Land_Cruiser', 'Landaulet', 'Laser', 'Le_Baron',
       'Le_Mans', 'Leaf', 'Legacy', 'Legend', 'LeSabre', 'Levante', 'LFA',
       'LHS', 'Loyale', 'LR2', 'LR3', 'LR4', 'LS_400', 'LS_430', 'LS_460',
       'LS_600h_L', 'LS', 'LSS', 'LTD_Crown_Victoria', 'Lucerne',
       'Lumina_Minivan', 'Lumina', 'LX_450', 'LX_470', 'LX_570',
       'M-Class', 'M2', 'M30', 'M35', 'M37', 'M3', 'M4_GTS', 'M45', 'M4',
       'M56', 'M5', 'M6_Gran_Coupe', 'M6', 'Macan', 'Magnum',
       'Malibu_Classic', 'Malibu_Hybrid', 'Malibu_Limited', 'Malibu_Maxx',
       'Malibu', 'Mark_LT', 'Mark_VIII', 'Mark_VII', 'Matrix', 'Maxima',
       'Maybach', 'Mazdaspeed_3', 'Mazdaspeed_6', 'Mazdaspeed_MX-5_Miata',
       'Mazdaspeed_Protege', 'M', 'MDX', 'Metris', 'Metro',
       'Mighty_Max_Pickup', 'Millenia', 'Mirage_G4', 'Mirage', 'MKC',
       'MKS', 'MKT', 'MKX', 'MKZ_Hybrid', 'MKZ', 'ML55_AMG', 'Model_S',
       'Monaco', 'Montana_SV6', 'Montana', 'Monte_Carlo', 'Montero_Sport',
       'Montero', 'MP4-12C', 'MPV', 'MR2_Spyder', 'MR2', 'Mulsanne',
       'Murano_CrossCabriolet', 'Murano', 'Murcielago',
       'Mustang_SVT_Cobra', 'Mustang', 'MX-3', 'MX-5_Miata', 'MX-6',
       'Navajo', 'Navigator', 'Neon', 'New_Beetle', 'New_Yorker',
       'Ninety-Eight', 'Nitro', 'NSX', 'NV200', 'NX_200t', 'NX_300h',
       'NX', 'Odyssey', 'Omni', 'Optima_Hybrid', 'Optima', 'Outback',
       'Outlander_Sport', 'Outlander', 'Pacifica', 'Panamera',
       'Park_Avenue', 'Park_Ward', 'Paseo', 'Passat', 'Passport',
       'Pathfinder', 'Phaeton', 'Phantom_Coupe', 'Phantom_Drophead_Coupe',
       'Phantom', 'Pickup', 'Pilot', 'Precis', 'Prelude', 'Previa',
       'Prius_c', 'Prius_Prime', 'Prius_v', 'Prius', 'Prizm', 'Probe',
       'Protege5', 'Protege', 'Prowler', 'PT_Cruiser', 'Pulsar', 'Q3',
       'Q40', 'Q45', 'Q50', 'Q5', 'Q60_Convertible', 'Q60_Coupe', 'Q70',
       'Q7', 'Quattroporte', 'Quest', 'QX4', 'QX50', 'QX56', 'QX60',
       'QX70', 'QX80', 'QX', 'R-Class', 'R32', 'R8', 'Rabbit', 'Raider',
       'Rainier', 'Rally_Wagon', 'RAM_150', 'RAM_250', 'Ram_50_Pickup',
       'Ram_Cargo', 'Ram_Pickup_1500', 'Ram_Van', 'Ram_Wagon',
       'Ramcharger', 'Range_Rover_Evoque', 'Range_Rover_Sport',
       'Range_Rover', 'Ranger', 'Rapide_S', 'Rapide', 'RAV4_EV',
       'RAV4_Hybrid', 'RAV4', 'RC_200t', 'RC_300', 'RC_350', 'RC_F',
       'RDX', 'Reatta', 'Regal', 'Regency', 'Rendezvous', 'Reno',
       'Reventon', 'Ridgeline', 'Rio', 'Riviera', 'RL', 'RLX',
       'Roadmaster', 'Rogue_Select', 'Rogue', 'Rondo', 'Routan', 'RS_4',
       'RS_5', 'RS_6', 'RS_7', 'RSX', 'RX_300', 'RX_330', 'RX_350',
       'RX_400h', 'RX_450h', 'RX-7', 'RX-8', 'S-10_Blazer', 'S-10',
       'S-15_Jimmy', 'S-15', 'S-Class', 'S2000', 'S3', 'S40', 'S4', 'S5',
       'S60_Cross_Country', 'S60', 'S6', 'S70', 'S7', 'S80', 'S8', 'S90',
       'Safari_Cargo', 'Safari', 'Samurai', 'Santa_Fe_Sport', 'Santa_Fe',
       'Savana_Cargo', 'Savana', 'SC_300', 'SC_400', 'SC_430', 'Scoupe',
       'Sebring', 'Sedona', 'Sentra', 'Sephia', 'Sequoia', 'Seville',
       'Shadow', 'Shelby_GT350', 'Shelby_GT500', 'Sidekick', 'Sienna',
       'Sierra_1500_Classic', 'Sierra_1500_Hybrid', 'Sierra_1500',
       'Sierra_1500HD', 'Sierra_C3', 'Sierra_Classic_1500', 'Sigma',
       'Silhouette', 'Silver_Seraph', 'Silverado_1500_Classic',
       'Silverado_1500_Hybrid', 'Silverado_1500', 'Sixty_Special',
       'Skylark', 'SL-Class', 'SLC-Class', 'SLK-Class', 'SLR_McLaren',
       'SLS_AMG_GT_Final_Edition', 'SLS_AMG_GT', 'SLS_AMG', 'SLX',
       'Solstice', 'Sonata_Hybrid', 'Sonata', 'Sonic', 'Sonoma',
       'Sorento', 'Soul_EV', 'Soul', 'Spark_EV', 'Spark', 'Spectra',
       'Spirit', 'Sportage', 'Sportvan', 'Spyder', 'SQ5', 'SRT_Viper',
       'SRX', 'SS', 'SSR', 'Stanza', 'Stealth', 'Stratus', 'STS-V', 'STS',
       'Suburban', 'Sunbird', 'Sundance', 'Sunfire', 'Superamerica',
       'Supersports_Convertible_ISR', 'Supra', 'SVX', 'Swift', 'SX4',
       'Syclone', 'T100', 'Tacoma', 'Tahoe_Hybrid', 'Tahoe_Limited/Z71',
       'Tahoe', 'Taurus_X', 'Taurus', 'TC', 'tC', 'Tempo', 'Tercel',
       'Terrain', 'Terraza', 'Thunderbird', 'Tiburon', 'Tiguan', 'Titan',
       'TL', 'TLX', 'Toronado', 'Torrent', 'Touareg_2', 'Touareg',
       'Town_and_Country', 'Town_Car', 'Tracker', 'TrailBlazer_EXT',
       'TrailBlazer', 'Trans_Sport', 'Transit_Connect', 'Transit_Wagon',
       'Traverse', 'Trax', 'Tribeca', 'Tribute_Hybrid', 'Tribute',
       'Truck', 'TSX_Sport_Wagon', 'TSX', 'TT_RS', 'TT', 'TTS', 'Tucson',
       'Tundra', 'Typhoon', 'Uplander', 'V12_Vanquish', 'V12_Vantage_S',
       'V12_Vantage', 'V40', 'V50', 'V60_Cross_Country', 'V60', 'V70',
       'V8_Vantage', 'V8', 'V90', 'Vanagon', 'Vandura', 'Van', 'Vanquish',
       'Vanwagon', 'Veloster', 'Venture', 'Venza', 'Veracruz', 'Verano',
       'Verona', 'Versa_Note', 'Versa', 'Veyron_16.4', 'Vibe', 'Vigor',
       'Viper', 'Virage', 'Vitara', 'Voyager', 'Windstar_Cargo',
       'Windstar', 'Wraith', 'WRX', 'X-90', 'X1', 'X3', 'X4', 'X5_M',
       'X5', 'X6_M', 'X6', 'xA', 'xB', 'XC60', 'XC70', 'XC90', 'XC', 'xD',
       'XG300', 'XG350', 'XL-7', 'XL7', 'XLR-V', 'XLR', 'XT5', 'Xterra',
       'XTS', 'XT', 'XV_Crosstrek', 'Yaris_iA', 'Yaris', 'Yukon_Denali',
       'Yukon_Hybrid', 'Yukon_XL', 'Yukon', 'Z3', 'Z4_M', 'Z4', 'Z8',
       'ZDX', 'Zephyr']
modelValues = [  1,   0,   2,   3,   4,   6,   7,   8,  10,   9,   5,  13,  12,
        15,  16,  14,  17,  18,  19,  20,  21,  22,  23,  11,  25,  24,
        26,  27,  28,  29,  30,  31,  34,  33,  36,  39,  35,  37,  38,
        40,  41,  43,  44,  42,  45,  32,  48,  47,  49,  50,  51,  53,
        52,  54,  55,  46,  56,  57,  58,  59,  60,  61,  62,  63,  64,
        65,  67,  66,  68,  69,  70,  73,  72,  71,  74,  75,  76,  77,
        78,  79,  80,  81,  83,  82,  84,  85,  86,  87,  95,  94,  96,
        97,  99, 100, 101,  98, 102, 103, 104, 105, 106, 107, 108, 109,
       904, 903,  88,  89, 110, 112, 111, 113,  90, 114, 115, 116, 117,
       119, 118,  92,  93,  91, 120, 121, 123, 122, 124, 125, 126, 127,
       128, 129, 130, 132, 131, 133, 135, 136, 134, 137, 139, 141, 140,
       142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 153, 152, 154,
       155, 138, 156, 157, 160, 161, 162, 163, 164, 186, 185, 187, 188,
       190, 189, 191, 193, 194, 192, 195, 196, 197, 198, 199, 200, 201,
       202, 203, 205, 204, 165, 206, 207, 208, 209, 210, 211, 212, 213,
       214, 216, 217, 215, 158, 159, 167, 168, 166, 218, 169, 170, 219,
       220, 221, 222, 225, 224, 228, 227, 229, 226, 231, 230, 233, 232,
       223, 235, 234, 236, 238, 237, 239, 240, 242, 241, 243, 171, 172,
       244, 245, 246, 247, 248, 250, 249, 173, 174, 176, 179, 180, 178,
       177, 175, 251, 252, 254, 255, 256, 253, 181, 182, 183, 184, 262,
       263, 264, 265, 257, 259, 258, 260, 267, 266, 268, 269, 271, 272,
       270, 261, 273, 274, 275, 276, 277, 905, 278, 279, 280, 281, 290,
       289, 291, 293, 292, 295, 296, 297, 294, 298, 299, 300, 301, 302,
       303, 304, 305, 306, 308, 309, 307, 310, 311, 312, 313, 314, 282,
       284, 283, 285, 286, 316, 317, 318, 315, 320, 319, 321, 322, 323,
       324, 325, 327, 326, 288, 328, 329, 287, 330, 333, 332, 331, 334,
       336, 335, 338, 339, 337, 340, 341, 342, 350, 343, 351, 352, 354,
       353, 355, 344, 356, 357, 358, 360, 361, 359, 362, 363, 364, 365,
       345, 366, 367, 368, 369, 371, 370, 347, 348, 349, 346, 375, 372,
       373, 374, 376, 378, 380, 381, 382, 379, 377, 383, 384, 386, 385,
       409, 410, 412, 411, 413, 415, 414, 387, 388, 389, 391, 390, 392,
       393, 394, 417, 418, 419, 420, 416, 424, 425, 426, 427, 428, 421,
       423, 422, 395, 396, 397, 398, 399, 400, 401, 402, 404, 403, 405,
       406, 407, 408, 429, 430, 431, 435, 434, 436, 432, 433, 437, 906,
       438, 439, 907, 908, 441, 440, 450, 449, 451, 453, 452, 909, 454,
       455, 456, 457, 910, 442, 444, 443, 445, 447, 446, 448, 458, 461,
       462, 463, 460, 464, 465, 466, 467, 459, 468, 469, 485, 487, 488,
       486, 489, 490, 491, 492, 493, 495, 496, 497, 494, 498, 470, 471,
       499, 472, 473, 474, 476, 477, 478, 479, 475, 480, 481, 500, 502,
       501, 482, 483, 484, 504, 505, 507, 508, 509, 506, 511, 512, 510,
       514, 513, 516, 515, 532, 533, 535, 536, 537, 538, 534, 539, 541,
       540, 542, 543, 544, 545, 546, 547, 548, 503, 517, 549, 550, 551,
       552, 554, 553, 518, 519, 520, 521, 523, 522, 524, 555, 556, 558,
       557, 559, 561, 560, 525, 526, 528, 527, 562, 564, 563, 565, 567,
       566, 529, 530, 531, 573, 574, 575, 576, 577, 578, 579, 568, 569,
       571, 572, 570, 580, 581, 583, 582, 584, 586, 585, 588, 589, 590,
       591, 592, 593, 594, 595, 596, 598, 599, 597, 600, 601, 602, 603,
       604, 607, 606, 608, 605, 609, 610, 612, 611, 613, 587, 614, 615,
       616, 617, 619, 618, 620, 621, 623, 622, 631, 632, 625, 626, 627,
       628, 629, 630, 624, 633, 634, 635, 660, 661, 662, 663, 636, 637,
       664, 665, 666, 667, 668, 669, 671, 672, 670, 673, 675, 674, 639,
       640, 638, 641, 642, 643, 644, 645, 676, 677, 678, 679, 680, 681,
       682, 683, 684, 646, 647, 685, 687, 686, 688, 689, 648, 649, 650,
       651, 652, 653, 654, 655, 656, 657, 658, 659, 691, 690, 693, 692,
       694, 695, 696, 698, 697, 699, 702, 701, 700, 704, 703, 706, 705,
       707, 729, 728, 730, 732, 731, 734, 733, 708, 709, 710, 735, 736,
       737, 738, 739, 740, 741, 742, 743, 744, 745, 746, 748, 749, 747,
       750, 751, 752, 753, 754, 755, 757, 758, 756, 759, 760, 711, 712,
       713, 714, 717, 716, 715, 718, 761, 763, 762, 764, 765, 766, 768,
       767, 770, 769, 771, 772, 773, 774, 775, 719, 720, 721, 722, 723,
       776, 777, 778, 725, 724, 779, 780, 781, 782, 783, 784, 785, 726,
       786, 727, 787, 788, 797, 799, 800, 798, 802, 801, 789, 911, 803,
       804, 805, 806, 807, 808, 809, 810, 790, 791, 811, 812, 814, 813,
       816, 815, 817, 819, 818, 820, 821, 822, 823, 824, 825, 827, 826,
       828, 793, 792, 795, 794, 796, 829, 830, 831, 832, 833, 835, 834,
       836, 837, 839, 838, 840, 842, 841, 843, 845, 846, 844, 847, 848,
       849, 850, 851, 852, 853, 854, 856, 855, 857, 858, 859, 860, 861,
       862, 863, 866, 865, 867, 864, 868, 869, 870, 871, 873, 872, 875,
       874, 912, 913, 877, 878, 879, 876, 914, 880, 881, 882, 883, 885,
       884, 887, 890, 888, 886, 889, 892, 891, 894, 895, 896, 893, 897,
       899, 898, 900, 901, 902]    
modelDic = dict(zip(modelKeys, modelValues))


def setVehicleSize(value):
    if value == "Compact" :
        return 0
    elif value == "Large" :
        return 1
    else:
        return 2

def setDrivenWheels(value):
    if value == "rear_wheel_drive" :
        return 3
    elif value == "front_wheel_drive" :
        return 2
    elif value == "all_wheel_drive" :
        return 0
    else:
        return 1

def setTransmissionType(value):
    if value == "MANUAL" :
        return 3
    elif value == "AUTOMATIC" :
        return 1
    elif value == "AUTOMATED_MANUAL" :
        return 0
    else:
        return 3

def setVehicleStyle(value):
    if value == "Coupe" :
        return 8
    elif value == "Convertible" :
        return 6
    elif value == "Sedan" :
        return 14
    elif value == "Wagon" :
        return 15
    elif value == "4dr_Hatchback" :
        return 2
    elif value == "2dr_Hatchback" :
        return 0
    elif value == "4dr_SUV" :
        return 3
    elif value == "Passenger_Minivan" :
        return 11
    elif value == "Cargo_Minivan" :
        return 4
    elif value == "Crew_Cab_Pickup" :
        return 9
    elif value == "Regular_Cab_Pickup" :
        return 13
    elif value == "Extended_Cab_Pickup" :
        return 10
    elif value == "2dr_SUV" :
        return 1
    elif value == "Cargo_Van" :
        return 5
    elif value == "Convertible_SUV" :
        return 7
    else:
        return 12




car=pd.read_csv("carData.csv")
# car_model=pd.read_csv("fmodel.csv")
# car_model_s=pd.read_csv("fmodelSpace.csv")


@app.route('/')
def index():
    make=car["Make"].str.replace(' ','_').unique()
    model=car["Model"].str.replace(' ','_').unique()
    year=sorted(car['Year'].unique(),reverse=True)
    engineFuelType=car["Engine Fuel Type"].str.replace(' ','_').unique()
    engineHP=sorted(car['Engine HP'].unique(),reverse=True)
    engineCylinders=sorted(car['Engine Cylinders'].unique())
    transmissionType=car['Transmission Type'].unique()
    driven_Wheels=car["Driven_Wheels"].str.replace(' ','_').unique()        
    numberofDoors=sorted(car['Number of Doors'].unique())
    vehicleSize=car['Vehicle Size'].unique()
    vehicleStyle=car["Vehicle Style"].str.replace(' ','_').unique()
    highwayMPG=sorted(car['highway MPG'].unique(),reverse=True)
    citympg=sorted(car['city mpg'].unique(),reverse=True)
    popularity=sorted(car['Popularity'].unique(),reverse=True)
    marketCategory=car['Market Category'].str.replace(' ','_').unique()
 
    return render_template('index.html' ,make=make,model=model,year=year,engineFuelType=engineFuelType,engineHP=engineHP,engineCylinders=engineCylinders,transmissionType=transmissionType,driven_Wheels=driven_Wheels,numberofDoors=numberofDoors,vehicleSize=vehicleSize,vehicleStyle=vehicleStyle,highwayMPG=highwayMPG,citympg=citympg,popularity=popularity,marketCategory=marketCategory)


@app.route('/predict',methods=['POST'])
def predict():
    makeReq=request.form.get('make')
    modelReq=request.form.get('model')
    yearReq=int(request.form.get('year'))
    engineFuelTypeReq=request.form.get('engineFuelType')
    engineHPReq=float(request.form.get('engineHP'))
    engineCylindersReq=float(request.form.get('engineCylinders'))
    transmissionTypeReq=setTransmissionType(request.form.get('transmissionType'))
    driven_WheelsReq=setDrivenWheels(request.form.get('driven_Wheels'))
    numberofDoorsReq=float(request.form.get('numberofDoors'))
    marketCategoryReq=request.form.get('marketCategory')
    vehicleSizeReq=setVehicleSize(request.form.get('vehicleSize'))
    vehicleStyleReq=setVehicleStyle(request.form.get('vehicleStyle'))
    highwayMPGReq=int(request.form.get('highwayMPG'))
    citympgReq=int(request.form.get('citympg'))
    popularityeReq=int(request.form.get('popularity'))

    new_mc = mar_cat[marketCategoryReq]
    new_eft=fuelDic[engineFuelTypeReq]
    new_make=makeDic[makeReq]
    new_model=modelDic[modelReq]
    print(new_make,new_model,yearReq,new_eft,engineHPReq,engineCylindersReq,transmissionTypeReq,driven_WheelsReq,numberofDoorsReq,new_mc,vehicleSizeReq,vehicleStyleReq,highwayMPGReq,citympgReq,popularityeReq)


    # resultValues=np.array([[4,1,2016,8,230,6,3,3,2,63,0,6,28,18,3916]])
    model = pickle.load(open('LinearRegressionModel.pkl','rb'))
    # predictionValue =model.predict(resultValues)
    
    prediction=model.predict(pd.DataFrame([[new_make,new_model,yearReq,new_eft,engineHPReq,engineCylindersReq,transmissionTypeReq,driven_WheelsReq,numberofDoorsReq,new_mc,vehicleSizeReq,vehicleStyleReq,highwayMPGReq,citympgReq,popularityeReq]], columns=['Make','Model','Year','Engine Fuel Type','Engine HP','Engine Cylinders','Transmission Type','Driven_Wheels','Number of Doors','Market Category','Vehicle Size','Vehicle Style','highway MPG','city mpg','Popularity']))
    print(prediction)
    
    #print(car["Driven_Wheels"].str.replace(' ','_'))
    
    return str(np.round(prediction[0],5))
   

if __name__ == "__main__":
    app.run(debug=True) 
