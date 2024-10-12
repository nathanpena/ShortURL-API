from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from database import SessionLocal, engine
from models import URLMapping, ReusePool
import models
from generator import get_next_value

# Create tables on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic model for request body validation
class URLRequest(BaseModel):
    url: str

# Function to get the next available short URL
def get_next_short_url(db: Session):
    # Check if there are any URLs in the reuse pool
    reuse_url = db.query(ReusePool).first()
    
    if reuse_url:
        # If there is a reusable URL, delete it from the pool and return it
        short_url = reuse_url.short_url
        db.delete(reuse_url)
        db.commit()
        return short_url
    
    # Otherwise, generate a new short URL
    return get_next_value()  # Assuming get_next_value is imported from your generator module


@app.get("/short_urls")
async def get_short_urls(db: Session = Depends(get_db)):
    # Query all records from the URLMapping table
    short_urls = db.query(URLMapping.short_url).all()
    
    # Extract only the short URLs (they come back as a list of tuples)
    short_urls_list = [url[0] for url in short_urls]
    
    print("Currently used short URLs:", short_urls_list)  # Debugging print
    return {"short_urls": short_urls_list}

@app.get("/reuse_pool")
async def get_reuse_urls(db: Session = Depends(get_db)):
    # Query all reused URLs from the ReusePool table
    reuse_urls = db.query(ReusePool.short_url).all()
    
    # Extract only the short URLs (they come back as a list of tuples)
    reuse_urls_list = [url[0] for url in reuse_urls]
    
    print("URLs in the reuse pool:", reuse_urls_list)  # Debugging print
    return {"reuse_pool": reuse_urls_list}

@app.post("/shorten")
async def shorten_url(request: URLRequest, db: Session = Depends(get_db)):
    # Get the next short URL from your generator
    short_url = get_next_short_url(db)
    
    # Create a new URLMapping instance
    db_url = URLMapping(short_url=short_url, original_url=request.url)
    
    # Add to the database session
    db.add(db_url)
    db.commit()
    
    return {"short_url": short_url, "original_url": request.url}

@app.get("/{short_url}")
async def redirect_url(short_url: str, db: Session = Depends(get_db)):
    # Query the URL mapping from the database
    db_url = db.query(URLMapping).filter(URLMapping.short_url == short_url).first()

    if not db_url:
        raise HTTPException(status_code=404, detail="Short URL not found")
    
    # Increment click count
    db_url.click_count += 1
    db.commit()

    return RedirectResponse(url=db_url.original_url)

@app.get("/clicks/{short_url}")
async def get_clicks(short_url: str, db: Session = Depends(get_db)):
    db_url = db.query(URLMapping).filter(URLMapping.short_url == short_url).first()

    if not db_url:
        raise HTTPException(status_code=404, detail="Short URL not found")
    
    return {"short_url": db_url.short_url, "clicks": db_url.click_count}

@app.delete("/delete/{short_url}")
async def delete_short_url(short_url: str, db: Session = Depends(get_db)):
    db_url = db.query(URLMapping).filter(URLMapping.short_url == short_url).first()

    if db_url:
        db.delete(db_url)
        db.commit()
        
        # Add the deleted URL to the ReusePool for reuse
        reused_url = ReusePool(short_url=short_url)
        db.add(reused_url)
        db.commit()
        
        return {"message": "Short URL deleted and returned to the pool"}
    else:
        raise HTTPException(status_code=404, detail="Short URL not found")

