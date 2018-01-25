import requests
import mysql.connector
from slimit import ast
from slimit.parser import Parser
from slimit.visitors import nodevisitor
import time
import warnings

# ignore warning
warnings.filterwarnings("ignore")

MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'port': 3306,
    'database': 'MyDataBase',
    'charset': 'utf8'
}

# connect database
try:
    mydb = mysql.connector.connect(**MYSQL_CONFIG)
    my_cursor = mydb.cursor()
except mysql.connector.Error as e:
    print('connect fails!{}'.format(e))

# insert data
def insert_soccer_team_data(team_id, chinese_name, english_name):
    insert_sql = "INSERT INTO `MyDataBase`.`Soccer_Team` (`team_id`, `Chinese_Name`, `English_Name`) VALUES ('{}', '{}', '{}');".format(team_id, chinese_name, english_name)
    try:
        my_cursor.execute(insert_sql)
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

def insert_soccer_game_data(*args):
    insert_sql = "INSERT INTO `MyDataBase`.`Game_Info` (`year`, `No`, `Date`, `Home`, `Score`, `Away`, `pageid`) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}');".format(*args)
    try:
        my_cursor.execute(insert_sql)
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

def get_page_data(url, headers):
    data = requests.get(url, headers=headers).text
    time.sleep(1)
    return data

# start_url config
year_list = list(range(2017, 2018))
start_url_pattern = 'http://info.nowgoal.cc/jsData/matchResult/{}/s25_943.js?flesh=0.5008168192746318'
start_page_headers = {
    'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
}

def parse_soccer_team_js(data):
    soccer_team_info_list = []
    parser = Parser()
    tree = parser.parse(data)
    for n in list(nodevisitor.visit(tree)):
        if isinstance(n, ast.VarDecl):
            var_name = n.children()[0].value
            var_data = n.children()[1].children()
            if var_name == 'arrTeam':
                for t in var_data:
                    team_info = [i.value for i in t]
                    team_useful_info = (int(team_info[0]), team_info[1][1:-1], team_info[3][1:-1])
                    soccer_team_info_list.append(team_useful_info)
    return soccer_team_info_list

def parse_soccer_game_js(data):
    soccer_game_info_list = []
    parser = Parser()
    tree = parser.parse(data)
    for n in list(nodevisitor.visit(tree)):
        if isinstance(n, ast.ExprStatement):
            var_expr_name = n.children()[0].children()[0]
            if not isinstance(var_expr_name, ast.Identifier):
                var_name = n.children()[0].children()[0].expr.value
                var_data = n.children()[0].children()[1]
                if var_name.startswith('"R'):
                    No = int(var_name[3:-1])
                    for t in var_data:
                        team_info = [i.value for i in t]
                        year = int(team_info[3][1:5])
                        team_useful_info = (year, No, team_info[3][1:-1], team_info[4], team_info[6][1:-1], team_info[5], int(team_info[0]))
                        soccer_game_info_list.append(team_useful_info)
    return soccer_game_info_list

# def main():
#
#     data_set = set()
#
#     for year in year_list:
#         data = get_page_data(start_url_pattern.format(year), headers=start_page_headers)
#         try:
#             team_info_list = parse_soccer_team_js(data)
#             for i in team_info_list:
#                 data_set.add(i)
#         except:
#             print('Failed in {}'.format(year))
#
#     while data_set:
#         insert_soccer_team_data(*data_set.pop())
#
#     mydb.commit()
#     my_cursor.close()
#     mydb.close()

def main():

    data_set = set()

    for year in year_list:
        data = get_page_data(start_url_pattern.format(year), headers=start_page_headers)
        try:
            team_info_list = parse_soccer_game_js(data)
            for i in team_info_list:
                data_set.add(i)
        except Exception as e:
            print('Failed in {} --- {}'.format(year, e))

    while data_set:
        insert_soccer_game_data(*data_set.pop())

    mydb.commit()
    my_cursor.close()
    mydb.close()


if __name__ == '__main__':
    main()