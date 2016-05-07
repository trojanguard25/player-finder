from dataSource import DataSource


class BRSource(DataSource):
    def __init__(self):
        DataSource.__init__(self)
        self.bat_table = 'br_war_bat'
        self.pitch_table = 'br_war_pitch'
        self.year = 'year_ID'
        self.war = 'WAR'
    
    def _uuidToId(self):
        return "data.player_ID = c.key_bbref"
