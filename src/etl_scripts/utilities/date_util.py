from datetime import datetime, timedelta


class DateUtil:
    @staticmethod
    def generate_past_30_days(input_date: datetime, days: int):
        """
        Logic to generate past 30 dates gives the start value

        :param input_date: the date in ISO date format
        :param days: total number of days to generate
        :return: list of past 30 dates
        """
        dates_list = [input_date.strftime("%Y-%m-%d")]
        for i in range(1, days):
            # create timedelta
            day_delta = timedelta(days=i)
            # subtract the timedelta with 1 day
            prev_date = input_date - day_delta
            dates_list.append(prev_date.strftime("%Y-%m-%d"))
        print(dates_list)
        return dates_list
