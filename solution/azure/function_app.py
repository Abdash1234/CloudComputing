import azure.functions as func
import logging
import time
from PIL import Image
import io

# Global variable to track container initialization time for cold start measurement
container_start_time = time.time()

app = func.FunctionApp()

@app.route(route="GrayscaleFunction", methods=["POST"], auth_level=func.AuthLevel.FUNCTION)
def grayscalefunction(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('GrayscaleFunction received a request.')

    request_start_time = time.time()
    
    cold_start_time = request_start_time - container_start_time

    try:
        image_bytes = req.get_body()
        input_buffer = io.BytesIO(image_bytes)
        
        image = Image.open(input_buffer)
        
        processing_start = time.time()
        grayscale_image = image.convert("L")
        processing_time = time.time() - processing_start

        output_buffer = io.BytesIO()
        grayscale_image.save(output_buffer, format="PNG")
        
        metrics = {
            "coldStartTime": cold_start_time,    
            "processingTime": processing_time,     
            "totalFunctionTime": time.time() - request_start_time 
        }
        
        headers = {
            "X-Cold-Start-Time": str(cold_start_time),
            "X-Processing-Time": str(processing_time),
            "X-Total-Function-Time": str(time.time() - request_start_time)
        }
        
        return func.HttpResponse(
            body=output_buffer.getvalue(),
            mimetype="image/png",
            headers=headers,
            status_code=200
        )
    except Exception as e:
        logging.error(f"Error processing image: {e}")
        return func.HttpResponse(
            "Error processing image: " + str(e),
            status_code=500
        )
