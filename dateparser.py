from datetime import datetime, timedelta

dt = datetime.strptime("Nov 8 15:26:51.198", "%b %d %H:%M:%S.%f")
dt2 = datetime.strptime("Nov 8 16:16:51.138", "%b %d %H:%M:%S.%f")

print timedelta.strftime(dt2-dt, "%M")
