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
- **Database:** Uses MySQL to store user data and movie information efficiently.
- **Containerization:** Employs Docker to create a robust and portable development environment, simplifying deployment and ensuring consistency across different systems.

## Project Structure 🌳

movieseek/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── main.py          # Entry point for the FastAPI app
│   │   ├── services/        # Business logic and service layer
│   │   └── ...
│   ├── requirements.txt     # Python dependencies
│   └── ...
├── frontend/                # React frontend (contents hidden)
├── README.md                # Project README file
├── docker-compose.yml       # Docker Compose configuration
└── ...
