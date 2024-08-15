import pandas as pd

def load_event_data(filepath):
    eventdata = pd.read_csv(filepath)
    eventdata['isoDate'] = [date[:-6] for date in eventdata['isoDate']]
    eventdata['isoDate'] = pd.to_datetime(eventdata['isoDate'])
    return eventdata

def fetch_data(uid, eventdata):
    eventdata_ = eventdata[eventdata['UID'] == uid]
    hr_data = pd.read_csv(f"{uid}_imputed_hr.csv")
    hr_data['dt'] = pd.to_datetime(hr_data['dt'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
    hr_nosleep = hr_data[hr_data['sleepornot'] == 0]
    return eventdata_, hr_data, hr_nosleep
