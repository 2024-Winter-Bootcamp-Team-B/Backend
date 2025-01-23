from datetime import datetime, timedelta
from typing import List

from app.models import History


class HistoryStat:

    def __init__(self, date: str, goal: str, actual: str):
        self.date = date
        self.goal = goal # 문자열로 된 목표 시간 (예: "2:30").
        self.actual = actual # 문자열로 된 실제 시간 (예: "2:15").


    def setting_date(self, date : datetime):
        """
        날짜 설정하기 예) 2024-01-15
        """
        self.date = date.strftime("%Y-%m-%d")

    def add_time(self, start_time : datetime, goal_time: datetime, end_time: datetime):
        """
        같은 날의 시간은 누적해서 더하기 
        """
        start_min = start_time.minute
        start_hour = start_time.hour

        goal_min = goal_time.minute
        goal_hour = goal_time.hour

        end_min = end_time.minute
        end_hour = end_time.hour


        g_time = list(map(int, self.goal.split(":")))  # 문자열 -> 정수 리스트
        a_time = list(map(int, self.actual.split(":")))  # 문자열 -> 정수 리스트

        # 목표 시간 계산
        total_goal_minutes = (goal_hour - start_hour) * 60 + (goal_min - start_min) + (g_time[0] * 60 + g_time[1])
        goal_hours, goal_minutes = divmod(total_goal_minutes, 60)  # 분을 시간과 분으로 변환
        self.goal = f"{goal_hours}:{goal_minutes:02}"  # 두 자리 형식 유지

        # 실제 시간 계산
        total_actual_minutes = (end_hour - start_hour) * 60 + (end_min - start_min) + (a_time[0] * 60 + a_time[1])
        actual_hours, actual_minutes = divmod(total_actual_minutes, 60)  # 분을 시간과 분으로 변환
        self.actual = f"{actual_hours}:{actual_minutes:02}"  # 두 자리 형식 유지


def get_stat_result(list : List[History], today : datetime):
    """
    History 리스트를 받고 7일 간의 데이터를 정리해주는 거
    """
    result_stat = []
    for i in range(6,-1,-1):
        stat = HistoryStat(date="", goal="0:0", actual="0:0")
        stat.setting_date(today - timedelta(days=i))
        result_stat.append(stat)
    
    for history in list :
        history_date = history.start_time.strftime("%Y-%m-%d")
        if result_stat[0].date == history_date :
            result_stat[0].add_time(
                start_time = history.start_time,
                goal_time = history.goal_time,
                end_time = history.end_time
                )
            
        elif result_stat[1].date == history_date :
            result_stat[1].add_time(
                start_time = history.start_time,
                goal_time = history.goal_time,
                end_time = history.end_time
                )
            
        elif result_stat[2].date == history_date :
            result_stat[2].add_time(
                start_time = history.start_time,
                goal_time = history.goal_time,
                end_time = history.end_time
                )
            
        elif result_stat[3].date == history_date :
            result_stat[3].add_time(
                start_time = history.start_time,
                goal_time = history.goal_time,
                end_time = history.end_time
                )
            
        elif result_stat[4].date == history_date :
            result_stat[4].add_time(
                start_time = history.start_time,
                goal_time = history.goal_time,
                end_time = history.end_time
                )
            
        elif result_stat[5].date == history_date :
            result_stat[5].add_time(
                start_time = history.start_time,
                goal_time = history.goal_time,
                end_time = history.end_time
                )
            
        elif result_stat[6].date == history_date :
            result_stat[6].add_time(
                start_time = history.start_time,
                goal_time = history.goal_time,
                end_time = history.end_time
                )
            
    for stat in result_stat:
        print(f"Date: {stat.date}, Goal: {stat.goal}, Actual: {stat.actual}")

    return result_stat