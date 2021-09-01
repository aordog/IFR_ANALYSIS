import numpy as np

def read_master_station_list(file):
    f = open(file)
    numline = 0
    for line in f:
        numline = numline+1

    all_stn = []
    all_lon = np.empty(numline-20)
    all_lat = np.empty(numline-20)

    f = open(file)
    for i in range(0,numline-1):
        line = f.readline()
        if i >18:
            all_stn.append(str(line.split()[0]))
            all_lon[i-19] = np.float(line.split()[-7])+np.float(line.split()[-6])/60.+np.float(line.split()[-5])/3600.
            all_lat[i-19] = np.float(line.split()[-4])+np.float(line.split()[-3])/60.+np.float(line.split()[-2])/3600.
    all_stn = np.asarray(all_stn)
    all_lon[all_lon>180.] = all_lon[all_lon>180.]-360.
    return all_stn, all_lon, all_lat


def read_stations_used(file,all_stn,all_lon,all_lat):
    good_stn = []

    f = open(file)
    numline = 0
    for line in f:
        numline = numline+1
        #print(numline)
    f = open(file)
    for i in range(0,numline):
        line = f.readline(6).split()[0]
        good_stn.append(line)

    good_stn = np.asarray(good_stn)    
    good_lon = np.empty(len(good_stn))
    good_lat = np.empty(len(good_stn))

    for i in range(0,len(good_stn)):
        w = np.where(all_stn == good_stn[i])
        good_lon[i] = all_lon[w[0][0]]
        good_lat[i] = all_lat[w[0][0]]
    
    return good_stn, good_lon, good_lat


def read_stations_failed(file,good_stn,all_stn,all_lon,all_lat,excl_stn):
    f = open(file)
    numline = 0
    for line in f:
        numline = numline+1

    ptl_stn = []
    f = open(file)
    for i in range(0,numline):
        line = f.readline().split()[3]
        ptl_stn.append(line)

    ptl_stn = np.asarray(ptl_stn)

    bad_stn = []
    for i in range(0,numline):
        w = np.where(good_stn == ptl_stn[i])
        wex = np.where(excl_stn == ptl_stn[i])
        if ((len(w[0]) == 0) & (len(wex[0])<1)):
            bad_stn.append(ptl_stn[i])

    bad_stn = np.asarray(bad_stn)
        
    #print(len(bad_stn))
    #print(bad_stn)

    bad_lon = np.empty(len(bad_stn))
    bad_lat = np.empty(len(bad_stn))
    for i in range(0,len(bad_stn)):
        w = np.where(all_stn == bad_stn[i])
        #print(len(w[0]))
        #print(w[0])
        if len(w[0]) > 0: 
            bad_lon[i] = all_lon[w[0][0]]
            bad_lat[i] = all_lat[w[0][0]]
        
    return bad_stn, bad_lon, bad_lat


def read_stations_excluded_from_master(file):
    f = open(file)
    numline = 0
    for line in f:
        numline = numline+1

    excl_stn = []
    excl_lon = np.empty(numline-1)
    excl_lat = np.empty(numline-1)

    f = open(file)
    for i in range(0,numline):
        line = f.readline()
        if i >0:
            excl_stn.append(str(line.split()[0]))
            excl_lon[i-1] = np.float(line.split()[-7])+np.float(line.split()[-6])/60.+np.float(line.split()[-5])/3600.
            excl_lat[i-1] = np.float(line.split()[-4])+np.float(line.split()[-3])/60.+np.float(line.split()[-2])/3600.
    excl_stn = np.asarray(excl_stn)
    excl_lon[excl_lon>180.] = excl_lon[excl_lon>180.]-360.
        
    return excl_stn, excl_lon, excl_lat


def read_in_fitted_models(file,UTCdiff):
    
    f = open(file)
    numline = 0
    for line in f:
        numline = numline+1
    print(numline)

    f = open(file, 'r')
    for i in range(0,26):
        line = f.readline()
        if i == 6:
            reftime = line.split()
    print(repr(line))
    print(repr(reftime))

    tstart = float(reftime[8])+float(reftime[9])/60.+float(reftime[10])/3600.
    print('')

    t = np.empty([numline-27])
    TEC = np.empty([numline-27])
    STEC = np.empty([numline-27])
    RM = np.empty([numline-27])
    t_hrs = np.empty([numline-27])

    for i in range(27,numline):
        line = f.readline()
        t[i-27] = line.split()[3]
        STEC[i-27] = float(line.split()[7])
        TEC[i-27] = float(line.split()[7])*float(line.split()[9])
        RM[i-27] = float(line.split()[8])
        t_hrs[i-27] = tstart+t[i-27]/3600.-UTCdiff
        
    return TEC, STEC, RM, t_hrs


def read_in_fitted_models_UTC(file):
    
    f = open(file)
    numline = 0
    for line in f:
        numline = numline+1
    print(numline)

    f = open(file, 'r')
    for i in range(0,26):
        line = f.readline()
        if i == 6:
            reftime = line.split()
    print(repr(line))
    print(repr(reftime))

    tstart = float(reftime[8])+float(reftime[9])/60.+float(reftime[10])/3600.
    print('')

    t = np.empty([numline-27])
    TEC = np.empty([numline-27])
    STEC = np.empty([numline-27])
    RM = np.empty([numline-27])
    t_hrs = np.empty([numline-27])

    for i in range(27,numline):
        line = f.readline()
        t[i-27] = line.split()[3]
        STEC[i-27] = float(line.split()[7])
        TEC[i-27] = float(line.split()[7])*float(line.split()[9])
        RM[i-27] = float(line.split()[8])
        t_hrs[i-27] = tstart+t[i-27]/3600.
        
    return TEC, STEC, RM, t_hrs


def read_in_fitted_models_CHIME(file,UTCdiff):
    
    f = open(file)
    numline = 0
    for line in f:
        numline = numline+1
    #print(numline)

    f = open(file, 'r')
    for i in range(0,28):
        line = f.readline()
        if i == 6:
            reftime = line.split()
    #print(repr(line))
    #print(repr(reftime))

    tstart = float(reftime[8])+float(reftime[9])/60.+float(reftime[10])/3600.
    #print('')

    t = np.empty([numline-29])
    el = np.empty([numline-29])
    az = np.empty([numline-29])
    TEC = np.empty([numline-29])
    STEC = np.empty([numline-29])
    RM = np.empty([numline-29])
    t_hrs = np.empty([numline-29])
    dSTEC = np.empty([numline-29])

    for i in range(29,numline):
        line = f.readline()
        #print(i,len(line))
        if len(line) > 5 :  # this could probably be anything greater than 2. Just looking for not blank line
            #print(i,line.split()[0])
            el[i-29] = line.split()[5]
            az[i-29] = line.split()[6]
            t[i-29] = line.split()[3]
            STEC[i-29] = float(line.split()[7])
            TEC[i-29] = float(line.split()[7])*float(line.split()[9])
            dSTEC[i-29] = float(line.split()[10])
            RM[i-29] = float(line.split()[8])
            t_hrs[i-29] = tstart+t[i-29]/3600.-UTCdiff
        
    return TEC, STEC, dSTEC, RM, t_hrs, el, az