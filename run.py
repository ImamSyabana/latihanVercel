from app import create_app

# This is WHEN and WHERE the function is called.
# It executes the factory and builds your entire app.
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5002)