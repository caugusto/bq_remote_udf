# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
from google.cloud import translate_v2 as translate
import six

def translation_handler(request):
    try:
        # Parses request data as JSON
        request_json = request.get_json()
        # Reads the variable mode, passed as a user_defined_context parameter, upon remote function definition  
        mode = request_json['userDefinedContext']['mode']
        # Reads the actual function call
        calls = request_json['calls']
        # translate_text is defined as part of the remote function definition, user_defined_context section  
        if mode == "translate_text":
            # Returns the result of translate_text function, defined below
            return translate_text(calls)
        # Exception handling in case the mode variable value is unknown
        return json.dumps({"Error in Request": request_json}), 400
    except Exception as inst:
        # Try block exception
        return json.dumps( { "errorMessage": 'something unexpected in input' } ), 400



def translate_text(calls):
    try:
        # Define return array
        return_value = []
        # Construct a Translation Client object
        translate_client = translate.Client()
        # Defines translation target language. es means Spanish
        target="es"
        for call in calls:
            # Reads original value passed to the function as the first parameter
            text = call[0]
            if isinstance(text, six.binary_type):
                # Decodes the string using the codec UTF-8
                text = text.decode("utf-8")
            # Calls the Translation api, passing the original text and target language    
            result = translate_client.translate(text, target_language=target)
            # Appends the translated value to the return array
            return_value.append(str(result["translatedText"]))
        # BigQuery expects the endpoint should return a HTTP response in the following format, 
        # otherwise BigQuery can't consume it and will fail the query calling the remote function.
        # See https://cloud.google.com/bigquery/docs/reference/standard-sql/remote-functions#output_format for more details
        return_json = json.dumps({"replies": return_value})
        return return_json
    except Exception as inst:
        # Try block exception handling
        return json.dumps( { "errorMessage": 'something unexpected in translate_text function' } ), 400
