from flask import Blueprint, redirect, url_for, render_template, render_template_string, abort, request, make_response, jsonify,  current_app
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path

lab8 = Blueprint('lab8', __name__, static_folder='static')


@lab8.route('/lab8/')
def main():
    return render_template('/lab8/lab8.html')
