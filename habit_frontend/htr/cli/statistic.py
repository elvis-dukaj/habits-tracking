# from typing import Optional
#
# import pandas
# from tabulate import tabulate
# import click
# import plotext as plot
#
# from htr.cli.cli import cli
# from htr.client.habit_tracker import HabitTrackerClient
# from htr.schemas.habit import Habit
# from htr.schemas.habit_event import HabitEvent
#
# from htr.analytics import transform_to_panda_dataframe, get_habit_events_statistic, tabulate_dataframe
#
#
# @cli.group()
# @click.option("--user-id", type=click.INT, envvar="HABIT_TRACKER_USER_ID", help="filter by habit id")
# @click.pass_obj
# def statistic(habit_tracker_client: HabitTrackerClient, user_id: int):
#     habit_tracker_client.set_current_user_id(user_id)
#
#
# def calculate_all_streaks(habits: list[tuple[Habit, list[HabitEvent]]]) -> list[int]:
#     dataframes: list[pandas.DataFrame] = []
#
#     for habit, events in habits:
#         dataframes.append(transform_to_panda_dataframe(events, habit.periodicity))
#
#     streaks: list[int] = [0 if len(df.index) == 0 else df.iloc[-1]['streak'] for df in dataframes]
#     return streaks
#
#
# @statistic.command()
# @click.option("--habit-id", "habit_id", required=True, type=click.INT, help="filter by habit id")
# @click.pass_obj
# def statistic(habit_tracker_client: HabitTrackerClient, habit_id: Optional[int], show_history: Optional[bool],
#               show_statistic: Optional[bool]):
#     pass
#
#
# @streak.command()
# @click.option("--with-habit-id", "habit_id", is_flag=False, type=click.INT, help="filter by habit id")
# @click.pass_obj
# def history(habit_tracker_client: HabitTrackerClient, habit_id: Optional[int], show_history: Optional[bool],
#             show_statistic: Optional[bool]):
#
#
# @streak.command()
# @click.option("--with-habit-id", "habit_id", is_flag=False, type=click.INT, help="filter by habit id")
# @click.option("--show-history", is_flag=True, default=True, help="filter by habit id")
# @click.option("--show-statistic", is_flag=True, default=True, help="filter by habit id")
# @click.pass_obj
# def display(habit_tracker_client: HabitTrackerClient, habit_id: Optional[int], show_history: Optional[bool],
#             show_statistic: Optional[bool]):
#     if habit_id is not None:
#         habit = habit_tracker_client.get_habit_by_id(habit_id)
#         events: list[HabitEvent] = habit_tracker_client.list_habit_events(habit.habit_id)
#         dataframe = transform_to_panda_dataframe(events, habit.periodicity)
#
#         if len(dataframe.index) == 0:
#             click.echo("No data registered")
#             return
#
#         if show_history:
#             click.echo("Streak History:")
#             click.echo(tabulate_dataframe(dataframe))
#
#         if show_statistic:
#             click.echo("Streak Statistics:")
#             click.echo(tabulate_dataframe(get_habit_events_statistic(dataframe)))
#         return
#
#     combined_habit_and_events: list[tuple[Habit, list[HabitEvent]]] = []
#
#     habits = habit_tracker_client.list_habits()
#     for habit in habits:
#         events = habit_tracker_client.list_habit_events(habit.habit_id)
#         combined = (habit, events)
#         combined_habit_and_events.append(combined)
#
#     tasks: list[str] = [habit.task for habit in habits]
#     current_streak = calculate_all_streaks(combined_habit_and_events)
#
#     plot.simple_bar(tasks, current_streak, title="progress of current streaks")
#     plot.show()
#
#
# @streak.command()
# @click.pass_obj
# def longest(habit_tracker_client: HabitTrackerClient):
#     habits = habit_tracker_client.list_habits_by_user_id()
#
#     longest_habit: Optional[Habit] = None
#     longest_streak: int = 0
#
#     for habit in habits:
#         events = habit_tracker_client.list_habit_events(habit.habit_id)
#         df = transform_to_panda_dataframe(events, habit.periodicity)
#         current_longest = df.max()['streak']
#         if longest_streak < current_longest:
#             longest_habit = habit
#             longest_streak = current_longest
#
#     if not longest_habit:
#         click.echo("No records")
#     else:
#         click.echo(f"Habit '{longest_habit.task}' has the longest streak with {longest_streak} streaks")
#
#     return
