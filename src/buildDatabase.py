import csv
#import Levenshtein
import os
import re

class BuildPlayerCache:
    def __init__(self,update=False):
        self.register_csv = '..\\data\\chadwickbureau\\people.csv'
        self.brbat_csv = '..\\data\\baseball-reference\\war_daily_bat.txt'
        self.brpitch_csv = '..\\data\\baseball-reference\\war_daily_pitch.txt'

        self.register_sql = '..\\sql\\chadwickbureau\\people.sql'
        self.brbat_sql = '..\\sql\\baseball-reference\\war_daily_bat.sql'
        self.brpitch_sql = '..\\sql\\baseball-reference\\war_daily_pitch.sql'

        if update:
            self.checkForUpdates()
        #self.parseSupportFile(support_filename)
        #self.validatePlayerNames(names)

    def checkForUpdates(self):
        #self.checkRegister()
        if not os.path.isfile(self.register_sql) or os.path.getmtime(self.register_csv) > os.path.getmtime(self.register_sql):
            self.parseRegister()
        if not os.path.isfile(self.brbat_sql) or os.path.getmtime(self.brbat_csv) > os.path.getmtime(self.brbat_sql):
            self.parseBrBatWar()
        if not os.path.isfile(self.brpitch_sql) or os.path.getmtime(self.brpitch_csv) > os.path.getmtime(self.brpitch_sql):
            self.parseBrPitchWar()

    def checkRegister(self):
        mycsv = csv.DictReader(open(self.register_csv, 'r'))
        lengths = {}
        for row in mycsv:
            for key in row.keys():
                if key in lengths:
                    if len(row[key]) > lengths[key]:
                        lengths[key] = len(row[key])
                else:
                    lengths[key] = len(row[key])

        print lengths
            

    def parseRegister(self):
        sql_f = open(self.register_sql, 'w')
        txt_f = open(self.register_csv, 'r')

        name_re = re.compile("name_")

        header = txt_f.readline()

        sql_f.write("USE 'mlbplayercache';\n")
        sql_f.write("DROP TABLE IF EXISTS chadwickbureau;\n")
        sql_f.write("CREATE TABLE chadwickbureau (\n")

        idx = 0
        quotes = []

        nums = False

        for x in header.split(','):
            if nums:
                sql_f.write(x)
                sql_f.write(" SMALLINT UNSIGNED DEFAULT NULL,\n")
            elif x == 'key_person':
                sql_f.write(x)
                sql_f.write(" VARCHAR(8),\n")
                quotes.append(idx)
            elif x == 'key_uuid':
                sql_f.write(x)
                sql_f.write(" VARCHAR(36),\n")
                quotes.append(idx)
            elif x == 'name_nick':
                sql_f.write(x)
                sql_f.write(" VARCHAR(50),\n")
                quotes.append(idx)
            elif x == 'name_given':
                sql_f.write(x)
                sql_f.write(" VARCHAR(50),\n")
                quotes.append(idx)
            elif name_re.match(x):
                sql_f.write(x)
                sql_f.write(" VARCHAR(20),\n")
                quotes.append(idx)
            else:
                sql_f.write(x)
                sql_f.write(" VARCHAR(15),\n")
                quotes.append(idx)

            idx = idx + 1

        sql_f.write(" PRIMARY KEY (key_person)\n);\n\n")
        #sql_f.write("INSERT INTO br_war_bat\n(")
        #sql_f.write(header)
        #sql_f.write(")\nVALUES\n")

        insert = "INSERT INTO chadwickbureau\n(" + header + ")\nVALUES\n";

        first = True

        for line in txt_f:
            #if first:
            #    first = False
            #else:
            #    sql_f.write(",\n")
            
            sql_f.write(insert)
            sql_f.write("(")
            #sql_f.write(line);
            idx = 0
            add_comma = False
            for value in line.split(','):
                if add_comma:
                    sql_f.write(",")
                else:
                    add_comma = True
                if idx in quotes:
                    sql_f.write("'")
                    sql_f.write(value.replace("'","''"))
                    sql_f.write("'")
                else:
                    sql_f.write(value)
                idx = idx + 1

            sql_f.write(")");

            sql_f.write(";\n")

        sql_f.close()

    def parseBrBatWar(self):
        sql_f = open(self.brbat_sql, 'w')
        txt_f = open(self.brbat_csv, 'r')

        header = txt_f.readline()

        sql_f.write("USE 'mlbplayercache';\n")
        sql_f.write("DROP TABLE IF EXISTS br_war_bat;\n")
        sql_f.write("CREATE TABLE br_war_bat (\n")
        sql_f.write("id INT UNSIGNED DEFAULT NULL AUTO_INCREMENT,\n")

        idx = 0
        quotes = []

        for x in header.split(','):
            if x == 'name_common':
                sql_f.write(x)
                sql_f.write(" VARCHAR(40),\n")
                quotes.append(idx)
            elif x == 'player_ID':
                sql_f.write(x)
                sql_f.write(" VARCHAR(20),\n")
                quotes.append(idx)
            elif x in ['team_ID','lg_ID','pitcher']:
                sql_f.write(x)
                sql_f.write(" VARCHAR(3),\n")
                quotes.append(idx)
            elif x in ['salary','age','year_ID','stint_ID','PA','G','salary']:
                sql_f.write(x)
                sql_f.write(" INT UNSIGNED DEFAULT NULL,\n")
            else:
                sql_f.write(x)
                sql_f.write(" FLOAT DEFAULT NULL,\n")

            idx = idx + 1

        sql_f.write(" PRIMARY KEY (id)\n);\n\n")
        #sql_f.write("INSERT INTO br_war_bat\n(")
        #sql_f.write(header)
        #sql_f.write(")\nVALUES\n")

        insert = "INSERT INTO br_war_bat\n(" + header + ")\nVALUES\n";

        first = True

        for line in txt_f:
            #if first:
            #    first = False
            #else:
            #    sql_f.write(",\n")
            
            sql_f.write(insert)
            sql_f.write("(")
            #sql_f.write(line);
            idx = 0
            add_comma = False
            for value in line.split(','):
                if add_comma:
                    sql_f.write(",")
                else:
                    add_comma = True
                if idx in quotes:
                    sql_f.write("'")
                    sql_f.write(value.replace("'","''"))
                    sql_f.write("'")
                else:
                    sql_f.write(value)
                idx = idx + 1

            sql_f.write(")");

            sql_f.write(";\n")

        sql_f.close()

    def parseBrPitchWar(self):
        sql_f = open(self.brpitch_sql, 'w')
        txt_f = open(self.brpitch_csv, 'r')

        header = txt_f.readline()

        sql_f.write("USE 'mlbplayercache';\n")
        sql_f.write("DROP TABLE IF EXISTS br_war_pitch;\n")
        sql_f.write("CREATE TABLE br_war_pitch (\n")
        sql_f.write("id INT UNSIGNED DEFAULT NULL AUTO_INCREMENT,\n")

        idx = 0
        quotes = []

        for x in header.split(','):
            if x == 'name_common':
                sql_f.write(x)
                sql_f.write(" VARCHAR(40),\n")
                quotes.append(idx)
            elif x == 'player_ID':
                sql_f.write(x)
                sql_f.write(" VARCHAR(20),\n")
                quotes.append(idx)
            elif x in ['team_ID','lg_ID','pitcher']:
                sql_f.write(x)
                sql_f.write(" VARCHAR(3),\n")
                quotes.append(idx)
            elif x in ['salary','age','year_ID','stint_ID','G','GS','IPouts','IPouts_start','IPouts_relief','salary']:
                sql_f.write(x)
                sql_f.write(" INT UNSIGNED DEFAULT NULL,\n")
            else:
                sql_f.write(x)
                sql_f.write(" FLOAT DEFAULT NULL,\n")

            idx = idx + 1

        sql_f.write(" PRIMARY KEY (id)\n);\n\n")
        #sql_f.write("INSERT INTO br_war_bat\n(")
        #sql_f.write(header)
        #sql_f.write(")\nVALUES\n")

        insert = "INSERT INTO br_war_pitch\n(" + header + ")\nVALUES\n";

        first = True

        for line in txt_f:
            #if first:
            #    first = False
            #else:
            #    sql_f.write(",\n")
            
            sql_f.write(insert)
            sql_f.write("(")
            #sql_f.write(line);
            idx = 0
            add_comma = False
            for value in line.split(','):
                if add_comma:
                    sql_f.write(",")
                else:
                    add_comma = True
                if idx in quotes:
                    sql_f.write("'")
                    sql_f.write(value.replace("'","''"))
                    sql_f.write("'")
                else:
                    sql_f.write(value)
                idx = idx + 1

            sql_f.write(")");

            sql_f.write(";\n")

        sql_f.close()

