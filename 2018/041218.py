from base import Base
import numpy as np
import pandas as pd
import re


class First(Base):
    def __init__(self):
        super(First, self).__init__()
        self.examples = {
            '[1518-11-01 00:00] Guard #10 begins shift\n'
            '[1518-11-01 00:05] falls asleep\n'
            '[1518-11-01 00:25] wakes up\n'
            '[1518-11-01 00:30] falls asleep\n'
            '[1518-11-01 00:55] wakes up\n'
            '[1518-11-01 23:58] Guard #99 begins shift\n'
            '[1518-11-02 00:40] falls asleep\n'
            '[1518-11-02 00:50] wakes up\n'
            '[1518-11-03 00:05] Guard #10 begins shift\n'
            '[1518-11-03 00:24] falls asleep\n'
            '[1518-11-03 00:29] wakes up\n'
            '[1518-11-04 00:02] Guard #99 begins shift\n'
            '[1518-11-04 00:36] falls asleep\n'
            '[1518-11-04 00:46] wakes up\n'
            '[1518-11-05 00:03] Guard #99 begins shift\n'
            '[1518-11-05 00:45] falls asleep\n'
            '[1518-11-05 00:55] wakes up\n': 240
        }
        self.regexp_guard_id = re.compile(r'#(\d+)')

    def most_asleep_minute(self, df):
        # Compute frequence distribution of asleep minutes
        freq = np.zeros((60))
        for _, row in df.iterrows():
            freq[row['start']:row['end']] += 1
        return pd.Series({'minute': freq.argmax(), 'freq': freq.max()})

    def pre_treat(self, logs):
        # The treated logs grammar is : (guard_start (asleep wakeup)+))+
        # The use of slice is a strong asumption
        data = []
        for line in logs:
            if 'Guard' in line:
                guard_id = self.regexp_guard_id.search(line)
                guard_id = int(guard_id.group(1))
            elif 'fall' in line:
                start = int(line[15:17])
            else:
                date = line[1:11]
                end = int(line[15:17])
                data.append([guard_id, date, start, end])

        df = pd.DataFrame(data, columns=['guard_id', 'date', 'start', 'end'])
        df['length'] = df['end'] - df['start']
        return df

    def _solve(self, input):
        logs = sorted(input.strip().split('\n'))
        df = self.pre_treat(logs)

        best_guard = df.groupby('guard_id')['length'].sum().idxmax()
        best_minute = self.most_asleep_minute(df[df['guard_id'] == best_guard])['minute']

        return best_guard * best_minute


class Second(First):
    def __init__(self):
        super(Second, self).__init__()
        self.examples = {
            '[1518-11-01 00:00] Guard #10 begins shift\n'
            '[1518-11-01 00:05] falls asleep\n'
            '[1518-11-01 00:25] wakes up\n'
            '[1518-11-01 00:30] falls asleep\n'
            '[1518-11-01 00:55] wakes up\n'
            '[1518-11-01 23:58] Guard #99 begins shift\n'
            '[1518-11-02 00:40] falls asleep\n'
            '[1518-11-02 00:50] wakes up\n'
            '[1518-11-03 00:05] Guard #10 begins shift\n'
            '[1518-11-03 00:24] falls asleep\n'
            '[1518-11-03 00:29] wakes up\n'
            '[1518-11-04 00:02] Guard #99 begins shift\n'
            '[1518-11-04 00:36] falls asleep\n'
            '[1518-11-04 00:46] wakes up\n'
            '[1518-11-05 00:03] Guard #99 begins shift\n'
            '[1518-11-05 00:45] falls asleep\n'
            '[1518-11-05 00:55] wakes up\n': 4455
        }

    def _solve(self, input):
        logs = sorted(input.strip().split('\n'))
        df = self.pre_treat(logs)
        tmp = df.groupby('guard_id').apply(self.most_asleep_minute)
        best_guard = tmp['freq'].idxmax()
        best_minute = tmp.loc[best_guard]['minute']
        return best_guard * best_minute


if __name__ == '__main__':
    import argparse

    def arguments():
        parser = argparse.ArgumentParser(description='Script desc')
        parser.add_argument(
            '-t', '--test', action='store_true', help='Execute tests')
        parser.add_argument(
            '-s', '--second', action='store_true', help='Execute second')
        args = parser.parse_args()
        return args

    args = arguments()

    if args.second:
        solver = Second()
    else:
        solver = First()
    if args.test:
        solver.test_all()
    else:
        solver.solve()
