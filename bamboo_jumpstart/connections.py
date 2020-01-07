class ConnectionsFile:
    def __init__(self, etl):
        self.code = ""
        self.etl = etl
        self.sources = self.get_sources()
        self.databases = self.get_databases()

    def add_code(self, code):
        self.code += code

    def get_sources(self):
        sources = []
        for source in self.etl["etl"]["sources"]:
            sources.append(source)

        return sources
    
    def get_databases(self):
        databases = []
        for source in self.etl["etl"]["sources"]:
            sources.append(source)

        return sources

    def get_driver(self, driver):
        drivers = {
            "clickhouse": "bamboo_lib.connectors.drivers.clickhouse.ClickhouseDriver",
            "gcs": "bamboo_lib.connectors.drivers.gcs.GCSDriver",
            "":""
        }

    def run(self):
        code = ""