from sqlalchemy.orm import Session

def check_db(db : Session, f : str):
    print()
    print(f" ******* 🚨 function : {f} / url : {db.bind.url} ")
    print()