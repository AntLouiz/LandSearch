from settings import app


@app.task
def add(x, y):
    result = x + y
    print("Sum {} + {} = {}".format(x, y, result))
    return result
