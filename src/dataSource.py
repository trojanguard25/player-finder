import pymysql
import config


class DataSource:
    def __init__(self):
        self.bat_table = ""
        self.pitch_table = ""
        self.year = ""
        self.war = ""
        self._cache = {}
        self._createConnection()

    def _createConnection(self):
        self.conn = pymysql.connect(host=config.Config.dbHost, port=config.Config.dbPort, user=config.Config.dbUser, passwd=config.Config.dbPass, db=config.Config.dbName)

    def _getWar(self, uuid, war_type):
        if uuid in self._cache:
            if war_type in self._cache[uuid]:
                return self._cache[uuid][war_type]
        else:
            self._cache[uuid] = {}

        table = ""
        if war_type == 'Bat':
            table = self.bat_table
        else:
            table = self.pitch_table

        cur = self.conn.cursor()
        sql = 'SELECT c.key_person as id, data.' + self.year + ' as year, data.' + self.war + ' as war '
        sql += ' FROM ' + table + ' data '
        sql += ' LEFT JOIN chadwickbureau c on ' + self._uuidToId()
        sql += ' WHERE c.key_person = \'' + uuid + '\''

        data = {}
        data['Total'] = 0.0
        cur.execute(sql)
        for row in cur:
            #print row
            data[str(row[1])] = float(row[2])
            data['Total'] += float(row[2])

        self._cache[uuid][war_type] = data

        return self._cache[uuid][war_type]

    def getBatWar(self, uuid, years=""):
        return self._getWar(uuid, 'Bat')

    def getPitchWar(self, uuid, years=""):
        return self._getWar(uuid, 'Pitch')

    def getCombinedWar(self, uuid, years=""):
        if uuid in self._cache:
            if 'Combined' in self._cache[uuid]:
                return self._cache[uuid]['Combined']
        else:
            self._cache[uuid] = {}


        combined_war = self.getPitchWar(uuid, years)
        bat_war = self.getBatWar(uuid, years)

        for key in bat_war:
            if key in combined_war:
                combined_war[key] += bat_war[key]
            else:
                combined_war[key] = bat_war[key]

        self._cache[uuid]['Combined'] = combined_war
        return self._cache[uuid]['Combined']

    def _uuidToId(self):
        raise ValueError('no implementation')

    def _getYearsSql(years):
        sql = ''
        first = True

        for year in years.split(','):
            if first:
                first = False
            else:
                sql += ' OR '

            sql += ' ('
            if '-' in year:
                (first, last) = years.split('-')
                sql += self.year + ' >= ' + first + ' AND ' + self.year + ' <= ' + last
            else:
                sql += self.year + ' = ' + year
            sql += ') '
