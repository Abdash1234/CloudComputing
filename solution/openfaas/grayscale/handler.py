import io
import base64
from PIL import Image
import sys
import time

def handle(event, context):

    func_start = time.time()
    
    try:

        read_start = time.time()
        image_bytes = event.body
        read_end = time.time()


        input_buffer = io.BytesIO(image_bytes)
        image = Image.open(input_buffer)

        process_start = time.time()
        grayscale_image = image.convert("L")
        process_end = time.time()

        output_buffer = io.BytesIO()
        grayscale_image.save(output_buffer, format="PNG")
        result_bytes = output_buffer.getvalue()

        func_end = time.time()


        total_time = func_end - func_start
        read_time = read_end - read_start
        processing_time = process_end - process_start

 
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "image/png",
                "X-Read-Time": str(read_time),
                "X-Processing-Time": str(processing_time),
                "X-Total-Time": str(total_time)
            },
            "body": result_bytes
        }
    except Exception as e:
        sys.stderr.write("Error processing image: %s" % e)
        return {
            "statusCode": 500,
            "body": "Error processing image: " + str(e)
        }
