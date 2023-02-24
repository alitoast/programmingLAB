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
            self.data = [] #so I reset the data every time I call get_data
            prev_month = 0
            prev_year = 0
            for line in lines[1:]:
                #split dates and passengers number
                if len(line.strip().split(',')) >= 2:
                    date_stringing = line.strip().split(',')[0]
                    passengers_string = line.strip().split(',')[1]
                    if len(date_stringing.split('-')) == 2:
                        #try for inconsistencies in the values
                        try: 
                            passengers = int(passengers_string)
                            year = int(date_stringing.split('-')[0])
                            month = int(date_stringing.split('-')[1])
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

                        self.data.append([date_stringing, passengers])       

        return self.data

time_series_file=CSVTimeSeriesFile(name='data.csv')

def detect_similar_monthly_variation(time_series, years):
    year_1 = [None] * 12
    year_2 = [None] * 12
    threshold = 2

    for date_string, passengers in time_series:
        year, month = map(int, date_string.split("-"))
        if year == years[0]:
            year_1[month - 1] = passengers
        elif year == years[1]:
            year_2[month - 1] = passengers

    # check that both years have data
    if year_1 == [None]*12 or year_2 == [None]*12:
        raise ExamException('Error, year/s not found in timeseries')

    #calculate the differences between a pair of consecutive months of the same year
    year_1_diffs = []
    year_2_diffs = []
    for n in range(1, 12):
        if year_1[n] is not None and year_1[n-1] is not None:
            year_1_diffs.append(year_1[n] - year_1[n-1])
        if year_2[n] is not None and year_2[n-1] is not None:
            year_2_diffs.append(year_2[n] - year_2[n-1])

    #check for similar monthly variations based on the threshold
    variation = []
    for m in range(11):
        if year_1_diffs[m] is not None and year_2_diffs[m] is not None:
            if abs(year_1_diffs[m] - year_2_diffs[m]) <= threshold:
                variation.append(True)
            else:
                variation.append(False)
        else:
            variation.append(False)
    
    return variation

print(detect_similar_monthly_variation(time_series_file.get_data(), [1949,1950]))
