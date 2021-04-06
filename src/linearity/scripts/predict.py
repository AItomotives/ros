import os
import csv
def predict(evaluate_binary,genome, stateList):
    fields = ["time","wind_speed","wind_angle","battery_voltage","battery_current","position_x","position_y","position_z","orientation_x","orientation_y","orientation_z","orientation_w","velocity_x","velocity_y","velocity_z","angular_x","angular_y","angular_z","linear_acceleration_x","linear_acceleration_y","linear_acceleration_z"]
    with open('state.csv' , 'w', newline = '') as outputfile:
        writer = csv.DictWriter(outputfile, fieldnames=fields)
        writer.writeheader()
        for state in stateList:
            writer.writerow(state)
        cmd = "/" + evaluate_binary +" --output_directory ./prediction --genome_file " + genome + " --testing_filenames state.csv  --std_message_level INFO --file_message_level INFO --time_offset 1" 
        os.system(cmd)
    with open('prediction/state_predictions.csv' , newline = '') as result:
        reader = csv.DictReader(result)
        result = {}
        for row in reader:
            result['battery_voltage'] = row['predicted_battery_voltage']
            result['battery_current'] = row['predicted_battery_current']
        return result
    
