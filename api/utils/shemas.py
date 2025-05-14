from pydantic import BaseModel

class Rotation(BaseModel):
    """
    Represents a rotation operation to be applied to a specific page in a document.

    Attributes:
        page (int): The page number to which the rotation should be applied.
        degrees (float): The degree of rotation to apply. Positive values indicate
                         clockwise rotation, while negative values indicate
                         counterclockwise rotation.
    """
    page: int
    degrees: float

class ClearCollectionResponse(BaseModel):
    """
    Represents the response returned after clearing a collection.

    Attributes:
        status (str): The status of the operation, typically indicating success or failure.
        message (str): A descriptive message providing additional details about the operation.
    """
    status: int
    message: str
