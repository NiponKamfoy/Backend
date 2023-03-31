import calendar,json
from datetime import date, timedelta, datetime
from dateutil import relativedelta
from app.config import Config
# import 
def get_array_day(dates):
    # Tue Jan 10 2006 00:00:00 GMT+0700,Wed Feb 15 2006 00:00:00 GMT+0700 
    temp_date = dates.split(' ')
    day_list = []

    if(len(temp_date) == 1):
        time = datetime.strptime(dates, '%Y')
        temp = day_list.append(time.strftime(str_date))
        return day_list
    else:
        month = {month: index for index, month in enumerate(calendar.month_abbr) if month}
        sdate = date(int(temp_date[3]), month[temp_date[2]], int(temp_date[1]))   # start date
        edate = date(int(temp_date[8]), month[temp_date[7]], int(temp_date[6]))   # end date

        delta = edate - sdate       # as timedelta
        for i in range(delta.days + 1):
            day = sdate + timedelta(days=i)
            day_list.append(day.strftime(str_date))
            temp = list(set(day_list))
        return temp

def get_data_histrogram(all_grid_data):
    histrogram_data = {}
    for grid in all_grid_data:
        index = round(grid['properties']['index'])
        if (str(index) not in histrogram_data.keys()):
            histrogram_data[str(index)] = 1
        else :
            histrogram_data[str(index)] += 1
    myKeysStr = list(histrogram_data.keys())
    myKeys = [int(i) for i in myKeysStr]
    myKeys.sort()
    sorted_dict = [{"value": i, "frequency": histrogram_data[str(i)]} for i in myKeys]
    return sorted_dict

def get_data_histrogram1(all_grid_data):
    list_index_value = []
    for grid in all_grid_data:
        index = round(grid['properties']['index'])
        list_index_value.append(index)
    return list_index_value


from os import path

basepath = path.dirname(__file__)
def convert_nc_json(province, date, index, index_folder):
    global str_date

    str_date = '%Y'
# D:\Coding\JavaScript\REACT_Native\Data_Project\Data_Project\
# E:\Data_Project\ensemble
#"C:\Users\s6201\Downloads\Data_Project\data_project\ensemble"
    dir_data = Config()
    index_name = index.split('_')[0]
    if( index_folder == '_SPI'):
        index_name = index.split('_')[0][:-2]
    
    dir_load_data = f"{dir_data['data_index_path']}/{index_name}"
    load_data = open(rf'{dir_load_data}\{index_folder}/{index}/{province}.json')
    data_province = json.load(load_data)
    # load_data = path.abspath(path.join(basepath, "..", "data", index_name, index_folder, index, province+'.json'))
    # f = open(load_data, "r")
    # data_province = json.load(f)

    time_unit = data_province['properties']['date_type']
    # it used to check string date format
    if (time_unit == 'year'):
        str_date = '%Y'
    else:
        str_date = '%Y-%m'

    day_list = get_array_day(date)

    temp_data = data_province['fetures']
       
    temp_time_series = {}
    for ind,grid_data in enumerate(data_province['fetures']):
        value = 0
        for day in day_list:
            if (day not in temp_time_series.keys()):
                temp_time_series[day] = []
            if(time_unit == "year"):
                str_index_time = str(int(day)-int(data_province['properties']['start_time']))
                if (grid_data['properties']['time_index'][str_index_time] != '--'):
                    value += float(grid_data['properties']['time_index'][str_index_time])
                    temp_time_series[day].append(float(grid_data['properties']['time_index'][str_index_time]))
            else :
                date_input = datetime.strptime(day, "%Y-%m")
                date_start = datetime.strptime(data_province['properties']['start_time'], "%Y-%m")
                r = relativedelta.relativedelta(date_input, date_start)
                index_month = r.months + (12*r.years)
                
                if (grid_data['properties']['time_index'][str(index_month)] != '--'):
                    value += float(grid_data['properties']['time_index'][str(index_month)])
                    temp_time_series[day].append(float(grid_data['properties']['time_index'][str(index_month)]))

        value /= len(day_list)
        temp_data[ind]['properties']['index'] = value

        # delete time_index when send data from api 
        temp_data[ind]['properties']['time_index'] = False

    time_series_data = []
    for date in temp_time_series.keys():
        time_series_data.append({"date": date, 'index': sum(temp_time_series[date])/len(temp_time_series[date])})
    index_center = len(data_province['fetures'])//2
    temp_data[index_center]['properties']['time_index'] = True
    temp_data[index_center]['properties']['time_series'] = sorted(time_series_data, key=lambda i: i['date'])

    if( index_folder == '_SPI'):
        seasonal_data_tmp = {}
        for data in time_series_data:
            month = data['date'].split("-")[1]
            if ( month not in seasonal_data_tmp.keys()):
                seasonal_data_tmp[month] = [data['index']]
            else :
                seasonal_data_tmp[month].append(data['index'])

        seasonal_data = []
        tmp_dict = {}
        for i in seasonal_data_tmp.keys():
            tmp_dict['month'] = i
            tmp_dict['value'] = sum(seasonal_data_tmp[i]) / len(seasonal_data_tmp[i])
            seasonal_data.append(tmp_dict)
            tmp_dict = {}
        temp_data[index_center]['properties']['seasonal'] = sorted(seasonal_data, key=lambda i: i['month'])
    # temp_data.append(time_series_data)
    test = temp_data[index_center]['properties']['time_series']
    histrogram_data = get_data_histrogram(temp_data)
    temp_data[index_center]['properties']['histrogram'] = histrogram_data

    return temp_data


