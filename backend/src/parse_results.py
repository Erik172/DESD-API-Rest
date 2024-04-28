import re

def parse_result_yolov8(result):
        verbose = result.verbose()

        verbose = verbose.split(',')
        verbose = [v.strip() for v in verbose]
        result_dict = {'data': []}
        for i in verbose:
            try:
                r = re.split(r'(\d+\.\d+)', i)
                class_name = r[0].strip()
                confidence = float(r[1])

                result_dict['data'].append({
                    'name': class_name,
                    'confidence': confidence
                })
            except:
                pass

        return result_dict