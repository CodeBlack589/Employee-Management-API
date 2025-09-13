from fastapi import FastAPI, HTTPException,Query
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import date
import uvicorn
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = "09031999"  # keep this safe
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
app = FastAPI()

"""Here we create the database in MongoDB compass using use assessment_db   
and after that db.createcollection("employees") and add some dummy data"""
client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.assessment_db   # database
employees = db.employees

@app.on_event("startup")
async def create_indexes():
    # Create an index on employee_id field
    await employees.create_index("employee_id", unique=True)
    employee_schema = {
        "bsonType": "object",
        "required": ["employee_id", "name", "department", "salary", "joining_date", "skills"],
        "properties": {
            "employee_id": {"bsonType": "string"},
            "name": {"bsonType": "string"},
            "department": {"bsonType": "string"},
            "salary": {"bsonType": "double"},
            "joining_date": {"bsonType": "date"},
            "skills": {
                "bsonType": "array",
                "items": {"bsonType": "string"}
            }
        }
    }

    try:
        # This applies schema if collection already exists
        await db.command({
            "collMod": "employees",
            "validator": {"$jsonSchema": employee_schema},
            "validationLevel": "strict"
        })
    except Exception as e:
        # If collection doesn't exist yet, create with schema
        try:
            await db.create_collection(
                "employees",
                validator={"$jsonSchema": employee_schema},
                validationLevel="strict"
            )
        except Exception:
            # Collection already exists with schema, safe to ignore
            pass
"""We use Pydantic for removing mannual thing too much"""
class Employee(BaseModel):
    employee_id: str
    name: str
    department: str
    salary: float
    joining_date: date
    skills: List[str]

"""We use for this updation"""
class update(BaseModel):
    name: Optional[str] = None
    department: Optional[str] = None
    salary: Optional[float] = None
    joining_date: Optional[date] = None
    skills: Optional[List[str]] = None

@app.get("/employees/avg-salary")
async def avg_salary_by_department():
    pipeline = [{"$group": {"_id": "$department","avg_salary": {"$avg": "$salary"}}}]
    res = employees.aggregate(pipeline)
    result = []
    async for doc in res:
        result.append({
            "department": doc["_id"],
            "avg_salary": doc["avg_salary"]
        })

    return result
@app.get("/employees/search")
async def search_employees(skill: str = Query(...)):
    res = employees.find({"skills": skill})
    result = []
    async for emp in res:
        emp["_id"] = str(emp["_id"])
        result.append(emp)
    return result
# 1. Create Employee
@app.post('/employees')
async def createemployees(employe: Employee):
    eixts = await employees.find_one({'employee_id': employe.employee_id})
    if eixts:
        raise HTTPException(status_code=400, detail="Employee ID already exits")
    emp_data = employe.dict()
    emp_data["joining_date"] = datetime.combine(emp_data["joining_date"], datetime.min.time())
    await employees.insert_one(emp_data)
    return {"message": "Employee created Successfully"}


# 2. Get Employee by ID
@app.get('/employees/{employee_id}')
async def getemployee(employee_id: str):
    emp = await employees.find_one({'employee_id': employee_id})
    if not emp:
        raise HTTPException(status_code=404, detail="Employee does not exists")
    emp["_id"] = str(emp["_id"])   # convert ObjectId to string
    return emp


# 3. Update Employee
@app.put('/employees/{employee_id}')
async def updatedetail(employee_id: str, updated_detail: update):
    update_data = {k: v for k, v in updated_detail.dict().items() if v is not None}
    if "joining_date" in update_data:
        update_data["joining_date"] = str(update_data["joining_date"])
    result = await employees.update_one(
        {"employee_id": employee_id},
        {"$set": update_data}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee updated successfully"}


# 4. Delete Employee
@app.delete('/employees/{employee_id}')
async def delte_employee(employee_id: str):
    result = await employees.delete_one({'employee_id': employee_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee deleted successfully"}

@app.get("/employees")
async def list_employees(department: Optional[str] = Query(None),skip: int = Query(0, ge=0),limit: int = Query(10, ge=1)):
    query = {}
    if department:
        query["department"] = department
    res = employees.find(query).sort("joining_date", -1).skip(skip).limit(limit)
    result = []
    async for emp in res:
        emp["_id"] = str(emp["_id"])
        emp["joining_date"] = str(emp["joining_date"])
        result.append(emp)
    return {
        "skip": skip,
        "limit": limit,
        "count": len(result),
        "employees": result
    }

"""@app.get('/employees')
async def listofemplyess(department:str=Query(...)):
    res= employees.find({'department':department}).sort('joining_date',-1)
    result=[]
    async for emp in res:
        emp["_id"] = str(emp["_id"])
        emp["joining_date"] = str(emp["joining_date"])
        result.append(emp)
    return result

"""

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
