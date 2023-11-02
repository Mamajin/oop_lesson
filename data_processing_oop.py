# import csv, os
#
# __location__ = os.path.realpath(
#     os.path.join(os.getcwd(), os.path.dirname(__file__)))
#
# cities = []
# with open(os.path.join(__location__, 'Cities.csv')) as f:
#     rows = csv.DictReader(f)
#     for r in rows:
#         cities.append(dict(r))
#
# countries = []
# with open(os.path.join(__location__, 'Countries.csv')) as f:
#     rows = csv.DictReader(f)
#     for r in rows:
#         countries.append(dict(r))
#
# # Print the average temperature for all the cities in Italy
# temps = []
# my_country = 'Italy'
# for city in cities:
#     if city['country'] == my_country:
#         temps.append(float(city['temperature']))
# print(sum(temps)/len(temps))
#
# print()
# # Print all cities that are not in the EU and whose average temperatures are below 5.0
# # Requires joining cities and countries
# import copy
# cities_ext = []
# for city in cities:
#     for country in countries:
#         if city['country'] == country['country']:
#             dict1 = copy.deepcopy(city)
#             dict2 = copy.deepcopy(country)
#             dict1.update(dict2)
#             cities_ext.append(dict1)
# for city in cities_ext:
#     if city['EU'] == 'no' and float(city['temperature']) < 5.0:
#         print(city)

import csv
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

cities = []
with open(os.path.join(__location__, 'Cities.csv')) as f:
    rows = csv.DictReader(f)
    for r in rows:
        cities.append(dict(r))

countries = []
with open(os.path.join(__location__, 'Countries.csv')) as f:
    rows = csv.DictReader(f)
    for r in rows:
        countries.append(dict(r))


class DB:
    def __init__(self):
        self.database = []

    def insert(self, table):
        """
        append table into database
        :param table:
        :return:
        """
        self.database.append(table)

    def search(self, table_name):
        """
        search for the table in the database if table does not exist return
        None.
        :param table_name:
        :return:
        """
        for table in self.database:
            if table.table_name == table_name:
                return table
        return None


import copy


class Table:
    def __init__(self, table_name, table):
        self.table_name = table_name
        self.table = table

    def join(self, other_table, common_key):
        """
        between two files cities and countries join them if they have a common
        key this case country and turn it into a bigger table the return the
        joined table
        :param other_table:
        :param common_key:
        :return:
        """
        joined_table = Table(
            self.table_name + '_joins_' + other_table.table_name, [])
        for item1 in self.table:
            for item2 in other_table.table:
                if item1[common_key] == item2[common_key]:
                    dict1 = copy.deepcopy(item1)
                    dict2 = copy.deepcopy(item2)
                    dict1.update(dict2)
                    joined_table.table.append(dict1)
        return joined_table

    def filter(self, condition):
        """
        input condition and return a filtered table
        :param condition:
        :return:
        """
        filtered_table = Table(self.table_name + '_filtered', [])
        for item1 in self.table:
            if condition(item1):
                filtered_table.table.append(item1)
        return filtered_table

    def aggregate(self, function, aggregation_key):
        """
        find avg of the key we put in
        :param function:
        :param aggregation_key:
        :return:
        """
        temps = []
        for item1 in self.table:
            temps.append(float(item1[aggregation_key]))
        return function(temps)

    def select(self, attributes_list):
        temps = []
        for item1 in self.table:
            dict_temp = {}
            for key in item1:
                if key in attributes_list:
                    dict_temp[key] = item1[key]
            temps.append(dict_temp)
        return temps

    def __str__(self):
        return self.table_name + ':' + str(self.table)


table1 = Table('cities', cities)
table2 = Table('countries', countries)
my_DB = DB()
my_DB.insert(table1)
my_DB.insert(table2)
my_table1 = my_DB.search('cities')
my_table1_filtered = my_table1.filter(lambda x: x['country'] == 'Italy')
my_table1_selected = my_table1.select(['city', 'latitude'])
print(my_table1)
print()
print(my_table1_selected)

temps = []
for item in my_table1_filtered.table:
    temps.append(float(item['temperature']))
print(sum(temps) / len(temps))
print("Using aggregation")
print(my_table1_filtered.aggregate(lambda x: sum(x) / len(x), 'temperature'))

print()
my_table2 = my_DB.search('countries')
my_table3 = my_table1.join(my_table2, 'country')
my_table3_filtered = my_table3.filter(lambda x: x['EU'] == 'no').filter(
    lambda x: float(x['temperature']) < 5.0)
print(my_table3_filtered.table)

# test case: Print min and max temp of cities in EU without coastline
# print(my_table3)
my_table4 = my_table3.filter(lambda x: x['EU'] == 'yes').filter(
    lambda x: x['coastline'] == 'no'
)
# print(my_table4) this is the filtered table EU yes and no coastline
print(my_table4.aggregate(lambda x: min(x), 'temperature'))
print(my_table4.aggregate(lambda x: max(x), 'temperature'))

# test case: Print min and max latitude for cities in every country
print(my_table3.aggregate(lambda x: min(x), 'latitude'))
print(my_table3.aggregate(lambda x: max(x), 'latitude'))