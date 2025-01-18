# Overview

Testing new software tools that I have never used before in web dev: Python, Flask, Sqlite.

The software provides a way to track automotive repair workorders. The home page lists the work orders and provide a link to another page where theworkorder can be edited. Work orders are listed on the home page. To edit a work order, click the id number of the workorder in the leftmost column.Update the fields and click the update button. To delete, click the delete button in the rightmost column in the workorders view. 

The purpose of this software is to track work orders in a repair shop.

[OK Work Order Demo](https://youtu.be/1V4fSBgFjA8)

# Relational Database
Sqlite
Two tables are used: workorders and customers. The workorders table includes a customer code field which facilitates a join to the customers table.

# Development Environment
VS Code
Python 3.11 & Flask 3.1.0

# Useful Websites
- [Flask Intro](https://www.youtube.com/watch?v=Ohj-CqALrwk)
- [Flask Blueprinting](https://www.youtube.com/watch?v=WteIH6J9v64)


# Future Work
- Page for adding/editing customer information
- Add filter to homepage to filter by status
- Formatting/CSS
- Add other table so multiple repair items can be associated with a single workorder
- Restrict deletion to managers/auth