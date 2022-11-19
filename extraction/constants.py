# Connection parameters for the SAP NWRFC library.
sap_conn_params = {
    'user': '',
    'passwd': '',
    'ashost': 's06lp1.ucc.in.tum.de',
    'saprouter': '/H/saprouter.hcc.in.tum.de/S/3299',
    'msserv': 'sapdp99',
    'sysid': 'S06',
    'group': 'SPACE',
    'client': '323',
    'lang': 'EN',
    'trace': '0'
}

# Path of the local database.
sqlite_path = 'data/internal_sqlite.db'

# Number of rows that are downloaded in each call by the NWRFC library.
ROWS_AT_A_TIME = 1000

# The following tables with given fields get downloaded from the SAP system into the local database.
# Number shows how many of the following fields are in the primary key.
tables = {
    'EBAN': [3, 'MANDT', 'BANFN', 'BNFPO', 'BSART', 'EKGRP', 'ERDAT', 'BADAT', 'LFDAT', 'FRGDT', 'EBELN', 'EBELP', 'BEDAT', 'PACKNO'],
    'BSEG': [5, 'MANDT', 'BUKRS', 'BELNR', 'GJAHR', 'BUZEI', 'BUZID', 'AUGDT', 'AUGCP', 'AUGBL', 'BSCHL', 'KOART', 'SHKZG', 'VALUT', 'ZUONR', 'SAKNR', 'HKONT', 'LIFNR', 'ZFBDT', 'MATNR', 'AWTYP', 'H_BUDAT', 'H_BLDAT', 'NETDT', 'SK1DT', 'SK2DT'],
    'BKPF': [4, 'MANDT', 'BUKRS', 'BELNR', 'GJAHR', 'BLART', 'BLDAT', 'BUDAT', 'MONAT', 'CPUDT', 'CPUTM', 'WWERT', 'TCODE', 'BVORG', 'XBLNR', 'DOCCAT'],
    'EKKO': [2, 'MANDT', 'EBELN', 'BUKRS', 'STATU', 'AEDAT', 'ERNAM', 'LPONR', 'LIFNR', 'BEDAT'],
    'RBKP': [3, 'MANDT', 'BELNR', 'GJAHR', 'BLDAT', 'BUDAT', 'USNAM', 'TCODE', 'CPUDT', 'CPUTM', 'XBLNR', 'BUKRS', 'LIFNR', 'RMWWR', 'ZFBDT', 'SGTXT', 'WWERT', 'NODE_KEY', 'ROOT_KEY'],
    'RSEG': [4, 'MANDT', 'BELNR', 'GJAHR', 'BUZEI', 'EBELN', 'EBELP', 'MATNR', 'BWKEY', 'WERKS', 'MWSKZ', 'TXJCD', 'BKLAS', 'SPGRT', 'MATBF'],
    'EKBE': [8, 'MANDT', 'EBELN', 'EBELP', 'ZEKKN', 'VGABE', 'GJAHR', 'BELNR', 'BUZEI', 'BEWTP', 'BUDAT', 'MENGE', 'BPMNG', 'DMBTR', 'WRBTR', 'AREWR', 'ELIKZ', 'XBLNR', 'CPUDT', 'CPUTM', 'REEWR', 'REFWR', 'MATNR', 'WERKS', 'AREWW', 'BAMNG', 'BLDAT', 'ERNAM'],
    'EKPO': [3, 'MANDT', 'EBELN', 'EBELP', 'AEDAT', 'TXZ01', 'MATNR', 'EMATN', 'BUKRS', 'WERKS', 'LGORT', 'MATKL', 'INFNR', 'MENGE', 'NETPR', 'ELIKZ', 'PRDAT', 'XOBLR', 'BERID'],
    'BSAK': [26, 'MANDT', 'BUKRS', 'LIFNR', 'AUGDT', 'AUGBL', 'GJAHR', 'BELNR', 'BUZEI', 'BUDAT', 'BLDAT', 'CPUDT', 'WAERS', 'BLART', 'MONAT', 'BSCHL', 'ZUMSK', 'SHKZG', 'MWSKZ', 'DMBTR', 'WRBTR', 'SGTXT', 'ZFBDT', 'ZTERM', 'ZLSPR', 'XZAHL', 'AUGGJ'],
    'CDHDR': [4, 'MANDANT', 'OBJECTCLAS', 'OBJECTID', 'CHANGENR', 'USERNAME', 'UDATE', 'UTIME', 'TCODE', 'CHANGE_IND'],
    'CDPOS': [8, 'MANDANT', 'OBJECTCLAS', 'OBJECTID', 'CHANGENR', 'TABNAME', 'TABKEY', 'FNAME', 'CHNGIND']
}

# tables_ = {
#    'BKPF',
#    'BSAK',
#    'BSEG',
#    'CDHDR',
#    'CDPOS',
#    'EBAN',
#    'EKBE',
#    'EKKO',
#    'EKPO',
#    'MKPF',
#    'MSEG',
#    'RBKP',
#    'VBFA',
#    'DD02T',
#    'DD07T',
#    'TSTCT'
#    'T003T',
#    'TSTCT',
# }
