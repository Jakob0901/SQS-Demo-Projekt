class DBConfig:
    def __init__(self, username, password, hostname, port, database_name):
        self.usr = username
        self.pwd = password
        self.hstnm = hostname
        self.prt = port
        self.db_nm = database_name

    def get_connection_string(self):
        return f"postgresql://{self.usr}:{self.pwd}@{self.hstnm}:{self.prt}/{self.db_nm}"

    def __repr__(self):
        return f"<DBConfig(username={self.usr}, hostname={self.hstnm}, port={self.prt}, database_name={self.db_nm})>"
