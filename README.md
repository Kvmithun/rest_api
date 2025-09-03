feat(api): implement Video REST API with Flask-RESTful and SQLAlchemy

- Added VideoModel with fields: id, name, views, likes, No_of_comments
- Configured SQLite database and ORM integration
- Implemented request parsers for PUT (create) and PATCH (update)
- Added GET, PUT, and PATCH endpoints for /video/<id>
- Applied response serialization using marshal_with
- Setup database initialization with app context
