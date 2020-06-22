def anti_fragile(func):
    dataObj = None

    try:
        dataObj = func()
        
    except Exception as error:
        print(error.msg)

