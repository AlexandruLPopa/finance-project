import logging
import subprocess
import os
import time
from fastapi import FastAPI, Request
from fastapi_utils.tasks import repeat_every
from starlette.responses import JSONResponse
from api.users import users_router
from api.assets import assets_router
from domain.user.factory import InvalidUsername
from domain.user.repo import UserIDNotFound

logging.basicConfig(
        filename="finance.log",
        level=logging.DEBUG,
        format="%(asctime)s _ %(levelname)s _ %(name)s _ %(message)s",
    )


app = FastAPI(
    debug=True,
    title="Fintech Portfolio API",
    # TODO add to README
    description="A webserver with a REST API for keeping track of different financial assets"
    " and see/compare their evolution.",
    version="0.4.4",
)
app.include_router(users_router)
app.include_router(assets_router)


@app.exception_handler(UserIDNotFound)
def return_id_not_found(_: Request, e: UserIDNotFound):
    userid_error = "User ID not found! Error: " + str(e)
    logging.error(userid_error)
    return JSONResponse(status_code=404, content=userid_error)


@app.exception_handler(InvalidUsername)
def return_invalid_username(_: Request, e: InvalidUsername):
    username_error = "Username is not valid! Error: " + str(e)
    logging.error(username_error)
    return JSONResponse(status_code=400, content=username_error)


@app.on_event("startup")
@repeat_every(seconds=3600 * 24)
def clean_images_older_than_24h():
    files = os.listdir(".")
    graphs = [f for f in files if f.endswith(".png")]
    current_posix_time = time.time()
    ago_24h = current_posix_time - 3600 * 24
    for g in graphs:
        g_creation_time = os.path.getctime(g)
        if g_creation_time < ago_24h:
            os.remove(g)


if __name__ == "__main__":
    logging.info("Starting webserver...")
    try:
        subprocess.run(["uvicorn", "main:app", "--reload"])
    except KeyboardInterrupt as e:
        logging.warning("Keyboard interrupt.")
    except Exception as e:
        logging.warning("Webserver has stopped. Reason: " + str(e))
