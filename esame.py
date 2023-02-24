class ExamException(Exception): 
    pass

class CSVTimeSeriesFile: 
    def __init__(self, name):
        self.name = name
        self.data = []

    def get_data(self):  
        #read and parse the given file
        with open(self.name, 'r') as csv_file:
            lines = csv_file.readlines() #rea all as strings
            self.data = [] #so I reset the timeseries every time I call get_data
            prev_month = 0
            prev_year = 0
            for line in lines[1:]:
                #split dates and number of passengers
                if len(line.strip().split(',')) >= 2:
                    date_string = line.strip().split(',')[0]
                    passengers_string = line.strip().split(',')[1]
                    if len(date_string.split('-')) == 2:
                        #try for inconsistencies in the values
                        try: 
                            passengers = int(passengers_string)
                            year = int(date_string.split('-')[0])
                            month = int(date_string.split('-')[1])
                        except ValueError:
                            continue
                        #in the same cicle check for order or duplicates
                        if year < prev_year:
                            raise ExamException('Error, timeseries disarranged')
                        elif year == prev_year:
                            if month < prev_month:
                                raise ExamException('Error, timeseries disarranged')
                            elif month == prev_month:
                                raise ExamException('Error, timeseries with duplicates')
                        prev_month = month
                        prev_year = year

                        self.data.append([date_string, passengers])       

        return self.data

time_series_file=CSVTimeSeriesFile(name='data.csv')

def detect_similar_monthly_variations(time_series, years):
    #initialized two lists with 12 empty spaces to be filled with passengers number 
    year_1 = [None] * 12
    year_2 = [None] * 12
    treshold = 2

    for date_string, passengers in time_series:
        year, month = map(int, date_string.split("-"))
        if year == years[0]:
            year_1[month - 1] = passengers
        elif year == years[1]:
            year_2[month - 1] = passengers
        
    if year_1 == [None]*12 or year_2 == [None]*12:
        raise ExamException('Error, year/s not found in timeseries')

    #initialized a list to be filled with the difference between month and month+1
    variation = []

    for month in range(1, 13):
        if year_1[month - 1] is not None and year_2[month - 1] is not None:
            difference = year_2[month - 1] - year_1[month - 1]
            if difference > treshold or difference < -treshold:
                variation.append(False)
            else:
                variation.append(True)
        else:
            variation.append(False)

    return variation

print(detect_similar_monthly_variations(time_series_file.get_data(), [1949,1950]))

