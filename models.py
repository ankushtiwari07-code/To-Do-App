from flask import render_template, redirect, url_for, session
from app import db
class task(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(100), nullable= False)
    status=db.Column(db.String(20), default="pending")
    