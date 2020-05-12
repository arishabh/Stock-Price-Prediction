import os
import connexion
from flask import Flask, request

app = connexion.App(__name__, specification_dir="./")

app.add_api("master.yaml")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)

