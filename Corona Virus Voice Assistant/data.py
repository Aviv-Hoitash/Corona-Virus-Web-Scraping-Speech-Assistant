import requests # for getting the url
from bs4 import BeautifulSoup #for scraping


def data_interval():
    URL = 'https://www.worldometers.info/coronavirus/#countries' #Where to scrape from
    page = requests.get(URL) #Getting the page
    soup = BeautifulSoup(page.content, 'html.parser') #making a BeautifulSoup object that parses through the html of the page provided

    results = soup.find(id="main_table_countries_today") #finding the table I want
    content = results.find_all('td') #finds all of the table data(td) in the table

    data = []
    for item in content:
        data.append(item.text.strip()) #for each of the items in the content object that we made, add it to data

    interval = data.index("USA") - data.index("World")

    return interval #finds and returns the amount of coulumns there are


def scrape_table(table_ID):
    #Exact same as before
    URL = 'https://www.worldometers.info/coronavirus/#countries'
    html_of_page = requests.get(URL)
    soup = BeautifulSoup(html_of_page.content, 'html.parser')

    table_container = soup.find(id=table_ID)
    table_content = table_container.find_all('td')

    table_data = []
    for item in table_content:
        table_data.append(item.text.strip())

    interval = data_interval() #creates an interval object that returns the interval

    #For all of these indexes you need to look at the website table to understand but pretty much it is just finding each of the coulumns
    old_countries = table_data[1::interval]
    countries = []
    for country in old_countries:
        countries.append(country.lower())

    total_cases = table_data[2::interval]
    new_cases = table_data[3::interval]
    total_deaths = table_data[4::interval]
    new_deaths = table_data[5::interval]
    total_recovered = table_data[6::interval]
    active_cases = table_data[7::interval]
    critical_cases = table_data[9::interval]
    case_per_mil = table_data[10::interval]
    death_per_mil = table_data[11::interval]
    total_tests = table_data[12::interval]
    tests_per_mil = table_data[13::interval]
    population = table_data[14::interval]

    column_names = ["Country", "Total Cases", "New Cases", "Total Deaths", "New Deaths", "Total Recovered",
                    "Active Cases", "Critical Cases", "Cases Per Million People", "Deaths Per Million People",
                    "Total Tests",
                    "Tests Per Million People", "Population"]
    covid19_table = {
        "columns": column_names,
        "country": countries,
        "total_cases": total_cases,
        "new_cases": new_cases,
        "total_deaths": total_deaths,
        "new_deaths": new_deaths,
        "active_cases": active_cases,
        "total_recovered": total_recovered,
        "critical_cases": critical_cases,
        "case_per_mil": case_per_mil,
        "death_per_mil": death_per_mil,
        "total_tests": total_tests,
        "tests_per_mil": tests_per_mil,
        "population": population

    }


    return covid19_table #returns the whole table with the coulumn names corrsponding to a list of the correct data


def dict_index(dict, search_term):
    return dict["country"].index(search_term) #function that returns the index of a key in a dictionary


#finds the growth factor by finding the amount of new cases and dividing it by the number of new cases yesterday.
def Growth_factor(growth_today, growth_yesterday):
    if growth_today:
        if growth_yesterday:
            if not growth_today and  not growth_yesterday == 'None':
                Gf = str(round(float(growth_today) / float(growth_yesterday), 4) * 100) + "%" #The times 100 and + "%" is to convert it into a percent
            else:
                Gf = 0 #there is no growth today pf growth yesterday
        else:
            Gf = 0
    else:
        Gf = 0

    return Gf

# A function that puts to use all of the functions made before to make all of our data.
def get_data(country_name, data_type="all"): #The parameters are the country you want and which couloumn you want(Default is all)
    table_today = scrape_table("main_table_countries_today") #Scrapes the data for the today table
    table_yesterday = scrape_table("main_table_countries_yesterday")#Scrapes the data for the yesterday table

    index_country_today = dict_index(table_today, country_name)
    index_country_yesterday = dict_index(table_yesterday, country_name) #finds the indexes of the country names

    Gf_country = Growth_factor(table_today["new_cases"][index_country_today].replace(',', ''),
                               table_yesterday["new_cases"][index_country_yesterday].replace(',', '')) #Finds the growth factor
    
    #Makes a dictionary with all of the data
    data = {
        "Total Cases": table_today["total_cases"][index_country_today],
        "New Cases": table_today["new_cases"][index_country_today],
        "Total Deaths": table_today["total_deaths"][index_country_today],
        "New Deaths": table_today["new_deaths"][index_country_today],
        "Total Recovered": table_today["total_recovered"][index_country_today],
        "Critical Cases": table_today["critical_cases"][index_country_today],
        "Case Per Million": table_today["case_per_mil"][index_country_today],
        "death per Million": table_today["death_per_mil"][index_country_today],
        "Total Tests": table_today["total_tests"][index_country_today],
        "Tests per Million": table_today["tests_per_mil"][index_country_today],
        "Population": table_today["population"][index_country_today],

        "Growth factor": Gf_country

    }
    
    #cleans up the data so that the computer can talk it better
    for key in data.keys():
             #Finds If there is empty data and makes it None instead
            if data[key] == '':
                print(data[key]+key)
                data[key] = "None"

            #Finds if there is a + in the data and takes it away 
            if '+' in str(data[key]):
                data[key] = data[key][1:]
                
                
                


    # if the data type paramter is all return the country you want and all of the data for it.
    if data_type == "all":
        return country_name + str(data)
    # if its not return the country name and the specific data you want
    else:
        for key in data.keys():
            if data_type == key:
                    return country_name + ":" + key + ":" + data[key]




