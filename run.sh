#!/usr/bin/env bash
uvicorn sql_app.main:app --reload --port 4000
