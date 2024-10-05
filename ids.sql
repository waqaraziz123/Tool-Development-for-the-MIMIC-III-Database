-- This code can generate the 'ids.csv' file used in mimic_numerics.py

\copy (select icustay_id,subject_id from icustays order by icustay_id) to 'C:\Users\Desktop\ids.csv' CSV header;
