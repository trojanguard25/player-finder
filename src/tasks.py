from fabric.api import task, local, lcd, settings
import config
import urllib
import os
import buildDatabase

@task
def update_databases():
    message = ''
    cwd = os.getcwd()
    bd = buildDatabase.BuildPlayerCache()

    br_path = config.Config.pathToBR

    with lcd(br_path):
        local("rm -rf tmp")
        local("mkdir tmp")
   
    with lcd(br_path + os.sep + "tmp"):
        local("wget http://www.baseball-reference.com/data/war_daily_bat.txt")
        local("wget http://www.baseball-reference.com/data/war_daily_pitch.txt")


    with lcd(br_path):
        with settings(warn_only=True):
            result = local("diff -q war_daily_bat.txt ./tmp/war_daily_bat.txt")
            if result.return_code == 1:
                local("cp ./tmp/war_daily_bat.txt war_daily_bat.txt")
                bd.parseBrBatWar()
                message += "BR batter WAR updated.\n"

            result = local("diff -q war_daily_pitch.txt ./tmp/war_daily_pitch.txt")
            if result.return_code == 1:
                local("cp ./tmp/war_daily_pitch.txt war_daily_pitch.txt")
                bd.parseBrPitchWar()
                message += "BR pitcher WAR updated.\n"



    chadwick_repo = config.Config.pathToChadwickRepo
    with lcd(chadwick_repo):
        local("git pull")

        with settings(warn_only=True):
            result = local("diff -q data/people.csv " + cwd + os.sep + config.Config.pathToChadwick + os.sep + "people.csv")
            if result.return_code == 1:
                local("cp data/people.csv " + cwd + os.sep + config.Config.pathToChadwick + os.sep + "people.csv")
                bd.parseRegister()
                message += "Chadwick register updated.\n"


    if message:
        local('echo "' + message + '" | mail -s "mlbplayercache updates" {0}'.format(config.Config.updateEmailAddress))
    else:
        local('echo "no updates" | mail -s "mlbplayercache updates" {0}'.format(config.Config.updateEmailAddress))



