import datetime
import time 
import sys


## DATE/TIME OPERATIONS
##--------------------------------------------------------------------------------------------------------------
def date_cleaner(dt_object):
    
   
    # if isinstance(dt_object,unicode):
    #     dt_object = dt_object.encode("utf-8")
    #     #print(dt_object)
    # else:
    #     pass

    # gets date into Y-m-d string format 
    date_string = dt_object
    if type(dt_object) == None:
        pass

    elif type(dt_object) == str:
        if "-" in dt_object:
            dt_object = dt_object[:10]
            if len(dt_object.split("-")[2] ) >= 4:
                dt_parts = dt_object.split("-")
                dt_parts[0].zfill(2)
                dt_parts[1].zfill(2)
                dt_parts[2] = dt_parts[2][:4]
                date_string = "-".join([dt_parts[2],dt_parts[0],dt_parts[1]])

          
            elif len(dt_object.split("-")[0] ) >= 4:
                dt_parts = dt_object.split("-")
                dt_parts[0] = dt_parts[0][:4]
                date_string = "-".join(dt_parts)
            
            else:
                date_string = dt_object


        elif "/" in dt_object:
            dt_parts = dt_object.split('/')
            dt_parts[0] = dt_parts[0].zfill(2) #m
            dt_parts[1] = dt_parts[1].zfill(2) #d

            if len(dt_parts[0] ) == 4:
                date_string='-'.join(dt_parts)

            else:

                if len( dt_parts[2] ) == 2:
                    dt_parts[2] = '20' + dt_parts[2].zfill(2) # Y
                
                elif len( dt_parts[2] ) == 4:
                    pass
                
                elif len( dt_parts[2] ) > 4:
                    dt_parts[2] = dt_parts[2].split(' ')[0]
                    if len( dt_parts[2] ) == 2:
                        dt_parts[2] = '20' + dt_parts[2].zfill(2) # Y
                    elif len( dt_parts[2] ) == 4:
                        pass
                
                else:
                    print('getting malformed Year dates')
                    sys.exit(0)

                re_ordered = [  dt_parts[2], dt_parts[0] , dt_parts[1] ]
                date_string = '-'.join(re_ordered)
                date_string = date_string[:10]

           
        else:
            pass
    
    elif type(dt_object) == datetime:
        date_string = dt_object.strftime('%Y-%m-%d')

    
    else:
        try:
            date_string = dt_object.to_pydatetime()
            date_string = date_string.strftime('%Y-%m-%d')
        except:
            print('encountered unkown data type in the date field: {0}, dtype={1}'.format(dt_object,type(dt_object)) )
            #sys.exit()
    return date_string
##--------------------------------------------------------------------------------------------------------------

def make_ts_string(datestring):
    # add in time stamp format - datetime.datetime.strftime(now,'%Y%d%X')
    # excpects date string
    date = datetime.datetime.strptime(datestring,'%Y-%m-%d')
    date = datetime.datetime.strftime(date,'%Y-%m-%d %X')
    return date


##--------------------------------------------------------------------------------------------------------------
def get_date_formatted(dt_object, day_selection, format):
    #returns string
    assert format in [ 'str', 'dt']

    # needs date in Y-m-d format
    value = None

    # DATE.WEEKDAY() - Mon =0, Sun =6
    weekday ={
        'm':0,
        't':1,
        'w':2,
        'th':3,
        'f':4,
        'sat':5,
        'sun':6
    }

    try:
        if type(dt_object)==str:
            date = datetime.datetime.strptime(dt_object,'%Y-%m-%d')

            # if date is after cutoff, no issue,  proceed as normal and truncate to the right day
            if date.weekday() >= weekday[day_selection]:
                value = date - datetime.timedelta(days = date.weekday() ) + datetime.timedelta(days = weekday[day_selection]) 
            else: # if date is before the cutoff day, need to go back a full week
                value = date - datetime.timedelta(days = date.weekday() ) + datetime.timedelta(days = weekday[day_selection] - 7 ) #go back a full week 
            
            if format == 'str':
                value = value.strftime('%Y-%m-%d')
            else:
                pass

        elif type(dt_object)==datetime:
            if date.weekday() >= weekday[day_selection]:
                value = dt_object - datetime.timedelta(days = dt_object.weekday()) + datetime.timedelta(days = weekday[day_selection]) 
            else:
                value = dt_object - datetime.timedelta(days = dt_object.weekday()) + datetime.timedelta(days = weekday[day_selection] - 7) 
            
            if format == 'dt':
                value = value.strftime('%Y-%m-%d')


        else:
            pass

    except ValueError:
        print('\nChck the format of your date inputs, code expected \'%Y-%m-%d\', but received \'{0}\''.format(dt_object))
        #sys.exit()

    return value
##--------------------------------------------------------------------------------------------------------------
def get_week_of (object_):
    return get_date_formatted(object_, day_selection = 'm' , format = 'str')



##--------------------------------------------------------------------------------------------------------------

def fix_excel_ts_year(timestamp):
    groups = timestamp.split('/')
    groups[2] = '20' + groups[2]
    corrected_ts = '/'.join(groups)
    return corrected_ts




##--------------------------------------------------------------------------------------------------------------
def split_timespan( datestring, cutoff_dt ):
    #expects date strings, can design to have it handle timestamp and datetime objects
    # Y-m-d
    # can turn this into a callable function to take the DF itseld and spit out a new df with cutoff date column filled in and classification
    
    needs_classification = datetime.datetime.strptime( datestring, '%Y-%m-%d')
    benchmark           = datetime.datetime.strptime( cutoff_dt, '%Y-%m-%d')

    if needs_classification < benchmark:
        value = 'Before'
    elif needs_classification >= benchmark:
        value = 'After'

    return value



##--------------------------------------------------------------------------------------------------------------
 # use format = 'dt'
def strfdelta(tdelta, fmt):
    d = {"days": tdelta.days}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    return fmt.format(**d)
