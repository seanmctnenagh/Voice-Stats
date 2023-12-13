import globals
import matplotlib.pyplot as plt
import math

with open('Match Reports\Test Match Nenagh vs Roscrea 12-03-2022\Test Match_command_log.txt', 'r') as f:
    commands = f.read().split('\n')

times = [command.split(": ")[0] for command in commands if "Undone" not in command]
# commands = [command.split(": ")[1] for command in commands if "Undone" not in command]

commands = [command for command in commands if "Undone" not in command]

team_0 = [command for command in commands if globals.team_names[0] in command]
team_1 = [command for command in commands if globals.team_names[1] in command]

minutes = [int(time.split(":")[0]) for time in times]
end = max(minutes)
# seconds = [int(time.split(":")[1]) for time in times]

events = globals.event_names

team_0_events = [(event, [], []) for event in events]

for i, event in enumerate(team_0_events):
    count = 0
    team_0_events[i][1].append(0)
    team_0_events[i][2].append(count)
    for command in team_0:
        if event[0] in command.lower():
            team_0_events[i][1].append(int(command[:2]))
            count += 1
            team_0_events[i][2].append(count)
    team_0_events[i][1].append(end)
    team_0_events[i][2].append(count)

    plt.plot(team_0_events[i][1], team_0_events[i][2])
    plt.title(f'{globals.team_names[0]} {event[0].capitalize()}')
    new_list = range(math.floor(min(team_0_events[i][1])), math.ceil(max(team_0_events[i][1]))+1)
    plt.xticks(new_list)
    plt.show()

print(team_0_events)
