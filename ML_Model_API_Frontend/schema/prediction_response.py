from pydantic import BaseModel, Field
from typing import Dict

class PredictionResponse(BaseModel):
    predicted_category : str = Field(..., description = "The predicted insurance premium category!!!")
    confidence : float = Field(..., description = "Model's confidence score for the predicted class!!!")
    class_probabilities : Dict[str, float] = Field(..., description = "Probability distribution across all the possible classes!!!")
    