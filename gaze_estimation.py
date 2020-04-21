'''
This is a sample class for a model. You may choose to use it as-is or make any changes to it.
This has been provided just to give you an idea of how to structure your model class.
'''
import numpy as np
import time
from openvino.inference_engine import IENetwork, IECore
import os
import cv2
import argparse
import sys


class GazeDetect:
    '''
    Class for the Face Detection Model.
    '''
    def __init__(self, model_name = "/Users/soymilk/edgeai/intel/gaze-estimation-adas-0002/FP32/gaze-estimation-adas-0002", device="CPU", threshold=0.60):
        '''
        TODO: Use this to set your instance variables.
        '''
        
        self.model_weights=model_name+'.bin'
        self.model_structure=model_name+'.xml'
        self.device=device
        self.threshold=threshold
        self.exec_net=None

        try:
            self.model=IENetwork(self.model_structure, self.model_weights)
        except Exception as e:
            raise ValueError("Could not Initialise the network. Have you enterred the correct model path?")

        self.input_name=next(iter(self.model.inputs))
        self.input_shape=self.model.inputs[self.input_name].shape
        self.output_name=next(iter(self.model.outputs))
        self.output_shape=self.model.outputs[self.output_name].shape
        

    def load_model(self):
        '''
        TODO: You will need to complete this method.
        This method is for loading the model to the device specified by the user.
        If your model requires any Plugins, this is where you can load them.
        '''
        core = IECore()
        self.exec_net = core.load_network(network=self.model, device_name=self.device, num_requests=1)

    def predict(self, left_eye, right_eye, angles):
        '''
        TODO: You will need to complete this method.
        This method is meant for running predictions on the input image.
        '''
        p_left_eye = self.preprocess_input(left_eye)
        p_right_eye = self.preprocess_input(right_eye)
        input_dict={"left_eye_image":p_left_eye,
                    "right_eye_image":p_right_eye,
                    "head_pose_angles":angles}
        start_time = time.time()
        outputs = self.exec_net.infer(input_dict)
        print("Time take for gaze estimation inference (in seconds):", time.time()-start_time)
        x, y = self.preprocess_output(outputs)
        return x, y

    def check_model(self):
        #KIV
        return

    def preprocess_input(self, image):
        '''
        Before feeding the data into the model for inference,
        you might have to preprocess it. This function is where you can do that.
        '''
        width, height = 60, 60
        image = cv2.resize(image, (width, height))
        image = image.transpose((2,0,1))
        image = image.reshape(1, 3, height, width)
        return image

    def preprocess_output(self, outputs):
        '''
        Before feeding the output of this model to the next model,
        you might have to preprocess the output. This function is where you can do that.
        '''
        # TODO: detections might be put under a key in output blob
        vector = outputs['gaze_vector']
        # assume [x,y,z]
        x, y = vector[0,0], vector[0,1]

        return x,y

    
