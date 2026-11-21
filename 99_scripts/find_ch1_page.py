#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tim trang PDF chua cau dau tien cua Chuong 1: 'On February 1, 1942'
"""
import fitz
from pathlib import Path

PDF = Path("books/The_Cambridge_History_of_the_Vietnam_War.pdf")
doc = fitz.open(PDF)

found = []
for i in range(doc.page_count):
    text = doc[i].get_text()
    if "On February 1, 1942" in text:
        found.append(i)
        print(f"Tim cau dau tren PDF index {i}")

print(f"Tong so trang chua cau: {found}")
