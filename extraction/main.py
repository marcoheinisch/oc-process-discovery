from sap_con import SapConnector
import constants

if __name__ == "__main__":
    con_params = constants.sap_conn_params
    user_name = '<username>'
    password = '<password>'
    con_params['user'] = user_name
    con_params['passwd'] = password
    print(con_params)
    sap_con = SapConnector.getInstance(constants.sap_conn_params)
    con_details = sap_con.get_con_details()
    print(con_details)

    tables = {
        'EBAN': [3, 'MANDT', 'BANFN', 'BNFPO', 'BSART', 'EKGRP', 'ERDAT', 'BADAT', 'LFDAT', 'FRGDT', 'EBELN', 'EBELP', 'BEDAT', 'PACKNO']
    }

    for table, fields in tables.items():
        results, headers = sap_con.qry(
            fields, table, MaxRows=constants.ROWS_AT_A_TIME)
        print(results)
        print(headers)

    sap_con.close_instance()
