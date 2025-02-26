from utils import get_image_hash, compare_images
from concurrent.futures import ThreadPoolExecutor
from typing import Optional, Dict, List, Tuple

def find_duplicate_pages(image_paths: list, similarity_threshold: float = 0.95, hash_threshold: int = 5) -> Tuple[list, List[Dict[str, Optional[str]]]]:
    duplicates = []
    report = []
    num_pages = len(image_paths)
    
    hashes = [get_image_hash(path) for path in image_paths]
    
    task = []
    with ThreadPoolExecutor() as executor:
        for i in range(num_pages):
            for j in range(i + 1, num_pages):
                # Comparar hashes antes de hacer SSIM
                hash_diff = hashes[i] - hashes[j]
                if hash_diff <= hash_threshold:
                    task.append(executor.submit(compare_images, image_paths[i], image_paths[j]))
                    
        results = [task.result() for task in task]
        
    index = 0
    for i in range(num_pages):
        for j in range(i + 1, num_pages):
            if hashes[i] - hashes[j] <= hash_threshold:
                similarity = results[index]
                if similarity > similarity_threshold:
                    duplicates.append((i + 1, j + 1, similarity))
                    report.append({
                        'pagina1': i + 1,
                        'pagina2': j + 1,
                        'similitud': similarity
                    })
                index += 1
                
    return duplicates, report