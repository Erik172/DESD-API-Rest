from openvino import Core
import onnxruntime as ort
import cpuinfo
import time
import os

from config import Config

class InferenceService:
    def __init__(self):
        self.cpu_info = cpuinfo.get_cpu_info()
        self.is_intel_cpu = 'Intel' in self.cpu_info['brand_raw']
        
        if self.is_intel_cpu:
            self.ie = Core()
            self.model = self.ie.read_model(model=Config.MODEL_OPENVINO_PATH)
            self.compiled_model = self.ie.compile_model(model=self.model, device_name='CPU', config={'INFERENCE_NUM_THREADS': f'{os.cpu_count()}'})
        else:
            self.session = ort.InferenceSession(Config.MODEL_ONNX_PATH)
            
    def infer(self, input_data) -> tuple[any, float]:
        start_time = time.time()
        if self.is_intel_cpu:
            results = self.compiled_model(input_data)
        else:
            input_name = self.session.get_inputs()[0].name
            results = self.session.run(None, {input_name: input_data})
        inference_time = time.time() - start_time
        
            
        return results, inference_time