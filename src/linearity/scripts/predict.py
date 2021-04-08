import os
import csv
import time


def predict(stateList, counter):
    print("#####Starting to Predict#####")
    evaluate_binary = '/exact/evaluate_rnn'
    genome = '/catkin_ws/genomes/truncated_current_position_genome.bin'

    fields = ["time","wind_speed","wind_angle","battery_voltage","battery_current","position_x","position_y","position_z","orientation_x","orientation_y","orientation_z","orientation_w","velocity_x","velocity_y","velocity_z","angular_x","angular_y","angular_z","linear_acceleration_x","linear_acceleration_y","linear_acceleration_z"]
    state_file_name = 'states/state' + str(counter) + '.csv'
    prediction_file_name = 'prediction/state' + str(counter) + '_predictions.csv'
    with open(state_file_name , 'w') as outputfile:
        writer = csv.DictWriter(outputfile, fieldnames=fields)
        writer.writeheader()
        for state in stateList:
            if len(state) == len(fields):
                writer.writerow(state)
    cmd = evaluate_binary +" --output_directory ./prediction --genome_file " + genome + " --testing_filenames " + state_file_name + " --std_message_level INFO --file_message_level INFO --time_offset 1" 
    os.system(cmd)
    with open(prediction_file_name) as result:
        reader = csv.DictReader(result)
        return_val = {}
        for row in reader:
            return_val['battery_voltage'] = row['predicted_battery_voltage']
            return_val['position_x'] = row['predicted_position_x']
            return_val['position_y'] = row['predicted_position_y']
            return_val['position_z'] = row['predicted_position_z']
        return return_val
    
