import os
import sys

import presamples as ps
import brightway2 as bw
from functions import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def flatten(t):
    return [item for sublist in t for item in sublist]

def downstream_connection(activity, level):
    '''
    This function return a the downstream activities of a certain activity at the desired depth (1-3)
    :param activity: The activity to be investigated
    :param level: The number of levels below the investigated activity
    :return: List (of lists, of lists) of downstream activities
    © Fabian Lechtenberg, UPC Barcelona, ETH Zürich, 09.03.2022
    Comment: Changed on 14.03.2022 to return a tuple [activity, reference product]. --> Reference product identification
    can be removed from here and placed in another function for elegance.
    '''
    if level == 1:
        exchanges = [exc for exc in activity[0].upstream()]
        return [[exc.output, exc.output._data['reference product']] for exc in exchanges]
    if level == 2:
        activities = downstream_connection(activity, 1)
        down_activities = [downstream_connection(act, 1) for act in activities]
        return down_activities
    if level == 3:
        activities = downstream_connection(activity, 2)
        down_activities = [[downstream_connection(act, 1) for act in act2] for act2 in activities]
        return down_activities
    return True

def pattern_list(n, l1, l2, l3=[]):
    '''
    For a list of (lists of lists) create a list that associates a pattern to every element in the nested list.
    E.g. [[[[a],[b,c],[d,e]],[[f],[g]]],[[h]]] --> f would be [1,2,1]
    :return: The list of patters
    © Fabian Lechtenberg, UPC Barcelona, ETH Zürich, 13.03.2022
    '''

    pattern = []
    for i in range(1,len(l1)+1):
        pattern.append([n,i,0,0])
    for i in range(1,len(l2)+1):
        for j in range(1, len(l2[i-1])+1):
            pattern.append([n,i,j,0])
    if l3!=[]:
        for i in range(1, len(l3) + 1):
            for j in range(1, len(l3[i - 1]) + 1):
                for k in range(1, len(l3[i-1][j-1]) + 1):
                    pattern.append([n,i,j,k])
    return pattern

def create_bar_plots(old, new, xlabel, pattern, folder, name, top_n):
    '''
    Calculates the relative change after implementing the change in the production system and plots the results in bar charts.
    Sorted by impact and non-sorted.
    :param old: Old results (np.array from dataframe)
    :param new: New results (np.array from dataframe)
    :param xlabel: Labels for the activities, reference products and patterns.
    :param pattern: Level pattern of the activities.
    :param folder: Folder to save the file to.
    :param name: Name of the file and method.
    :param top_n: Number of the most influenced activities to be plotted.
    :return: Nothing. Creates and saves the plots.
    © Fabian Lechtenberg, UPC Barcelona, ETH Zürich, 17.03.2022
    '''
    # Caculate the percentage decrease in impact
    change = np.multiply(np.divide(np.subtract(old.to_numpy(), new.to_numpy()),old.to_numpy()),100)

    # Set the xlabel and print the methods
    xlabel = xlabel.to_numpy()
    print(name)

    # Colors based on level
    colors = []
    for pat in pattern:
        pat = pat.lstrip('[').rstrip(']').split(',')
        pat = [pat.strip() for pat in pat]
        if pat[2] == '0':
            colors.append('#003399') # Dark blue
        elif pat[3] == '0':
            colors.append('#0099ff') # Medium blue
        else:
            colors.append('#66ccff') # Light blue

    fig, ax = plt.subplots()

    # Unsorted without Label
    y_pos = np.arange(len(change))
    ax.bar(y_pos,change, color=colors)
    ax.set_xlim((0,len(change)))
    ax.set_xlabel('Activity')
    ax.set_ylabel(name + ' [%]')
    fig.savefig(folder + name + '_unsorted.png', bbox_inches='tight', dpi=300)

    fig2, ax2 = plt.subplots()
    # Sorted with label (Decrease)
    inds = change.argsort()
    change_sorted = change[inds[::-1]]
    xlabel_sorted = xlabel[inds[::-1]]
    colors_sorted = np.array(colors)[inds[::-1]]

    y_pos = np.arange(top_n)
    if np.average(change_sorted) > 0:
        ax2.barh(y_pos, (change_sorted[0:top_n])[::-1], edgecolor='black', color=(colors_sorted[0:top_n])[::-1])
        ax2.set_yticks(y_pos, (xlabel_sorted[0:top_n])[::-1])
    else:
        ax2.barh(y_pos, change_sorted[-top_n::], edgecolor='black', color=colors_sorted[-top_n::])
        ax2.set_yticks(y_pos, xlabel_sorted[-top_n::])
    ax2.set_ylim((0, top_n))
    ax2.yaxis.tick_right()
    ax2.set_xlabel(name + ' [%]')
    fig2.savefig(folder + name + '_sorted.png', bbox_inches='tight', dpi=300)
    return

def get_level_pattern(activities, rev):
    '''
    This functions returns a flattened list of downstream activities to the passed activities. Also returns a pattern
    list that allows to identify how a certain activity branches from the main activities.
    :param activities: Activities to be substituted (preferably markets)
    :param rev: Number of levels to investigate (currently only 2-3 possible)
    :return: level - flattened list of all the downstream activities. Contains a tuple of (activity, reference product)
             pattern - flattened list of patterns. See implementation of a description
    © Fabian Lechtenberg, UPC Barcelona, ETH Zürich, 17.03.2022
    '''
    level = []
    pattern = []
    n = 1
    for activity in activities:
        level_1 = downstream_connection([activity, ''], 1)
        level_2 = downstream_connection([activity, ''], 2)
        if rev == 3:
            level_3 = downstream_connection([activity, ''], 3)
            pattern = pattern + pattern_list(n, level_1, level_2, level_3)
            level_2 = flatten(level_2)
            level_3 = flatten(flatten(level_3))
            level = level + level_1 + level_2 + level_3
        else:
            pattern = pattern + pattern_list(n, level_1, level_2)
            level_2 = flatten(level_2)
            level = level + level_1 + level_2
        n += 1
    return level, pattern

def perform_multiLCA(prodsys, methods, presample=None):
    '''
    Perform the Multi-LCA for a given product system, methods and presample.
    :param prodsys: Product system.
    :param methods: Methods.
    :param presample: Presamples.
    :return: Multi-LCA results
    © Fabian Lechtenberg, UPC Barcelona, ETH Zürich, 17.03.2022
    '''
    bw.calculation_setups['multiLCA'] = {'inv': prodsys, 'ia': methods}
    if presample == None:
        myMultiLCA = bw.MultiLCA('multiLCA')
    else:
        myMultiLCA = bw.MultiLCA('multiLCA', presample)
    return myMultiLCA.results

def save_results(path, results, methods, level, pattern):
    '''
    Save the results to a specified path. Pass all the arguments to reasonably structure the dataframe.
    :param path: Path to store the results to.
    :param results: Dataframe of results - obtained from Multi-LCA methods.
    :param methods: Methods that were used to obtain the results.
    :param level: List of activities and reference products.
    :param pattern: List of patterns.
    :return: Nothing
    © Fabian Lechtenberg, UPC Barcelona, ETH Zürich, 17.03.2022
    '''
    # Adjust the level and pattern to create reasonable labels for each activity
    level_pattern = []
    for i in range(0, len(level)):
        act = str(level[i][0]).split('\'')
        loc = act[2].split(',')
        level_pattern.append(act[1] + ' ¦ ' + level[i][1] + ' ¦ ' + loc[1] + ' ¦ ' + str(pattern[i]))

    # Construct the dataframe
    df_impact = pd.DataFrame(data=results, columns=methods)
    df_impact.insert(0, 'Level_Pattern', level_pattern)
    df_impact.insert(0, 'Pattern', pattern)
    df_impact.insert(0, 'Activity', [str(lev) for lev in level])

    # Save the results
    df_impact.to_excel(path)
    return

def perform_replacement(config):
    '''
    This is the core function to perform the replacement calculations. It takes as input a config file that specifies
    all the activities that are to be exchanged, the methods to be applied and so on. An example for the config file
    can be found in the read.me.
    :param config: Config file for all specifications of the replacement action.
    :return: ---
    '''
    # Set the project and database
    if config['project'] in bw.projects:
        bw.projects.set_current(config['project'])
    else:
        print('Selected project does not exist. Please create project and proceed with the assessment.')
        sys.exit()
    if config['db'] in bw.databases:
        eidb = bw.Database(config['db'])
        print('Perform a replacement in the Ecoinvent database: ' + config['db'] + '\n')
    else:
        print('Selected database does not exist. Please create database and proceed with the assessment.')
        sys.exit()

    # Retrieve the activities
    activity = []
    for act_key in config['activities']:
        # FL (17.03.2022) - Is there a faster way to do this?
        activity = activity + [act for act in eidb if str(act.key) == act_key]
    print('The activities that will be altered are: ')
    for act in activity:
        print(act['name'] + ' --- ' + act['location'])

    # Select the methods to be applied
    methods = []
    for meth in config['methods']:
        methods = methods + [m for m in bw.methods if str(m) == meth]
    print('\nThe LCIA methods to be evaluated are: ')
    for meth in methods:
        print(meth)

    # Define the product system
    level, pattern = get_level_pattern(activity, config['level'])
    prod_sys = [{act[0].key: 1} for act in level]

    # Define the exchange that should be altered
    new_activity = [act for act in eidb if str(act.key) == config['new activity']][0]

    # Define the list of activities that should be exchanged based on the reference product.
    replace = []
    i = 0
    for act in activity:
        replace.append([])
        for exc in act.exchanges():
            if any(exc['name'] == ref for ref in config['reference product']):
                replace[i].append(exc.input)
        replace[i].pop(0)  # Otherwise the production is set to zero !!!!!!!!!!
        i += 1

    ''' Check if BAU case has been calculated yet. If not, perform the calculations and save the results. '''
    if os.path.exists(os.getcwd() + '\data\BAU.xlsx') == False:
        print('\nIt seems there is no BAU data available ... Proceed with LCA caluclations \n')
        results = perform_multiLCA(prod_sys, methods)
        save_results(os.getcwd() + '\data\BAU.xlsx', results, methods, level, pattern)
        print('Done. \n')
    else:
        print('There is already a BAU case stored. \n')

    ''' Check if Altered case has been calculated yet. If not, perform the calculations and save the results. '''
    if os.path.exists(os.getcwd() + '\data\Altered.xlsx') == False:
        print('Proceed with calculating the altered case ...\n')
        # Setup the presample
        scenario_array = []
        scenario_indices = []
        i = 0
        for rep in replace:
            scenario_array = scenario_array + [0 for exc in rep] + [1]
            scenario_indices = scenario_indices + [(exc.key, activity[i].key, 'technosphere') for exc in rep]
            scenario_indices.append((new_activity.key, activity[i].key, 'technosphere'))
            i += 1
        scenario_array = np.array(scenario_array).reshape(-1, 1)
        scenario_matrix_data = [(scenario_array, scenario_indices, 'technosphere')]
        scen_pp_id, scen_pp_path = ps.create_presamples_package(matrix_data=scenario_matrix_data)

        # Perform mulit-LCA
        results = perform_multiLCA(prod_sys, methods, presample=[scen_pp_path])
        save_results(os.getcwd() + '\data\Altered.xlsx', results, methods, level, pattern)
        print('Done. \n')
    else:
        print('There is already an altered case stored. \n')

    # Loading the results, drop duplicates and sort by activity
    print('Loading the data for BAU and altered case ... \n')
    NEW_results = pd.read_excel(os.getcwd() + '\data\Altered.xlsx')
    NEW_results.drop_duplicates(subset='Activity', inplace=True)
    NEW_results.sort_values(by=['Activity'], ascending=False, inplace=True)


    BAU_results = pd.read_excel(os.getcwd() + '\data\BAU.xlsx')
    BAU_results.drop_duplicates(subset='Activity', inplace=True)
    BAU_results.sort_values(by=['Activity'], ascending=False, inplace=True)

    print('Done. \n')

    print('Proceed with creating the images ... \n')
    path = os.getcwd() + r'/Results/' + config['folder']
    folder = path + r'/image_'

    # Check whether the specified path exists or not
    isExist = os.path.exists(path)
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(path)
        print("The new directory is created!")

    for method in methods:
        create_bar_plots(BAU_results[str(method)], NEW_results[str(method)], NEW_results["Level_Pattern"], NEW_results["Pattern"], folder, str(method), config['n_top'])
