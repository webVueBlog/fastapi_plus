# fastapi_plus/controller/router.py
import pkgutil, importlib
from fastapi import FastAPI
from pathlib import Path

def register_routers(app: FastAPI):
    pkg_path = Path(__file__).parent
    for finder, module_name, is_pkg in pkgutil.iter_modules([str(pkg_path)]):
        module = importlib.import_module(f"fastapi_plus.controller.{module_name}")
        router = getattr(module, "router", None)
        if router:
            app.include_router(router)
