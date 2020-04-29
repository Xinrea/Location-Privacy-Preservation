# encoding=utf-8
import math
import os
import pickle
import random
import sqlite3 as sq
import pandas as pd
import numpy as np


def add_location(locations, frequences, location):
    try:
        location_num = len(locations)
        idx = locations.index(location)
        frequences[idx] += 1
        for i in range(idx + 1, location_num):
            if frequences[i] < frequences[i - 1]:
                frequences[i], frequences[i - 1] = frequences[i - 1], frequences[i]
                locations[i], locations[i - 1] = locations[i - 1], locations[i]
            else:
                break
    except ValueError:
        locations.insert(0, location)
        frequences.insert(0, 1)


def entropy(probabilities):
    ent = 0.0
    for probability in probabilities:
        ent -= math.log(probability, 2) * probability
    return ent


def frequences2probabilities(frequences):
    frequences_sum = sum(frequences)
    probabilities = [frequence / frequences_sum for frequence in frequences]
    return probabilities


def euclidean_distance(loc1, loc2):
    return math.sqrt((loc1[0] - loc2[0]) ** 2 + (loc1[1] - loc2[1]) ** 2)


def distance_product(candidate_location, anonymous_location):
    product = 1.0
    for location in anonymous_location:
        product *= euclidean_distance(candidate_location, location)
    return product


def random_choice(elements):
    rand = random.uniform(0, sum(elements))
    first_i_element_sum = 0
    for index, element in enumerate(elements):
        first_i_element_sum += element
        if first_i_element_sum >= rand:
            return index
    return 0


def rindex(iterable, value):
    try:
        return len(iterable) - next(i for i, val in enumerate(reversed(iterable)) if val == value) - 1
    except StopIteration:
        raise ValueError


def get_maxentropy_locationset(locations, frequences, cdt_num, offsets, crt_loc, M=5):
    """
    Get candidate locations according to query frequencies from all locations.
    :param locations: 1x# list, all locations in the map.
    :param frequences: 1x# list, frequences of locations in the map.
    :param cdt_num: int, maximum number of candidate locations.
    :param offsets: 2x2 list, [0][0]: longitudegrid_negative_offset, [0][1]: longitudegrid_positive_offset,
    [1][0]: latitudegrid_negative_offset, [1][1]: latitudegrid_positive_offset.
    :param crt_loc: 1x2 list, real location.
    :return maxentropy_locset: #x2 list, note that # of candidate locations <= cdt_num.
    """
    if offsets is not None:
        # if offsets is given,
        # candidate locations will only be chose from locations which are around the real location.
        region_border = (crt_loc[0] + offsets[0][0], crt_loc[0] + offsets[0][1],
                         crt_loc[1] + offsets[1][0], crt_loc[1] + offsets[1][1])
        all_locs = []
        all_frqs = []
        for location, frequency in zip(locations, frequences):
            if region_border[0] <= location[0] <= region_border[1] and \
                                    region_border[2] <= location[1] <= region_border[3]:
                all_locs.append(location)
                all_frqs.append(frequency)
    else:
        # if offsets is not given, all locations in the map could be cadidate locations.
        all_locs = locations
        all_frqs = frequences

    # Delete real location from all_locs if exists, since it should be chose as a candidate location.
    if crt_loc in all_locs:
        crt_loc_index = all_locs.index(crt_loc)
        crt_frq = all_frqs[crt_loc_index]
        crt_frq_rindex = rindex(all_frqs, crt_frq)
        crt_frq_cindex = int((all_frqs.index(crt_frq) + crt_frq_rindex) / 2)
        del (all_locs[crt_loc_index])
        del (all_frqs[crt_loc_index])
    # If the real location doesn't exist in all_locs, that is, it has never been visited,
    # regard the first location as real location.
    else:
        crt_frq = 1
        crt_frq_cindex = 0

    # Generate cdt_num locations as cdt_locs.
    cdt_halfnum = int(cdt_num.__truediv__(2))
    if len(all_locs) < cdt_num:
        # If # of all locations is less than candidate num, refuse to anonymize and returned None.
        return None
    else:
        # If # of candidate locations on the left side of current location is less than candidate halfnum,
        # choose the first cdt_num locations in all_locs as candidate locations.
        if crt_frq_cindex - 0 < cdt_halfnum:
            cdt_locs = all_locs[:cdt_num]
            cdt_frqs = all_frqs[:cdt_num]
        # If # of candidate locations on the right side of current location is less than candidate halfnum,
        # choose the last cdt_num locations in all_locs as candidate locations.
        elif len(all_locs) - crt_frq_cindex < cdt_halfnum:
            cdt_locs = all_locs[-cdt_num:]
            cdt_frqs = all_frqs[-cdt_num:]
        else:
            cdt_locs = all_locs[crt_frq_cindex - cdt_halfnum:crt_frq_cindex + cdt_halfnum]
            cdt_frqs = all_frqs[crt_frq_cindex - cdt_halfnum:crt_frq_cindex + cdt_halfnum]

    # Generate M sets containing cdt_halfnum locations, that is, real location and cdt_halfnum - 1 dummy locations.
    mlocation_sets = []
    mprobability_sets = []
    mentropy_set = []
    for i in range(0, M):
        # Generate M sets, each contains a real location placed to front and
        # candidate_halfnum - 1 dummy locations sampled from candidate_locations.
        random_indexes = random.sample(range(0, len(cdt_locs)), cdt_halfnum - 1)
        mlocation_set = [cdt_locs[j] for j in random_indexes]
        mlocation_set.insert(0, crt_loc)
        mfrequency_set = [cdt_frqs[j] for j in random_indexes]
        mfrequency_set.insert(0, crt_frq)

        mlocation_sets.append(mlocation_set)
        mprobability_sets.append(frequences2probabilities(mfrequency_set))
        mentropy_set.append(entropy(mprobability_sets[-1]))
    return mlocation_sets[mentropy_set.index(max(mentropy_set))]


def get_anonymous_location(locations, frequences, cdt_num, offsets, crt_loc, K):
    anonymous_loc = [crt_loc]
    loc_set = get_maxentropy_locationset(locations, frequences, cdt_num, offsets, crt_loc)
    if loc_set is None:
        return None
    for i in range(0, K - 1):
        distance_products = [distance_product(cdt_dummy_loc, anonymous_loc)
                             for cdt_dummy_loc in loc_set]
        index = random_choice(distance_products)
        dummy_loc = loc_set[index]
        anonymous_loc.append(dummy_loc)
        loc_set.remove(dummy_loc)
    assert len(anonymous_loc) == K
    return anonymous_loc


def generate_anonymous_checkin(rows):
    for checkinid, userid, locdatetime, anonymous_loc in rows:
        record = (checkinid, userid, locdatetime)
        if anonymous_loc is None:
            for i in range(0, K):
                record += (FLAG_FAIL2ANONYMIZE, FLAG_FAIL2ANONYMIZE)
        else:
            for loc in anonymous_loc:
                for coordinate in loc:
                    record += (coordinate,)
        yield record


def save_anonymous_checkins(table_name, anonymous_checkins):
    """
    Create a table to store anonymous checkins.
    :param table_name: str, name of table storing anonymous checkins.
    :param anonymous_checkins: row_num x (2K + 3) list.
    """
    # Create a table after dropping the old one.
    sql_drop_table = ''.join(['DROP TABLE ', 'IF EXISTS ', table_name])
    cursor.execute(sql_drop_table)
    sql_create = ''.join(['CREATE TABLE ', table_name, ' (id INTEGER, userid INTEGER, locdatetime DATETIME,',
                          ''.join([''.join([' lon', str(i), ' INTEGER, lat', str(i), ' INTEGER,'
                                            ]) for i in range(0, K - 1)]),
                          ' lon', str(K - 1), ' INTEGER, lat', str(K - 1), ' INTEGER)'])
    cursor.execute(sql_create)

    # Insert all anonymous checkins into the table.
    sql_insert = ''.join(['INSERT INTO ', table_name, ' VALUES(', '?, ' * (2 * K + 2), '?)'])
    cursor.executemany(sql_insert, generate_anonymous_checkin(anonymous_checkins))


def dls(enhanced, real_locs_table_name):
    """
    Main algorithm for the locations k-anonymization method 'DLS'.
    Refer to:   Niu, B., et al. Achieving k-anonymity in privacy-aware location-based services.
                in IEEE INFOCOM 2014 - IEEE Conference on Computer Communications. 2014.
    :param enhanced: bool, True represents Enhanced-DLS, False represents normal DLS.
    :param real_locs_table_name: name of the table storing real locations which need to k-anonymize.
    :return: None.
    """
    print('dls')
    # Get all checkins orderred by datetime.
    cursor.execute(''.join(['SELECT id, userid, locdatetime, gridlon, gridlat FROM ', real_locs_table_name,
                            ' ORDER BY locdatetime']))  # , ' WHERE userid = 1481'
    results = cursor.fetchall()
    checkin_num = len(results)
    locations = []
    frequences = []

    # Generate anonymous locations for each real location according to DLS.
    anonymous_checkins = []
    checkin_cnt = 0
    offsets = None
    # offsets = [[-10, 10], [-10, 10]]
    if enhanced:
        cdt_num = 4 * K
        anon_locs_table_name = ''.join([real_locs_table_name, '_EnhancedDLS_K', str(K), '_M', str(M)])
        for checkinid, userid, locdatetime, lon, lat in results:
            checkin_cnt += 1
            print('EnhancedDLS %5.2f%% work complete.' % (checkin_cnt / checkin_num * 100))
            location = (lon, lat)
            anonymous_loc = get_anonymous_location(locations, frequences, cdt_num, offsets, location, K)
            anonymous_checkins.append((checkinid, userid, locdatetime, anonymous_loc))
            add_location(locations, frequences, location)
    else:
        cdt_num = 2 * K
        anon_locs_table_name = ''.join([real_locs_table_name, '_DLS_K', str(K), '_M', str(M)])
        for checkinid, userid, locdatetime, lon, lat in results:
            checkin_cnt += 1
            print('DLS %5.2f%% work complete.' % (checkin_cnt / checkin_num * 100))
            location = (lon, lat)
            anonymous_loc = get_maxentropy_locationset(locations, frequences, cdt_num, offsets, location)
            anonymous_checkins.append((checkinid, userid, locdatetime, anonymous_loc))
            add_location(locations, frequences, location)

    # Save anonymous checkins to disk.
    with open(anon_locs_table_name + '.dat', 'wb') as filehandle:
        pickle.dump(anonymous_checkins, filehandle)

    # Save anonymous checkins to database.
    save_anonymous_checkins(anon_locs_table_name, anonymous_checkins)
    # Do NOT update one record each time, otherwise the updates will be slower and slower.

    print('TABLE', anon_locs_table_name, ' is created.')

def dls_pure(dfc:pd.DataFrame,K):
    """
    Main algorithm for the locations k-anonymization method 'DLS'.
    Refer to:   Niu, B., et al. Achieving k-anonymity in privacy-aware location-based services.
                in IEEE INFOCOM 2014 - IEEE Conference on Computer Communications. 2014.
    :param real_locs_table_name: name of the table storing real locations which need to k-anonymize.
    :return: None.
    """

    results = dfc
    checkin_num = len(results)
    locations = []
    frequences = []

    # Generate anonymous locations for each real location according to DLS.
    anonymous_checkins = []
    checkin_cnt = 0
    offsets = None
    # offsets = [[-10, 10], [-10, 10]]
    cdt_num = 4 * K
    for index,row in results.iterrows():
        userid = row['uid']
        locdatetime = row['utc']
        lon = row['lon']
        lat = row['lat']
        lid = row['lid']
        checkin_cnt += 1
        location = (lon, lat)
        anonymous_loc = get_anonymous_location(locations, frequences, cdt_num, offsets, location,K)
        if (anonymous_loc is not None):
            i = random.randint(0,len(anonymous_loc)-1)
            p = anonymous_loc[i]
            newloc = [userid, locdatetime, p[0], p[1],lid]
            anonymous_checkins.append(newloc)
        add_location(locations, frequences, location)
    ndfc = pd.DataFrame(anonymous_checkins, columns=['uid','utc','lat','lon','lid'])
    return ndfc

    

if __name__ == '__main__':
    from dataset import GowallaAustin as Dataset
    K = M = 5
    FLAG_FAIL2ANONYMIZE = -1  # As a symbol representing the actual location which cannot be anonymized.

    # Set current directory. Note that the database file checkins.db should be placed under current directory.
    os.chdir('D:\\Workspace\\Datasets\\Location-Based Social Network\\SNAP Gowalla')

    # Connect to sqlite database.
    conn = sq.connect(Dataset.url[10:])
    cursor = conn.cursor()

    dls(True, Dataset.checkins.name)

    # Commit changes to the database, and close connection.
    conn.commit()
    conn.close()
