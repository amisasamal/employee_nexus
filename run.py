from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


# 📌 Future Improvements
# Implement Admin Dashboard
# Add Pagination, Search, Filters
# Export data as CSV/PDF
# Improve UI/UX with a frontend framework (e.g., Bootstrap)