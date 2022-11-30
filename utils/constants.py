## Flask

home_page_location = "/"
dms_page_location = "/dms"
analyse_page_location = "/analyse"

TIMEOUT = 60

## SAP connection parameters

# Path of the local database.
sqlite_path = 'data/internal_sqlite.db'

# Number of rows that are downloaded in each call by the NWRFC library.
ROWS_AT_A_TIME = 1000

# The following tables with given fields get downloaded from the SAP system into the local database.
# Number shows how many of the following fields are in the primary key.
tables = {
    'EBAN': [3, 'MANDT', 'BANFN', 'BNFPO', 'BSART', 'EKGRP', 'ERDAT', 'BADAT', 'LFDAT', 'FRGDT', 'EBELN', 'EBELP',
             'BEDAT', 'PACKNO'],
    'BSEG': [5, 'MANDT', 'BUKRS', 'BELNR', 'GJAHR', 'BUZEI', 'BUZID', 'AUGDT', 'AUGCP', 'AUGBL', 'BSCHL', 'KOART',
             'SHKZG', 'VALUT', 'ZUONR', 'SAKNR', 'HKONT', 'LIFNR', 'ZFBDT', 'MATNR', 'AWTYP', 'H_BUDAT', 'H_BLDAT',
             'NETDT', 'SK1DT', 'SK2DT'],

    'EKKO': [2, 'MANDT', 'EBELN', 'BUKRS', 'STATU', 'AEDAT', 'ERNAM', 'LPONR', 'LIFNR', 'BEDAT'],
    # purchasing document
    'RBKP': [3, 'MANDT', 'BELNR', 'GJAHR', 'BLDAT', 'BUDAT', 'USNAM', 'TCODE', 'CPUDT', 'CPUTM', 'XBLNR', 'BUKRS',
             'LIFNR', 'RMWWR', 'ZFBDT', 'SGTXT', 'WWERT', 'NODE_KEY', 'ROOT_KEY'],
    'RSEG': [4, 'MANDT', 'BELNR', 'GJAHR', 'BUZEI', 'EBELN', 'EBELP', 'MATNR', 'BWKEY', 'WERKS', 'MWSKZ', 'TXJCD',
             'BKLAS', 'SPGRT', 'MATBF'],
    'EKBE': [8, 'MANDT', 'EBELN', 'EBELP', 'ZEKKN', 'VGABE', 'GJAHR', 'BELNR', 'BUZEI', 'BEWTP', 'BUDAT', 'MENGE',
             'BPMNG', 'DMBTR', 'WRBTR', 'AREWR', 'ELIKZ', 'XBLNR', 'CPUDT', 'CPUTM', 'REEWR', 'REFWR', 'MATNR', 'WERKS',
             'AREWW', 'BAMNG', 'BLDAT', 'ERNAM'],
    'EKPO': [3, 'MANDT', 'EBELN', 'EBELP', 'AEDAT', 'TXZ01', 'MATNR', 'EMATN', 'BUKRS', 'WERKS', 'LGORT', 'MATKL',
             'INFNR', 'MENGE', 'NETPR', 'ELIKZ', 'PRDAT', 'XOBLR', 'BERID'],
    'BSAK': [26, 'MANDT', 'BUKRS', 'LIFNR', 'AUGDT', 'AUGBL', 'GJAHR', 'BELNR', 'BUZEI', 'BUDAT', 'BLDAT', 'CPUDT',
             'WAERS', 'BLART', 'MONAT', 'BSCHL', 'ZUMSK', 'SHKZG', 'MWSKZ', 'DMBTR', 'WRBTR', 'SGTXT', 'ZFBDT', 'ZTERM',
             'ZLSPR', 'XZAHL', 'AUGGJ'],
    # change tables: 
    'CDHDR': [4, 'MANDANT', 'OBJECTCLAS', 'OBJECTID', 'CHANGENR', 'USERNAME', 'UDATE', 'UTIME', 'TCODE', 'CHANGE_IND'],
    'CDPOS': [8, 'MANDANT', 'OBJECTCLAS', 'OBJECTID', 'CHANGENR', 'TABNAME', 'TABKEY', 'FNAME', 'CHNGIND'],
    # o2c ,
    'VBAK': [0, "VBELN", "ERDAT", "ERZET", "KUNNR"],
    'BKPF': [4, 'MANDT', 'BUKRS', 'BELNR', 'GJAHR', 'BLART', 'BLDAT', 'BUDAT', 'MONAT', 'CPUDT', 'CPUTM', 'WWERT',
             'TCODE', 'BVORG', 'XBLNR', 'DOCCAT'],
    'VBFA': [0, "ERDAT", "ERZET", "VBELN", "VBELV", "VBTYP_N", "VBTYP_V", "RFMNG", "MEINS", "RFWRT", "WAERS", "MATNR",
             "BWART", "VRKME", "FKTYP", "POSNN", "POSNV"],
    # explains the status of objects that are associated with the o2c process / flow table
}

#  transaction table describes the execution of transactions (TCODE)


# tables_ = {
#    'BKPF', #
#    'BSAK', #
#    'BSEG', # payments items -  purchase order items
#    'CDHDR', # change tables
#    'CDPOS',
#    'EBAN', # (purchase order)
#    'EKBE', # information about goods/invoice receipts,  could be seen as a master table, also links the purchase order items with the invoices through the goods/invoice receipts.
#    'EKKO', # master table
#    'EKPO', # purchase order item - corresponding purchase requisition item
#    'MKPF',
#    'MSEG', #
#    'RBKP',
#    'VBFA',
#    'DD02T',
#    'DD07T', #
#    'T003T',
#    'TSTCT', #
# }
