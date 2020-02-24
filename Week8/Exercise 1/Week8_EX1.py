import numpy as np
import matplotlib.pyplot as plt

filename = './befkbhalderstatkode.csv'

stats = np.genfromtxt(filename, delimiter=',', dtype=np.uint, skip_header=1)

neighb = {1: 'Indre By', 2: 'Østerbro', 3: 'Nørrebro', 4: 'Vesterbro/Kgs. Enghave', 
       5: 'Valby', 6: 'Vanløse', 7: 'Brønshøj-Husum', 8: 'Bispebjerg', 9: 'Amager Øst', 
       10: 'Amager Vest', 99: 'Udenfor'}

def number_of_people_per_neighbourhood(n, mask):
    all_people_in_given_n = stats[mask & (stats[:,1] == n)]
    sum_of_people = all_people_in_given_n[:,4].sum()
    return sum_of_people

#Year 2015 mask
year_mask = (stats[:,0] == 2015)

people_in_area_specific_year = {}
for key in neighb:
    people_in_area_specific_year[neighb[key]] = number_of_people_per_neighbourhood(key, year_mask)

def bar_chart_cities(stats_dict):
    sorted_stats = {k: v for k, v in sorted(stats_dict.items(), key=lambda item: item[1])}

    plt.bar(sorted_stats.keys(), sorted_stats.values(), width=0.9, align='center')

    max_y = 0
    for key in stats_dict:
        if max_y < stats_dict[key]:
            max_y = stats_dict[key]

    plt.axis([0, len(stats_dict) + 1, 0, max_y + 1000])
    plt.title("City areas", fontsize=12)
    plt.xlabel("Name", fontsize=10)
    plt.ylabel("Amount of people", fontsize=10)
    #Making and empty space before the first shown person in the chart:
    plt.xlim(-1, len(stats_dict))
    #Rotate x axis labels:
    plt.xticks(rotation=17)
    plt.tick_params(axis='both', which='major', labelsize=10)

    plt.show()

#bar_chart_cities(people_in_area_specific_year)

def n_of_people_in_year_above_specific_age(year, age, extra_mask):
    if str(type(extra_mask)) == "<class 'NoneType'>":
        filtered_data = stats[(stats[:,0] == year) & (stats[:,2] > age)]
    else:
        filtered_data = stats[(stats[:,0] == year) & (stats[:,2] > age) & extra_mask]
    sum_of_people = filtered_data[:,4].sum()
    return sum_of_people

#print(n_of_people_in_year_above_specific_age(2015, 65, None))

origin_mask = (stats[:,3] != 5100)

#print(n_of_people_in_year_above_specific_age(2015, 65, origin_mask))

Østerbro_data = {}
Vesterbro_data = {}

for i in range(1992,2016):
    Østerbro_data[i] = number_of_people_per_neighbourhood(2, (stats[:,0] == i))
    Vesterbro_data[i] = number_of_people_per_neighbourhood(4, (stats[:,0] == i))


def line_plot_for_two_cities(city_dict_1, city_dict_2):
    
    #First dict of data:
    plt.plot(list(city_dict_1.keys()),list(city_dict_1.values()), linewidth=2)
    #Second dict of data:
    plt.plot(list(city_dict_2.keys()),list(city_dict_2.values()), linewidth=2)
    # Set chart title and label axes. 
    plt.title("Østerbro and Vesterbro", fontsize=24)
    plt.xlabel("Year", fontsize=14)
    plt.ylabel("Amount of people", fontsize=14)
    # Set size of tick labels.
    plt.tick_params(axis='both', labelsize=14)

    plt.show()

line_plot_for_two_cities(Østerbro_data, Vesterbro_data)