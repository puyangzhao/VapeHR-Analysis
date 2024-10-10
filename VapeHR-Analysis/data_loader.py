import pandas as pd

def load_event_data(filepath):
    eventdata = pd.read_csv(filepath)
    eventdata['Date'] = [date[:-6] for date in eventdata['Date']]
    eventdata['Date'] = pd.to_datetime(eventdata['Date'])
    return eventdata

def fetch_data(uid, eventdata):
    eventdata_ = eventdata[eventdata['UID'] == uid]
    hr_data = pd.read_csv(f"{id}_data.csv")
    hr_data['dt'] = pd.to_datetime(hr_data['time'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
    hr_nosleep = hr_data[hr_data['is_sleep'] == 0]
    return eventdata_, hr_data, hr_nosleep
