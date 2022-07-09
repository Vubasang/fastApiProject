from fastapi import Request, APIRouter, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import DateTime

from .models import Order

from dotenv import load_dotenv
load_dotenv()

templates = Jinja2Templates(directory="templates")

router = APIRouter()


'''@router.get("/database", response_class=HTMLResponse)
async def database_home(request: Request):
    key = os.getenv("database_key")
    print(key)
    return templates.TemplateResponse("database.html", {"request": request})'''

@router.get("/database", response_class=HTMLResponse)
def form_database1(request: Request):
    SQLALCHEMY_DATABASE_URL = "postgresql://wubashang:wubashang_password@gogotech.ru:7777/db"

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        echo=True
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    BaseException = declarative_base()
    db = SessionLocal()
    # print('QUERY', db.query(Order.date))
    result = db.query(Order.date)
               .filter(Order.statuses.any(Status.status != 'CANCELED'))
               .all()
    results = [a[0].strftime('%Y/%m/%d') for a in result]
    print(result)
    return templates.TemplateResponse('database.html', context={'request': request, 'results': result, 'results_sort': sorted(results)})

