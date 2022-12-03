try:
    from pyrfc import Connection, ABAPApplicationError, ABAPRuntimeError, LogonError, CommunicationError
except ImportError:
    print("You do not have pyrfc installed! You can not use the SAP Connector functionality!")
from environment.settings import SAP_CON_PARAMS

class SapConnector:
    """Singleton SAP connector to connect to the SAP system with PYRFC"""
    __instance = None

    def getInstance(conn_params):
        """A function to return singleton SAP connection"""
        if not (SapConnector.__instance != None):
            SapConnector(conn_params)
        return SapConnector.__instance

    def __init__(self, conn_params):
        """ Virtually private constructor. """
        if SapConnector.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            print("Initialize SAP Connector")
            SapConnector.__instance = self
            try:
                self.conn = Connection(**conn_params)
                print("SAP connection successful")

            # Handle errors
            except (CommunicationError, LogonError, ABAPApplicationError, ABAPRuntimeError) as error:
                print(error)
                raise

    def close_instance(self):
        """A function the destroy the singleton SAP connection"""
        if SapConnector.__instance != None:
            print("Closing SAP connection")
            self.conn.close()
            print("SAP connection closed")
            self = None

    def qry(self, Fields, SQLTable, Where='', MaxRows=50, FromRow=0):
        """A function to query SAP with RFC_READ_TABLE"""

        Fields = Fields[1::1]

        # By default, if you send a blank value for fields, you get all of them
        # Therefore, we add a select all option, to better mimic SQL.
        if Fields[0] == '*':
            Fields = ''
        else:
            Fields = [{'FIELDNAME': x} for x in Fields]  # Notice the format

        # the WHERE part of the query is called "options"
        options = [{'TEXT': x} for x in Where]  # again, notice the format
        print(options)

        # we set a maximum number of rows to return, because it's easy to do and
        # greatly speeds up testing queries.
        rowcount = MaxRows

        # Here is the call to SAP's RFC_READ_TABLE
        tables = self.conn.call("RFC_READ_TABLE", QUERY_TABLE=SQLTable, DELIMITER='|',
                                FIELDS=Fields, OPTIONS=options, ROWCOUNT=MaxRows, ROWSKIPS=FromRow)

        # We split out fields and fields_name to hold the data and the column names
        fields = []
        fields_name = []

        data_fields = tables["DATA"]  # pull the data part of the result set
        # pull the field name part of the result set
        data_names = tables["FIELDS"]

        headers = [x['FIELDNAME'] for x in data_names]  # headers extraction
        long_fields = len(data_fields)  # data extraction
        long_names = len(data_names)  # full headers extraction if you want it

        # now parse the data fields into a list
        for line in range(0, long_fields):
            fields.append(data_fields[line]["WA"].strip())

        # for each line, split the list by the '|' separator
        fields = [x.strip().split('|') for x in fields]

        # return the 2D list and the headers
        return fields, headers

    def get_num_of_rows(self, table):
        """Simple function to get the number of rows of a given table in the SAP system"""
        return self.conn.call("EM_GET_NUMBER_OF_ENTRIES",  IT_TABLES=[table])["IT_TABLES"][0]['TABROWS']

    def get_con_details(self):
        """ Function to get the connection details of a session with the SAP system """
        return self.conn.call("STFC_CONNECTION")['RESPTEXT']

    def check_conn(user, password):
        conn_params = SAP_CON_PARAMS
        conn_params['user'] = user
        conn_params['passwd'] = password
        try:
            conn = Connection(**conn_params)
            print("SAP connection successful")
            return None
            # Handle errors
        except CommunicationError:
            print("Could not connect to server.")
            return "Could not connect to server. Try activating your IP: https://remotelogin.sapucc.in.tum.de/"
        except LogonError:
            print("Could not log in. Wrong credentials?")
            return "Could not log in. Wrong credentials?"
        except (ABAPApplicationError, ABAPRuntimeError):
            print("An error occurred.")
            return "An error occurred."
