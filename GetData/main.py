from definition import DATA_DIR, TARGET_DIR
import os
import GetData.DataFromTS as dfts
import readTS.read_ts as rt
import readTS.write_ts_net as wt

source_filename = "anomaly_art_daily_drift.csv"
abs_file_path = os.path.join(DATA_DIR, source_filename)

ts_dates, ts_values, ts_outliers = rt.split_up_ts(abs_file_path)
networks = dfts.data_from_ts(ts_values, 100)
# print("networks: {}".format(networks))
sparsifyed_networks = dfts.reduce_networks(networks)

wt.networks_to_file(sparsifyed_networks, source_filename)
