from datetime import datetime, timezone

DEFAULT_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


def validate_dateformat(date, format=DEFAULT_DATETIME_FORMAT):
    try:
        datetime.strptime(date, format)
        return True 
    except ValueError:
        return False  


def str_to_datetime(date_str, format=DEFAULT_DATETIME_FORMAT):
    '''
    change str date to datetime using format parameter  
    '''
    return(datetime.strptime(date_str, format))


def datetime_to_str(datetime_obj, format=DEFAULT_DATETIME_FORMAT):
    '''
    change datetime to str date using format parameter  
    '''
    return(datetime.strftime(datetime_obj, format))


def datetime_to_utctimestamp(datetime_obj):
    '''
    convert datetime (utc) to timestamp (utc)  
    ''' 

    return(datetime_obj.replace(tzinfo=timezone.utc).timestamp())


def utctimestamp_to_datetime(timestamp):
    '''
    convert timestamp (utc) to datetime (utc) 

    ''' 
    return(datetime.fromtimestamp(timestamp, timezone.utc))


