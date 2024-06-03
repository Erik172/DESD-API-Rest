import re

def parse_result_yolov8(result):
    """
    Parses the result of the YOLOv8 algorithm and returns a dictionary containing the class names and confidence scores.

    Args:
        result (str): The verbose result string from the YOLOv8 algorithm.

    Returns:
        dict: A dictionary containing the parsed data with class names and confidence scores.
              The dictionary has the following structure:
              {
                  'data': [
                      {
                          'name': <class_name>,
                          'confidence': <confidence_score>
                      },
                      ...
                  ]
              }
    """
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
