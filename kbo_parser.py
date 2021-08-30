from os import getcwd
from re import search
from time import sleep

from multiprocessing import Pool, freeze_support

import pandas as pd

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

from sqlalchemy import create_engine, inspect, Column, Integer, String, ForeignKey
from sqlalchemy.engine.url import URL, make_url
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import Float

dbDriver = 'postgresql+psycopg2'
dbHost = '192.168.0.10'
dbPort = '5432'
dbUsername = 'postgres'
dbPassword = 'qwas)%@^4078'
dbName = 'kbo'

Base = declarative_base()
class Team(Base):
    __tablename__ = "team"
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String, unique=True)

class Hitter(Base):
    __tablename__ = "hitter"
    player_id = Column('player_id', Integer, primary_key=True)
    year = Column('year', Integer, primary_key=True)
    name = Column('name', String)
    team_id = Column('team_id', Integer, ForeignKey('team.id'))
    avg = Column('avg', String)
    g = Column('g', Integer)
    pa = Column('pa', Integer)
    ab = Column('ab', Integer)
    h = Column('h', Integer)
    _2b = Column('2b', Integer)
    _3b = Column('3b', Integer)
    hr = Column('hr', Integer)
    rbi = Column('rbi', Integer)
    bb = Column('bb', Integer)
    hbp = Column('hbp', Integer)
    so = Column('so', Integer)
    gdp = Column('gdp', Integer)

class Pitcher(Base):
    __tablename__ = "pitcher"
    player_id = Column('player_id', Integer, primary_key=True)
    year = Column('year', Integer, primary_key=True)
    name = Column('name', String)
    team_id = Column('team_id', Integer, ForeignKey('team.id'))
    era = Column('era', String)
    g = Column('g', Integer)
    w = Column('w', Integer)
    l = Column('l', Integer)
    sv = Column('sv', Integer)
    hld = Column('hld', Integer)
    wpct = Column('wpct', String)
    ip = Column('ip', String)
    h = Column('h', Integer)
    hr = Column('hr', Integer)
    bb = Column('bb', Integer)
    hbp = Column('hbp', Integer)
    so = Column('so', Integer)
    r = Column('r', Integer)
    er = Column('er', Integer)

def init_engine(driver, host, port, username, password, database):
    url = URL.create(drivername=driver, host=host, port=port, username=username, password=password, database=database)
    engine = create_engine(url)
    return engine

def init_session(engine):
    session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    return session

def create_table(engine, table):
    if not inspect(engine).has_table(table.__tablename__): # check exist teams table
        table.__table__.create(bind=engine, checkfirst=True)

def read_table(engine, session, table):
    if inspect(engine).has_table(table.__tablename__): # check exist teams table
        return session.query(table).all()

def get_kbo_teams(url, year):
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument('--headless')
    chromeDriver = webdriver.Chrome(executable_path=getcwd() + '/driver/chromedriver.exe', options=chromeOptions)

    teamList = []
    try:
        chromeDriver.get(url)
        chromeDriver.implicitly_wait(10)

        seasonSelect = Select(chromeDriver.find_element_by_xpath('//select[@id="cphContents_cphContents_cphContents_ddlSeason_ddlSeason"]'))
        seasonSelect.select_by_value(str(year))
        sleep(1)
    except Exception as e:
        print("Fail to get " + str(year) + " season data")
        chromeDriver.close()
        return []

    try:
        teams = chromeDriver.find_elements_by_xpath('//select[@id="cphContents_cphContents_cphContents_ddlTeam_ddlTeam"]/option')
        if len(teams) > 1:
            for idx in range (1, len(teams)):
                teamList.append(teams[idx].text)
    except Exception as e:
        print("Fail to get season list")
        chromeDriver.close()
        return []
    chromeDriver.close()
    return teamList

def get_kbo_stats(url, year):
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument('--headless')
    chromeDriver = webdriver.Chrome(executable_path=getcwd() + '/driver/chromedriver.exe', options=chromeOptions)

    try:
        chromeDriver.get(url)
        chromeDriver.implicitly_wait(10)

        seasonSelect = Select(chromeDriver.find_element_by_xpath('//select[@id="cphContents_cphContents_cphContents_ddlSeason_ddlSeason"]'))
        seasonSelect.select_by_value(str(year))
        sleep(1)
    except Exception as e:
        print("Fail to select " + str(year) + " season")
        chromeDriver.close()
        return pd.DataFrame([], columns=[])
    
    try:
        chromeDriver.find_element_by_xpath('//div[@class="more_record"]')
        isMoreExist = True
    except NoSuchElementException as e:
        isMoreExist = False

    try:
        if isMoreExist:
            prevData = []
            prevTitle = ['PLAYER_ID', 'YEAR']
            nextData = []
            nextTitle = ['PLAYER_ID']
            isInitPrevTitle = False
            isInitNextTitle = False

            numOfTeams = len(chromeDriver.find_elements_by_xpath('//select[@id="cphContents_cphContents_cphContents_ddlTeam_ddlTeam"]/option'))
            for teamIdx in range(1, numOfTeams):
                teamSelect = Select(chromeDriver.find_element_by_xpath('//select[@id="cphContents_cphContents_cphContents_ddlTeam_ddlTeam"]'))
                teamSelect.select_by_index(teamIdx)
                sleep(1)

                prev = chromeDriver.find_element_by_xpath('//div[@class="more_record"]').find_element_by_xpath('//a[@class="prev"]')
                prev.click()
                sleep(1)

                numOfPages = len(chromeDriver.find_element_by_xpath('//div[@class="paging"]').find_elements_by_xpath('//a[starts-with (@id, "cphContents_cphContents_cphContents_ucPager_btnNo")]'))
                for pageIdx in range(0, numOfPages):
                    page = chromeDriver.find_element_by_xpath('//div[@class="paging"]').find_elements_by_xpath('//a[starts-with (@id, "cphContents_cphContents_cphContents_ucPager_btnNo")]')[pageIdx]
                    page.click()
                    sleep(1)

                    html = chromeDriver.page_source
                    soup = BeautifulSoup(html, 'html.parser')
                    result = soup.find('div', attrs={"class":"record_result"})
                    table_data = result.find('table', attrs={"class":"tData01 tt"})
                    if not isInitPrevTitle:
                        prevTitle.extend([title.text for title in table_data.select('thead > tr > th')])
                        isInitPrevTitle = True
                    stats = table_data.select('tbody > tr')
                    for stat in stats:
                        a_href = stat.find('a')["href"]
                        m = search("\?playerId=(\d+)", a_href)
                        if m.group(0):
                            id = m.group(1)
                            playerData = [id, year]
                            playerData.extend([s.get_text().strip() for s in stat.find_all('td')])
                            prevData.append(playerData)
                
                next = chromeDriver.find_element_by_xpath('//div[@class="more_record"]').find_element_by_xpath('//a[@class="next"]')
                next.click()
                sleep(1)

                for pageIdx in range(0, numOfPages):
                    page = chromeDriver.find_element_by_xpath('//div[@class="paging"]').find_elements_by_xpath('//a[starts-with (@id, "cphContents_cphContents_cphContents_ucPager_btnNo")]')[pageIdx]
                    page.click()
                    sleep(1)

                    html = chromeDriver.page_source
                    soup = BeautifulSoup(html, 'html.parser')
                    result = soup.find('div', attrs={"class":"record_result"})
                    table_data = result.find('table', attrs={"class":"tData01 tt"})
                    if not isInitNextTitle:
                        nextTitle.extend([title.text for title in table_data.select('thead > tr > th')][4:])
                        isInitNextTitle = True
                    stats = table_data.select('tbody > tr')
                    for stat in stats:
                        a_href = stat.find('a')["href"]
                        m = search("\?playerId=(\d+)", a_href)
                        if m.group(0):
                            id = m.group(1)
                            playerData = [id]
                            playerData.extend([s.get_text().strip() for s in stat.find_all('td')][4:])
                            nextData.append(playerData)
            prevDataFrame = pd.DataFrame(prevData, columns=prevTitle)
            nextDataFrame = pd.DataFrame(nextData, columns=nextTitle)
            dataFrame = pd.merge(prevDataFrame, nextDataFrame, on='PLAYER_ID')
        else:
            data = []
            title = ['PLAYER_ID', 'YEAR']
            isInitTitle = False

            numOfTeams = len(chromeDriver.find_elements_by_xpath('//select[@id="cphContents_cphContents_cphContents_ddlTeam_ddlTeam"]/option'))
            for teamIdx in range(1, numOfTeams):
                teamSelect = Select(chromeDriver.find_element_by_xpath('//select[@id="cphContents_cphContents_cphContents_ddlTeam_ddlTeam"]'))
                teamSelect.select_by_index(teamIdx)
                sleep(1)

                numOfPages = len(chromeDriver.find_element_by_xpath('//div[@class="paging"]').find_elements_by_xpath('//a[starts-with (@id, "cphContents_cphContents_cphContents_ucPager_btnNo")]'))
                for pageIdx in range(0, numOfPages):
                    page = chromeDriver.find_element_by_xpath('//div[@class="paging"]').find_elements_by_xpath('//a[starts-with (@id, "cphContents_cphContents_cphContents_ucPager_btnNo")]')[pageIdx]
                    page.click()
                    sleep(1)

                    html = chromeDriver.page_source
                    # html.parser, lxml, lxml-xml, html5lib
                    soup = BeautifulSoup(html, 'html.parser')
                    result = soup.find('div', attrs={"class":"record_result"})
                    table_data = result.find('table', attrs={"class":"tData01 tt"})
                    if not isInitTitle:
                        title.extend([ title.text for title in table_data.select('thead > tr > th') ])
                        isInitTitle = True
                    stats = table_data.select('tbody > tr')
                    for stat in stats:
                        a_href = stat.find('a')["href"]
                        m = search("\?playerId=(\d+)", a_href)
                        if m.group(0):
                            id = m.group(1)
                            playerData = [id, year]
                            playerData.extend([s.get_text().strip() for s in stat.find_all('td')])
                            data.append(playerData)
            dataFrame = pd.DataFrame(data, columns=title)
    except Exception as e:
            print("Fail to get " + str(year) + " season stat")
            chromeDriver.close()
            return pd.DataFrame([], columns=[])
    if '순위' in dataFrame.columns:
        dataFrame = dataFrame.drop(['순위'], axis=1)
    if '선수명' in dataFrame.columns:
        dataFrame.rename(columns={'선수명':'NAME'}, inplace=True)
    if '팀명' in dataFrame.columns:
        def convert_team_id(x):
            id = session.query(Team.id).filter(x == Team.name).scalar()
            if id is not None:
                return id
            return x
        dataFrame['팀명'] = dataFrame['팀명'].apply(convert_team_id)
        dataFrame.rename(columns={'팀명':'TEAM_ID'}, inplace=True)
    for column in dataFrame.columns:
        dataFrame.rename(columns={column:column.lower()}, inplace=True)
    chromeDriver.close()

    print("Success to get " + str(year) + " season stat")
    return dataFrame

# Crawling KBO All Pitcher's stats
def get_all_pitchers(year):
    stats = get_kbo_stats('https://www.koreabaseball.com/Record/Player/PitcherBasic/Basic1.aspx', year)
    for column in stats.columns:
        if not column in Pitcher.__table__.columns:
            stats = stats.drop([column], axis=1)
    stats.to_sql(name=Pitcher.__tablename__, con=engine, if_exists='append', index=False)

# Crawling KBO All Hitter's stats
def get_all_hitters(year):
    stats = get_kbo_stats('https://www.koreabaseball.com/Record/Player/HitterBasic/Basic1.aspx', year)
    for column in stats.columns:
        if not column in Hitter.__table__.columns:
            stats = stats.drop([column], axis=1)
    stats.to_sql(name=Hitter.__tablename__, con=engine, if_exists='append', index=False)

engine = init_engine(dbDriver, dbHost, dbPort, dbUsername, dbPassword, dbName)
session = init_session(engine)

#create_table(engine, Team)
#create_table(engine, Hitter)
create_table(engine, Pitcher)

if __name__=='__main__':
    freeze_support()
    pitcher_pool = Pool(12)
    #hitter_pool = Pool(12)

    # Crawling KBO All Teams
    #teamList = []
    #for year in range(1982, 2021):
    #    teams = get_kbo_teams('https://www.koreabaseball.com/Record/Player/HitterBasic/Basic1.aspx', year)
    #    teamList.extend(teams)
    #teamSeries = pd.Series(teamList, name='name')
    #teamSeries.drop_duplicates(keep='first', inplace=True)
    #teamSeries.to_sql(name=Team.__tablename__, con=engine, if_exists='append', index=False)

    pitcher_pool.map(get_all_pitchers, list(range(1982, 2021)))
    pitcher_pool.close()
    pitcher_pool.join()

    #hitter_pool.map(get_all_hitters, list(range(1982, 2021)))
    #hitter_pool.close()
    #hitter_pool.join()