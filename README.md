# MovieSeek 🎬

![MovieSeekLogo](./MovieSeekLogo.png)

MovieSeek is a dynamic and user-friendly web application designed for movie enthusiasts. It provides a seamless platform for users to discover movies, create an account, and save their favorite titles for future reference. 

## Key Features
- **Movie Search:** Quickly find detailed information about movies using an intuitive search interface.
- **User Accounts:** Sign up and log in to personalize your experience and save favorites.
- **Favorites Management:** Save your top picks to your account and access them anytime.

## Technology Stack
MovieSeek is built with modern technologies to ensure performance, scalability, and ease of development:
- **Backend:** Powered by [FastAPI](https://fastapi.tiangolo.com/), a high-performance Python framework for building APIs.
- **Frontend:** [React](https://reactjs.org/) for building a dynamic and responsive user interface.
- **Database:** Uses MySQL to store user data and movie information efficiently.
- **Containerization:** Employs Docker to create a robust and portable development environment, simplifying deployment and ensuring consistency across different systems.

## Environment Setup 🌱
To configure the necessary environment variables for the project, follow these steps:

1. Locate the `.env.example` file in the project root directory.
2. Create a copy of the `.env.example` file and rename it to `.env`:
   ```bash
   cp .env.example .env
   ```
3. Open the newly created `.env` file and replace the placeholder values with your actual configuration details. For example:
```
API_KEY=your_actual_api_key
DB_HOST=your_database_host
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
MYSQL_ROOT_PASSWORD=your_root_password
```
4. Save the .env file. The project will now use these environment variables during execution.

## Project Structure 🌳
```
movieseek/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── main.py          # Entry point for the FastAPI app
│   │   ├── services/        # Business logic and service layer
│   │   └── ...
│   ├── requirements.txt     # Python dependencies
│   └── ...
├── frontend/                # React frontend (contents hidden)
├── .env                     # Environment variables
├── .env.example             # Example environment variables
├── README.md                # Project README file
├── docker-compose.yml       # Docker Compose configuration
├── .gitignore               # Ignore file for telling the git what files to ignore from publishing
└── ...
```



