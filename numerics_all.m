%%% Creating numerics_all.csv file

clear all;
path1 = 'C:\Users\Desktop\';
cd(path1)
fid1 = fopen("numerics_all.csv",'wt'); % output file
%path2 = 'Z:\mimic3wdb-matched/';
%cd(path2)
numerics_file = readtable('RECORDS-numerics','ReadVariableNames',false); % available on mimic-iii matched waveform website
numerics_records = numerics_file.(3);
path3 = 'C:\Users\Desktop\numerics_database'; % link to local copy of numerics database
cd(path3)
for i = 1:length(numerics_records)
    i
    numerics_record = strcat(numerics_records{i},'.hea');
    
    fid2 = fopen(numerics_record);
    file_reading = textscan(fid2,'%s');
    fclose(fid2);
    file_content = file_reading{1};
    
    file_name = file_content{1};
    frequency_res = str2double(file_content{3});
    total_samples = str2num(file_content{4});
    start_time = file_content{5};
    start_date = file_content{6};
    dat_file = file_content{7};
    
    if frequency_res ~= 1
        resolution = 60;
    else
        resolution = 1;
    end
    %resolution = ceil(inv(frequency_res));
    
    
    datetime_combined = strcat(start_date,{' '},start_time);
    temp = regexprep(datetime_combined,':\d\d$','$&.0','lineanchors');
    %datetime = datenum(datetime_combined)
    record_start = posixtime(datetime(temp,'InputFormat','dd/MM/yyyy HH:mm:ss.S'));
    
    fprintf(fid1,'%s,%f,%d,%d,%s\n',file_name,record_start,resolution,total_samples,dat_file);
    
end
fclose(fid1);
cd(path1)
fclose all;

