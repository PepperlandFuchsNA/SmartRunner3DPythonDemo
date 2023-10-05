import VsxProtocolDriver
import pandas as pd
import numpy as np
import cv2
import open3d as o3d

#Settings reader portion, this reads all the settings fromt the settings.txt
with open(r'settings.txt', 'r') as fp:

    Settings = fp.readlines()

    try:
        for row in Settings:

            if row.find('SR3D_IP_Address') != -1:
                equal = row.index("=")
                Ip_Address = str(row[equal+1:].strip())
            elif row.find('ViewPCD') != -1:
                equal = row.index("=")
                showPCD = (row[equal+1:].strip())
            elif row.find('Push_Parameter') != -1:
                equal = row.index("=")
                Parameter_Push = (row[equal+1:].strip())
            elif row.find('TriggerEnabled') != -1:
                equal = row.index("=")
                TriggerEnabled = str(row[equal+1:].strip())
            elif row.find('TriggerSource') != -1:
                equal = row.index("=")
                TriggerSource = str(row[equal+1:].strip())
            elif row.find('TriggerActivation') != -1:
                equal = row.index("=")
                TriggerActivation = str(row[equal+1:].strip())
            elif row.find('AutoTriggerFrameRate') != -1:
                equal = row.index("=")
                AutoTriggerFrameRate = str(row[equal+1:].strip())
            elif row.find('Illumination') != -1:
                equal = row.index("=")
                Illumination = str(row[equal+1:].strip())
            elif row.find('Gain') != -1:
                equal = row.index("=")
                Gain = str(row[equal+1:].strip())
            elif row.find('SGBMPenalty1') != -1:
                equal = row.index("=")
                SGBMPenalty1 = str(row[equal+1:].strip())
            elif row.find('SGBMPenalty2') != -1:
                equal = row.index("=")
                SGBMPenalty2 = str(row[equal+1:].strip())
            elif row.find('SGBMEnableMedian') != -1:
                equal = row.index("=")
                SGBMEnableMedian = str(row[equal+1:].strip())
            elif row.find('SGBMUniqueness') != -1:
                equal = row.index("=")
                SGBMUniqueness = str(row[equal+1:].strip())
            elif row.find('OutputMode') != -1:
                equal = row.index("=")
                OutputMode = str(row[equal+1:].strip())
            elif row.find('ExposureTime') != -1:
                equal = row.index("=")
                ExposureTime = str(row[equal+1:].strip())
            elif row.find('Get_Parameter') != -1:
                equal = row.index("=")
                GetParameter = (row[equal+1:].strip())
    except:
        print("Please check settings.txt file something is not correct there, if not copy the settings file from back up folder and re populate it")      
      

# ret in following code represents the status of the function:
# ret = 0 means VSX_STATUS_SUCCESS;
# For more information of different output please refer to Definition.py in directory
# VsxProtocolDriver-3.0.0.tar/VsxProtocolDriver-3.0.0/src/VsxProtocolDriver/Definition.py
# function that can be used for this driver is available within Sensor.py in the same directory

# this function is used to grab data : this function is used in line 124 in main
def consume_data(sensor, SaveFileName):
    # obj is data_container_handle
    ret, obj = sensor.GetDataContainer(500)

    if ret == 0 and obj is not None:
        # grab x,y and z values
        #ret_a, image_a, results_a = obj.GetImage("CalibratedA")  # x data
        #ret_b, image_b, results_b = obj.GetImage("CalibratedB")  # y data
        #ret_c, image_c, results_c = obj.GetImage("CalibratedC")  # z data

        #ret, image_left_raw, results_left_raw = obj.GetImage("LeftRaw")
        #ret, image_right_raw, results_right_raw = obj.GetImage("RightRaw")
        #ret, image_disparity_c, results_disparity_c = obj.GetImage("DisparityC")
        #ret, image_amplitude, result_amplitude = obj.GetImage("Amplitude")

        #imageA = image_a[~np.isnan(image_a)]
        #imageB = image_b[~np.isnan(image_b)]
        #imageC = image_c[~np.isnan(image_c)]
        #print(len(imageA))
        #cv2.imshow("test", image_disparity_c)
        #cv2.waitKey(1000)
        #input("press enter for next frame: ")
        # save file into pcd
        # this works: create a point cloud file called "SR3D_stereo_trial.pcd"
        save_pcd = obj.Save3DPointCloudData(tag_x="CalibratedA", tag_y="CalibratedB", tag_z="CalibratedC",
                                            file_name=SaveFileName)
        
        



# main
if __name__ == "__main__":

    SaveFileName = input("Whats the file name for the pcd file? ")+".pcd"
    print(f"File name saved is {SaveFileName}")

    # connecting device
    ret, devices = VsxProtocolDriver.Sensor.GetUdpDeviceList()

    sensor = VsxProtocolDriver.Sensor.InitTcpSensor(Ip_Address, "")

    ret = sensor.Connect()

    if ret == 0:
        print("SR3D is connected")
    else:
        print("Connection error")

    # get device information
    ret, device_list = sensor.GetDeviceInformation()
    if ret == 0:
        print(device_list)
    else:
        print("unable to get device information")

    print("hellow")
    print(GetParameter)
    if eval(GetParameter):

        # get complete parameter list
        ret, param_list = sensor.GetParameterList()
        if ret == 0:
            for i in param_list:
                print(i.__dict__)
        else:
            print("unable to get parameter list.")

    # to receive single parameter value:
    # parameter_id:  TriggerEnabled, TriggerSource, TriggerActivation, AutoTriggerFrameRate, ExposureTime, Gain, Illumination, SGBMPenalty1, SGBMPenalty2,SGBMUniqueness, SGBMEnableMedian, OutputMode
    # function: GetSingleParameterValue(self, settings_version: int, configuration_id: str, configuration_version: int,parameter_id: str)
    print("hellow")
    print(eval(Parameter_Push))
    if eval(Parameter_Push):
        ret, exposure_time = sensor.GetSingleParameterValue(settings_version=1, configuration_id="Base",
                                                        configuration_version=1, parameter_id="ExposureTime")
        if ret == 0:
            print("single parameter value received (exposure time): " + str(exposure_time))
        else:
            print("unable to receive single parameter value")

        # to set single parameter value:
        # function: SetSingleParameterValue(self, settings_version: int, configuration_id: str, configuration_version: int,parameter_id: str, value: str) -> int:
        ret = sensor.SetSingleParameterValue(settings_version=1, configuration_id="Base", configuration_version=1,
                                            parameter_id="ExposureTime", value=ExposureTime)
        if ret == 0:
            print("setting successful")
        else:
            print("fail to set single parameter")

        # setup the rest of the parameters for the sensor with set single parameter value (all ret (i.e output from function) to return 0 to represent successful setup)
        ret = sensor.SetSingleParameterValue(1, "Base", 1, "TriggerEnabled", TriggerEnabled)
        ret = sensor.SetSingleParameterValue(1, "Base", 1, "TriggerSource", TriggerSource)
        ret = sensor.SetSingleParameterValue(1, "Base", 1, "TriggerActivation", TriggerActivation)
        ret = sensor.SetSingleParameterValue(1, "Base", 1, "AutoTriggerFrameRate", AutoTriggerFrameRate)
        ret = sensor.SetSingleParameterValue(1, "Base", 1, "Illumination", Illumination)
        ret = sensor.SetSingleParameterValue(1, "Base", 1, "Gain", Gain)
        ret = sensor.SetSingleParameterValue(1, "Base", 1, "SGBMPenalty1", SGBMPenalty1)
        ret = sensor.SetSingleParameterValue(1, "Base", 1, "SGBMPenalty2", SGBMPenalty2)
        ret = sensor.SetSingleParameterValue(1, "Base", 1, "SGBMEnableMedian", SGBMEnableMedian)
        ret = sensor.SetSingleParameterValue(1, "Base", 1, "SGBMUniqueness", SGBMUniqueness)
        ret = sensor.SetSingleParameterValue(1, "Base", 1, "OutputMode", OutputMode)
        ret = sensor.ResetDynamicContainerGrabberEx(buffer_size=5,
                                                    strategy=VsxProtocolDriver.Definitions.Strategy.DROP_OLDEST)
    if ret == 0:
        i = 0
        print("start grabbing data from dynamic container")
        # trying to grab data repetitively
        while i < 1:
            consume_data(sensor, SaveFileName)
            print(i)
            i += 1

    else:
        print("unable to establish dynamic container grabber")

    # disconnect device
    ret = sensor.Disconnect()
    if ret == 0:
        print("Done grabbing the PCD")
        if(eval(showPCD)):
            o3d.utility.set_verbosity_level(o3d.utility.VerbosityLevel.Error)
            pcd = o3d.io.read_point_cloud(SaveFileName)
            pcd = pcd.remove_non_finite_points(remove_nan=True, remove_infinite=True)
            o3d.visualization.draw_geometries([ pcd],
                                        zoom=0.7,
                                        front=[0.5439, -0.2333, -0.8060],
                                        lookat=[2.4615, 2.1331, 1.338],
                                        up=[-0.1781, -0.9708, 0.1608], window_name= "Smart Runner 3D Point Cloud")
        input("Press Enter to Quit")
    else:
        print("something is wrong")
        input("Press Enter to Quit")
