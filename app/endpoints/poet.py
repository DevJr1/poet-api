from fastapi import APIRouter, HTTPException, Query
import requests

router = APIRouter()

POETRYDB_URL = "https://poetrydb.org/author"

@router.get("/poet")
def get_poets(letter: str, single: bool = Query(False, description="If true, return a single poet. Otherwise, return all matching poets.")):
    if not letter.isalpha() or len(letter) != 1:
        raise HTTPException(status_code=400, detail="Input must be a single alphabet letter.")
    
    response = requests.get(POETRYDB_URL)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching poets.")
    
    try:
        data = response.json()
        poets = data["authors"]
    except (ValueError, KeyError):
        raise HTTPException(status_code=500, detail="Invalid response format.")
    
    matching_poets = [poet for poet in poets if poet.startswith(letter.upper())]
    if not matching_poets:
        raise HTTPException(status_code=404, detail="No poets found with the given initial.")
    
    if single:
        return {"poet": matching_poets[0]}
    else:
        return {"poets": matching_poets}
