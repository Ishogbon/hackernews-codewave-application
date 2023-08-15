def generate_missing_or_invalid_field_error(field_name: str):
    return {
        "error": {
            "code": f"MISSING_OR_INVALID_{field_name.upper()}_FIELD",
            "message": f"The '{field_name}' field is missing or invalid. Refer to documentation for more help"
        }
}
    
JSON_DECODE_ERROR = {"error": {"code": "JSON_PARSE_ERROR", "message": "Failed to parse the provided JSON data. Please ensure that the data is properly formatted JSON."}}

MISSING_OR_INVALID_KIDS_FIELD = {"error": {"code": "MISSING_OR_INVALID_KIDS_FIELD", "message": "The 'kids' field is missing or invalid. It should be a list of integers (hints)."}}

MISSING_INVALID_TYPE_FIELD = {"error": {"code": "MISSING_INVALID_TYPE_FIELD","message": "The 'type' field is missing or invalid. It should be one of: 'story', 'job', 'comment', 'poll', 'pollopt'."}}

INVALID_URL = {"error": {"code": "INVALID_URL","message": "The url you supplied is invalid"}}

INVALID_ITEM = {"error": {"code": "INVALID_ITEM", "message": "The item you are trying to fetch does not exist in our database"}}

INVALID_SOURCE = {"error": {"code": "INVALID_SOURCE", "message": "The available sources you can retrieve item for now are hns(the hackernews) and cwe(CodeWave) sources"}}

INTERNAL_ERROR = {"error": {"code": "INTERNAL_ERROR", "message": "An internal error occurred, while trying to process your request, please contact admin"}}

PROCESS_ERROR = {"error": {"code": "PROCESS_ERROR", "message": "Error occurred while processing request, contact admin"}}

INVALID_ITEM_QUERY = {"error": {"code": "INVALID_ITEM_QUERY", "message": "The available items you can query for are stories, jobs, comments, polls and pollopts"}}

UNSPECIFIED_ITEM = {"error": {"code": "UNSPECIFIED_ITEM", "message": "You need to specify the item type you are trying to retrieve, Acceptable types are story, job, comment, poll, pollopt"}}

INVALID_ID = {"error": {"code": "INVALID_ID", "message": "You can't have an id value lesser than one"}}

PARENT_NO_EXISTS = {"error": {"code": "PARENT_NO_EXISTS", "message": "The parent element for this item does not exists"}}

NO_API = {"error": {"code": "NO_API", "message": "There is no service for this API url you are trying to access"}}


ITEM_POST_SUCCESS = {"success": {"code": "ITEM_POST_SUCCESS", "message": "Your item has been stored successfully"}}