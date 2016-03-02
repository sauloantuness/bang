# Models

User
----
* facebookId (char)
* name (char)
* photo (char)
* uriId (char)
* uvaId (char)
* spojId (char)
* team fk(Team)
* group fk(Group)


Group
-----
* name (char)
* city (char)
* photo (char)


Team
----
* name (char)


Judge
-----
* name (char)
* url (char)
* urlProblem (char)
* urlProfile (char)


Category
--------
* name (char)


Problem
-------
* judge fk(Judge)
* name (char)
* code (char)
* category fk(Category)
* level (int)
* solved (int)


Solution
--------
* user fk(User)
* problem fk(Problem)
* date (Date)


Contest
-------
* name (char)
* date (Date)
* duration (integer)
* users fk(User)
* problems fk(Problems)
* solutions fk(Solution)
* (qtd, categories)  (int, fk(Category))