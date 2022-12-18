## Flask

home_page_location = "/"
dms_page_location = "/dms"
analyse_page_location = "/analyse"

TIMEOUT = 60

## SAP connection parameters

# Path of the local database.
sqlite_path = 'data/internal_sqlite.db'

# Number of rows that are downloaded in each call by the NWRFC library.
ROWS_AT_A_TIME = 3000

# The following tables with given fields get downloaded from the SAP system into the local database.
# Number shows how many of the following fields are in the primary key.
tables = {
    'BSAD': [11, 'MANDT', 'BUKRS', "KUNNR", "UMSKS", "UMSKZ", 'AUGDT', 'AUGBL', "ZUONR", 'GJAHR', 'BELNR', 'BLART', 'VBELN'],
    'VBFA': [0, "ERDAT", "ERZET", "VBELN", "VBELV", "VBTYP_N", "VBTYP_V", "RFMNG", "MEINS", "RFWRT", "WAERS", "MATNR",
             "BWART", "VRKME", "FKTYP", "POSNN", "POSNV"],
    'VBAK': [0, "VBELN", "ERDAT", "ERZET", "KUNNR"],
    'CDHDR': [4, 'MANDANT', 'OBJECTCLAS', 'OBJECTID', 'CHANGENR', 'USERNAME', 'UDATE', 'UTIME', 'TCODE', 'CHANGE_IND'],
    'CDPOS': [8, 'MANDANT', 'OBJECTCLAS', 'OBJECTID', 'CHANGENR', 'TABNAME', 'TABKEY', 'FNAME', 'CHNGIND'],
}

tables2 = {
    #'RBKP':[0, '*'],
    'EBAN': [3, 'MANDT', 'BANFN', 'BNFPO', 'BSART', 'EKGRP', 'ERDAT', 'BADAT', 'LFDAT', 'FRGDT', 'EBELN', 'EBELP',
             'BEDAT', 'PACKNO'],
    'BSEG': [5, 'MANDT', 'BUKRS', 'BELNR', 'GJAHR', 'BUZEI', 'BUZID',"VBELN", 'VBEL2', 'AUGDT', 'AUGCP', 'AUGBL', 'BSCHL', 'KOART',
             'SHKZG', 'VALUT', 'ZUONR', 'SAKNR', 'HKONT', 'LIFNR', 'ZFBDT', 'MATNR', 'AWTYP', 'H_BUDAT', 'H_BLDAT',
             'NETDT', 'SK1DT', 'SK2DT'],

    #'EKKO': [2, 'MANDT', 'EBELN', 'BUKRS', 'STATU', 'AEDAT', 'ERNAM', 'LPONR', 'LIFNR', 'BEDAT'],
    # purchasing document
    'RBKP': [3, 'MANDT', 'BELNR', 'GJAHR', 'BLDAT', 'BUDAT', 'USNAM', 'TCODE', 'CPUDT', 'CPUTM', 'XBLNR', 'BUKRS',
             'LIFNR', 'RMWWR', 'ZFBDT', 'SGTXT', 'WWERT', 'NODE_KEY', 'ROOT_KEY'],
    #'RSEG': [4, 'MANDT', 'BELNR', 'GJAHR', 'BUZEI', 'EBELN', 'EBELP', 'MATNR', 'BWKEY', 'WERKS', 'MWSKZ', 'TXJCD',
     #        'BKLAS', 'SPGRT', 'MATBF'],
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
             'TCODE', 'BVORG', 'XBLNR', 'DOCCAT', 'AWTYP', 'AWKEY'],
    'VBFA': [0, "ERDAT", "ERZET", "VBELN", "VBELV", "VBTYP_N", "VBTYP_V", "RFMNG", "MEINS", "RFWRT", "WAERS", "MATNR",
             "BWART", "VRKME", "FKTYP", "POSNN", "POSNV"],
    'VBRK': [2, 'MANDT', 'VBELN', 'VBTYP', 'BELNR', 'GJAHR'],
    'BSAD': [11, 'MANDT', 'BUKRS', "KUNNR", "UMSKS", "UMSKZ", 'AUGDT', 'AUGBL', "ZUONR", 'GJAHR', 'BELNR', 'BLART', 'VBELN']
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

OBJECTCLAS_DESCRIPTIONS = {
    "LIEFERUNG": "Delivery",
    "VERKBELEG": "Order",
}


VBTYP_DESCRIPTIONS = {
    "A": "Inquiry",
    "B": "Quotation",
    "C": "Order",
    "D": "Item proposal",
    "E": "Scheduling agreement",
    "F": "Scheduling agreement with external service agent",
    "G": "Contract",
    "H": "Returns",
    "I": "Order w/o charge",
    "J": "Delivery",
    "K": "Credit memo request",
    "L": "Debit memo request",
    "M": "Invoice",
    "N": "Invoice cancellation",
    "O": "Credit memo",
    "P": "Debit memo",
    "Q": "WMS transfer order",
    "R": "Goods movement",
    "S": "Credit memo cancellation",
    "T": "Returns delivery for order",
    "U": "Pro forma invoice",
    "V": "Purchase order",
    "W": "Independent reqts plan",
    "X": "Handling unit",
    "0": "Master contract",
    "1": "Sales activities (CAS)",
    "2": "External transaction",
    "3": "Invoice list",
    "4": "Credit memo list",
    "5": "Intercompany invoice",
    "6": "Intercompany credit memo",
    "7": "Delivery/shipping notification",
    "8": "Shipment",
    "a": "Shipment costs",
    "e": "Allocation table",
    "g": "Rough Goods Receipt (only IS-Retail)",
    "h": "Cancel goods issue",
    "i": "Goods receipt",
    "j": "JIT call",
    "r": "TD Shipment (IS-Oil Only)",
    "s": "Loading Confirmation, Reposting (IS-Oil Only)",
    "t": "Gain/Loss (IS-Oil Only)",
    "u": "Placing Back in Stock (IS-Oil Only)",
    "v": "Two-Step Goods Receipt (IS-Oil Only)",
    "w": "Reservation (IS-Oil Only)",
    "x": "Loading Confirmation, Goods Receipt (IS-Oil Only)"
    }