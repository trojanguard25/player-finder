import pymysql
import config

class YearWar:
    def __init__(self, uuid=""):
        self.uuid = uuid
        self.bat_war = 0
        self.pitch_war = 0
        self.year = 0

    def combine(self, war):
        if self.uuid != war.uuid or self.year != war.year:
            raise
        self.pitch_war = self.pitch_war + war.pitch_war
        self.bat_war = self.bat_war + war.bat_war

    def Print(self):
        print "uuid: " + self.uuid
        print "year: " + str(self.year)
        print "bat_war: " + str(self.bat_war)
        print "pitch_war: " + str(self.pitch_war)

class TotalWar:
    def __init__(self, uuid=''):
        self.uuid = uuid
        self.bat_war = 0
        self.pitch_war = 0
        self.total_war = 0
        self.years = []
        self._year_wars = {}

    def addYearWar(self, war, combine=False):
        if self.uuid != war.uuid:
            raise

        if not war.year in self._year_wars:
            self.years.append(war.year)
            self._year_wars[war.year] = war
            self.years.sort()
        else:
            if combine:
                self._year_wars[war.year].combine(war)
            else:
                raise "Duplicate year added"

        self.calcTotals()

    def Print(self):
        print "uuid: " + self.uuid
        print "total_war: " + str(self.total_war)
        print "bat_war: " + str(self.bat_war)
        print "pitch_war: " + str(self.pitch_war)
        for year in self.years:
            self._year_wars[year].Print()


    def calcTotals(self):
        self.bat_war = 0
        self.pitch_war = 0
        for key in self._year_wars:
            self.bat_war += self._year_wars[key].bat_war
            self.pitch_war += self._year_wars[key].pitch_war

        self.total_war = self.bat_war + self.pitch_war


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

        data = TotalWar(uuid)
        cur.execute(sql)
        for row in cur:
            #print row
            yw = YearWar()
            yw.uuid = row[0]
            yw.year = row[1]
            if war_type == 'Bat':
                try: 
                    yw.bat_war = float(row[2])
                except TypeError:
                    yw.bat_war = 0
            else:
                try: 
                    yw.pitch_war = float(row[2])
                except TypeError:
                    yw.pitch_war = 0

            data.addYearWar(yw, True)

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

        for key in bat_war.years:
            combined_war.addYearWar(bat_war._year_wars[key], True)

        self._cache[uuid]['Combined'] = combined_war
        return self._cache[uuid]['Combined']

    def getTeamControlWar(self, uuid):
        combined_war = self.getCombinedWar(uuid)
        team_control_war = TotalWar(uuid)
        if combined_war.years:
            start_year = min(combined_war.years)
            if not start_year == 0:
                for yr in range(start_year, start_year+7):
                    if yr in combined_war._year_wars:
                        team_control_war.addYearWar(combined_war._year_wars[yr], True)

        return team_control_war

    def getName(self, uuid):
        cur = self.conn.cursor()
        sql = 'SELECT c.name_first, c.name_last '
        sql += ' FROM chadwickbureau c '
        sql += ' WHERE c.key_person = \'' + uuid + '\''

        cur.execute(sql)
        for row in cur:
            return '{0} {1}'.format(row[0], row[1])

        return ''
 

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
